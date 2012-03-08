"""
Expresso is a little Python continuous builder for CoffeeScript for Pythonistas,
built using PyV8 and PyYAML.
"""

import os
import sys
import time
import urllib
import optparse

try:
    from yaml import load
except ImportError:
    print """Please install PyYAML.
    It can be as easy as pip install PyYAML or easy_install PyYAML"""
    sys.exit(1)

try:
    import PyV8
except ImportError:
    print """Please install PyV8.
    You can download it from http://code.google.com/p/pyv8/downloads/list"""

VERSION = (0, 2, 1)

class NoCodeToCompile(Exception):
    "Exception to arise when there is no code to be compiled."
    pass


class CompileException(Exception):
    "Exception to arise when there is an error in the compile process."
    pass


class V8CoffeeCompiler:
    """
    The PyV8 CoffeeScript compiler. Use it as base for your own compilers.
    """
    v8_context  = None
    v8_compiler = None
    compiled    = {}
    url         = None
    coffee_src  = "coffee-script.js" #same directory

    def __init__(self, latest=False):        
        """
        Init the PyV8 context and load the compiler either from CoffeeScript's
        Github repository or from a file.
        """        
        self.v8_context = PyV8.JSContext()
        self.v8_context.enter()
        if latest and self.url is not None:
            self.v8_compiler = self.v8_context.eval(
                                urllib.urlopen(self.url).read()
                                )
        else:
            self.v8_context.eval( urllib.urlopen(self.coffee_src).read() )
            self.v8_compiler = self.v8_context.locals.CoffeeScript

    def __del__(self):
        if self.v8_context:
            self.v8_context.leave()

    def compile(self, coffee=None):
        "Returns CoffeeScript code compiled to JavaScript"
        if coffee is None:
            raise NoCodeToCompile()
        if self.v8_compiler is None:
            raise NoCompilerError()
        try:
            return self.v8_compiler.compile(coffee)
        except:
            pass

    def get_version(self):
        "In this case, version is 1.2"
        if self.v8_compiler is not None:
            return (1, 2)
        return None


class CartIsEmptyError(Exception):
    "This exception will arise when trying to run the cart without loading it"
    pass


class ShouldHaveFilesError(Exception):
    "This exception will arise when trying to load an order without files"
    pass


class NullStreamError(Exception):
    "This exception will arise when trying to load an empty order"
    pass


class NoCompilerError(Exception):
    """
    This exception will arise from the compile method in the Cart class
    whenever it is executed without Cart.compiler being an actual Compiler.
    """
    pass


def change_ext(filepath):
    "Get the filepath for the compiled file"
    return "%s.js" % os.path.splitext(filepath)[0]


def get_src(filepath):
    "Get the source from a given file"
    with open(filepath, "r") as file_d:
        return file_d.read()

            
def save(content=None, dest=None, srcfile=None, only_if_new=False):
    "Force saving a compiled file."
    if not os.path.exists(os.path.dirname(dest)):
        os.makedirs(os.path.dirname(dest))

    if not os.path.exists(dest):
        with open(dest, "w+") as file_d:
            file_d.write(str(content))
            file_d.flush()
            os.fsync(file_d)
            print "%s - compiled %s" % (time.strftime('%X'), dest)

    if only_if_new and os.stat(srcfile).st_mtime > os.stat(dest).st_mtime or\
    not only_if_new:
        with open(dest, "w+") as file_d:
            file_d.write(str(content))
            file_d.flush()
            os.fsync(file_d)
            print "%s - compiled %s" % (time.strftime('%X'), dest)


