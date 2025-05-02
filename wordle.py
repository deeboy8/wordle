"""
Wordle Game Implementation

This module implements a Wordle game with the following features:
- 5-letter word guessing game
- 6 attempts maximum
- Color-coded feedback for letters
- Vocabulary validation
- Player statistics tracking
"""

from typing import List, Dict, Any
from collections import defaultdict
from typing_extensions import Self
from enum import Enum
from pydantic import BaseModel, Field, model_validator
import random
import os
from colorama import init, Fore, Back, Style

# Initialize colorama for terminal color support
init()

# Game constants
MAX_USER_GUESSES = 6  # Maximum number of guesses allowed
MAX_WORD_LEN = 5      # Length of words in the game
TEXT_FILE = 'vocabulary.txt'  # File containing valid words

# Individual states each letter can hold
# State will dictate color to convey if a letter is in the secret word, not in the secret word or misplaced
class LetterState(Enum):
    """Enum representing possible states of a letter in the game"""
    unselected = "UNSELECTED"  # Initial state
    grey = "GREY"             # Letter not in word
    green = "GREEN"           # Letter in correct position
    yellow = "YELLOW"         # Letter in word but wrong position

class Letter(BaseModel):
    """Represents a single letter in a word with its state"""
    # Instance variables
    name: str = Field(max_length=1)  # The actual letter character
    letter_state: LetterState = Field(default=LetterState.unselected)  # Current state of the letter

#! hard mode will use this class
# class Alphabet(BaseModel): #two use cases: 
    # 1. display keyboard/list of letters that have been used
    # 2. hard mode
#     alpha = [Letter(x) for x in range(ord('a'), ord('z') + 1)]  #generate list letters a-z
    
#     def update_letter_state(self, ch: str) -> None:
#         #letter state changed to appropriate color
#         pass

class Player(BaseModel):
    """Represents a player in the game"""
    name: str  # Player's name
    number_of_guesses: int = MAX_USER_GUESSES  # Number of guesses remaining

    def get_player_name(self, name: str, number_of_guess: int) -> str:
        """Returns formatted string with player name and remaining guesses"""
        return f"name is: {name} and you have {number_of_guess} remaining"
    
