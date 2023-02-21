import pickle
from langdetect import detect

class DataHelper(object):
    def removeNotPortuguese(self,messages):
        filtered_dictionaries = []
        for phrase in messages:
            if detect(phrase["description"]) == "pt":
                filtered_dictionaries.append(phrase)
            return filtered_dictionaries

    def removeMinDescription(self,messages):
        return [d for d in messages if len(d.get("description", "")) >= 50]

    def removeDuplicates(self, messages):
        return [dict(t) for t in {tuple(d.items()) for d in messages if "source" in d and not any(d["source"] == x["source"] for x in messages if x is not d)}]

helper = DataHelper()
current_dictionaries = []

def get_test_file():
    try:
        file = open('bap_ddg_resultss.txt', 'rb')
        dictionary_list = pickle.load(file)
        
        for d in dictionary_list:
            current_dictionaries.append(d)
        file.close()
    except:
        print("Something unexpected occurred!")

get_test_file()
print ("alpaca",len(current_dictionaries))

remove_duplicates_current_dictionaries = helper.removeDuplicates(current_dictionaries)
print ("alpaca",len(remove_duplicates_current_dictionaries))

remove_min_description_dictionaries = helper.removeMinDescription(remove_duplicates_current_dictionaries)
print ("alpaca",len(remove_min_description_dictionaries))

remove_nonpt_descriptions_dictionaries = helper.removeMinDescription(remove_min_description_dictionaries)
print ("alpaca",len(remove_nonpt_descriptions_dictionaries))