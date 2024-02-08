# This is a sample Python script.
import fileinput

# Press Shiffor line in fileinput.input(encoding="utf-8"):
# t+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import torch
import decimal
import fileinput
from transformers import pipeline, DistilBertTokenizer, DistilBertForSequenceClassification, TextClassificationPipeline



model_id = "lxyuan/distilbert-base-multilingual-cased-sentiments-student"


def analyze_sentiment(text):
    sentiment_analyzer = pipeline("sentiment-analysis", model=model_id, top_k=None)
    result = sentiment_analyzer(text)
    return result[0]['label'], result[0]['score']


class ScriptLine:
    def __init__(self, voice=-1, text=None, gestures=[]):
        self.voice = voice
        self.text = text
        self.gestures = gestures

    def __str__(self):
        string = f"Voice: {self.voice} | Text: \"{self.text}\" | Gesture: "
        for i in range(len(self.gestures)):
            if i < len(self.gestures) - 1:
                string += f"{self.gestures[i]}, "
            else:
                string += f"{self.gestures[i]}"
        return string

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None


class LinkedList:
    def __init__(self):
        self.head = None

    def add_node(self, data):
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node

    def print(self):
        current = self.head
        while current:
            print(current.data, end=" -> ")
            current = current.next
        print("None")


def create_linked_list(input_string):
    words = input_string.split()
    linked_list = LinkedList()
    for word in words:
        linked_list.add_node(word)
    return linked_list


def check_speed(line_number, line):
    # extracts the speed number (1-5) before the '#'
    line_speed = line.partition('#')[0]
    # checks if the speed number is valid, else error
    if not line_speed.isdigit():
        print(f"\033[1:91mIn Script line({line_number}): speed (prior to '#') is snot a positive integer\033[0m")
        exit(1)
    else:
        line_speed = int(line_speed)
    if line_speed < 1 or line_speed > 5:
        print(f"\033[1:91mIn Script line({line_number}): speed out of range: {line_speed}\033[0m")
        exit(1)
    return line_speed


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


def print_line_sentiments(line_number, sentiment_file_results):
    # prints out these line-sentiments
    for i in range(3):
        current_sentiment_label = sentiment_file_results[line_number][0][i]['label'].upper()
        # labels the color to the sentiment
        if current_sentiment_label == 'POSITIVE':
            print(f"\033[92m", end='')
        elif current_sentiment_label == 'NEGATIVE':
            print(f"\033[91m", end='')
        elif current_sentiment_label == 'NEUTRAL':
            print(f"\033[93m", end='')
        print(f"\t{current_sentiment_label}", end='')
        print(f"\033[0m \t{round(sentiment_file_results[line_number][0][i]['score'] * 100, 2)}%")
    return


def main():
    # receive text input from script file
    with fileinput.input(files='InputScript.txt') as input_script:
        with open(r"InputScript.txt", 'r') as fp:
            lines = len(fp.readlines())
        line_results = [lines]


        # goes through each line of file
        for line in input_script:
            line_number = fileinput.lineno()
            # returns a str array of gestures

            gestures = extract_gesture(line)
            text = extract_text(line)
            voice = extract_voice(line)
            testing_class = ScriptLine(voice, text, gestures)
            print(testing_class)

"""         #TESTING print
            print(f"\t{line_number}\t", end='')
            for i in range(len(gestures)):
                print(f"{gestures[i]}", end='')
                if i < len(gestures) - 1:
                    print(f", ", end='')
            print(f" ")
"""


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
