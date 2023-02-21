import pickle
# using duckduckgo_search, because DuckDuckGo does not collect or share personal
# information. That its privacy policy, it prevents search leakage by default.  
# read more about it at https://duckduckgo.com/privacy
from duckduckgo_search import ddg_suggestions, ddg

# escape function causes param to be rendered as text, preventing the execution of 
# injection script in the user’s browser or the in the api request.
from markupsafe import escape

#for feed in feed_categories:
#    results = ddg_suggestions(feed, region='br-pt')
#    for result in results:    
#        print("\"",result['phrase'],"\",")

class BapDDG():
    def phrase_to_search(self,value):
        self.phrase_to_results = ddg(value, region='br-pt', safesearch='on', time='y', max_results=5)

        for phrase in self.phrase_to_results:
            new_phrase = { 
                    "description":phrase['body'],
                    "title":phrase['title'],
                    "source":phrase['href'],
                    "categorie":"none" }

            self.list_suggestions.append(new_phrase)

    def __init__(self,debugMode=False,export=False):
        self.list_suggestions = []

        if (debugMode):
            for i in [" autoesporte "," autoesporte g1 "," tecnologia da informação tempo de curso "," memória social e memória coletiva "," quais as tecnologias utilizadas em memórias "," revista de memoria social "," economia de energia do pc "," economia de energia monitor "," economia de água e energia elétrica "," economia de energia com energia solar "," opções de economia de energia "," economia criativa no brasil "," turismo sustentável açores "]:
                self.phrase_to_search(value=i)
        else:
            print("Debug Mode is offline")

        if (export):
            # total time 14 minutes
            with open("bap_ddg_resultss.txt", "wb") as f:
                pickle.dump(self.list_suggestions, f, protocol=pickle.HIGHEST_PROTOCOL)
        else:
            print("Export is disable")

something = BapDDG(True,True)