# Configure require.js settings some aliases
require.config 
  baseUrl: 'js/'
  paths:
    text: 'libs/require/text'
    templates: '../templates'

# Now call it.
require([
  # Load our app module and pass it to our definition function
  'app' #this translastes into app.js in the current folder, so ./app.js

], (App) ->
  # The "app" dependency is passed in as "App"
    App.initialize()
)
