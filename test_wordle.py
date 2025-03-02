import pytest 
from wordle import Letter, LetterState, Word, Board
from typing import List

##########################Letter class#######################
def test_letter_creation():
    """Test creating a Letter with a valid character."""
    letter = Letter(name="a") 
    assert letter.name == "a"
    assert letter.letter_state == LetterState.unselected

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

def test_letter_validation():
    "Test that a letter cannot be more than on character long"
    with pytest.raises(ValueError):
        Letter(name="abc")

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
def test_word_length_incorrect():
    """Test if word length is within specification"""
    #arrange
    word1 = 'powerful'
    #act
    with pytest.raises(ValueError):
        Word(word=word1)

def test_word_length_correct():
    """Test if word length is within specification"""
    #arrange
    word1 = 'power'
    #act
    with pytest.raises(ValueError):
        Word(word=word1)

def test_check_correct_type_returned():
    """Test correct type returned from Word class"""
    #arrange
    # class_type = type(Letter)
    word_string = 'happy'
    #act
    result = Word(word=word_string)
    #assert
    assert type(result) == Word
    assert type(result) != List

def test_create_returns_correct_type():
    # arrange
    word_str = "dices"
    #act
    result = Word.create(word_str)
    assert type(result) == Word

def test_check_correct_letter_count_returned():
    pass

def test_create_classmethod():
    pass

def test_word_attribute_is_str():
    pass

def test_create_param_is_str():
    pass

###########################test Board Class##########################
def test_board_attribute_returns_correct_type():
    pass

def test_number_user_guesses_allowed():
    pass

def test_insert_user_guess_str():
    pass 

def test_insert_user_guess_return_type():
    pass 