class Game(BaseModel): 
    """Main game class managing game state and logic"""
    player: Player  # Current player
    vocabulary: List[str] = Field(default_factory=list)  # List of valid words
    secret_word: str = ""  # Word to be guessed
    player_guesses: int = 0  # Number of guesses made

    @model_validator(mode='before')
    @classmethod
    def load_vocabulary_and_secret_word(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validator that loads vocabulary and selects secret word if not provided
        Args:
            data: Dictionary containing game initialization data
        Returns:
            Updated data dictionary with vocabulary and secret word
        """
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
        """
        Loads vocabulary from file
        Args:
            file_name: Name of the file containing valid words
        Returns:
            List of valid words
        """
        try:
            with open(file_name, "r") as file:
                return sorted([line.strip() for line in file if len(line.strip()) == MAX_WORD_LEN])
        except FileNotFoundError as fnf_error:
            print(f"Vocabulary file not found: {fnf_error}")

    # Normalize player guess by making lowercase and removing any whitespace
    def normalize_player_guess(self, player_guess: str) -> str:
        """
        Normalizes player's guess by converting to lowercase and removing whitespace
        Args:
            player_guess: Raw player input
        Returns:
            Normalized guess string
        """
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
        """
        Compares player's guess with secret word and updates letter states
        Args:
            player_guess: Word object containing player's guess
        """
        for i, letter in enumerate(player_guess.word):
            if letter.name in self.secret_word: 
                letter.letter_state = LetterState.yellow
                if letter.name == self.secret_word[i]: 
                    letter.letter_state = LetterState.green
            else: 
                letter.letter_state = LetterState.grey   
  
    def is_secret_word(self, player_guess: "Word") -> bool: 
        """
        Checks if player's guess matches the secret word
        Args:
            player_guess: Word object containing player's guess
        Returns:
            True if guess matches secret word, False otherwise
        """
        player_guess_str = str(player_guess)
        return player_guess_str == self.secret_word

#word will be string user passes in from stdin
#must be converted from a string word to a list of letters
class Word(BaseModel): 
    """Represents a word in the game, composed of Letter objects"""
    word: List[Letter] = Field([], min_length=5, max_length=5) 

    def __str__(self) -> str:
        """Returns string representation of the word"""
        word_as_str: str = ""
        for letter in self.word:
            word_as_str += letter.name
        return word_as_str
    
    def __repr__(self) -> str:
        """Returns detailed string representation for debugging"""
        return f"Word(word=[{', '.join(repr(letter) for letter in self.word)}])"

    @classmethod
    def create(cls, word_str: str, vocabulary: List[str]) -> Self | bool: 
        """
        Creates a Word object from a string if it's valid
        Args:
            word_str: String to convert to Word object
            vocabulary: List of valid words
        Returns:
            Word object if valid, False otherwise
        """
        if not all('a'<= ch <= 'z' for ch in word_str):
            raise ValueError("all letters must be lowercase ASCII characters (a-z)")
        
        if vocabulary is not None and word_str not in vocabulary:
            return False
        
        return cls(word = [Letter(name=ch) for ch in word_str])

class Board(BaseModel):
    """Manages the game board state, storing and displaying player guesses"""
    words: List[Word] = Field(default_factory=list, max_length=MAX_USER_GUESSES)
    
    def add_word(self, word: Word) -> None:
        """
        Adds a word to the board if space is available
        Args:
            word: Word object to add
        Raises:
            ValueError: If board is full
        """
        if len(self.words) >= MAX_USER_GUESSES:
            raise ValueError("Maximum number of guesses reached")
        self.words.append(word)
    
    def get_words(self) -> List[Word]:
        """Returns current list of words on the board"""
        return self.words
    
    def is_full(self) -> bool:
        """Checks if board has reached maximum capacity"""
        return len(self.words) >= MAX_USER_GUESSES
    
    def get_word_at_position(self, position: int) -> Word | None:
        """
        Gets word at specific position on board
        Args:
            position: Index of word to retrieve
        Returns:
            Word object if position is valid, None otherwise
        """
        if 0 <= position < len(self.words):
            return self.words[position]
        return None
    
    def clear(self) -> None:
        """Clears all words from the board"""
        self.words.clear()

class Display:
    """Handles all screen output for the game"""
    
    @staticmethod
    def clear_screen() -> None:
        """Clears the terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    @staticmethod
    def show_welcome(name: str) -> None:
        """
        Displays welcome message
        Args:
            name: Player's name
        """
        Display.clear_screen()
        print(f"\n{Fore.CYAN}Welcome to Wordle, {name}!{Style.RESET_ALL}")
        print(f"You have a maximum of {MAX_USER_GUESSES} guesses to guess the secret word.\n")
    
    @staticmethod
    def show_guess_prompt() -> str:
        """Displays prompt for user's guess and returns input"""
        return input(f"{Fore.YELLOW}Please enter your guess: {Style.RESET_ALL}")
    
    @staticmethod
    def show_invalid_guess() -> None:
        """Displays message for invalid guess"""
        print(f"{Fore.RED}Invalid guess! Please enter a valid 5-letter word.{Style.RESET_ALL}")
    
    @staticmethod
    def show_guesses_remaining(remaining: int) -> None:
        """
        Displays number of guesses remaining
        Args:
            remaining: Number of guesses left
        """
        print(f"\n{Fore.CYAN}Guesses remaining: {remaining}{Style.RESET_ALL}\n")
    
    @staticmethod
    def show_word(word: "Word") -> None:
        """
        Displays a word with appropriate colors based on letter states
        Args:
            word: Word object to display
        """
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
    def show_board(board: Board) -> None:
        """
        Displays the game board
        Args:
            board: Board object to display
        """
        print("\nCurrent Board:")
        print("-" * 15)
        for word in board.words:
            Display.show_word(word)
        print("-" * 15)
    
    @staticmethod
    def show_win_message(player: Player, word: str) -> None:
        """
        Displays win message
        Args:
            player: Player object
            word: Secret word that was guessed
        """
        print(f"\n{Fore.GREEN}Congratulations, {player.name}! You guessed the secret word: {word}{Style.RESET_ALL}")
    
    @staticmethod
    def show_lose_message(secret_word: str) -> None:
        """
        Displays lose message
        Args:
            secret_word: The word that wasn't guessed
        """
        print(f"\n{Fore.RED}Game Over! The secret word was: {secret_word}{Style.RESET_ALL}")

def main() -> None:
    """Main game loop"""
    # Get player name or use default
    name: str = input("Please enter your name: ") or 'Demitrus'
    Display.show_welcome(name)
    
    # Initialize game objects
    player: Player = Player(name=name, number_of_guesses=MAX_USER_GUESSES)
    game: Game = Game(player=player)
    board = Board()

    # Main game loop
    for guess in range(MAX_USER_GUESSES):
        # Get and validate player's guess
        player_guess: str = game.normalize_player_guess(Display.show_guess_prompt())
        player_guess: Word | bool = Word.create(player_guess, game.vocabulary)
        
        # Handle invalid guess
        if player_guess is False:
            Display.show_invalid_guess()
            continue
        assert isinstance(player_guess, Word)  # Type narrowing
        
        # Check for win
        if game.is_secret_word(player_guess):
            Display.show_win_message(game.player, str(player_guess))
            break
            
        # Update game state and display
        game.compare(player_guess)
        board.add_word(player_guess)
        Display.show_board(board)
        
        # Show remaining guesses
        remaining_guesses = MAX_USER_GUESSES - (guess + 1)
        Display.show_guesses_remaining(remaining_guesses)
    else:
        # Game over - player lost
        Display.show_lose_message(game.secret_word)
    
if __name__ == "__main__":
    main()