"""
Property-based tests for Wordle using hypothesis.
Tests verify properties that should always hold true for the game.
"""

from hypothesis import given, strategies as st
from wordle import (
    Letter, LetterState, Word, Board, Game, Player,
    MAX_USER_GUESSES, MAX_WORD_LEN
)

# Strategy for generating valid letters
letter_strategy = st.characters(min_codepoint=ord('a'), max_codepoint=ord('z'))

# Strategy for generating valid words
word_strategy = st.text(
    alphabet=st.characters(min_codepoint=ord('a'), max_codepoint=ord('z')),
    min_size=MAX_WORD_LEN,
    max_size=MAX_WORD_LEN
)

# Strategy for generating letter states
letter_state_strategy = st.sampled_from(list(LetterState))

# Test Letter class properties
@given(letter=letter_strategy)
def test_letter_creation_property(letter):
    """Test that any valid letter can be created"""
    l = Letter(name=letter)
    assert l.name == letter
    assert l.letter_state == LetterState.unselected

@given(letter=letter_strategy, state=letter_state_strategy)
def test_letter_state_update_property(letter, state):
    """Test that letter state can be updated to any valid state"""
    l = Letter(name=letter)
    l.letter_state = state
    assert l.letter_state == state

# Test Word class properties
@given(word=word_strategy)
def test_word_creation_property(word):
    """Test that any valid word can be created"""
    w = Word.create(word, [word])
    assert isinstance(w, Word)
    assert len(w.word) == MAX_WORD_LEN
    assert str(w) == word

@given(word1=word_strategy, word2=word_strategy)
def test_word_equality_property(word1, word2):
    """Test word equality based on string representation"""
    w1 = Word.create(word1, [word1])
    w2 = Word.create(word2, [word2])
    assert (str(w1) == str(w2)) == (word1 == word2)

# Test Board class properties
@given(words=st.lists(word_strategy, max_size=MAX_USER_GUESSES))
def test_board_capacity_property(words):
    """Test board capacity property"""
    board = Board()
    for word in words:
        w = Word.create(word, [word])
        board.add_word(w)
    assert len(board.words) <= MAX_USER_GUESSES

@given(word=word_strategy, position=st.integers(min_value=0, max_value=MAX_USER_GUESSES-1))
def test_board_word_retrieval_property(word, position):
    """Test word retrieval at any valid position"""
    board = Board()
    w = Word.create(word, [word])
    board.add_word(w)
    if position < len(board.words):
        assert board.get_word_at_position(position) == w
    else:
        assert board.get_word_at_position(position) is None

# Test Game class properties
@given(guess=word_strategy)
def test_guess_normalization_property(guess):
    """Test that guess normalization preserves letters"""
    game = Game(player=Player(name="test"))
    normalized = game.normalize_player_guess(guess)
    assert normalized == guess.lower().strip()

@given(secret=word_strategy, guess=word_strategy)
def test_letter_comparison_property(secret, guess):
    """Test letter comparison properties"""
    game = Game(player=Player(name="test"))
    game.secret_word = secret
    word = Word.create(guess, [guess])
    game.compare(word)
    
    # Properties that should always hold:
    for i, letter in enumerate(word.word):
        if letter.name == secret[i]:
            assert letter.letter_state == LetterState.green
        elif letter.name in secret:
            assert letter.letter_state == LetterState.yellow
        else:
            assert letter.letter_state == LetterState.grey

# Test Player class properties
@given(name=st.text(min_size=1), guesses=st.integers(min_value=0, max_value=MAX_USER_GUESSES))
def test_player_guesses_property(name, guesses):
    """Test player guesses property"""
    player = Player(name=name)
    player.number_of_guesses = guesses
    assert 0 <= player.number_of_guesses <= MAX_USER_GUESSES

# Test integration properties
@given(secret=word_strategy, guesses=st.lists(word_strategy, max_size=MAX_USER_GUESSES))
def test_game_flow_property(secret, guesses):
    """Test properties that should hold during game flow"""
    game = Game(player=Player(name="test"))
    game.secret_word = secret
    board = Board()
    
    for guess in guesses:
        word = Word.create(guess, [guess])
        if word is not False:
            game.compare(word)
            board.add_word(word)
            
            # Properties that should always hold:
            assert len(board.words) <= MAX_USER_GUESSES
            if guess == secret:
                assert game.is_secret_word(word)
            else:
                assert not game.is_secret_word(word)

# Test edge cases
@given(word=st.text())
def test_word_validation_edge_cases(word):
    """Test word validation with various inputs"""
    result = Word.create(word, [word])
    if len(word) != MAX_WORD_LEN or not word.isalpha() or not word.islower():
        assert result is False
    else:
        assert isinstance(result, Word)

@given(guesses=st.integers())
def test_player_guesses_edge_cases(guesses):
    """Test player guesses with edge cases"""
    player = Player(name="test")
    try:
        player.number_of_guesses = guesses
        assert 0 <= player.number_of_guesses <= MAX_USER_GUESSES
    except ValueError:
        assert guesses < 0 or guesses > MAX_USER_GUESSES 