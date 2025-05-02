from typing import List, Dict, Any
from collections import defaultdict
from typing_extensions import Self
from enum import Enum
from pydantic import BaseModel, Field, model_validator
import random
import os
from colorama import init, Fore, Back, Style

# Initialize colorama
init()

"""!?//todo*

The Word class has a word attribute which is a list of Letter objects. Each Letter object has a name attribute that contains the actual character. You can iterate through this list using a standard for loop or with enumerate() if you need the index position as well.
# print(player_guess.word[0].name)

"""

MAX_USER_GUESSES = 6
MAX_WORD_LEN = 5
TEXT_FILE = 'vocabulary.txt'

#states each individual letter can hold
#state will dictate color to be used to convery if letter is in the secret word, not in the secrect word or misplaced
class LetterState(Enum):
    unselected = "UNSELECTED" 
    grey = "GREY"
    green = "GREEN"
    yellow = "YELLOW"

class Letter(BaseModel): #! ask DG: is each letter an object?????
    name: str = Field(max_length=1)
    letter_state: LetterState = Field(default=LetterState.unselected) #TODO pydantic validation to ensure LetterState is accurate and not returned to unselected

# #create a Board as a list and appends each user word 
# class Board(BaseModel):
    # keep state of board
#     board: List[Word] = Field([], max_length=MAX_USER_GUESSES)
#     def insert_user_guess(self, user_guess: Word) -> list:
#         self.board.append(user_guess)
    # what do we want board to do? update state and render itself
        #fx update -> insert_user_guess -> take single parameter 

# class Board(BaseModel):
#     board: List["Word"] = Field([], max_length=MAX_USER_GUESSES)

#     def update(self, update_board: Self) -> Self:
#         self.board.append(update_board)

#     def draw(self, draw_board: Self) -> None:
#         for word in draw_board.board:
#             print(word)

#! hard mode will use this class
# class Alphabet(BaseModel): #two use cases: 
    # 1. display keyboard/list of letters that have been used
    # 2. hard mode
#     alpha = [Letter(x) for x in range(ord('a'), ord('z') + 1)]  #generate list letters a-z
    
#     def update_letter_state(self, ch: str) -> None:
#         #letter state changed to appropriate color
#         pass

class Player(BaseModel):
    name: str 
    number_of_guesses: int = MAX_USER_GUESSES

    def get_player_name(self, name, number_of_guess):
        return f"name is: {name} and you have {number_of_guess} remaining"
    
class Game(BaseModel): 
    # board: Board = Field(default_factory=Board)
    player: Player
    # alphabet: Alphabet = Alphabet()
    vocabulary: List[str] = Field(default_factory=list)
    secret_word: str = ""
    player_guesses: int = 0

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
            # return []  # Return empty list if file not found    
    
    # Normalize player guess by making lowercase and removing any whitespace
    def normalize_player_guess(self, player_guess: str) -> str:
        return "".join(player_guess.lower().split())

    #udpate board, to update game, Word and Player objects
    def update_game(self, player_guess: "Word") -> None:
        # number of player guesses
        self.player_guesses += 1
        print(f"You have {MAX_USER_GUESSES - self.player_guesses} guesses left.")
        # inform player of number of guesses remaining
        # update alphabet 
        # update board
        pass

    def compare(self, player_guess: "Word") -> None:
        # Compare to player_guess and secret word
        for i, letter in enumerate(player_guess.word):
            if letter.name in self.secret_word: 
                letter.letter_state = LetterState.yellow
                if letter.name == self.secret_word[i]: 
                      letter.letter_state = LetterState.green
            else: 
                letter.letter_state = LetterState.grey   
  
    def is_secret_word(self, player_guess: "Word") -> bool: 
        player_guess_str = str(player_guess)
        return player_guess_str == self.secret_word

#word will be string user passes in from stdin
#must be converted from a string word to a list of letters
class Word(BaseModel): 
    """Will generate a Word class object"""
    word: List[Letter] = Field([], min_length=5, max_length=5) 

    def __str__(self) -> str:
        word_as_str: str = ""
        for letter in self.word:
            word_as_str += letter.name
        return word_as_str
    
    def __repr__(self) -> str:
        return f"Word(word=[{', '.join(repr(letter) for letter in self.word)}])"

    @classmethod
    def create(cls, word_str: str, vocabulary: List[str]) -> Self | bool: 
        if not all('a'<= ch <= 'z' for ch in word_str):
            raise ValueError("all letters must be lowercase ASCII characters (a-z)")
        
        if vocabulary is not None and word_str not in vocabulary:
            # raise ValueError(f"{word_str} not in the vocabulary")
            return False
        
        return cls(word = [Letter(name=ch) for ch in word_str])

