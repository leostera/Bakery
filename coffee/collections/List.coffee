define([
    # This are dependenciens this model uses
    'models/Item',  # The model this collection will hold
    'api.config'    # Some API configuration.
    ],
    (Item,API) ->
        class List extends Backbone.Collection

            # This is the tricky part here as we are using backbone-tastypie
            # Interface. This urlRoot is used in the new url property that now
            # Happens to be a callable variable (it gets something done and then
            # returns it's value).
            urlRoot: API.URL

            # This just sets this collection to an specific model
            # In this case, Item.
            model: Item
    )


