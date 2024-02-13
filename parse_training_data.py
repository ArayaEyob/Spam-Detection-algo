import csv
import string
import re

class EmailCSVParser:
    def __init__(self):
        self.spam = 0
        self.ham = 0
        self.unique_words = set()
        self.total_spam_words = 0
        self.total_ham_words = 0
        self.spam_words = {}
        self.ham_words = {}

    def tally(self, is_spam, message):
        message = re.sub(r'[^\w\s]', '', message.lower())  # Remove punctuations
        message = re.sub(r'\d+', '', message)  # Remove digits
        words = message.split()
        word_count = {}
        for word in words:
            self.unique_words.add(word)
            word_count[word] = word_count.get(word, 0) + 1
        if is_spam:
            self.total_spam_words += len(words)
            self.spam += 1
            for word, count in word_count.items():
                self.spam_words[word] = self.spam_words.get(word, 0) + count
        else:
            self.total_ham_words += len(words)
            self.ham += 1
            for word, count in word_count.items():
                self.ham_words[word] = self.ham_words.get(word, 0) + count

    def parse(self, training_data):
        with open(training_data, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='|')
            currently_reading_spam = False
            for row in reader:
                if len(row) < 2:
                    continue
                label, *message = row
                if label.isdigit() and message and message[0] in ['spam', 'ham']:
                    is_spam = message[0] == 'spam'
                    currently_reading_spam = is_spam
                    self.tally(is_spam, ' '.join(message[1:]))
                else:
                    self.tally(currently_reading_spam, ' '.join(row))

     
