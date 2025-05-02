"""
Unit tests for the Wordle game implementation.
Tests cover all major classes and their methods.
"""

import pytest
from wordle import (
    Letter, LetterState, Word, Board, Game, Player,
    MAX_USER_GUESSES, MAX_WORD_LEN
)

##########################Letter class#######################
def test_letter_creation():
    """Test creating a Letter with valid character"""
    letter = Letter(name="a")
    assert letter.name == "a"
    assert letter.letter_state == LetterState.unselected

def test_letter_state_update():
    """Test updating letter state"""
    letter = Letter(name="a")
    letter.letter_state = LetterState.green
    assert letter.letter_state == LetterState.green

def test_letter_invalid_name():
    """Test creating Letter with invalid name"""
    with pytest.raises(ValueError):
        Letter(name="ab")  # More than one character

def test_letter_state_default_to_unselected():
    """Testing letter creation defaulted to unselected"""
    #act
    letter = Letter(name='a', letter_state=LetterState.unselected)
    #assert
    assert letter.letter_state == LetterState.unselected

def test_letter_state_default():
    """Testing letter creation does not default to unselected"""
    #act
    letter = Letter(name='a', letter_state=LetterState.grey)
    #assert
    assert letter != LetterState.unselected

def test_empty_name():
    """Test empty string for name"""
    letter = Letter(name="")
    assert letter.name == ""

def test_letter_equality():
    """Test that the letters with same name and state are equal"""
    letter1 = Letter(name="d", letter_state=LetterState.green)
    letter2 = Letter(name="d", letter_state=LetterState.green)
    lettter3 = Letter(name="d", letter_state=LetterState.yellow)

    assert letter1 == letter2
    assert letter1 != lettter3

def test_list_of_strings():
    #arrange
    word = 'happy'
    #act
    result = Word.create(word)
    assert isinstance(result, Word)
     
#######################test Word class#######################
def test_word_creation():
    """Test creating a Word with valid letters"""
    word = Word.create("hello", ["hello"])
    assert isinstance(word, Word)
    assert len(word.word) == 5
    assert word.word[0].name == "h"

def test_word_invalid_length():
    """Test creating Word with invalid length"""
    with pytest.raises(ValueError):
        Word.create("hell", ["hell"])  # Too short

def test_word_not_in_vocabulary():
    """Test creating Word not in vocabulary"""
    result = Word.create("xyzzy", ["hello"])
    assert result is False

def test_word_str_representation():
    """Test string representation of Word"""
    word = Word.create("hello", ["hello"])
    assert str(word) == "hello"

def test_check_correct_letter_count_returned():
    pass

def test_create_classmethod():
    pass

def test_word_attribute_is_str():
    pass

def test_create_param_is_str():
    pass

###########################test Board Class##########################
def test_board_add_word():
    """Test adding word to board"""
    board = Board()
    word = Word.create("hello", ["hello"])
    board.add_word(word)
    assert len(board.words) == 1

def test_board_max_words():
    """Test board maximum capacity"""
    board = Board()
    word = Word.create("hello", ["hello"])
    for _ in range(MAX_USER_GUESSES):
        board.add_word(word)
    with pytest.raises(ValueError):
        board.add_word(word)

def test_board_get_word_at_position():
    """Test getting word at specific position"""
    board = Board()
    word = Word.create("hello", ["hello"])
    board.add_word(word)
    assert board.get_word_at_position(0) == word
    assert board.get_word_at_position(1) is None

def test_board_clear():
    """Test clearing the board"""
    board = Board()
    word = Word.create("hello", ["hello"])
    board.add_word(word)
    board.clear()
    assert len(board.words) == 0

###########################test Game Class##########################
def test_game_normalize_guess():
    """Test normalizing player guess"""
    game = Game(player=Player(name="test"))
    assert game.normalize_player_guess(" HELLO ") == "hello"

def test_game_compare_letters():
    """Test letter comparison logic"""
    game = Game(player=Player(name="test"))
    game.secret_word = "hello"
    word = Word.create("hallo", ["hallo"])
    game.compare(word)
    assert word.word[0].letter_state == LetterState.green  # h
    assert word.word[1].letter_state == LetterState.grey   # a
    assert word.word[2].letter_state == LetterState.yellow # l

def test_game_is_secret_word():
    """Test secret word checking"""
    game = Game(player=Player(name="test"))
    game.secret_word = "hello"
    word = Word.create("hello", ["hello"])
    assert game.is_secret_word(word)
    word = Word.create("world", ["world"])
    assert not game.is_secret_word(word)

def test_game_load_vocabulary():
    """Test vocabulary loading"""
    game = Game(player=Player(name="test"))
    assert isinstance(game.vocabulary, list)
    assert all(len(word) == MAX_WORD_LEN for word in game.vocabulary)

###########################test Player Class##########################
def test_player_creation():
    """Test creating a player"""
    player = Player(name="test")
    assert player.name == "test"
    assert player.number_of_guesses == MAX_USER_GUESSES

def test_player_get_name():
    """Test player name formatting"""
    player = Player(name="test")
    assert "test" in player.get_player_name("test", 5)

def test_player_guesses_update():
    """Test updating player guesses"""
    player = Player(name="test")
    player.number_of_guesses = 3
    assert player.number_of_guesses == 3

###########################test Display Class##########################
def test_display_clear_screen(monkeypatch):
    """Test screen clearing"""
    import os
    called = False
    def mock_system(cmd):
        nonlocal called
        called = True
    monkeypatch.setattr(os, 'system', mock_system)
    from wordle import Display
    Display.clear_screen()
    assert called

def test_display_show_word(capsys):
    """Test word display with colors"""
    from wordle import Display
    word = Word.create("hello", ["hello"])
    Display.show_word(word)
    captured = capsys.readouterr()
    assert "h" in captured.out

def test_display_show_board(capsys):
    """Test board display"""
    from wordle import Display
    board = Board()
    word = Word.create("hello", ["hello"])
    board.add_word(word)
    Display.show_board(board)
    captured = capsys.readouterr()
    assert "Current Board" in captured.out
    assert "hello" in captured.out

###########################test Integration##########################
def test_game_flow():
    """Test complete game flow"""
    from wordle import Game, Player, Word, Board, Display
    player = Player(name="test")
    game = Game(player=player)
    board = Board()
    
    # Simulate a game round
    game.secret_word = "hello"
    guess = Word.create("world", ["world"])
    game.compare(guess)
    board.add_word(guess)
    
    assert len(board.words) == 1
    assert not game.is_secret_word(guess)
    assert player.number_of_guesses == MAX_USER_GUESSES


