from langdetect import detect
from urllib.request import urlopen
from urllib.error import URLError, HTTPError

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
        unique_sources = set()
        deduplicated_messages = []

        for message in messages:
            if message["source"] not in unique_sources:
                deduplicated_messages.append(message)
                unique_sources.add(message["source"])

        return deduplicated_messages

    def validateUrl(self,url):
        try:
            response = urlopen(url)
            print("The URL exists")
        except HTTPError as e:
            print("The URL does not exist (HTTP Error)")
            return False
        except URLError as e:
            print("The URL does not exist (URL Error)")
            return False
        
        return True