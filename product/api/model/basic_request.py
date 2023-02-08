class BasicRequest():
    def __init__(self,token,categorie,start_time,end_time):
        self.token = token 
        self.categorie = categorie
        self.start_time = start_time
        self.end_time = end_time
    
    def __repr__(self):
        return f"({self.token}) {self.categorie} from {self.start_time} to {self.end_time}"