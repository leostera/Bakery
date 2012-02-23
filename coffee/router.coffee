#  This router glues the views with urls.

define([
  'views/List'
  ],
  (ListView) ->

    class AppRouter extends Backbone.Router.extend
      routes: 
        # Define some URL routes here like
        # 'path': 'foo'
        '*actions': 'defaultAction'
    
      defaultAction: (actions)->
        ListView.render()

    initialize = () ->
      app_router = new AppRouter;
      Backbone.history.start();
  
    {
      initialize: initialize
    }
    
)
