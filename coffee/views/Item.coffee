define(
  # This are dependenciens this model uses
  ['']  #Actually none hah, but it's better to get this here anyway.
  , () ->
      class ItemView extends Backbone.View

        # The tag that will be used to create new items.
        tagName = "li"

        initialize: ->
          # For starters, I've been having an issue with binding something to
          # @model before it's declaration, so I'd just declare it as Backbone.Model
          # Since every other model inherit from there.
          @model = Backbone.Model
          # Now bind the change event to the render function.
          @model.bind 'change', @render

        render: =>      
          # We should be using templates here!
          $(@el).html """
          <div class="item">
            <input class="done" type="checkbox" #{ if @model.get 'done' then "checked=checked" else ""} />
            <span class="content">#{ @model.get 'content' }</span>
            <span class="delete"></span>
          </div>
          """
          console.log "Implement template here too"
          @

        remove: =>
          # Remove the element from screen.
          $(@el).remove()
          # Remove the model from the storage.
          @model.destroy()
          @

        toggle: =>
          # Toggle the object's done flag.
          @model.toggleDone()
          @

        # Bind events here.
        events:
          # When clicked on .done, trigger the toggle function.
          'click .done'   : 'toggle'
          # When clicked on .delete, trigger the delete function.
          'click .delete' : 'remove'
          # More to do:
          #   dblclick .content let's you modify the content.
          #   dragging the element let's you re-order it.
  )