define ["Item","specs/Utils"], (Item,logm)->

  ###
  Specs for the Item model
  ###
  describe "Item model", ->

    ###
    Common setup and teardown
    ###  
    beforeEach ->
      # Add a new item
      @item = new Item()

      collection = 
          url: "/collection"
          localStorage: new Store("Test")

      @item.collection = collection;

    ###
    Instantiation tests
    ###
    describe "When instantiated", ->

      it "provides access to its attributes (dummy-existance check)", ->          
        # Check that the title can be accessed
        expect(@item.get 'title').toEqual "Empty item"

      it "sets priority to 3 by default", ->  
        # Check that priority is 3 by default    
        expect(@item.get 'priority').toEqual 3

      it "sets itself as undone", ->
        # Check that the done flag is flase by default
        expect(@item.get 'done').toBeFalsy()

    ###
    URL tests
    ###
    describe "url", ->

      describe "when no id is set", ->
        it "should return the collection URL", ->
          expect(@item.url()).toEqual "/collection"

      describe "when id is set", ->
        it "should return the collection URL and id", ->
          @item.id = 1
          expect(@item.url()).toEqual "/collection/1"

    ###
    Saving tests
    ###
    describe "When saving", ->

      beforeEach ->        
        # Create a sinon Spy
        @eventSpy = sinon.spy()
        # Bind it to the error event from the item model
        @item.bind "error", @eventSpy

      it "should not save when title is empty", ->
        # Now let's try to save
        @item.save
          # This item with no title
          title: ""
        # And check if the spy was called once
        expect(@eventSpy).toHaveBeenCalledOnce()
        # With the item as paremeter and resulted in  <this string just below here>
        expect(@eventSpy).toHaveBeenCalledWith @item, "Cannot have an empty title"

      it "should not save when done is other than boolean", ->
        # And now let's try to save it
        @item.save
          # And let's set done to something else than a boolean
          done: "Not"
        # Now check if the spy was called once
        expect(@eventSpy).toHaveBeenCalledOnce()
        # And assure it was passed the item as a parameter and returns that string.
        expect(@eventSpy).toHaveBeenCalledWith @item, "Done must be yes or no"

      it "should not save when priority is not a number", ->
        # And now let's try to save it
        @item.set
          # Using a string for the priority
          priority: "First"
        # Now check if the spy was called once
        expect(@eventSpy).toHaveBeenCalledOnce()
        # And assure it was passed the item as a parameter and returns that string.
        expect(@eventSpy).toHaveBeenCalledWith @item, "Priority must be a number"

    ###
    Business Logic
    ###
    describe "Common logic", ->

      it "should tell if it's done or not", ->
        expect( @item.isDone() ).toBeFalsy()

      it "should be able to toggle from pending to done", ->                
        @item.set
          done: no
        expect( @item.toggle() ).toBeTruthy()

      it "should be able to toggle from done to pending", ->
        @item.set
          done: yes
        expect( @item.toggle() ).toBeFalsy()