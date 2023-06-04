## =========> License Verification (Copyright ©️) <=========
## Programmer(s) : Omar Medhat Aly
## Date of Creation : 05.10.2022
## Date of Last Modification : 28.11.2022
## Institution \ Company : Alexandria University
## Supervised by : Dr.M. Habrook

import string  # # used for punctuation purposes
from datetime import (  # # famous package used in date stuff like converting dates to strft format
    date,
    datetime,
)
from enum import (  # # support for enumerations - Base class for creating enumerated constants.
    Enum,
)
from uuid import (  # # Universal Unique Identifier, is a python library which helps in generating random objects of 128 bits as ids
    uuid4,
)

import joblib  # # It has various usages but in our case just to initialize the Model
import numpy as np  # # the fastest Package to perform any Calculations

## we can only use pyttsx3 version 2.71 [very important]
import pyttsx3  # # text-to-speech conversion library in Python.
import speech_recognition as sr

## he generation of a v4 UUID is much simpler to comprehend. The bits that comprise a UUID v4 are generated randomly and with no inherent logic.
from essential_proccesses import (  # # that's self-created function to read json files and return it as a list
    get_json,
)
from geopy import (  # # Nominatim uses OpenStreetMap data to find locations on Earth by name and address (geocoding)
    Nominatim,
)
from nrclex import (  # # pretrained research Model by National Research Council Canada's
    NRCLex,
)

## PyOWM is a client Python wrapper library for OpenWeatherMap web APIs. It allows quick and easy consumption of OWM data from Python applications
from pyowm import (  # # Open Weather Management where we're using the Weather API we got access to
    OWM,
)
from transformers import (  # # the main Model of GPT-2 [FULL EXPLAINATION IN OTHER FILE]
    GPT2LMHeadModel,
    GPT2Tokenizer,
)

## we're using a petrained model so we just need to download it and upload to the Script
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")  ## GPT-2 small
model = GPT2LMHeadModel.from_pretrained("gpt2", pad_token_id=tokenizer.eos_token_id)
## old Model to detect Emotions for Emergency
emotion_detecion = joblib.load(open("Emotions_classification_model.pkl", "rb"))


