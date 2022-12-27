# from asyncio import Task
# import pyttsx3
# import json
# import speech_recognition as sr
# from main import ITEM, CONVERSATION, TASKS, WeatherForecasting
# from pyowm import OWM
# from geopy import Nominatim
# from datetime import datetime
from essential_proccesses import get_json

# recognizer = sr.Recognizer()
# microphone = sr.Microphone()
# engine = pyttsx3.init()

# # for i in range(len(new_dict)):
# #     engine.say(new_dict[i])
# #     engine.runAndWait()

# # # i = "i'm so young"
# # # y = "the Aham is here"
# # # i = list(i.split(" "))
# # # y = list(y.split(" "))
# # # if "the" in y:
# # #     print(1)


# # # import speech_recognition as sr
# # # import pyttsx3

# # # with sr.Microphone() as source:
# # #     ans = sr.Recognizer().listen(source=source)
# # #     p = sr.Recognizer().recognize_google(ans, show_all=False, language="en-us")


# # # print(list(p.split(" ")))
# # # if "joke" in p:
# # #     print(0)

# with open('team_members.json') as f:
#     dt = json.load(f)
# new_dict = list()
# for i in dt:
#     new_dict.append(i['name'])

# def NewIdentity():
#     ## it's essential to let the robot understand you in English
#     engine.say("Ok well. you're not a team member .. Do you mind telling me your Name ? that will help me to be more flexible ") ## to say the sentence above
#     engine.runAndWait()
#     ## answering if you would like to say your name or not
#     with microphone as source:
#         ANS_1 = recognizer.listen(source=source)

#     phrase = recognizer.recognize_google(ANS_1, show_all=False, language='en-us')
#     phrase_r = list(phrase.split(" "))
#     for _ in phrase_r:
#         if "no" in phrase_r:
#         ## those lines are just the entrance of the Conversation .. The Robot is asking you for your name
#             engine.say("Ok What's your Name then?") ## to say the sentence above
#             engine.runAndWait()
#             with microphone as source:
#                 audio = recognizer.listen(source=source) ## Records a single phrase from source (an AudioSource instance) into an AudioData instance, which it returns.
#                 phrase = recognizer.recognize_google(audio, show_all=False, language='en-uk')
#                 user_name= phrase ## store the name in that variable
#                 engine.say(f"Ok fine.. Hello {user_name}.It's Pleasure to meet you Today") ## to say the sentence above
#                 engine.runAndWait()
#         ## if you refused to tell the robot your name
#         else:
#             user_name = "Stranger"
#             engine.say(f"Ok so I'll call you {user_name}..") ## to say the sentence above
#             engine.runAndWait()

#     ## now just testing the robot and it's performance
#     sentence = f"Ok {user_name} that's only a testing phase you are just testing my performance of repeating and recognizing what you say.. so what do you wanna say then?"
#     engine.say(sentence)
#     engine.runAndWait()
#     return user_name

# def IsMember():
#     ## Names List
#     NAMES = new_dict
#     user_name = ""
#     ## it's essential to let the robot understand you in English
#     engine.say("Welcome..Here is your Assistant Tornado 1CAD1. Are you a Member of the Team that built me?") ## to say the sentence above
#     engine.runAndWait()
#     ## just  to check if you are a memeber or not
#     with microphone as source:
#             ans = recognizer.listen(source=source)
#     phrase = recognizer.recognize_google(ans, show_all=False, language='en-us') ## Performs speech recognition on audio_data (an AudioData instance), using the Google Speech Recognition API.
#     phrase_r = list(phrase.split(" ")) ## just to be able to iterate through the words
#     print(phrase_r)
#     if "yes" in phrase_r:
#         ## now catching your name
#         engine.say("Tell me your name please..")
#         engine.runAndWait()
#         ## if you've proved you're a member so the robot will handle the conversation with your name
#         with microphone as source:
#             ANS = recognizer.listen(source=source)
#         phrase = recognizer.recognize_google(ANS, show_all=False, language='en-us')
#         phrase_r = list(phrase.split(" "))
#         print(phrase_r)
#         ## here we're iterating over two lists at the same time
#         for i in range(len(phrase_r)):
#             if phrase_r[i] in NAMES:
#                 user_name = phrase_r[i]
#                 print(f"Welcome back {user_name}")
#                 engine.say(f"Welcome back {user_name}") ## to say the sentence above
#                 engine.runAndWait()
#                 break
#             else:
#                 ## the assistant can't confirm your identity
#                 ## you'll be given two choices
#                 engine.say("You're either not a Team Member or have said something wrong..would you like to try again or continue with a new identity") ## to say the sentence above
#                 engine.runAndWait()
#                 ## getting your answer
#                 with microphone as source:
#                     ANS = recognizer.listen(source=source)
#                 phrase = recognizer.recognize_google(ANS, show_all=False, language='en-us')
#                 phrase_r = list(phrase.split(" "))
#                 print(phrase_r)
#                 if "yes" in phrase_r or "try" in phrase_r:
#                     ## using recursion to redo the process again
#                     IsMember()
#                 else:
#                     ## creating a new identity
#                     user_name = NewIdentity()
#     else:
#         NewIdentity()
# IsMember()


# with open("data_essential.json") as f:
#     dt = json.load(f)
# for i in dt["reaction"]:
#     pass

# print(i["acceptance"])
# Tornado = CONVERSATION()
# def add_todo(user_name)->bool:
#     item = ITEM()
#     Tornado.say(f"Tell me your Orders {user_name}")

#     item.title = Tornado.listen(user_name=user_name)
#     TASKS().new_item(item=item)
#     message = "Added" + item.title
#     Tornado.say(message)
#     return True

# add_todo("omar")

# API_KEY = "c328e7069830ea49e177c0db3e223a3a"

# OpenWeather = OWM(API_KEY) ## takes the API KEY to the MAP
# manager = OpenWeather.weather_manager() ## weather Manager can be used for stuff like fetch air pollution data.
# ## to find the location we're in we need to create a locator with Nominatim
# locator = Nominatim(user_agent="myGeocoder") ## User_Agent is an http request header that is sent with each request.
# ## declare our location
# location = "Alexandria, EG"
# loc = locator.geocode(location) ## we've assigned our location to the geocoder
# ## Geocoding is the process of transforming a street address or other description of a location into a (latitude, longitude) coordinate
# ## so we're going to declare 'em
# lat = loc.latitude
# long = loc.longitude
# forecasting = manager.one_call(lat=lat, lon = long)
# # daily = str(forecasting.forecast_daily[0].detailed_status)
# # print(daily)
# weather_report = WeatherForecasting()
# forecast = weather_report.forecast()
# print(forecast)
# print(forecasting.forecast_daily[0].uvi)
# # Tornado.say(forecast)

# engine = pyttsx3.init()
# speech = engine.getProperty('voices')
# engine.setProperty('voice', speech[2].id)
# engine.say("Hello I'm here to make your fucking life")
# engine.runAndWait()
# x = "omar medhat aly"
# x = list(x.split(" "))
# names = get_json('team_members','name')
# for i in range(len(x)):
#     if x[i] in names[i].lower():
#         print("ok")
#         break
#     else:
#         print('no')
#         continue


def CommandTeller(tag, main="commands", json_file="data_essential.json"):
    output = get_json(json_file, tag, main)
    return output


r = CommandTeller(tag="add_commands")
x = "add more tasks"
x = set(x.split(" "))
for i in r:
    if i in x:
        print("x")
