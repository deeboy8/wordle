# import pytest
from typing import Annotated, List
from attr import field
from hypothesis import given
from hypothesis.strategies import text, characters
from pydantic import AfterValidator, BaseModel, StringConstraints, field_validator
from wordle import Letter, Word, LetterState

def lowercase_letters():
    return characters(min_codepoint=ord('a'), max_codepoint=ord('z'))

################ Word Class ############
@given(text(lowercase_letters(), min_size=5, max_size=5))
def test_create_returns_list(test_string: str) -> None:
    assert type(Word.create(test_string)) == Word


################ djg start ############
# load the vocabulary.txt file into a list of strings
def load_vocabulary() -> List[str]:
    with open("vocabulary.txt", "r") as f:
        return f.read().split("\n")


vocabulary: List[str] = load_vocabulary()
assert vocabulary is not None


class Word_djg(BaseModel):
    # [decorator validator](https://docs.pydantic.dev/2.10/concepts/validators/#__tabbed_1_2)
    # pydantic 'after' field validator to ensure the str arg is in the vocabulary
    @field_validator("word1", mode="after")
    @classmethod
    def check_word_in_vocabulary(cls, word: str):
        if word not in vocabulary:
            raise ValueError(f"{word} not in vocabulary.txt")
    word1: Annotated[
        str, StringConstraints(to_lower=True, min_length=5, max_length=5)
    ]
    # [annotated validator](https://docs.pydantic.dev/2.10/concepts/validators/#__tabbed_1_1)
    word2: Annotated[
        str, StringConstraints(to_lower=True, min_length=5, max_length=5), AfterValidator(lambda word: word in vocabulary)
    ]

# hypothesis based PBT test for Word_djg
@given(text(lowercase_letters(), min_size=5, max_size=5))
def test_djg_create_returns_list(test_string: str) -> None:
    try:
        # [assignment expression](https://docs.python.org/3/whatsnew/3.8.html#assignment-expressions)
        assert type(word_djg := Word_djg(word1=test_string, word2=test_string.upper())) == Word_djg
        assert type(word_djg) == Word_djg
        assert word_djg.word1 == test_string.lower()
        assert word_djg.word2 == test_string.upper()
    except ValueError:
        pass

################  djg end  ############

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
    
