# base class inherited by all actions
class Action:
    
    def __init__(self, action_id):
        self.id = action_id
    
    def get_id(self):
        return self.id
    
    # this method gets called when action executed.  can be overridden in subclass
    def do_action(self,game,room,request):
        return
    
    # should this action be available to player?
    # default is yes, but can be overridden.
    def is_enabled(self):
        return True
    
    # is this a navigation action?
    # we decide this based on whether the action has defined
    # a get_destination method
    def is_nav_action(self):
        return hasattr(self,'get_destination')
    
    # return description of action (used in label on webpage)
    # should be overridden in subclass with specific description
    def get_description(self):
        return "Action"
    
    # return http method to use when user clicks on an action
    # use "get" if just moving to another room.  if changing something
    # like the state of an inventory item or room then use "post"
    #
    # if omitted in your action we return "post"
    def get_method(self):
        if self.is_nav_action():
            return "get"
        else:
            return "post"