import pytest 
from wordle import Letter, LetterState, Word, Board, Game, Player
from typing import List

player = Player(name="demitrus")
assert player
game = Game(player = player)
assert game

def test_normalization_of_player_guess():
    """Test basic normalization of player guess with leading space and uppercase"""
    #arrange
    player_guess = " ABCDE"
    #act
    result = game.normalize_player_guess(player_guess)
    #assert
    assert result == "abcde"

def test_normalization_trailing_whitespace():
    """Test normalization with trailing whitespace"""
    #arrange
    player_guess = "HELLO       "
    #act
    result = game.normalize_player_guess(player_guess)
    #assert
    assert result == "hello"

def test_return_type():
    #arrange
    guess = "wEdNeSdAy "
    #act
    result = game.normalize_player_guess(guess)
    #assert
    assert type(result) == str

######################### convert_vocabulary_to_list ######################
def test_vocabulary_list_returns_list_type():
    """Test if vocabulary list returns a list"""
    vocab_file = "test_vocabulary.txt"
    with open(vocab_file, "w") as f:
        f.write("write\nspurt\npower\ndecay\nfiles")
    result = game.convert_vocabulary_to_list(vocab_file)
    assert type(result) == list

def test_vocabulary_list_strips_whitespace():
    """Test if fx strips whitespace in text file"""
    vocab_file = "test_vocabulary.txt"
    returned_vocab_list = sorted(['write', 'spurt', 'power', 'decay', 'files'])
    with open(vocab_file, "w") as f:
        # Added tab to end of list
        f.write("write\nspurt\npower\ndecay\nfiles\t")
    result = game.convert_vocabulary_to_list(vocab_file)
    assert result == returned_vocab_list

def test_empty_string_passed_as_argument():
    """Testing result of an empty string being passed as argument"""
    with pytest.raises(ValueError):
        result = game.convert_vocabulary_to_list([])

