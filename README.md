## Bakery: The tasty boilerplate for CoffeeScripters.

Bakery is a delicious project template that will let you focus right on your flaming CoffeeScript project using:

* Backbone.js, the rockstar MV-Something framework for the web.
* jQuery, the --ok, this guy doesn't need an introduction.
* Require.js, successfully modularizing web apps in the major leagues.
* Bootstrap, or the fanciest thing Twitter has done..
* Less, so your designer can have a good time, too.

All of which are globally accessible for your application, or easily modularized if that's what you need. Along such big bundle, and regarding testing, there's some more:

* Jasmine, Jasmine-jQuery, Jasmine-HTML, Jasmine-Sinon and Sinon himself.

And I dare you find an excuse not to test again.

Finally, should this not deserve your attention, I've included Expresso, or "CoffeeScript compiling for Pythonistas", a tool that will make you a happier developer by continuous building your CoffeeScript according to a set of rules described in human-friendly files. Serve yourself examples of it in the "orders" folder. Expresso does JUST that, so no need of an environment or even a CoffeeScript compiler going round. Just Python, which is most likely already installed in your computer.

### Usage and Guidelines

Providing you already set your order files up, usual work cycle will be something like:

* Start Expresso V8 [1]
* Create a new spec for an incredible new feature
* Make it pass!
* Check your specs using the SpecRunner.html under the specs folder

You can always check how your app is looking like in the build folder. Just do not open it thru file:// protocol since it is very restrictive.

### Notes

#### Serving

While having Apache server your app is really nice, it's not usually the easier setup solution. Right now I do have Apache but I'm evaluating a lightweight, dependency-less options to bundle with Bakery. If you have any thoughts on this, just let me know!

#### Where do this come from?

I'm extracting it from the What's Next app I'm developing. Feel free to check it out.

[1] Right now Expresso V8 won't recognize NEW files created after it loaded the orders.

