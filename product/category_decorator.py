
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
class CategoryDecorator:
    def __init__(self, category_service):
        self._category_service = category_service

    def get_all_categorys(self):
        return self._category_service.get_all_categorys()

    def create_category(self, categorie_name):
        return self._category_service.create_category(categorie_name)

    def create_categorys(self,categories):
        return self._category_service.create_categorys(categories)

    def update_category(self, category_id, categorie_name):
        return self._category_service.update_category(category_id, categorie_name)

    def delete_category(self, category_id):
        return self._category_service.delete_category(category_id)