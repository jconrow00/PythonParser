from __future__ import print_function
import sys
import fileinput
import decimal
import fileinput
import csv
import os
import inspect
from mutagen.wave import WAVE

sys.path.insert(1, os.path.realpath(os.path.pardir))

from gesturesConfig import *
# to find INPUT_FILE
from config import *

import timez
from contextlib import closing
import execnet

# import urllib3.contrib.pyopenssl
# import certifi
# import urllib3
# http = urllib3.PoolManager(
#     cert_reqs='CERT_REQUIRED',
#     ca_certs=certifi.where()
# )
# urllib3.contrib.pyopenssl.inject_into_urllib3()




def speech_file(mytext="Hello World", output_file="output", voice= "tts_models/en/jenny/jenny", chosen_language = None, chosen_speaker = None):
    import torch
    from TTS.api import TTS
    # Get device
    device = "cuda" if torch.cuda.is_available() else "cpu"
    # List available 🐸TTS models
    print(TTS().list_models())
    # Init TTS with the target model name
    tts = TTS(model_name = voice, progress_bar=False).to(device)
    # Run TTS
    tts.tts_to_file(text=mytext, file_path=output_file, language=chosen_language, speaker=chosen_speaker)


# CLASS that holds the characteristics of a script line
class ScriptLine:
    def __init__(self, current_timestamp, line="1) Hello #wave World", line_num=1, ):
        # Sets almost all class variables
        self.line_no = line_num
        self.current_timestamp = current_timestamp
        self.line = line
        self.text = self.extract_text()
        self.voice = self.extract_voice()
        self.gesture_arr = self.extract_gesture()
        self.gesture_pos_arr = self.extract_gesture_pos()

        # Outputs sound file if NOT '0' (human)
        if self.voice != '0':
            self.output_file = '../outputs/' + 'line' + str(line_num) + '.wav'
            # if no voice for this line
            if self.text:
                speech_file(self.text, self.output_file, get_voice_name(int(self.voice)))
                # Get audio length
                audio = WAVE(self.output_file)
                self.voice_time = round(audio.info.length, 3)
            else:
                # Creates an empty file
                with open(self.output_file, 'w') as fp:
                    pass
                self.voice_time = 0.0

            # Sets gesture_time class variable
            self.gesture_time = 0.0
            for i in range(len(self.gesture_arr)):
                # Error handling for non-gesture
                if get_gesture_length(self.gesture_arr[i]) == 0.0:
                    print("\033[91mUnknown gesture \"" + self.gesture_arr[i] + "\" in Line " + str(self.line_no) + "\033[0m")
                    exit(1)
                self.gesture_time = round(float(get_gesture_length(self.gesture_arr[i])) + self.gesture_time, 3)
                # self.gesture_time = round(float(get_gesture_length(self.gesture_arr[i]) + 2 * (get_gesture_length("init"))) + self.gesture_time, 3)  # account for 0.4sec 'init' pos beforehand and after PER gesture in array


            #fills human out
            # put file with spacers
            with open('../outputs/' + 'lines(human).txt', "a") as myfile:
                myfile.write('\trobot: ' + self.line)
        # If '0' (human)
        else:
            self.output_file = '../outputs/' + 'lines(human).txt'
            with open(self.output_file, "a") as myfile:
                myfile.write('line' + str(self.line_no) + ': ' + self.line)
            # based on 130 WPM speech
            self.voice_time = round(float(self.text.count(' ')) * 60.00 / 130.00, 3)
            # gesture length assumed to exactly fit in the length of speech
            self.gesture_time = self.voice_time

        self.total_time = 0.0

        self.help_csv()


    def __str__(self):
        string = ('\033[94mPlaytime / Gesturetime: {} / {} \033[0m| \033[91mVoice: {} \033[0m|'
                  ' \033[92mText: "{}" \033[0m| \033[93mGestures: '
                  .format(self.voice_time, self.gesture_time, self.voice, self.text))
        for i in range(len(self.gesture_arr)):
            if i < len(self.gesture_arr) - 1:
                string += self.gesture_arr[i]
                string += ', '
            else:
                string += self.gesture_arr[i]
        string += "\033[0m"
        return string

    # RETURNS the text element string from script line
    def extract_text(self):
        # get rid of the "person" syntax
        liner = self.line
        liner = liner.partition(')')[2]
        gesture_count = liner.count('#')
        # initialize empty line to build
        text = ""
        for i in range(gesture_count + 1):
            # adds the text to the left of the leftmost gesture
            text += liner.partition('#')[0]
            # updates the running line to remove up to the leftmost gesture
            liner = liner.partition('#')[2]
            # updates the running line to remove the leftmost gesture
            liner = liner.partition(' ')[2]
        text = text.rstrip('\n ')
        text = text.lstrip('\n ')
        return text

    # RETURNS an int of the voice
    def extract_voice(self):
        return self.line.partition(')')[0]

    # RETURNS an array of gestures in the form: "BLAH #gesture1 BLAH #gesture2 BLAH" -> arr = [gesture1, gesture 2]
    def extract_gesture(self):
        liner = self.line
        gesture_count = liner.count('#')
        gestures = [''] * gesture_count
        for i in range(gesture_count):
            # removes all to the left of the first '#'
            gestures[i] = liner.partition('#')[2]
            # copies the removal to the running line string
            liner = gestures[i]
            # removes all after the gesture
            gestures[i] = gestures[i].partition(' ')[0]
            gestures[i] = gestures[i].rstrip('\n ')
            gestures[i] = gestures[i].lstrip('\n ')
            # Error handling for non_valid chars
            if not gestures[i].isalnum() and gestures[i].count("_") == 0:
                print("\033[91mSYNTAX ERROR: Gesture \"" + gestures[i] + "\" in Line " + str(self.line_no) + " contains a non-valid character\033[0m")
                exit(1)
        return gestures

    # RETURNS an array gesture position from the line
    def extract_gesture_pos(self):
        pos_arr = [-1] * len(self.gesture_arr)
        for i in range(len(self.gesture_arr)):
            pos_arr[i] = self.line.find(self.gesture_arr[i]) - 4 - i   # remove 3 positions
                                                                    # for the voice spacer
                                                                    # and 1 for the '#' sign
            # print (pos_arr[i])                                                # TEMP
        return pos_arr

    # OUTPUTS one csv file in the /output folder with the timestamps for the voices and gestures
    def help_csv(self):
        with open("../outputs/commandFile.csv", 'a+') as file:
            file_writer = csv.writer(file)
            # adds the voice at current time stamp
            file_writer.writerow([self.current_timestamp, self.output_file.partition('/')[2].partition('/')[2]])    #removes 'outputs/' and adds voice timeline

            # adds the gesture positions in at correct times
            total_delay = 0.0
            last_pos_ratio = 0.0
            last_gesture_timestamp = 0.0
            last_gesture_delay = 0.0
            last_gesture_length = 0.0
            last_delay_from_timestamp = 0.0
            for i in range(len(self.gesture_arr)):
                position_ratio = float(self.gesture_pos_arr[i]) / len(self.line)  # gets the fractional position
                delay_from_timestamp = round((position_ratio - last_pos_ratio) * self.voice_time, 3)
                timestamp = round(self.current_timestamp + delay_from_timestamp, 3)
                gesture_length = round(get_gesture_length(self.gesture_arr[i]), 3)
                # gesture_length = round(get_gesture_length(self.gesture_arr[i]) + 2 * get_gesture_length("init"), 3)  # account for 0.4sec 'init' pos beforehand and after
                # compares to see if relative sentance position is too close to previous gesture (overlapping)
                if timestamp < last_gesture_timestamp + last_gesture_length:
                    timestamp = round(last_gesture_timestamp + last_gesture_length, 3)
                file_writer.writerow([timestamp, self.gesture_arr[i]])
                delay_between_gestures = last_gesture_delay + last_delay_from_timestamp
                # prevent negative delay to contributing to total delay
                if delay_between_gestures > 0:
                    total_delay = round(delay_between_gestures + total_delay, 3)
                # print("\033[95m-------Gesture---\"" + self.gesture_arr[i] + "\"------------------------")   # TEMP
                # print("gesture length:" + str(gesture_length))                                  # TEMP
                # print("gesture delay:" + str(delay_between_gestures))                           # TEMP
                # print("timestamp:" + str(timestamp))                                            # TEMP
                # print("---")                                                                    # TEMP
                # print("last length:" + str(last_gesture_length))                                # TEMP
                # print("last delay:" + str(last_gesture_delay))                                  # TEMP
                # print("last timestamp:" + str(last_gesture_timestamp))                          # TEMP
                # print("---")                                                                    # TEMP
                # print("total delay:" + str(total_delay))                                        # TEMP
                # print("total gesture time:" + str(self.gesture_time))                           # TEMP
                # print("-----------------------------------------------")                        # TEMP
                # saves last gesture values
                last_pos_ratio = position_ratio
                last_gesture_timestamp = timestamp
                last_gesture_delay = delay_between_gestures
                last_gesture_length = gesture_length
                last_delay_from_timestamp = delay_from_timestamp
            # adds to the ongoing current timestamp for the next line
            if self.gesture_time + total_delay > self.voice_time:
                self.total_time = round(self.gesture_time + total_delay, 3)
                # print("(1) Total time:" + str(self.total_time))                                 # TEMP
            else:
                self.total_time = round(self.voice_time + self.total_time, 3)
                # print("(2) Total time:" + str(self.total_time) + "\033[0m")                                 # TEMP
            self.total_time = round(self.total_time + get_gesture_length("init"), 3)
            self.current_timestamp = round(self.total_time, 3)

