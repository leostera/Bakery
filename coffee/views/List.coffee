define([
  # This are dependenciens this view uses.
  'collections/List', # The item collection, called List
  'views/Item'        # And the item view, called ItemView.
  ], (List, ItemView) ->
    
    class ListView extends Backbone.View
      
      # Cache of the element we will be working at
      el: $ 'body'
      
      initialize: ->
        # On startup create a new list
        @collection = new List
        # And try to get everything from the server (or the localStorage)
        @collection.fetch
          add: true # This flag tells that we will add whatever the server gives us
        # Also lets bind a method to the addition step
        @collection.bind 'add', @appendItem

        # Cache of the input field, thanks jQuery
        @input = $ '.new-todo'
        # And let's render this biatch
        @render()

      render: =>
        # Render the template. Oops, it's not a template yet!
        $(@el).html """
        <div id="create-todo">
            <input class="new-todo" placeholder="What needs to be done?" type="text" />
          </div>
          <ul>
          </ul>
        """
        console.log "Implement templating."

      createOnEnter: (e) =>
        # This methods allows us to create a new item once the user pressed enter
        # while writting in the input box.
        if( e.keyCode == 13) # 13 is the keycode for the Enter key.
          
          # Check if the input box is empty
          if $('.new-todo').val() == "" or $('.new-todo').val() == null
            # We don't want blank to-dos!            
            return console.log "Tried to create blank item."
          
          # Then try to create a new item.
          @collection.create
            # It will always start as undone
            done: false
            # And the input box content will be set here
            content: $('.new-todo').val()
          
          # And now reset the box.
          $('.new-todo').val('')
        @

      appendItem: (item) =>
        # A new item has been added
        # Let's create a new ItemView for it
        item_view = new ItemView
        # Assign that item to the view
        item_view.model = item
        # And show it accordingly
        $('ul').append item_view.render().el

      # Here we bind events to functions
      events:
        # Bind keypressing in the input box to the createOnEnter function
        'keypress .new-todo': 'createOnEnter'

    # At the end, we will always instantiate a vew for it's use
    # So it's ok if we just return a new instance of it.
    # As views contain no data that can't be retrieved from server or local storage.
    new ListView

  )