define "Item", ->

  class App.Item extends Backbone.Model

    defaults:
      date    : 3
      picture : null
      title   

    validate: (args) ->