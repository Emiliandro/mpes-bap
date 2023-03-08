import datetime

# using duckduckgo_search, because DuckDuckGo does not collect or share personal
# information. That its privacy policy, it prevents search leakage by default.  
# read more about it at https://duckduckgo.com/privacy
from duckduckgo_search import ddg_suggestions, ddg

# escape function causes param to be rendered as text, preventing the execution of 
# injection script in the user’s browser or the in the api request.
from markupsafe import escape
from abc import ABC, abstractmethod
from data_helper import DataHelper

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
    def handle(self, data):
        return data

class BapMain():
    def createTodayFile(self):
        self.research = self.webscrapper.research()

    def set_categories(self, categories):
        list_categories = []
        for category in categories:
            list_categories.append(category['category'])
        self.webscrapper.set_categories(list_categories)

    def getTodayFile(self):
        dictionary_list = self.research
        for d in dictionary_list:
            self.current_dictionaries.append(d)
    
    def getAndValidateTodayFiles(self):
        self.getTodayFile()
        print("initial size of scrapping", len(self.current_dictionaries))

        # Chain of responsibility
        handler_create_file = HandlerCreateFile()
        handler_remove_non_portuguese = HandlerRemoveNonPortuguese(handler_create_file)
        handler_remove_min_description = HandlerRemoveMinDescription(handler_remove_non_portuguese)
        handler_remove_duplicates = HandlerRemoveDuplicates(handler_remove_min_description)

        validated_data = handler_remove_duplicates.handle(self.current_dictionaries)
        return validated_data
            
    def __init__(self):
        self.file_name = today_str + ".txt"
        self.webscrapper = BapDDG(today_str)
        self.research = []
        self.current_dictionaries = []
        
    def get_messages(self):
        self.createTodayFile()
        self.today_files = self.getAndValidateTodayFiles()
        return self.today_files

class BapDDG():
    def set_categories(self,categories):
        self.categories = categories

    def search_phrase(self,value,category='none'):
        self.phrase_to_results = ddg(value, region='br-pt', safesearch='on', time='y', max_results=9)

        for phrase in self.phrase_to_results:
            self.list_suggestions.append({ 
                "description":str(phrase['body']),
                "title":str(phrase['title']),
                "source":str(phrase['href']),
                "category":str(category)})

    def __init__(self,today):
        self.default_turismo = [" turismo sustentável", "turismo g1"]
        self.default_tecnologia = [" tecnologia "," tecnologia da informação "," tecnologia assistiva "," tecnologia 5g "," tecnologia na educação "," tecnologia sinônimo "," tecnologias disruptivas "," tecnologia e inovação "," tecnologia da informação "," tecnologia da informação faculdade "," tecnologia da informação e comunicação ", " tecnologia g1"]
        self.default_automobilismo = [" autoesporte "," autoesporte g1 "," auto esporte globo "," autoesporte domingo "," autoesporte passo fundo "," autoesporte qual comprar 2022 "," autoesporte mclaren "," auto esporte revista "," autoesporte g1 "," auto esporte globo "," auto esporte globoplay "," auto esporte globo domingo "," autoesporte domingo "," auto esporte revista "," autosport revista "," autoesporte g1 "," auto esporte globo "," auto esporte globoplay "," auto esporte globo domingo "," auto esporte globoplay "," auto esporte globo domingo "," auto esporte de hoje domingo "," auto esporte globo hoje "," auto esporte de domingo "," auto esporte na globo "," auto esporte globo ontem "," programa auto esporte globo "," auto esporte globo play "," autoesporte domingo "," autoesporte passo fundo "," auto esporte passo fundo telefone "," auto esporte passo fundo rs "," auto esporte passo fundo centro "," autoesporte mclaren "," autosport mclaren f1 forum "," autosport mclaren f1 forum "," automotive forums mclaren f1 "]
        self.list_suggestions = []
        self.file_name = "" + today + ".txt"
        self.categories = []

    def research(self):

        for i in self.categories:
            self.search_phrase(value=i,category=i)

        for i in self.default_automobilismo:
            self.search_phrase(value=i,category="autoesporte")

        for i in self.default_tecnologia:
            self.search_phrase(value=i,category="tecnologia")
            
        for i in self.default_turismo:
            self.search_phrase(value=i,category="turismo")
        
        return self.list_suggestions