class Cart:
    """
    The Cart that holds the commands, loads them and runs them.
    It pretty much does everything here.
    """

    order       = {}
    loaded      = False
    compiler    = None
    done        = False

    def __init__(self):
        self.order  = {}
        self.loaded = False
        self.done   = False
        self.compiler = V8CoffeeCompiler()

    def load(self, stream=None):
        "Loads a stream and parses it."
        if stream:
            self.order = load(stream)
            self.loaded = True
            if self.order.get('files') is None:
                raise ShouldHaveFilesError()
            else:
                newfiles = []
                for filepath in self.order.get('files'):
                    if os.path.splitext(filepath)[0].endswith("/**"):
                        # list all dirs
                        # and parse all files inside all those dirs
                        for folder in os.listdir(os.path.split(filepath)[0]):
                            folder = os.path.split(filepath)[0] + '/' + folder
                            for newfile in os.listdir(folder):
                                if newfile.endswith(".coffee"):
                                    newfiles.append("%s/%s" %
                                        (folder, newfile)
                                        )
                                    print "\tAdded %s/%s" % (folder, newfile)                            

                        print "\tInstead of %s" % filepath
                        self.order.get('files').remove(filepath)

                    elif os.path.splitext(filepath)[0].endswith("/*"):
                        self.order.get('files').remove(filepath)
                        for newfile in os.listdir(os.path.split(filepath)[0]):
                            if newfile.endswith(".coffee"):
                                newfiles.append("%s/%s" %
                                (os.path.split(filepath)[0], newfile)
                                )
                                print "\tAdded %s" % newfile
                        print "\tInstead of %s" % filepath

                for newfile in newfiles:
                    self.order.get('files').append(newfile)

        else:
            self.order = {}
            self.loaded = False
            raise NullStreamError()

    def get_run_times(self):
        "Should it run forever or just once?"
        if self.order.get('watch') is True:
            return -1
        return 1

    def run(self):
        "Runs the cart"
        if self.order is {}:
            raise CartIsEmptyError()
        elif self.compiler is None:
            raise NoCompilerError()
        else:
            if self.order.get("watch"):
                self.watch()                
            else:
                self.build()
                                
    def compile(self, src):        
        "Get the compiled source code using the compiler at self.compiler"
        if self.compiler is None:
            raise NoCompilerError()
        else:
            compiled_src = None
            try:
                compiled_src = self.compiler.compile(src)
            except CompileException, exception:
                print "Error compiling: %s" % str(exception)
            return compiled_src

    def build(self, only_changed=False):
        "Build the order based on it's configuration"
        if self.done:
            return
        # if no delivery specified
        if self.order.get('deliver', None) is None:
            # but files should be joined
            if self.order.get('join'):                        
                # compile self._join() and save it to 
                # a single file in the highest common folder
                # from all the files listed
                save(
                    self.compile(self._join()), 
                    os.path.join(
                        os.path.commonprefix( self.order.get('files') ), 
                        self.order.get('join')
                        )
                    )
            else:
                # compile each file into its folder                
                for file_d in self.order.get('files'):
                    save(
                        self.compile( get_src(file_d) ), 
                        change_ext(file_d),
                        srcfile=file_d,
                        only_if_new=only_changed
                        )                

        else:
            if self.order.get('join'):
                # compile self._join() and save it to
                # a single file in the specified delivery folder
                save(
                    self.compile(self._join()), 
                    self._deliver_path(self.order.get('deliver'))
                    )
            else:
                # compile each file into the delivery folder
                # as separate js files
                for file_d in self.order.get('files'):
                    save(
                        self.compile( get_src(file_d) ), 
                        self._deliver_path(file_d),
                        srcfile=file_d,
                        only_if_new=only_changed
                        )

        self.done = True

    def watch(self):
        "Check for changes in the filepaths and re build if necessary"
        # do the watching here, as this is the process we will be threading
        for filepath in self.order.get('files'):
            try:
                filepath_mtime = os.stat(filepath).st_mtime
                if self.order.get('deliver', None) is None:
                    if self.order.get('join'): 
                        endpath = os.path.join(
                                    os.path.commonprefix(self.order.get('files')), 
                                    self.order.get('join')
                                    )
                    else:
                        endpath = change_ext(filepath)
                else:
                    if self.order.get('join'):
                        endpath = self._deliver_path(self.order.get('deliver'))
                    else:
                        endpath = self._deliver_path(filepath)
                        
                if os.path.exists(endpath):
                    endpath_mtime = os.stat( endpath ).st_mtime
                else:
                    endpath_mtime = 0

                if endpath_mtime < filepath_mtime or not os.path.exists(endpath):
                    self.build(only_changed=True)
                    
            except Exception:
                pass

        self.done = False
    
    def _deliver_path(self, filepath):
        "Get the delivery path for the compiled file"        
        if self.order.get('join'):
            # Use the join-files name
            filename = self.order.get('join')
        else:
            # Get the actual filename
            filename = os.path.splitext(os.path.split(filepath)[1])[0]
            filename += ".js"
            
        # Return just the joined delivery path with the filename.js
        return os.path.join( "%s" % self.order.get('deliver'), 
                            "%s" % filename)

    def _join(self):
        "Returns the joined source for all given files in an order."
        srcs_joined = ""
        # get all the file descriptors
        for filepath in self.order.get('files'):
            srcs_joined += get_src(filepath) + "\n"

        return srcs_joined

class EmptyCartsError(Exception):
    """
    Arises when there is no carts and the run method from the ExpressoMachine
    is called.
    """
    pass

class ExpressoMachine:
    """
    Handle multiple carts
    """

    carts = []

    def __init__(self, folder="orders"):
        "Init carts as a blank list"
        self.load(folder)
        self.version = VERSION

    def run(self, check_interval=2):
        "Run the carts"
        if self.carts is []:
            raise EmptyCartsError()
        else:
            while True:
                try:
                    should_finish = True

                    for cart in self.carts:
                        cart.run()

                        if not cart.done:
                            should_finish = False

                    if should_finish:
                        sys.exit(0)

                    time.sleep(check_interval)
                    
                except KeyboardInterrupt:
                    self.kill()

    def kill(self):
        "Finish it."
        print "Thanks for using Expresso v%s.%s.%s!" % self.version
        print "@author Leandro Ostera"
        print "@email  leostera @ gmail.com"
        print "@git    https://github.com/leostera/Expresso"
        sys.exit(0)

    def load(self, folder="orders"):
        "Looks inside a folder for order files and loads them."
        orders = [order for order in os.listdir(folder)\
                    if order.endswith(".order") ]

        for order in orders:
            cart = Cart()
            path = "%s/%s" % (folder, order)

            if os.path.getsize(path) is 0 :
                continue
            print "Loading...orders/%s" % order
            cart.load( os.read( os.open(path, os.O_RDONLY) , 100000) )
            self.carts.append(cart)


################################################################################
#
# The actual runnable program starts below.
#
################################################################################

if __name__ == "__main__":

    OPARSER = optparse.OptionParser(
    description="A little continuous builder for CoffeeScript for Pytonistas.",
    usage='Usage: %prog <orders_folder>',
    version = "%prog 0.2.1",
    epilog="Feel free to contribute at https://github.com/leostera/Expresso"
    )

    OPARSER.add_option("-f", "--folder", dest="folder",
                      help="look for .order files inside FOLDER")

    (OPTIONS, ARGS) = OPARSER.parse_args()

    EXPRESSO_MACHINE = None
    
    if len(ARGS) == 0:
        EXPRESSO_MACHINE = ExpressoMachine()
    elif OPTIONS.directory:
        EXPRESSO_MACHINE = ExpressoMachine(OPTIONS.directory)

    if EXPRESSO_MACHINE:
        EXPRESSO_MACHINE.run()
    else:
        print "Holy BUGS Batman!"