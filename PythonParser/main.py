from __future__ import print_function
import sys

import fileinput
import decimal
import fileinput
import csv
import naoqi
import os

from mutagen.mp3 import MP3
from speechFiler import speech_file
import qi
import time
from contextlib import closing
from pepper_robot.robot import *
import pepper_robot.config

PEPPER_PORT = 9559
PEPPER_IP = '192.168.50.155'
INPUT_FILE = 'InputScript2.txt'
# Press Shiffor line in fileinput.input(encoding="utf-8"):
# t+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

#import torch
#from transformers import pipeline, DistilBertTokenizer, DistilBertForSequenceClassification, TextClassificationPipeline


#model_id = "lxyuan/distilbert-base-multilingual-cased-sentiments-student"


#def analyze_sentiment(text):
#    sentiment_analyzer = pipeline("sentiment-analysis", model=model_id, top_k=None)
#    result = sentiment_analyzer(text)
#    return result[0]['label'], result[0]['score']


class ScriptLine:
    def __init__(self, voice=-1, text=None, gestures=[]):
        self.voice = voice
        self.text = text
        self.gestures = gestures

    def __str__(self):
        string = ('\033[91mVoice: {} \033[0m| \033[92mText: "{}" \033[0m| \033[93mGestures: '
                  .format(self.voice, self.text))
        for i in range(len(self.gestures)):
            if i < len(self.gestures) - 1:
                string += self.gestures[i]
                string += ', '
            else:
                string += self.gestures[i]
        return string

    def help_csv(self):
        array = [self.voice, self.text]
        for i in range(len(self.gestures)):
            array.append(self.gestures[i])
        return array

    def append_to_csv(self, filename):
        with open(filename, 'a') as f:
            writer = csv.writer(f)
            writer.writerow(self.help_csv())


def run_behavior(ip, port, behavior_name):
    session = qi.Session()
    try:
        session.connect("tcp://" + ip + ":" + str(port))
    except RuntimeError:
        print ("Can't connect to Naoqi at ip \"" + ip + "\" on port " + str(port) +".\n"
                                                                                   "Please check your script arguments. Run with -h option for help.")
        sys.exit(1)

    behavior_mng_service = session.service("ALBehaviorManager")
    getBehaviors(behavior_mng_service)
    launchAndStopBehavior(behavior_mng_service, behavior_name)
    defaultBehaviors(behavior_mng_service, behavior_name)


def getBehaviors(behavior_mng_service):
    """
    Know which behaviors are on the robot.
    """
    names = behavior_mng_service.getInstalledBehaviors()
    print ("Behaviors on the robot:")
    print (names)
    names = behavior_mng_service.getRunningBehaviors()
    print ("Running behaviors:")
    print (names)

def launchAndStopBehavior(behavior_mng_service, behavior_name):
    """
    Launch and stop a behavior, if possible.
    """
    # Check that the behavior exists.
    if behavior_mng_service.isBehaviorInstalled(behavior_name):
        # Check that it is not already running.
        if not behavior_mng_service.isBehaviorRunning(behavior_name):
            # Launch behavior. This is a blocking call, use _async=True if you do not
            # want to wait for the behavior to finish.
            behavior_mng_service.runBehavior(behavior_name, _async=True)
            time.sleep(0.5)
        else:
            print ("Behavior is already running.")
    else:
        print ("Behavior not found.")
    return

    names = behavior_mng_service.getRunningBehaviors()
    print ("Running behaviors:")
    print (names)

    # Stop the behavior.
    if behavior_mng_service.isBehaviorRunning(behavior_name):
        behavior_mng_service.stopBehavior(behavior_name)
        time.sleep(1.0)
    else:
        print ("Behavior is already stopped.")
    names = behavior_mng_service.getRunningBehaviors()
    print ("Running behaviors:")
    print (names)

def defaultBehaviors(behavior_mng_service, behavior_name):
    """
    Set a behavior as default and remove it from default behavior.
    """
    # Get default behaviors.
    names = behavior_mng_service.getDefaultBehaviors()
    print ("Default behaviors:")
    print (names)
    # Add behavior to default.
    behavior_mng_service.addDefaultBehavior(behavior_name)
    names = behavior_mng_service.getDefaultBehaviors()
    print ("Default behaviors:")
    print (names)
    # Remove behavior from default.
    behavior_mng_service.removeDefaultBehavior(behavior_name)
    names = behavior_mng_service.getDefaultBehaviors()
    print ("Default behaviors:")
    print (names)


