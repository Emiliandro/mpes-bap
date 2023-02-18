from datetime import datetime
import copy

# The Prototype pattern is a creational design pattern that allows an object 
# to create duplicate objects or clones of itself, without depending on specific classes.

# The pattern involves creating a prototype object that serves as a template for 
# creating other objects. When a new object is needed, a clone of the prototype is 
# created and modified as needed. This approach allows the creation of new objects 
# with minimal overhead, and it allows objects to be created dynamically at runtime, 
# without requiring a specific class to be known in advance.

# The Prototype pattern is useful in situations where creating an object is expensive 
# or complex, and where there are many variations of a similar object. By using a prototype,
# you can easily create new objects by cloning an existing one and modifying its properties 
# as needed, which can save time and resources.

# Additionally, the Prototype pattern can promote encapsulation and reduce coupling by 
# separating the client code from the object creation process.
class MessagePrototype:
    def __init__(self):
        self.name = ''
        self.description = ''
        self.source = 0.0
        self.category = ''
        self.published_at = datetime.now

    def clone(self):
        return copy.deepcopy(self)