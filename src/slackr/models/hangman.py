import random
import string

import wikiquote

from slackr import db


class Hangman(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    is_active = db.Column(db.Boolean, default=False)
    word = db.Column(db.String(100))
    guesses = db.Column(db.String(23), default='')
    incorrect = db.Column(db.String(23), default='')
    stage = db.Column(db.Integer, default=0)
    # prev_msg_id = db.Column(db.Integer)
    channel_id = db.Column(db.Integer, db.ForeignKey('channel.channel_id'))

    def start(self):
        if self.is_active:
            return
        self.is_active = True
        self.word = get_word()
        db.session.commit()
        return self.get_dashed()

    # def set_prev_msg_id(self, prev_msg_id):
    #     self.prev_msg_id = prev_msg_id
    #     db.session.commit()

    def guess(self, letter):
        letter = letter.lower()
        if letter not in self.guesses:
            self.guesses += letter

        # incorrect guess
        is_correct = True
        if letter not in self.word.lower():
            if letter not in self.incorrect:
                self.stage += 1
                self.incorrect += letter
            is_correct = False

        db.session.commit()

        return is_correct

    def stop(self):
        self.is_active = False
        self.word = None
        self.guesses = ''
        self.incorrect = ''
        self.stage = 0
        # self.prev_msg_id = 0
        db.session.commit()

    def get_dashed(self):
        '''
        Returns a string where all unguessed letters are '_'.
        '''
        for char in self.word:
            if char not in string.ascii_letters:
                return False

        # getting list of all lowercase letters.
        dashed = self.word
        for char in dashed:
            if char.lower() not in self.guesses and char.isalpha():
                dashed = dashed.replace(char, '_ ')
            elif char == ' ':
                dashed = dashed.replace(char, '   ')
        return dashed


def get_word():
    '''
    Function to get a random word from wikiquote
    '''
    word = random.choice(wikiquote.random_titles(lang='en'))
    while not word.isalpha() and not check_ascii(word):
        word = random.choice(wikiquote.random_titles(lang='en'))
    return word.strip()


def check_ascii(word):
    '''
    Function to check if word is valid.
    '''
    for char in word:
        if char not in string.ascii_letters:
            return False

    return True
