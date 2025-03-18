import pytest
# from _hypothesis import given, text
from wordle import Letter, Word, LetterState

################ Word Class ############
@given(text())
def test_letter_returns_list():
    """Test if Word object returns a list"""
    word = 'spurt'
    #act
    obj = Word(word)
    #asset
    assert obj == list 
    assert isinstance(obj, list)

def test_letter_in_Word_object():
    """Test if Word object is made up of Letter objects"""
    word = 'spurt'
    #act
    obj = Word(word)
    #asset
    assert obj.word[0] == Letter  

def test_letterstate_in_Word_object_():
    """Test if Word object is made up of Letter objects"""
    word = 'spurt'
    #act
    obj = Word(word)
    #asset
    assert isinstance(obj.word[0].letter_state == LetterState.unselected)
    
