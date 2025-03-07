
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
    
    def convert_guess_to_lowercase(self, user_guess: str) -> str:
        return user_guess.lower()

    #validate user_guess length and present in dictionary and each char is ASCII a-z
    def validate_user_guess(self, user_guess: str) -> bool:
        #will use validate_guss  in dict and validate length
        pass
    
    def validate_guess_in_word_list(self, user_guess: Self) -> bool:
        #check if word in dictionary of words
        pass

    def validate_guess_length(self, user_guess: Self) -> bool:
        #check if word in dictionary of words
        pass
    
    # check all chars of Word object are a-z
    def validate_characters_ASCIII(self, user_guess: Self) -> bool:
        pass
    
    def compare_against_secret_word(self, user_guess: Self) -> bool:
        pass
    
    def update_color_state(self, ch: str, color: str) -> bool:
        # if color is green, yellow, grey:
            # change ch.letterstate to color -> USE THAT THING THAT STARTS WITH A 'C' AND GIVES OPTIONS TO CHOOSE        
        pass

    def remove_word_from_list(self, user_guess: Self) -> bool:
        # create list of letters to form a string
        # remove string from list 
        pass 

    #score user_guess for each letter in guess
    def score_user_guess(self, secret_word: str, user_guess: Self) -> None:
        #for loop iterating over each letter
                # if letter in word and in correct location (index): 
                    # update state with green
                # elif letter in word but in wrong location (index):
                    # change state to yellow
                # else:
                    #1. change state color to grey
                    #2. remove all words from list containing that character
                    #return false
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
        #generate a board object #! DG mentioned user won't have access to Board by placing here in Game obj. what do you mean?
        #generate a player obj
        #generate alphabet class
    
    #iterate over MAX_USER_GUESSES - GAME LOOP -> 1. once have word, compare against secrect word (updated state of word)
        #user enters guess
            # convert to lowercase
            # convert to word object -> create()
            # validate if it is five letters long
                #if not return output length is too long or short
            # each letter is an ASCII character a-z
                #if not return output length is too long or short
            #validate if guess in list of vocabulary list
        #compare against secret word
            #user_guess == secrect_word
                #if correct -> congrats
        
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