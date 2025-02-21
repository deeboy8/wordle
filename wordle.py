
from typing import List
from enum import Enum
from pydantic import BaseModel, Field

MAX_USER_GUESSES = 6
MAX_WORD_LEN = 5

#various states each individual can hold to signify to user if letter position is in secrect word
class LetterState(Enum):
    unselected = "UNSELECTED" 
    grey = "GREY"
    green = "GREEN"
    yellow = "YELLOW"

class Letter(BaseModel):
    def __init__(self, name: str): #use annotqtion to set to 1 char
        self.name: str = Field(max_length = 1)
        self.letter_state: LetterState = LetterState.unselected 
    
    #TODO pydantic validation to ensure LetterState is accurate and not returned to unselected
    # def set_letter_state(new_value: LetterState): #setter, getter
    #     pass

class Word(BaseModel):
    #wht is a word going to contain? -> a bunch of letters => word of five letters
    #TODO pydantic: no longer than five letters
    # word: List[Letter] = []
    def __init__(self, word: str):
        self.word: List[Letter] = Field(min_length = 5, max_length = 5)
        # iterate over string passed from user appending letter to the internal list
        for ch in word:
            ch_to_letter = Letter(ch)
            self.word.append(ch_to_letter)

class Board(BaseModel):
    # def __init__(self):
    #     self.board: List[Word] = Field(default_factory = lambda: [Word(user_word = []) for _ in range(MAX_USER_GUESS‹ES)])
    # board: List[Word] = Field(default_factory = lambda: [Word(user_word = []) for _ in range(MAX_USER_GUESS‹ES)])
    board: List[Word] = Field(max_length = MAX_WORD_LEN)

    

class Alphabet(BaseModel):
    #used for tracking
    def __init__(self):
        self.alpha = [Letter(x) for x in range('a' - 'z')] #generate list letters a-z

class Player (BaseModel):
    number_of_guess: int 

#number of guesses
#name

class Game(BaseModel): 
    def __init__(self, name):
        self.alphabet = Alphabet()
        self.player = Player(name)
        self.board = Board()
        pass
        #open txt file w list of words

    def get_secrect_word():
        #choose a secrect word randomly
        pass
    
    def user_guess():
        #take in user guess and hold in variable
        pass

    ################################
    #methods below this line will be used after user inputs guess
    #methods above are to be run to initialize a game object 
    def validate_guess_in_dictionary(self) -> bool:
        #check if word in dictionary of words
        pass

    def score_user_guess(self):
        #return five pieces of info one per letter
        pass

def main(): #just write the structure of the game as pseudocode in the main loop 
    #create an instance of a game aka create a game object
    #open file with list of potential words
        #choose secrect word and store in var
    #read in user guess and store in var

    #crate board for user guesses to be stored
    board = Board()
    print(board)
    #for loop of six guess
        #
    pass

if __name__ == "__main__":
    main()