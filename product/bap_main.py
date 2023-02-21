from data_helper import DataHelper
from bap_ddg import BapDDG

import datetime
import pickle

today = datetime.datetime.today()
today_str = today.strftime('%Y-%m-%d')

class BapMain():
    def __init__(self):
        self.file_name = "" + today_str + ".txt"
        self.valdation = DataHelper()
        self.webscrapper = BapDDG(today_str)
        self.webscrapper.makeTxtFile()

        self.current_dictionaries = []

        def get_test_file():
            try:
                file = open(self.file_name, 'rb')
                dictionary_list = pickle.load(file)
                
                for d in dictionary_list:
                    self.current_dictionaries.append(d)
                file.close()
            except:
                print("Something unexpected occurred!")

        get_test_file()
        print ("alpaca",len(self.current_dictionaries))

        remove_duplicates_current_dictionaries = self.valdation.removeDuplicates(self.current_dictionaries)
        print ("alpaca",len(remove_duplicates_current_dictionaries))

        remove_min_description_dictionaries = self.valdation.removeMinDescription(remove_duplicates_current_dictionaries)
        print ("alpaca",len(remove_min_description_dictionaries))

        remove_nonpt_descriptions_dictionaries = self.valdation.removeMinDescription(remove_min_description_dictionaries)
        print ("alpaca",len(remove_nonpt_descriptions_dictionaries))

start = BapMain()