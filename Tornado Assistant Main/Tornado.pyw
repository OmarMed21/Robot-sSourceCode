## till that moment we're going to call our robot "Tornado"
from main import CONVERSATION, TASKS, ITEM ## import the proper dependencies
import pyjokes ## specific library to insert jokes
import joblib

Tornado = CONVERSATION()
tasks = TASKS()
emotion_detecion = joblib.load(open("Emotions_classification_model.pkl", "rb"))

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

joke_commands = ['joke', 'jokes', 'funny']
command = ""
#name = Tornado.IsMember()
name = "mark"
while True and command != "goodbye":
    situation = True
    command = Tornado.listen(name)
    print(f'command was : {command} of type {type(str(command))}\nI Think you got {emotion_detecion.predict([command])[0]} Feeelings')
    commad_lst = list(command.split(" "))
    
    for i in commad_lst:
        if i in joke_commands:
            joke()
            situation = False

    if "add" in command :
        add_todo(name)
        command = ""
        situation = False

    if "list" in command:
        list_tasks()
        command = ""
        situation = False

    if command in ["remove"]:
        remove_todo(name)
        command = ""
        situation = False

    if situation:
        Tornado.text_generation(command)

Tornado.say(f"It was a pleasure {name} to meet you today ,, please come back later when you are free .. see you!!")
