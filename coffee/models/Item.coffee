define([
    # This are dependenciens this model uses
    'api.config' # Just some API configuration.
    ],
    (API) ->
      class Item extends Backbone.Model

        # This is the tricky part here as we are using backbone-tastypie
        # Interface. This urlRoot is used in the new url property that now
        # Happens to be a callable variable (it gets something done and then
        # returns it's value).
        urlRoot: API.URL

        # Default values in case that SOMEHOW the user manages to get pass
        # Our validation and stuff and instantiate a default item.
        defaults:
          content: "Holy DOM Manipulation!"
          done: false

        # Toggles the element done flag.
        toggleDone: =>
          # For this object, set done as
          # The opposite value of this objects done flag.
          # Of course this objects done flag won't get lost
          # Read from Right to left.
          @set done: not @get "done"
          # And let's save it.
          @save()

        # Sets the item content.
        setText: (text)=>
          # Set the content attribute to the parameter text.
          @set content: text 
          # And save the object.
          @save()

        # Here we validate.
        validate: (attrs)->
          # Attrs is a list of the attributes just about to be passed to the object.

          # If the content is null
          if attrs.content == null or attrs.content == ""
            # Complain.
            return "Item content can't be blank"
          
          # If the done flag ain't true nor false
          if attrs.done != false or attrs.done != true
            # Complain.
            return "Item done state must be false or true"
  )