# This right now points to my localhost implementation of the api.
# I can upload a working api to AlwaysData and we can test this across both servers.
define( [''],
    ()-> 
        # One time config here.
        # Backbone.emulateHTTP = if not Backbone.emulateHTTP then true
        # This next dictionary will be returned.
        {            
            URL: "http://django.locker/whatsnext_api/v1/item"
            KEY:  ""
        }
)

# This can be accessed as API.URL and API.KEY if you pass this object as var API when using define