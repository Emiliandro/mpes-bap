
# The Decorator pattern is a structural design pattern that allows behavior
# to be added to an individual object, either statically or dynamically, 
# without affecting the behavior of other objects from the same class.

# The pattern involves creating a "wrapper" class, also known as a decorator, 
# that encapsulates the original class and adds new behaviors to it by defining
# new methods or modifying existing ones. This allows the decorator to modify 
# the behavior of the object at runtime, without requiring changes to the original 
# object. The decorator pattern is useful when you want to add functionality to an 
# object in a flexible and dynamic way, without modifying the underlying code. 

# It promotes open-closed principle by allowing the extension of the behavior 
# of an object without changing the original code.
class MessageDecorator:
    def __init__(self, message_service):
        self._message_service = message_service

    def get_all_messages(self):
        return self._message_service.get_all_messages()

    def get_all_messages_between_dates(self,from_date,to_date):
        return self._message_service.get_message_between_dates(from_date=from_date,to_date=to_date)

    def get_message_by_category(self, category):
        return self._message_service.get_message_by_category(category)

    def get_message_by_id(self, message_id):
        return self._message_service.get_message_by_id(message_id)

    def create_message(self, title, description, source, category, published_at):
        return self._message_service.create_message(title, description, source, category, published_at)
    
    def create_messages(self,messages):
        return self._message_service.create_messages(messages)

    def update_message(self, message_id, title, description, source, category, published_at):
        return self._message_service.update_message(message_id, title, description, source, category, published_at)

    def delete_message(self, message_id):
        return self._message_service.delete_message(message_id)