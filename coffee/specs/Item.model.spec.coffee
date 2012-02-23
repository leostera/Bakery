describe "Item common capabilities", () ->

  item=""

  beforeEach ()->
    item = new Item 
                  done: false
                  content: "Test"
    

  it "should be able to toggle from undone to done", ()->
    item.toggleDone()
    expect(item.get 'done').toEqual(true)
  
  it "should be able to set a new text", ()->
    item.setText("New Text")
    expect(item.get 'content').toEqual("New Text")

  describe "when being created", ()->
    beforeEach ()->
      item = new Item 
                  done: false
                  content: "Test"
      

    it "should complain if it does not have a text", ()->
      item.setText("")
      expect(item.validate()).toEqual "Item content can't be blank"