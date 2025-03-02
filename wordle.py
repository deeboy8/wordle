
from typing import List
from typing_extensions import Self
from enum import Enum
from pydantic import BaseModel, Field

MAX_USER_GUESSES = 6
MAX_WORD_LEN = 5

#states each individual letter can hold
#state will dictate color to be used to convery if letter is in the secret word, not in the secrect word or misplaced
class LetterState(Enum):
    unselected = "UNSELECTED" 
    grey = "GREY"
    green = "GREEN"
    yellow = "YELLOW"

class Letter(BaseModel):
    name: str = Field(max_length=1)
    letter_state: LetterState = Field(default=LetterState.unselected) #TODO pydantic validation to ensure LetterState is accurate and not returned to unselected

#word will be string user passes in from stdin
#must be converted from a string word to a list of letters
class Word(BaseModel):
    """Will generate a Word class object"""
    word: List[Letter] = Field([], min_length=5, max_length=5)

    #LEARNING: class methods give access to class objects (access class attri or methods) but NOT the instance object itself
    #TODO: why using class method better option than a general 
    @classmethod
    def create(cls, word_str: str) -> 'Word': 
        return cls(word = [Letter(name=ch) for ch in word_str])

#create a Board as a list and appends each user word 
class Board(BaseModel):
    board: List[Word] = Field([], max_length=MAX_USER_GUESSES)

    def insert_user_guess(self, user_guess: Word) -> list:
        return self.board.append(user_guess)

class Alphabet(BaseModel):
    #TODO: this will be used in the main loop to update letter after being appended to Board
    alpha = [Letter(x) for x in range(ord('a'), ord('z') + 1)]  #generate list letters a-z
    pass 

class Player (BaseModel):
    player_name: str 
    number_of_guess: int 
    pass 

class Game(BaseModel): 
    # alphabet = Alphabet()
    # # player = Player(name)
    # board = Board()
    #open txt file w list of words

    def get_secrect_word():
        #choose a secrect word randomly
        pass
    
    def user_guess():
        #take in user guess and hold in variable
        pass

##############################################
    #methods below this line will be used after user inputs guess
    #methods above are to be run to initialize a game object 
    def validate_guess_in_dictionary(self) -> bool:
        #check if word in dictionary of words
        pass

    def score_user_guess(self):
        #return five pieces of info one per letter
        pass

#just write the structure of the game as pseudocode in the main loop
def main():  
    #create an instance of a game aka create a game object
        #ask for basic details of the user
    #open file with list of potential words
        #choose secrect word and store in var
    #read in user guess and store in var

    #iterate over user guess from stdin
    # for user_guess in range(6):
    # user_guess = 'users' #this will be taken from stdin

    #####################################
    str_to_word_obj = Word.create('happy')
    # print(str_to_word_obj.word[0].name)
    # print(str_to_word_obj)
    obj = Board()
    obj.insert_user_guess(str_to_word_obj)
    str_to_word_obj_2 = Word.create('power')
    obj.insert_user_guess(str_to_word_obj_2)
    print(obj)
    

if __name__ == "__main__":
    main()