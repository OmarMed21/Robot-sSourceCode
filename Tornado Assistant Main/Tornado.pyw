## till that moment we're going to call our robot "Tornado"
from main import CONVERSATION, TASKS, ITEM, WeatherForecasting, EmotionDetection ## import the proper dependencies
import pyjokes ## specific library to insert jokes
import joblib
from randfacts import randfacts ## an additional feature of telling you facts randomly
from essential_proccesses import get_json

Tornado = CONVERSATION()
tasks = TASKS()

def joke():
    funny = pyjokes.get_joke()
    print(funny)
    Tornado.say(funny)

def add_todo(user_name)->bool:
    item = ITEM()
    Tornado.say("Tell me your Orders ")
    try:
        item.title = Tornado.listen(user_name=user_name)
        TASKS().new_item(item)
        message = f"{item.title} has been Added {user_name}" 
        Tornado.say(message)
        return True
    except:
        print("Error")
        return False
    
def list_tasks():
    if len(tasks) >0:
        Tornado.say("That's Your list of Tasks")
        for item in tasks:
            Tornado.say(item.title)
    else:
        Tornado.say("I don't have any orders")

def remove_todo(user_name)->bool:
    Tornado.say(f"Which Task are you willig to remove {user_name}?")
    try:
        item_title = Tornado.listen(user_name=user_name)
        TASKS().remove_item(title=item_title)
        message = f"{item_title} has been Removed {user_name}"  
        Tornado.say(message)
        return True
    except:
        print("Error")
        return False

def weather_report():
    weather_report = WeatherForecasting()
    forecast = weather_report.forecast()
    print(forecast)
    Tornado.say(forecast)

def facts():
    fact = randfacts.get_fact()
    print(fact)
    Tornado.say(fact)

def EmotionDetector(command):
    return EmotionDetection(command)

def CommandTeller(tag, main='commands', json_file="data_essential.json"):
    ## i've assigned the parameters in that order to be away from that error (SyntaxError: non-default argument follows default argument
    output = get_json(json_file, tag, main)
    return output

joke_commands = ['joke', 'jokes', 'funny']
command = ""
#name = Tornado.IsMember()
name = "mark"
while True and command != "goodbye":
    situation = True
    command = Tornado.listen(name)
    print(f'command was : {command} \nI Think you got {EmotionDetector(command=command)} Feeelings')
    commad_lst = set(command.split(" ")) ## we've used set instead of list just for time complexity
    
    for i in commad_lst:
        if i in joke_commands:
            joke()
            situation = False

    for i in CommandTeller("add_commands"):
        if i in command :
            add_todo(name)
            command = ""
            situation = False

    for i in CommandTeller("list_commands"):
        if i in command:
            list_tasks()
            command = ""
            situation = False

    if command in ["remove"]:
        remove_todo(name)
        command = ""
        situation = False

    for i in CommandTeller("weather_commands"): 
        if i in command:
            weather_report()
            command = ""
            situation = False
            
    for i in CommandTeller("fact_commands"):
        if i in command:
            facts()
            command = ""
            situation = False

    if situation:
        Tornado.text_generation(command)

Tornado.say(f"It was a pleasure {name} to meet you today ,, please come back later when you are free .. see you!!")
