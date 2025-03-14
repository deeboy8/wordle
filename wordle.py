
from typing import List
from typing_extensions import Self
from enum import Enum
from pydantic import BaseModel, Field, ValidationError, field_validator
import random

"""!?//todo*"""

MAX_USER_GUESSES = 6
MAX_WORD_LEN = 5
TEXT_FILE = 'vocabulary.txt'

#states each individual letter can hold
#state will dictate color to be used to convery if letter is in the secret word, not in the secrect word or misplaced
class LetterState(Enum):
    unselected = "UNSELECTED" # blue
    grey = "GREY"
    green = "GREEN"
    yellow = "YELLOW"

class Letter(BaseModel):
    name: str = Field(max_length=1)
    letter_state: LetterState = Field(default=LetterState.unselected) #TODO pydantic validation to ensure LetterState is accurate and not returned to unselected

#word will be string user passes in from stdin
#must be converted from a string word to a list of letters
class Word(BaseModel): #! classes are self contained; it doesn't know about where it's being called
    """Will generate a Word class object"""
    word: List[Letter] = Field([], min_length=5, max_length=5) #TODO is in vocabulary and in ascii chars   
                                                                    #TODO:maybe move ascii check move to letters
    @classmethod
    def create(cls, word_str: str) -> Self: 
        if type(word_str) != str or word_str is None: #! was using to debug hypothesis but no luck
            raise TypeError('input must be a string')
        return cls(word = [Letter(name=ch) for ch in word_str])

    @field_validator('word')
    def validate_characters_ASCIII(self, player_guess: Self) -> bool:
        for letter in player_guess.word:
            if not 'a' <= letter.name <= 'z': 
                raise ValueError(f"Letter '{letter.name}' is not a lowercase ASCII character (a-z)")
            
    #validate user_guess length and present in dictionary and each char is ASCII a-z
    def validate_user_guess(self, user_guess: str) -> bool:
        #will use validate_guss  in dict and validate length
        pass
    
    def validate_guess_in_libary(self, player_guess: Self, library_list: List) -> bool:
        return player_guess in library_list

    def validate_guess_length(self, user_guess: Self) -> bool:
        #check if word in dictionary of words
        pass
    
    # check all chars of Word object are a-z
    
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

    def is_letter_in_secrect_word(self, ch: str, secrect_word: str) -> bool:
        pass

    def is_letter_in_correct_index(self, ch_index: int, secrect_word: str) -> bool:
        pass

    #will only return bool data and update letter_state changes
    #board will be updated by Game obj
    def score_user_guess(self, secret_word: str, user_guess: Self, secrect_word: str) -> None:
        #for loop iterating over each letter
            # need to check if ch in word (iteration) and equivalent to the same index position
            # therefore need two fx to return bools
                # if both fx:
                    # update state with green
                # elif letter_found and index_pos is False:
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

#! hard mode will use this class
# class Alphabet(BaseModel): 
#     alpha = [Letter(x) for x in range(ord('a'), ord('z') + 1)]  #generate list letters a-z
    
#     def update_letter_state(self, ch: str) -> None:
#         #letter state changed to appropriate color
#         pass

class Player(BaseModel):
    name: str 
    number_of_guess: int = MAX_USER_GUESSES

    def get_player_name(self, name, number_of_guess):
        return f"name is: {name} and you have {number_of_guess} remaining"

class Game(BaseModel): 
    board: List[List] = Board()
    player: Player
    # alphabet: Alphabet = Alphabet()

    #import txt of five letter words and return a list 
    def convert_vocabulary_to_list(self, file_name: str):
        with open(file_name, "r") as file:
            return sorted([line.strip() for line in file])
    
    #randomly choose a secrect word and return chosen word
    def get_secrect_word(self, list_of_words: list, file_len: int):
        random_int: int = random.randint(1, file_len)
        return list_of_words[random_int]
    
    #container for user guess
    def user_guess():
        pass

    #udpate board, to update game, Word and Player objects
    def update(self):
        pass

     # Normalize player guess by making lowercase and removing any whitespace
    def normalize_player_guess(self, player_guess: str) -> str:
        return "".join(player_guess.lower().split())

def main():
    print(f"Welcome to Wordle")
    name: str = input("Please enter your name: ")
    player: Player = Player(name=name, number_of_guesses=MAX_USER_GUESSES)
    game: Game = Game(player=player)
    library_list: list = game.convert_vocabulary_to_list(TEXT_FILE)
    secrect_word: str = game.get_secrect_word(library_list, len(library_list))
    
    #iterate over MAX_USER_GUESSES - GAME LOOP
    for guess in range(MAX_USER_GUESSES):
        #user enters guess
        player_guess: str = game.normalize_player_guess(input("Please enter your guess: "))          
        player_guess = Word(guess) #passed to create() as a class method
        player_guess_in_library: bool = player_guess.validate_guess_in_libary(player_guess, library_list)
        if not player_guess_in_library:
            
        # compare against secret word 
            #if correct -> i/o congratulations
        
        #score word
            #only focus is to determine position and correct letters and update information

            #TODO: must say to game -> board to UPDATE yourself aka pushing responsibility down to lowest point 
        # update board
            #use game object to update Player (update details), Board (update letters) 

#idea: create a dict in score word where letter is key and value is letter state information
    #change letter_state in word object
    #pass word object to Game which will update board
        
#TODO: how will you compare a str (secrect_word) to a word object (player_guess) -> Python may have a method for this
    

if __name__ == "__main__":
    main()