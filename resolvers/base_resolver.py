from abc import ABC, abstractmethod

class BaseResolver:
    
    def __init__(self, msg: str):
        self.msg = msg
        
        
    @abstractmethod
    def resolve(self):
        pass