class CONVERSATION:
    """
    That very First Class is the main class of all we've created as it initializes the conversation itself
    It doesn't take any parameters as it's just like an interactive conversations with the Microphone or any other thing that conducts a sound
    Here we are doing two main Stuff [Voice Recognition] and converting text to speech that can be understand by the bot of [1s and 0s] and
    the Human of the Known English
    """

    __name = ""
    __skill = []  ## list of skills that the robot gained or learned

    def __init__(self, name=None):
        """
        The Main class that's considered to be the brain of our AI based Robot Model
        Params:
        ------
            name : the name that we're going to give to it
        """
        self.engine = pyttsx3.init()
        self.voices = self.engine.getProperty("voices")
        ## changing the voice of the robot to be female
        self.engine.setProperty(
            "voice", self.voices[0].id
        )  # after some modifications in System Files now we can use 3 voices [0 --> 2]
        self.recognizer = sr.Recognizer()  ## voice recognition
        self.microphone = sr.Microphone()  ## the microphone we're going to use

        ## store the name that's have heared
        if name is not None:
            self.__name = name

        ## now trying to get rid of background noise when we're talking through our microphone
        print("I'm listening")
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(
                source=source
            )  ## Adjusts the energy threshold dynamically using audio from source (an AudioSource instance) to account for ambient noise.
            ## Intended to calibrate the energy threshold with the ambient energy level

    @property
    def name(self):
        ## if we're willing to change the name without messing the things up so we used property decorator
        return self.__name

    @name.setter
    def name(self, value):
        ## this function is used to make the maipulation a little bit easier and simple
        ## let's make it say something
        sentence = f"Welcome..Here is your Assistant {self.__name}..How can i help you?"
        self.__name = value
        self.engine.say(sentence)
        self.engine.runAndWait()  ## just like a delay function

    def say(self, sentence):
        self.engine.say(sentence)
        self.engine.runAndWait()  ## just like a delay function

    def __NewIdentity(self, name=None):
        ACCEPTANCE_PHRASES = get_json("data_essential.json", "acceptance_2", "reaction")
        user_name = name  ## get the name if you have kindly given it
        if name is not None:
            self.engine.say(
                f"Ok fine.. Hello {user_name}.It's Pleasure to meet you Today"
            )  ## to say the sentence above
            self.engine.runAndWait()

        else:
            ## it's essential to let the robot understand you in English
            self.engine.say(
                "Ok well. you're not a team member .. Do you mind telling me your Name ? that will help me to be more flexible "
            )  ## to say the sentence above
            self.engine.runAndWait()
            ## answering if you would like to say your name or not
            with self.microphone as source:
                ANS_1 = self.recognizer.listen(source=source)

            phrase = self.recognizer.recognize_google(
                ANS_1, show_all=False, language="en-us"
            )
            phrase_r = list(phrase.split(" "))
            for i in phrase_r:
                if i in ACCEPTANCE_PHRASES or phrase in ACCEPTANCE_PHRASES:
                    ## those lines are just the entrance of the Conversation .. The Robot is asking you for your name
                    self.engine.say(
                        "Ok What's your Name then?"
                    )  ## to say the sentence above
                    self.engine.runAndWait()
                    with self.microphone as source:
                        audio = self.recognizer.listen(
                            source=source
                        )  ## Records a single phrase from source (an AudioSource instance) into an AudioData instance, which it returns.
                        phrase = self.recognizer.recognize_google(
                            audio, show_all=False, language="en-uk"
                        )
                        user_name = phrase  ## store the name in that variable
                        self.engine.say(
                            f"Ok fine.. Hello {user_name}.It's Pleasure to meet you Today"
                        )  ## to say the sentence above
                        self.engine.runAndWait()
                ## if you refused to tell the robot your name
                else:
                    user_name = "Stranger"
                    self.engine.say(
                        f"Ok so I'll call you {user_name}.."
                    )  ## to say the sentence above
                    self.engine.runAndWait()

        ## now just testing the robot and it's performance
        sentence = f"{user_name} i've to say something to you.. that's only a testing phase you are just testing my performance of repeating and recognizing what you say.. so what do you wanna say then?"
        self.engine.say(sentence)
        self.engine.runAndWait()
        return user_name

    def IsMember(self):
        ## Names List
        NAMES = get_json(filename="team_members", tag="name")
        IDS = get_json(filename="team_members", tag="ID")
        ACCEPTANCE_PHRASES = get_json("data_essential.json", "acceptance", "reaction")
        user_name = ""
        ## it's essential to let the robot understand you in English
        self.engine.say(
            "Welcome..Here is your Assistant Tornado 1CAD1. Are you a Member of the Team that built me?"
        )  ## to say the sentence above
        self.engine.runAndWait()
        ## just  to check if you are a memeber or not
        with self.microphone as source:
            ans = self.recognizer.listen(source=source)
        phrase = self.recognizer.recognize_google(
            ans, show_all=False, language="en-us"
        )  ## Performs speech recognition on audio_data (an AudioData instance), using the Google Speech Recognition API.
        phrase_r = list(
            phrase.split(" ")
        )  ## just to be able to iterate through the words
        print(phrase_r)
        for x in phrase_r:
            if x in ACCEPTANCE_PHRASES:
                ## now catching your name
                self.engine.say("Tell me your name please..")
                self.engine.runAndWait()
                ## if you've proved you're a member so the robot will handle the conversation with your name
                with self.microphone as source:
                    ANS = self.recognizer.listen(source=source)
                phrase = self.recognizer.recognize_google(
                    ANS, show_all=False, language="en-us"
                )
                phrase_r = list(phrase.split(" "))
                print(phrase_r)
                ## here we're iterating over two lists at the same time
                for i in phrase_r:
                    if i in NAMES:
                        user_name = i
                        print(f"Welcome back {user_name}")
                        self.engine.say(
                            f"Welcome back {user_name}"
                        )  ## to say the sentence above
                        self.engine.runAndWait()
                        ## now just testing the robot and it's performance
                        sentence = f"{user_name} i've to say something to you.. that's only a testing phase you are just testing my performance of repeating and recognizing what you say.. so what do you wanna say then?"
                        self.engine.say(sentence)
                        self.engine.runAndWait()
                        break
                    else:
                        user_name = phrase.split(" ")
                        print(user_name)
                        ## the assistant can't confirm your identity
                        ## you'll be given two choices
                        self.engine.say(
                            "You're either not a Team Member or have said something wrong..would you like to try again or continue with a new identity"
                        )  ## to say the sentence above
                        self.engine.runAndWait()
                        ## getting your answer
                        with self.microphone as source:
                            ANS = self.recognizer.listen(source=source)
                        phrase = self.recognizer.recognize_google(
                            ANS, show_all=False, language="en-us"
                        )
                        phrase_r = list(phrase.split(" "))
                        print(phrase_r)
                        if "yes" in phrase_r or "try" in phrase_r:
                            ## using recursion to redo the process again
                            self.IsMember()
                        else:
                            ## creating a new identity
                            user_name = self.__NewIdentity(name=user_name)
            else:
                self.__NewIdentity()
        return user_name

    def text_generation(self, input_text: str):
        """
        To generate text using GPT-2 we just need to initialize it then encode the entered text from string form to binary form then applying some generations and finally
        return the output in the form of string after decoding
        """
        encoded_input = tokenizer.encode(
            input_text, return_tensors="pt"
        )  ## Firstly decoding of the text if ABC to 1s and 0s
        generator = model.generate(
            encoded_input,
            max_length=100,
            num_beams=5,
            no_repeat_ngram_size=2,
            early_stopping=True,
        )  ## the model is working now
        output = (
            tokenizer.decode(generator[0], skip_special_tokens=True)
            .translate(str.maketrans("", "", string.punctuation))
            .replace("\n", " ")[len(input_text) :]
        )  ## the output
        self.engine.say(output)
        self.engine.runAndWait()

    def listen(self, user_name):
        with self.microphone as source:
            audio = self.recognizer.listen(
                source=source
            )  ## Records a single phrase from source (an AudioSource instance) into an AudioData instance, which it returns.
        try:
            ## checking wether it got it or not
            phrase = self.recognizer.recognize_google(
                audio, show_all=False, language="en-us"
            )  ## Performs speech recognition on audio_data (an AudioData instance), using the Google Speech Recognition API.
            sentence = (
                f"got it, you've just said {phrase} "  ## just as a debugging line
            )
            self.engine.say(sentence)  ## to say the sentence above
            self.engine.runAndWait()
        except:
            print("That wasnot clear to me")
            self.engine.say(f"{user_name}That was'nt clear to me")
            self.engine.runAndWait()
        ## very important
        return phrase


