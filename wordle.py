
from typing import List
from typing_extensions import Self
from enum import Enum
from pydantic import BaseModel, Field, model_validator
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
class Word(BaseModel): 
    """Will generate a Word class object"""
    word: List[Letter] = Field([], min_length=5, max_length=5) #TODO is in vocabulary and in ascii chars   
                                                                    #TODO:maybe move ascii check move to letters
    @classmethod
    def create(cls, word_str: str, vocabulary: List[str]) -> Self: #TODO: add validation within libary as part of contructor method create()
        if not all('a'<= ch <= 'z' for ch in word_str):
            raise ValueError("all letters must be lowercase ASCII characters (a-z)")
        
        if vocabulary is not None and word_str not in vocabulary:
            raise ValueError(f"{word_str} not in the vocabulary")
        
        return cls(word = [Letter(name=ch) for ch in word_str])
    
    def compare_against_secret_word(self, player_guess: Self, secret_word) -> bool:
        for ch, i in player_guess.word, range(len(secret_word)):
            if not str(ch.name) == secret_word[i]:
                return False
        return True
    
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
    board: Board = Field(default_factory=Board)
    player: Player
    # alphabet: Alphabet = Alphabet()
    vocabulary: List[str] = Field(default_factory=list)
    secret_word: str = ""

    @model_validator(mode='before')
    @classmethod
    def load_vocabulary_and_secret_word(cls, data):
        # Handle both dict and object inputs
        if isinstance(data, dict):
            # Load vocabulary if not provided
            if 'vocabulary' not in data or not data['vocabulary']:
                data['vocabulary'] = cls._load_vocabulary()
            
            # Set secret word if not provided
            if 'secret_word' not in data or not data['secret_word']:
                if not data['vocabulary']:
                    raise ValueError("Vocabulary is empty, cannot select a secret word")
                data['secret_word'] = random.choice(data['vocabulary'])
                
        return data

    @staticmethod
    def _load_vocabulary(file_name: str = TEXT_FILE) -> List[str]:
        """Load vocabulary from file into a list"""
        try:
            with open(file_name, "r") as file:
                return sorted([line.strip() for line in file if len(line.strip()) == MAX_WORD_LEN])
        except FileNotFoundError as fnf_error:
            print(f"Vocabulary file not found: {fnf_error}")
            return []  # Return empty list if file not found    
        
    def validate_guess_in_libary(self, player_guess: Self, library_list: List) -> bool:
        return player_guess in library_list
    
    # Normalize player guess by making lowercase and removing any whitespace
    def normalize_player_guess(self, player_guess: str) -> str:
        return "".join(player_guess.lower().split())


    #udpate board, to update game, Word and Player objects
    def update(self):
        pass

def main():
    print(f"Welcome to Wordle!")
    name: str = input("Please enter your name: ") or 'Demitrus'
    player: Player = Player(name=name, number_of_guesses=MAX_USER_GUESSES)
    game: Game = Game(player=player)
    

    #iterate over MAX_USER_GUESSES - GAME LOOP
    for guess in range(MAX_USER_GUESSES):
        player_guess: str = game.normalize_player_guess(input("Please enter your guess: "))
        # Convert players guess into a Word object       
        player_guess: Word = Word.create(player_guess, game.vocabulary) 
        # player_guess_in_library: bool = game.validate_guess_in_libary(player_guess, library_list) #TODO: add directly to field() of pydantic 
        # if not player_guess_in_library:
        #     print(f"word: {player_guess} is not valid.")
        #     print(f"Please chooseanother word.")
        # compare against secret word 
            #if correct -> i/o congratulations
        # comparison: bool = game.compare_against_secret_word(player_guess, secrect_word)

        # score word
        #     only focus is to determine position and correct letters and update information

        #     TODO: must say to game -> board to UPDATE yourself aka pushing responsibility down to lowest point 
        # update board
        #     use game object to update Player (update details), Board (update letters) 

#idea: create a dict in score word where letter is key and value is letter state information
    #change letter_state in word object
    #pass word object to Game which will update board
        
#TODO: how will you compare a str (secrect_word) to a word object (player_guess) -> Python may have a method for this
    

if __name__ == "__main__":
    main()