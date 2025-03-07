
from typing import List
from typing_extensions import Self
from enum import Enum
from pydantic import BaseModel, Field

"""!?//todo*"""

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

    #validate user_guess length and present in dictionary 
    def validate_user_guess(self, user_guess: str) -> bool:
        #will use validate_guss  in dict and validate length
        pass
    
    def validate_guess_in_dictionary(self, user_guess: str) -> bool:
        #check if word in dictionary of words
        pass

    def validate_guess_length(self, user_guess: str) -> bool:
        #check if word in dictionary of words
        pass
    
    #score user_guess
    def score_user_guess(self):
        #criteria: is 
        pass

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
    #gather basic information about user- name
    #import txt file with potential words and return a list data class
    def convert_vocabulary_to_list(self, file_name: str):
        pass
    
    #randomly choose a secrect word and return chosen word
    def get_secrect_word(self, list_of_words: list):
        pass
    
    #container for user guess
    def user_guess():
        pass

    def generate_board_object():
        pass 

    def generate_player_object():
        pass

#just write the structure of the game as pseudocode in the main loop
def main():  
    #create an instance of a game
    game = Game()
        #ask for basic details of the user
        #open file with optional words and turn into a list of words called vocabulary
        #choose secrect word and store in var
        #generate a board object #! DG mentioned user won't have access to Board by placing here in Game obj. what do you mean specifically?
        #generate a player obj
        #generate alphabet class
    
    #iterate over MAX_USER_GUESSES - GAME LOOP -> 1. once have word, compare against secrect word (updated state of word)
        #user enters guess
            # convert to lowercase
            #validate if it is five letters long
                #if not return output length is too long or short
            #each letter is an ASCII character a-z
                #if not return output length is too long or short
            #validate if guess in list of vocabulary list
        #compare against secret word
            #user_guess == secrect_word
                #if correct -> congrats
        #convert user guess into a Word obj -> create method #converting to Word object at this point as previously needed it to be a string for easy comparioson when validating
        #score word
            #criteria: 
            # is letter in secret word
                #if not, remove word from vocabulary list -> GREY
                #update general alphabet state from Alphabet class 
            #letter in word but not in correct location -> YELLOW
                # update letter state
            #letter in word and correct position
                # update latter state
        #update player details (ie. guesses) 
        #if ansewr corrects (aka all letters match secrect word)
            #output congrats
        #else
            #output user guess to terminal 
                #highlight colors
    

if __name__ == "__main__":
    main()