# def check_speed(line_number, line):
#    # extracts the speed number (1-5) before the '#'
#    line_speed = line.partition('#')[0]
#    # checks if the speed number is valid, else error
#    if not line_speed.isdigit():
#        print(f"\033[1:91mIn Script line({line_number}): speed (prior to '#') is snot a positive integer\033[0m")
#        exit(1)
#    else:
#        line_speed = int(line_speed)
#    if line_speed < 1 or line_speed > 5:
#        print(f"\033[1:91mIn Script line({line_number}): speed out of range: {line_speed}\033[0m")
#        exit(1)
#    return line_speed


# RETURNS an int of the voice
def extract_voice(line):
    return line.partition(')')[0]


# RETURNS an array of gestures in the form: BLAH #gesture1 BLAH #gesture2 BLAH -> arr = [gesture1, gesture 2]
def extract_gesture(line):
    gesture_count = line.count('#')
    gestures = [''] * gesture_count
    for i in range(gesture_count):
        # removes all to the left of the first '#'
        gestures[i] = line.partition('#')[2]
        # copies the removal to the running line string
        line = gestures[i]
        # removes all after the gesture
        gestures[i] = gestures[i].partition(' ')[0]
        gestures[i] = gestures[i].rstrip('\n ')
        gestures[i] = gestures[i].lstrip('\n ')
    return gestures


def extract_text(line):
    # get rid of the "person" syntax
    line = line.partition(')')[2]
    gesture_count = line.count('#')
    # initialize empty line to build
    text = ""
    for i in range(gesture_count + 1):
        # adds the text to the left of the leftmost gesture
        text += line.partition('#')[0]
        # updates the running line to remove up to the leftmost gesture
        line = line.partition('#')[2]
        # updates the running line to remove the leftmost gesture
        line = line.partition(' ')[2]
    text = text.rstrip('\n ')
    text = text.lstrip('\n ')
    return text


#def print_line_sentiments(line_number, sentiment_file_results):
#    # prints out these line-sentiments
#    for i in range(3):
#        current_sentiment_label = sentiment_file_results[line_number][0][i]['label'].upper()
#        # labels the color to the sentiment
#        if current_sentiment_label == 'POSITIVE':
#            print('\033[92m', )
#        elif current_sentiment_label == 'NEGATIVE':
#            print('\033[91m')
#        elif current_sentiment_label == 'NEUTRAL':
#            print('\033[93m')
#        print('\t',current_sentiment_label,)
#        print('\033[0m \t', round(sentiment_file_results[line_number][0][i]['score'] * 100, 2), '%')
#    return


def main():
    # setup CIIRC Pepper API qi wrapper
    pepper = Pepper(PEPPER_IP, PEPPER_PORT)
    # receive text input from script file
    input_script = fileinput.input(files=INPUT_FILE)
    # open file
    fp = open(INPUT_FILE, 'r')
    lines = len(fp.readlines())
    line_results = [lines]
    fp.close()
    for line in input_script:
        # Extract line to class
        line_number = fileinput.lineno()
        voice = extract_voice(line)
        text = extract_text(line)
        gestures = extract_gesture(line)
        testing_class = ScriptLine(voice, text, gestures)
        print(testing_class)
        #testing_class.append_to_csv('OutputScript.csv')

        # Outputs sound file
        # output_file= 'line' + str(line_number) + ''
        # speech_file(text, 1, output_file)
        # audio = MP3(output_file)
        # playtime = audio.info.length
        # pepper.play_sound(output_file + '.mp3')

        # testing below
        session = qi.Session()
        session.connect("tcp://" + PEPPER_IP + ":" + str(PEPPER_PORT))
        tts = session.service("ALTextToSpeech")

        # Testing Below
        tts.say(text)
        behavior_mng_service = session.service("ALBehaviorManager")
        if gestures[0] == "wave":
            run_behavior(PEPPER_IP,PEPPER_PORT,"dancemoves-a0f94b/Wave and bow")
            time.sleep(11.0)
            behavior_mng_service.stopBehavior("dancemoves-a0f94b/Wave and bow") 
        elif gestures[0] == "shocked":
            run_behavior(PEPPER_IP,PEPPER_PORT,"animations/Stand/Emotions/Negative/Shocked_1")
            time.sleep(4.5)
            behavior_mng_service.stopBehavior("animations/Stand/Emotions/Negative/Shocked_1") 
        run_behavior(PEPPER_IP, PEPPER_PORT, "boot-config/animations/poseInitUp")
        time.sleep(1.2)
        run_behavior(PEPPER_IP, PEPPER_PORT, "boot-config/animations/poseInitUp")

    fileinput.close()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
