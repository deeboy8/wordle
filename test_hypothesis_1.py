# import pytest
from hypothesis import given
from hypothesis.strategies import text, characters
from wordle import Letter, Word, LetterState

def lowercase_letters():
    return characters(min_codepoint=ord('a'), max_codepoint=ord('z'))

################ Word Class ############
@given(text(lowercase_letters(), min_size=5, max_size=5))
def test_create_returns_list(test_string: str) -> None:
    assert type(Word.create(test_string)) == Word


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
    
