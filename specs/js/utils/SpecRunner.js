define( [
"specs/Item",
"specs/List",
"specs/ItemView",
"specs/ListView",
"specs/Routes",
"specs/MainRouter",
  ], function(){

      return SpecRunner = function() {

        var jasmineEnv = jasmine.getEnv();
        jasmineEnv.updateInterval = 1000;

        var trivialReporter = new jasmine.TrivialReporter();

        jasmineEnv.addReporter(trivialReporter);

        jasmineEnv.specFilter = function(spec) {
          return trivialReporter.specFilter(spec);
        };

        return jasmineEnv.execute();
      }
      
    }
);