# CLEARS out the output files from previous run
def clear_csv():
    with open("../outputs/commandFile.csv", "w") as t:
        t.truncate()
    with open("../outputs/lines(human).txt", "w") as t:
        t.truncate()
    # adds header
    with open("../outputs/commandFile.csv", 'a+') as file:
        file_writer = csv.writer(file)
        file_writer.writerow(['timestamp', 'action'])
        # file_writer.writerow(['timestamp', 'action', '(voice)', '(speed)'])       #TEMP
    os.system("rm ../outputs/line*")


def main():
    clear_csv()
    # receive text input from script file
    input_script = fileinput.input(files=INPUT_FILE)
    # # open file
    # fp = open(INPUT_FILE, 'r')
    # lines = len(fp.readlines())
    # line_results = [lines]
    # fp.close()
    ongoing_length = 0.0
    for line in input_script:
        # Extract line to class
        line_number = fileinput.lineno()


        # print("\033[95mCurrent Timestamp:" + str(ongoing_length) + "\033[0m")                   #TEMP
        testing_class = ScriptLine(ongoing_length, line, line_number)

        # adds the line length to the onging total length
        ongoing_length = round(testing_class.total_time + ongoing_length, 3)
        # print("\033[95mongoing_length:" + str(ongoing_length) + "\033[0m")                      #TEMP
        print(testing_class)


        # #
        # gestures_take_longer = is_gestures_longer(gestures_arr, playtime)
        # csv_handling(gestures_arr, gestures_take_longer, playtime)


    fileinput.close()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # speech_file("yoooo hooooo bababooie", "../outputs/bababooie.wav")     # TEMP
    # audio = WAVE("../outputs/bababooie.wav")                              # TEMP
    # playtime = audio.info.length                                          # TEMP
    # print("playtime: ", playtime)                                         # TEMP

    main()


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
