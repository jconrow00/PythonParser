# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import torch
from transformers import pipeline, DistilBertTokenizer, DistilBertForSequenceClassification, TextClassificationPipeline

model_id = "lxyuan/distilbert-base-multilingual-cased-sentiments-student"


def analyze_sentiment(text):
    sentiment_analyzer = pipeline("sentiment-analysis", model=model_id, top_k=None)
    result = sentiment_analyzer(text)
    return result[0]['label'], result[0]['score']


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


def main():
    # The following block is for linked list parsing
    """
    input_string = input("Enter a string of words: ")
    word_linked_list = create_linked_list(input_string)
    print("Linked List:")
    word_linked_list.print()
    """

    # The following block is for sentiment analysis
    # setup a pipeline model
    sentiment_pipe = pipeline("sentiment-analysis", model=model_id, top_k=None)

    print(sentiment_pipe("test")) # TEMP

    # recieve text from user
    input_text = input("Enter a sentence or phrase: ")
    words = input_text.split()

    # print out results of pipeline

    for word in words:
        pass

    for word in words:
        print(f"Word: {word}")
        sentiment_result = sentiment_pipe(word)
        for i in range(3):
            print(f"\tSentiment: \t{sentiment_result[0][i]['label']} \n\tScore: \t\t{sentiment_result[0][i]['score'] * 100}")
        ##print(analyze_sentiment(word))
        ##sentiment_label, sentiment_score = analyze_sentiment(word)
        ##print(f"Word: {word}, Sentiment: {sentiment_label}, Score: {sentiment_score}")
        #for out in sentiment_pipe:
        #    print(out)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