class Board(BaseModel):
    """Manages the game board state, storing and displaying player guesses"""
    words: List[Word] = Field(default_factory=list, max_length=MAX_USER_GUESSES)
    
    def add_word(self, word: Word) -> None:
        """Add a new word to the board if there's space available"""
        if len(self.words) >= MAX_USER_GUESSES:
            raise ValueError("Maximum number of guesses reached")
        self.words.append(word)
    
    def get_words(self) -> List[Word]:
        """Return the current list of words on the board"""
        return self.words
    
    def is_full(self) -> bool:
        """Check if the board has reached maximum capacity"""
        return len(self.words) >= MAX_USER_GUESSES
    
    def get_word_at_position(self, position: int) -> Word | None:
        """Get the word at a specific position on the board"""
        if 0 <= position < len(self.words):
            return self.words[position]
        return None
    
    def clear(self) -> None:
        """Clear all words from the board"""
        self.words.clear()

class Display:
    """Handles all screen output"""
    
    @staticmethod
    def clear_screen():
        """Clear the terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    @staticmethod
    def show_welcome(name: str):
        """Display welcome message"""
        Display.clear_screen()
        print(f"\n{Fore.CYAN}Welcome to Wordle, {name}!{Style.RESET_ALL}")
        print(f"You have a maximum of {MAX_USER_GUESSES} guesses to guess the secret word.\n")
    
    @staticmethod
    def show_guess_prompt():
        """Display prompt for user's guess"""
        return input(f"{Fore.YELLOW}Please enter your guess: {Style.RESET_ALL}")
    
    @staticmethod
    def show_invalid_guess():
        """Display message for invalid guess"""
        print(f"{Fore.RED}Invalid guess! Please enter a valid 5-letter word.{Style.RESET_ALL}")
    
    @staticmethod
    def show_guesses_remaining(remaining: int):
        """Display number of guesses remaining"""
        print(f"\n{Fore.CYAN}Guesses remaining: {remaining}{Style.RESET_ALL}\n")
    
    @staticmethod
    def show_word(word: "Word"):
        """Display a word with appropriate colors based on letter states"""
        for letter in word.word:
            if letter.letter_state == LetterState.green:
                print(f"{Back.GREEN}{Fore.BLACK}{letter.name}{Style.RESET_ALL}", end=" ")
            elif letter.letter_state == LetterState.yellow:
                print(f"{Back.YELLOW}{Fore.BLACK}{letter.name}{Style.RESET_ALL}", end=" ")
            elif letter.letter_state == LetterState.grey:
                print(f"{Back.LIGHTBLACK_EX}{Fore.WHITE}{letter.name}{Style.RESET_ALL}", end=" ")
            else:
                print(f"{letter.name}", end=" ")
        print()
    
    @staticmethod
    def show_board(board: Board):
        """Display the game board"""
        print("\nCurrent Board:")
        print("-" * 15)
        for word in board.words:
            Display.show_word(word)
        print("-" * 15)
    
    @staticmethod
    def show_win_message(player: Player, word: str):
        """Display win message"""
        print(f"\n{Fore.GREEN}Congratulations, {player.name}! You guessed the secret word: {word}{Style.RESET_ALL}")
    
    @staticmethod
    def show_lose_message(secret_word: str):
        """Display lose message"""
        print(f"\n{Fore.RED}Game Over! The secret word was: {secret_word}{Style.RESET_ALL}")

def main():
    name: str = input("Please enter your name: ") or 'Demitrus'
    Display.show_welcome(name) 
    player: Player = Player(name=name, number_of_guesses=MAX_USER_GUESSES)
    game: Game = Game(player=player)
    board = Board()

    #iterate over user guesses
    for guess in range(MAX_USER_GUESSES):
        player_guess: str = game.normalize_player_guess(Display.show_guess_prompt())
        # Convert players guess into a Word object       
        player_guess: Word | bool = Word.create(player_guess, game.vocabulary)
        # Check to see if player guess is valid in vocabulary
        if player_guess is False:
            Display.show_invalid_guess()
            continue
        assert isinstance(player_guess, Word)  # Type narrowing
        
        if game.is_secret_word(player_guess):
            Display.show_win_message(game.player, str(player_guess))
            break
            
        game.compare(player_guess)
        board.add_word(player_guess)
        Display.show_board(board)
        
        remaining_guesses = MAX_USER_GUESSES - (guess + 1)
        Display.show_guesses_remaining(remaining_guesses)
    else:
        Display.show_lose_message(game.secret_word)
    
if __name__ == "__main__":
    main()