## create enumerations for purposes we're going to see later
class Status(Enum):
    """
    This Enumeration are going to store the progress of the missions and tasks that the robot have been ordered to do
    we'll split 'em to three status and give each one a value [==> Just to know that's an Application of RL between the Agent and Award :)]
    [1] COMPLETED = 2 [2] IN_PROGRESS = 1 [3] NOT_STARTED = 0
    """

    COMPLETED = 2
    IN_PROGRESS = 1
    NOT_STARTED = 0


class Priority(Enum):
    """
    This Enumeration are going to store the priorities of the missions and tasks that the robot have been ordered to do
    we'll split 'em to three status and give each one a value as above
    [1] LOW = 0 [2] MEDIUM = 1 [3] HIGH = 2
    """

    HIGH = 2
    MEDIUM = 1
    LOW = 0


class ITEM:
    """Here we're going to preprare the items and the topics that can be either discussed with the robot or added"""

    __CREATION_DATE = date.today()  ## that will display the day
    __TITLE = "empty"  ## we should initialize the list of tasks to be empty and then full fill it with tasks and missions
    __STATUS = Status.NOT_STARTED  ## we haven't yet ordered anything :)
    __PRIORITY = Priority.LOW
    __FLAG = False  ## Boolen value
    __URL = ""  ## that will store the given url
    __DUE_DATE = date
    __STATE = False
    __NOTES = ""  ## The given notes
    __ICON = ""

    def __init__(self, title: str = None):
        ## checking that the title is not empty and store it
        if title is not None:
            self.__TITLE = title
        self.__ID = str(uuid4())  ## create a random unique id

    @property
    def title(self) -> str:
        ## make it easier to get manipulated - protect and do some check
        return self.__TITLE

    @title.setter
    def title(self, value):
        self.__TITLE = value

    ## doing the same for the following
    @property
    def priority(self):
        return self.__PRIORITY

    @priority.setter
    def priority(self, value):
        self.__PRIORITY = value

    @property
    def creation_date(self):
        return self.__CREATION_DATE

    @creation_date.setter
    def creation_date(self, value):
        self.__CREATION_DATE = value

    @property
    def age(self):
        ## that returns the age of creation
        return self.__CREATION_DATE - date.today()

    @property
    def status(self):
        return self.__STATUS

    @status.setter
    def status(self, value):
        self.__STATUS = value

    @property
    def due_date(self):
        return self.__DUE_DATE

    @due_date.setter
    def due_date(self, value: date):
        self.__DUE_DATE = value

    @property
    def icon(self):
        return self.__ICON

    @icon.setter
    def icon(self, value: str):
        self.__ICON = value

    @property
    def state(self):
        return self.__STATE

    @state.setter
    def state(self, value: bool):
        self.__STATE = value

    @property
    def id(self):
        return self.__ID

    @property
    def flag(self):
        return self.__FLAG

    @flag.setter
    def flag(self, value: bool):
        self.__FLAG = value

    @property
    def notes(self):
        return self.__NOTES

    @notes.setter
    def notes(self, value: str):
        self.__value = value

    @property
    def url(self):
        return self.__URL

    @url.setter
    def url(self, value):
        self.__URL = value


