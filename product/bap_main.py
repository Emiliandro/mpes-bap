from data_helper import DataHelper
from bap_ddg import BapDDG

import datetime
import pickle

today = datetime.datetime.today()
today_str = today.strftime('%Y-%m-%d')

class BapMain():
    def createTodayFile(self):
        self.webscrapper.makeTxtFile()

    def getTodayFile(self):
        try:
            file = open(self.file_name, 'rb')
            dictionary_list = pickle.load(file)
            
            for d in dictionary_list:
                self.current_dictionaries.append(d)
            file.close()
        except:
            print("Something unexpected occurred!")
    
    def getAndValidateTodayFiles(self,create_file=False):
        self.getTodayFile()
        print ("alpaca",len(self.current_dictionaries))

        remove_duplicates_current_dictionaries = self.valdation.removeDuplicates(self.current_dictionaries)
        print ("alpaca",len(remove_duplicates_current_dictionaries))

        remove_min_description_dictionaries = self.valdation.removeMinDescription(remove_duplicates_current_dictionaries)
        print ("alpaca",len(remove_min_description_dictionaries))

        remove_nonpt_descriptions_dictionaries = self.valdation.removeMinDescription(remove_min_description_dictionaries)
        print ("alpaca",len(remove_nonpt_descriptions_dictionaries))

        if(create_file):
            with open("validated_"+self.file_name, "wb") as f:
                pickle.dump(remove_nonpt_descriptions_dictionaries, f, protocol=pickle.HIGHEST_PROTOCOL)

        return remove_nonpt_descriptions_dictionaries
            
    def __init__(self):
        self.file_name = "" + today_str + ".txt"
        self.valdation = DataHelper()
        self.webscrapper = BapDDG(today_str)
        self.current_dictionaries = []
        
    def getMessages(self):
        self.createTodayFile()
        self.today_files = self.getAndValidateTodayFiles(create_file=True)
        return self.today_files