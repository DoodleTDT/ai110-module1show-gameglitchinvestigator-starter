from app import st
import random
from logic_utils import check_guess, get_range_for_difficulty, update_score, parse_guess

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    result = check_guess(50, 50)
    assert result == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    result = check_guess(60, 50)
    assert result == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    result = check_guess(40, 50)
    assert result == "Too Low"

def test_new_game_after_wonORlost():
    # After winning, starting a new game should reset the status to "playing"
    st.session_state.status = "won"  # This will always be "won" due to Python's boolean evaluation
    st.session_state.status = "lost"  # Overwrite to test the "lost" case
    st.session_state.attempts = 0
    st.session_state.secret = random.randint(1, 100)
    st.session_state.score = 0
    st.session_state.history = []
    assert st.session_state.status == "playing"