class TASKS:
    """Now let's get our hands dirty and combine all the last classes"""

    __TASKS = (
        []
    )  ## here is where we are going to store the tasks as the form of strings

    def __init__(self):
        # ## recalling this bunch of code from the Conversation class just to let the robot talk interactively
        # self.engine = pyttsx3.init()
        # self.voices = self.engine.getProperty('voices')
        # self.recognizer = sr.Recognizer() ## voice recognition
        # self.microphone = sr.Microphone() ## the microphone we're going to use
        ## now the robot is going to confirm that the list have been created
        print("Tasks List have been successfully created")
        # self.engine.say(f"I'm ready to take your orders")
        self._CURRENT = -1

    ## we need to expose all the different items in the last at a time
    ## the follwoing functions are magic methods which work anonymously
    def __iter__(self):
        return self

    def __next__(self):
        ## that line means that there is no items at all as a condition
        if self._CURRENT < len(self.__TASKS) - 1:
            self._CURRENT += 1  ## jumping to the next
            print(self.__TASKS[self._CURRENT].title)  ## return the title of the objects
            return self.__TASKS[self._CURRENT]
        else:
            ## otherwise setting the counter back again to the initialized value
            self._CURRENT = -1
        ## now we're going to tell the interperter (compiler in languages like C/C++) that there's no more items in the list
        ## so that we're going to raise a specific error
        raise StopIteration

    def __len__(self):
        return len(self.__TASKS)  ## that's simply returns how many items exist

    def new_item(self, item: ITEM):
        ## Adding the new order or task to the list
        self.__TASKS.append(item)

    @property
    def items(self) -> list:
        return self.__TASKS

    def show_progress(self):
        ## that function is just for debugging to check our list
        print("*" * 80)  ## adding a line
        for item in self.__TASKS:
            print(
                item.title, item.status, item.priority, item.age
            )  ## checking the following stuff

    def remove_item(self, uuid: str = None, title: str = None) -> bool:
        ## firstly if the robot didn't find neither any id or any title so you need to add something to your inputs
        if title is None and uuid is None:
            print(
                "I think there is something wrong .. you need to provide some information"
            )
            # self.engine.say(f"I think there is something wrong .. you need to provide some information")
            # self.engine.runAndWait()
        ## now if there's no id but it found a title so it executes like the following normally
        if uuid is None and title:
            for item in self.__TASKS:
                if item.title == title:
                    ## here if it found a duplicate it removes it and returns True
                    self.__TASKS.remove(item)
                    return True
            ## here if if didn't find the entered title so it returns an error
            # self.engine.say(f"I think the title of {title} isn't yet added to my Memory so you better choose something else as i don't find it")
            # self.engine.runAndWait()
            print(
                f"I think the title of {title} isn't yet added to my Memory so you better choose something else as i don't find it"
            )
            return False
        ## now if it found an id
        if uuid:
            self.__TASKS.remove(uuid)
            return True


