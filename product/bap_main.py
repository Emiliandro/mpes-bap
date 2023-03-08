from data_helper import DataHelper
from bap_ddg import BapDDG
from abc import ABC, abstractmethod
import datetime
import pickle

today = datetime.datetime.today()
today_str = today.strftime('%Y-%m-%d')
validation = DataHelper()

class Handler(ABC):
    @abstractmethod
    def handle(self, data):
        pass

class HandlerRemoveDuplicates(Handler):
    def __init__(self, successor=None):
        self._successor = successor

    def handle(self, data):
        data = validation.removeDuplicates(data)
        print("removing duplicated", len(data))
        if self._successor is not None:
            return self._successor.handle(data)
        return data

class HandlerRemoveMinDescription(Handler):
    def __init__(self, successor=None):
        self._successor = successor

    def handle(self, data):
        data = validation.removeMinDescription(data)
        print("remove with low characters", len(data))
        if self._successor is not None:
            return self._successor.handle(data)
        return data

class HandlerRemoveNonPortuguese(Handler):
    def __init__(self, successor=None):
        self._successor = successor

    def handle(self, data):
        data = validation.removeNotPortuguese(data)
        print("removing non portuguese", len(data))
        if self._successor is not None:
            return self._successor.handle(data)
        return data

class HandlerCreateFile(Handler):
    def __init__(self, create_file=False):
        self.create_file = create_file
        self.file_name = "" + today_str + ".txt"

    def handle(self, data):
        if self.create_file:
            with open("validated_"+self.file_name, "wb") as f:
                pickle.dump(data, f, protocol=pickle.HIGHEST_PROTOCOL)
        return data

class BapMain():
    def createTodayFile(self):
        self.webscrapper.make_txt_file()

    def set_categories(self, categories):
        list_categories = []
        for category in categories:
            list_categories.append(category['category'])
        self.webscrapper.set_categories(list_categories)

    def getTodayFile(self):
        try:
            file = open(self.file_name, 'rb')
            dictionary_list = pickle.load(file)
            
            for d in dictionary_list:
                self.current_dictionaries.append(d)
            file.close()
        except:
            print("Something unexpected occurred!")
    
    def getAndValidateTodayFiles(self, create_file=False):
        self.getTodayFile()
        print("initial size of scrapping", len(self.current_dictionaries))

        # Chain of responsibility
        handler_create_file = HandlerCreateFile(create_file)
        handler_remove_non_portuguese = HandlerRemoveNonPortuguese(handler_create_file)
        handler_remove_min_description = HandlerRemoveMinDescription(handler_remove_non_portuguese)
        handler_remove_duplicates = HandlerRemoveDuplicates(handler_remove_min_description)

        validated_data = handler_remove_duplicates.handle(self.current_dictionaries)
        return validated_data
            
    def __init__(self):
        self.file_name = today_str + ".txt"
        self.webscrapper = BapDDG(today_str)
        self.current_dictionaries = []
        
    def get_messages(self):
        self.createTodayFile()
        self.today_files = self.getAndValidateTodayFiles(create_file=True)
        return self.today_files
