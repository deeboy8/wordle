
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
    def create(cls, word_str: str) -> Self: #TODO: add validation within libary as part of contructor method create()
        if not all('a'<= ch <= 'z' for ch in word_str):
            raise ValueError("all letters must be lowercase ASCII characters (a-z)")
        return cls(word = [Letter(name=ch) for ch in word_str])
    
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

    #import file of words and return a list 
    def convert_word_library_to_list(self, file_name: str) -> List:
        if not file_name:
            raise ValueError('empty string')
        try:
            with open(file_name, "r") as file:
                return sorted([line.strip() for line in file]) #TODO: determine if this is acceptable if file not found
        except FileNotFoundError as fnf_error:
            print(fnf_error)
        
    def validate_guess_in_libary(self, player_guess: Self, library_list: List) -> bool:
        return player_guess in library_list
    
    #randomly choose a secrect word and return chosen word
    def get_secrect_word(self, list_of_words: list, file_len: int):
        random_int: int = random.randint(1, file_len)
        return list_of_words[random_int]
    

    # Normalize player guess by making lowercase and removing any whitespace
    def normalize_player_guess(self, player_guess: str) -> str:
        return "".join(player_guess.lower().split())

    def compare_against_secret_word(self, player_guess: Word, secret_word) -> bool:
        for ch, i in player_guess.word, range(len(secret_word)):
            if not str(ch.name) == secret_word[i]:
                return False
        return True


    #udpate board, to update game, Word and Player objects
    def update(self):
        pass

def main():
    print(f"Welcome to Wordle!")
    name: str = input("Please enter your name: ")
    player: Player = Player(name=name, number_of_guesses=MAX_USER_GUESSES)
    game: Game = Game(player=player)
    library_list: list = game.convert_vocabulary_to_list(TEXT_FILE) #TODO: change name to library F2
        #TODO: create library_list and secrect_word in game object directly as part of contructor
    secrect_word: str = game.get_secrect_word(library_list, len(library_list)) #TODO: change name to correct spelling of secrect F2
    
    #iterate over MAX_USER_GUESSES - GAME LOOP
    for guess in range(MAX_USER_GUESSES):
        player_guess: str = game.normalize_player_guess(input("Please enter your guess: "))
        # Convert players guess into a Word object       
        player_guess: Word = Word(player_guess) #! if going to create an object, upon intializtion it should be guranteed to be validate
        player_guess_in_library: bool = game.validate_guess_in_libary(player_guess, library_list) #TODO: add directly to field() of pydantic 
        if not player_guess_in_library:
            print(f"word: {player_guess} is not valid.")
            print(f"Please chooseanother word.")
        # compare against secret word 
            #if correct -> i/o congratulations
        comparison: bool = game.compare_against_secret_word(player_guess, secrect_word)

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