class WeatherForecasting:
    """
    This Class returns a full Forecast of Weather according to your Location on Earth by Scrapping the Information from a Weather API
    we've used https://openweathermap.org/ website to do that stuff, we can use https://meteoblue.com as well but unfortunately it's only 6 days trial
    """

    ## Decalre the Location .. for our situation [Alexandria, Egypt]
    _LOCATION = "Alexandria, EG"
    ## our API key from OpenWeather
    API_KEY = "c328e7069830ea49e177c0db3e223a3a"

    def __init__(self, location="Alexandria, EG"):
        """Just declare and set the Variables that will be used to get the weather"""
        self.OpenWeather = OWM(self.API_KEY)  ## takes the API KEY to the MAP
        self.manager = (
            self.OpenWeather.weather_manager()
        )  ## weather Manager can be used for stuff like fetch air pollution data.
        ## to find the location we're in we need to create a locator with Nominatim
        locator = Nominatim(
            user_agent="myGeocoder"
        )  ## User_Agent is an http request header that is sent with each request.
        ## declare our location
        self.location = (
            location  ## that should be specifically correct as it's a database
        )
        loc = locator.geocode(
            self.location
        )  ## we've assigned our location to the geocoder
        ## Geocoding is the process of transforming a street address or other description of a location into a (latitude, longitude) coordinate
        ## so we're going to declare 'em
        self.lat = loc.latitude
        self.long = loc.longitude

    @property
    def get_weather(self):
        """
        That function should return the weather [forecasting]
        to just notice the API we've used is called "One Call API 2.7" from OpenWeather :)
        """
        forecasting = self.manager.one_call(
            lat=self.lat, lon=self.long
        )  ## that's what i'm talking about One Call API, takes the longitude and latitude of your location
        return forecasting  ## here it doesn't return the data as varibale , it returns as an object with it's location in memory that we should unpack

    def forecast(self):
        """That should return the forecast in the form of variable (string)"""
        """We can actually return many things like sunrise, humidty, sunset ,...etc"""
        forecasting = self.manager.one_call(lat=self.lat, lon=self.long)
        ## for me it's enough to just return only six forecasting items
        daily = forecasting.forecast_daily[0].detailed_status  ## weather status daily
        hourly = forecasting.forecast_hourly[
            0
        ].detailed_status  ## weather status hourly
        temp = (
            forecasting.forecast_daily[0].temperature("celsius").get("day")
        )  ## the temprature in celsius
        humidity = forecasting.forecast_daily[
            0
        ].humidity  ## THI index, we've casted it as everything should be the same type during printing
        uvi = forecasting.forecast_daily[
            0
        ].uvi  ## The UVI is a measure of the level of UV radiation
        sunrise = datetime.utcfromtimestamp(
            forecasting.forecast_daily[0].sunrise_time()
        ).strftime(
            "%H:%M:%S"
        )  ## time of sunrise
        sunset = datetime.utcfromtimestamp(
            forecasting.forecast_daily[0].sunset_time()
        ).strftime(
            "%H:%M:%S"
        )  ## time of sunset

        ## now creating our Report
        messege = f"The Weather Report of Today states in the Following :\nFor Status: The Forecasting says that it has {daily} Today\nFor Status the Last Hour : The Forecasting says that it has {hourly} Today\nFor Humidity: {self.THI_index(humidity=humidity)}\nFor Temprature: it says it's {temp} degree Celsius Today\nFor Ultraviolet Radiation: {self.UVI_index(uvi)}\nLastly the Sunset Today was at {sunset} , while the Sunrise was at {sunrise}"

        return messege

    def THI_index(self, humidity: int):
        """A temperature-humidity index (THI) is a single value representing the combined effects of air temperature
        and humidity associated with the level of thermal stress"""
        """
        Research from the Building Science Corporation found that humidity of 70% or higher adjacent to a surface can cause serious damage to the property. 
        The Health and Safety Executive recommendsthat relative humidity indoors should be maintained at 40-70%, while other experts recommend 
        that the range should be 30-60%
        """
        messege = ""
        if humidity in range(30, 61):
            messege = f"The Humidity is {humidity} Percentage, it's in the Perfect range according to experts"
        elif humidity in range(61, 71):
            messege = f"The Humidity is {humidity} Percentage,  it's still safe for chilling outside but it's almost pretty near to the Danger Zone, so take care"
        elif humidity > 70:
            messege = f"The Humidity is {humidity} Percentage , it's very Dangerous to go outside"
        ## return the messege
        return messege

    def UVI_index(self, uvi: float):
        """to detect the exact ranges we've used EPA [Environmental Protection Agency] paper to get the ranges"""
        messege = ""
        if uvi >= 1 and uvi < 3:
            messege = f"it's {uvi} which's Low UVI so no Screen Protection required"
        elif uvi >= 3 and uvi < 6:
            messege = f"it's {uvi} which's Moderate UVI so you Skin Protection"
        elif uvi >= 6 and uvi < 11:
            messege = "It's either High or Very High UVI, it's required to have Skin Protection"
        elif uvi > 11:
            messege = "Don't get out, it's Extremely high UVI"
        ## return the messege in the Report
        return messege


class EmotionDetection:
    """I've made a whole class to detect the emotions just bec we're going to choose between to models to display the Output
    by giving the Major to NRC reasearch
    """

    def __init__(self, input_text):
        self.text = input_text

    def TheMajorDetector(self):
        """The Major Model, It has just a Limitaion as if it couldn't detect the Emotion it'll return nothing
        so in that moment we'll switch to option 2 of our old Model
        """
        try:
            emotion = NRCLex(
                self.text
            )  ## taking the Input and perform the Operations on it
            ## the Following line is excecuted by that way as that Method returns propabilitis of various Emotions as Dictionary
            ## we just need the Highest emotion with the highest score
            output = list(emotion.raw_emotion_scores.keys())[
                np.argmax(list(emotion.raw_emotion_scores.values()))
            ]
            return output
        except ValueError or TypeError as e:
            MinorDetector(self.text)
        
    def MinorDetector(self):
        ## just for Emergency
        return emotion_detecion.predict([self.text])[0]
