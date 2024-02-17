
from __future__ import print_function
import fileinput
import decimal
import fileinput
import csv
import naoqi
from contextlib import closing

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
    # receive text input from script file
    input_script = fileinput.input(files='InputScript.txt')

    fp = open(r'InputScript.txt', 'r')
    lines = len(fp.readlines())
    line_results = [lines]
    fp.close()

    # goes through each line of file
    for line in input_script:
        #line_number = fileinput.lineno()
        voice = extract_voice(line)
        text = extract_text(line)
        gestures = extract_gesture(line)
        testing_class = ScriptLine(voice, text, gestures)
        print(testing_class)
        testing_class.append_to_csv('OutputScript.csv')
    fileinput.close()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
