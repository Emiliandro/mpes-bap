# pip install nodejs-bin
from nodejs import node, npm, npx
import feedreader.feedreader as fr

# control variables
running = 0
max_chances = 10

# run javascript webscrapper
def get_from_webscrapping():
    node.call(['scraping/index.js'])

# run python feed reader
def get_all_from_feedbreader():
    fr.get_organic_results()

def get_input_from_feedreader():
    print ("Type the topic of your research")
    tag_for_feedreader = str(input())
    result = fr.get_if_contain(tag_for_feedreader)
    for msg in result:
      print(msg.toJson())

def end_loop():
    print("Ending")
    running = 10

def get_categories():
    categories = fr.get_categories()
    print(categories)

def commands():
    print("What do want to do?")
    print("Type 0 to use the feed reader to research an specific subject")
    print("Type 1 to use the feed reader to research all values")
    print("Type 2 to use the web scrapping to research an example value")
    print("Type 3 to use the web scrapping to research an specific subject")
    print("Type 98 to see the categories in feed reader")
    print("Type 99 no exit")
    print ("----------------------------")
    print("Enter your input:")
    action =  int(input())
    match action:
        case 99: 
            end_loop()
        case 98: 
            get_categories()
        case 0: 
            get_input_from_feedreader()
        case 1: 
            get_all_from_feedbreader()
        case __: 
            get_from_webscrapping()
    print ("----------------------------")

while (running < max_chances):
    running+=1
    print("Executing",running,"from",max_chances,"chances")
    if (running >= max_chances):
        break
    commands()