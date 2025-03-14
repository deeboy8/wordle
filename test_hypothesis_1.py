# import pytest
from hypothesis import given
from hypothesis.strategies import text 
from wordle import Letter, Word, LetterState

################ Word Class ############
@given(text())
def test_creat_returns_list(test_string: str) -> None:
    assert Word.create(test_string) == type(Word)

# def test_letter_in_Word_object():
#     word = 'spurt'
#     #act
#     obj = Word(word)
#     #asset
#     assert type(obj.word[0]) == Letter  

# def test_letterstate_in_Word_object_():
#     word = 'spurt'
#     #act
#     obj = Word(word)
#     #asset
#     assert isinstance(obj.word[0].letter_state == LetterState.unselected)

######################### Game Class ################################

# def test 
    
