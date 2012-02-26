import subprocess

class ExpressoMachine:  
    cmd = []

    def order(self):
        subprocess.Popen(self.cmd,shell=True)



if __name__ == "__main__":    

    print "WELCOME TO EXPRESSO!\nI'll take care of the compiling from now on, you just code ;)\n\n"

    coffeewatcher = 'coffee --watch -l '

    Collections = ExpressoMachine()
    Models      = ExpressoMachine()
    Views       = ExpressoMachine()
    Config      = ExpressoMachine()
    Specs       = ExpressoMachine()

    Collections.cmd = coffeewatcher + '-o js/collections -c coffee/collections/*'
    Models.cmd = coffeewatcher + '-o js/models -c coffee/models/*'
    Views.cmd = coffeewatcher + '-o js/views -c coffee/views/*'  
    Config.cmd = coffeewatcher + '-o js -c coffee/*.coffee' 
    Specs.cmd = coffeewatcher + '--join specs.js -o js/tests -c coffee/specs/*'

    Collections.order()
    Models.order()
    Views.order()
    Config.order()
    Specs.order()