class BaseGameModel:
 
    def __init__(self, model_name):
        self.model_name = model_name
        
    def move(self, environment):
        pass
 
    def user_input(self, event):
        pass