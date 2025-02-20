
from ast import List
from enum import Enum
from pydantic import BaseModel, Field

#various states each individual can hold to signify to user if letter position is in secrect word
class LetterState(Enum):
    unselected = "UNSELECTED" 
    grey = "GREY"
    green = "GREEN"
    yellow = "YELLOW"
    
    
class Game(BaseModel):
    def __init__():
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

class Board(BaseModel):
    def __init__(self):
        self.board: List[Word] = [for word in ]

    def create_board():
        pass

    def insert_letters():
        #place letters entered by user into data container
        pass

class Letter(BaseModel):
    name: str
    letter_state: LetterState = Field(default_factory = LetterState.unselected)
    
    #TODO pydantic validation to ensure LetterState is accurate and not returned to unselected
    def set_letter_state(new_value: LetterState): #setter, getter
        pass

class Alphabet(BaseModel):
    #used for tracking
    def __init__(self):
        self.alpha = [Letter(x) for x in range('a' - 'z')] #generate list letters a-z

class Word(BaseModel):
    #wht is a word going to contain? -> a bunch of letters => word of five letters
    #TODO pydantic: no longer than five letters
    word: List[Letter] 
    user_word: List[Letter] = [Letter(x) for x in word]

class Player: #TODO: necessary?
    pass
#number of guess
#name

def main():
    #create an instance of a game aka create a game object
    pass

if __name__ == "__main__":
    main()