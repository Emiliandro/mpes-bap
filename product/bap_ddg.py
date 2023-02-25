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
    def set_categories(self,categories):
        self.categories = categories

    def search_phrase(self,value,category='none'):
        self.phrase_to_results = ddg(value, region='br-pt', safesearch='on', time='y', max_results=9)

        for phrase in self.phrase_to_results:
            new_phrase = { 
                    "description":str(phrase['body']),
                    "title":str(phrase['title']),
                    "source":str(phrase['href']),
                    "category":str(category)}

            self.list_suggestions.append(new_phrase)

    def __init__(self,today):
        self.list_suggestions = []
        self.file_name = "" + today + ".txt"
        self.categories = []

    def make_txt_file(self):

        for i in self.categories:
            self.search_phrase(value=i,category=i)

        for i in [" autoesporte "," autoesporte g1 "," auto esporte globo "," autoesporte domingo "," autoesporte passo fundo "," autoesporte qual comprar 2022 "," autoesporte mclaren "," auto esporte revista "," autoesporte g1 "," auto esporte globo "," auto esporte globoplay "," auto esporte globo domingo "," autoesporte domingo "," auto esporte revista "," autosport revista "," autoesporte g1 "," auto esporte globo "," auto esporte globoplay "," auto esporte globo domingo "," auto esporte globoplay "," auto esporte globo domingo "," auto esporte de hoje domingo "," auto esporte globo hoje "," auto esporte de domingo "," auto esporte na globo "," auto esporte globo ontem "," programa auto esporte globo "," auto esporte globo play "," autoesporte domingo "," autoesporte passo fundo "," auto esporte passo fundo telefone "," auto esporte passo fundo rs "," auto esporte passo fundo centro "," autoesporte mclaren "," autosport mclaren f1 forum "," autosport mclaren f1 forum "," automotive forums mclaren f1 "]:
            self.search_phrase(value=i,category="autoesporte")

        for i in [" tecnologia "," tecnologia da informação "," tecnologia assistiva "," tecnologia 5g "," tecnologia na educação "," tecnologia sinônimo "," tecnologias disruptivas "," tecnologia e inovação "," tecnologia da informação "," tecnologia da informação faculdade "," tecnologia da informação e comunicação ", " tecnologia g1"]:
            self.search_phrase(value=i,category="tecnologia")
            
        for i in [" turismo sustentável", "turismo g1"]:
            self.search_phrase(value=i,category="turismo")
        
        with open(self.file_name, "wb") as f:
            pickle.dump(self.list_suggestions, f, protocol=pickle.HIGHEST_PROTOCOL)
