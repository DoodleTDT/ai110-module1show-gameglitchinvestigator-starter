import pytest

from logic_utils import (
    check_guess,
    get_range_for_difficulty,
    parse_guess,
    update_score,
)


# ---------------------------------------------------------------------------
# get_range_for_difficulty
# FIX: Added functions from app.py to logic_utils.py
# ---------------------------------------------------------------------------

def test_easy_range():
    assert get_range_for_difficulty("Easy") == (1, 20)


def test_normal_range():
    assert get_range_for_difficulty("Normal") == (1, 100)


def test_hard_range():
    assert get_range_for_difficulty("Hard") == (1, 50)


def test_unknown_difficulty_defaults_to_normal():
    assert get_range_for_difficulty("Expert") == (1, 100)


def test_difficulty_is_case_sensitive():
    # Lowercase falls through to the default range instead of the Easy range.
    assert get_range_for_difficulty("easy") == (1, 100)


@pytest.mark.parametrize("difficulty", ["Easy", "Normal", "Hard"])
def test_low_is_less_than_high(difficulty):
    low, high = get_range_for_difficulty(difficulty)
    assert low < high


# ---------------------------------------------------------------------------
# parse_guess
# ---------------------------------------------------------------------------

def test_valid_integer():
    assert parse_guess("42") == (True, 42, None)


def test_negative_integer():
    assert parse_guess("-5") == (True, -5, None)


def test_float_truncates_toward_zero():
    assert parse_guess("7.9") == (True, 7, None)


def test_negative_float_truncates_toward_zero():
    assert parse_guess("-7.9") == (True, -7, None)


def test_whitespace_padded_number_is_accepted():
    assert parse_guess(" 42 ") == (True, 42, None)


def test_empty_string_is_rejected():
    assert parse_guess("") == (False, None, "Enter a guess.")


def test_none_input_is_rejected():
    assert parse_guess(None) == (False, None, "Enter a guess.")


def test_non_numeric_is_rejected():
    assert parse_guess("abc") == (False, None, "That is not a number.")


def test_bare_dot_is_rejected():
    assert parse_guess(".") == (False, None, "That is not a number.")


def test_whitespace_only_reports_not_a_number():
    # A blank-looking guess reports "That is not a number." rather than
    # "Enter a guess." because it is not caught by the empty-string check.
    ok, value, err = parse_guess("   ")
    assert ok is False
    assert value is None
    assert err == "That is not a number."


@pytest.mark.parametrize("raw", ["42", "-5", "7.9", "", None, "abc", "."])
def test_ok_flag_agrees_with_value_and_error(raw):
    ok, value, err = parse_guess(raw)
    if ok:
        assert isinstance(value, int)
        assert err is None
    else:
        assert value is None
        assert isinstance(err, str)


# ---------------------------------------------------------------------------
# check_guess
# FIX: Refactored the return statements to give accurate hints
# ---------------------------------------------------------------------------

def test_exact_match_wins():
    assert check_guess(50, 50) == ("Win", "🎉 Correct!")


def test_guess_above_secret_says_go_lower():
    outcome, message = check_guess(75, 50)
    assert outcome == "Too High"
    assert "LOWER" in message


def test_guess_below_secret_says_go_higher():
    outcome, message = check_guess(25, 50)
    assert outcome == "Too Low"
    assert "HIGHER" in message


def test_off_by_one_above():
    assert check_guess(51, 50)[0] == "Too High"


def test_off_by_one_below():
    assert check_guess(49, 50)[0] == "Too Low"


def test_lowest_guess_against_highest_secret():
    assert check_guess(1, 100)[0] == "Too Low"


def test_highest_guess_against_lowest_secret():
    assert check_guess(100, 1)[0] == "Too High"


def test_hint_direction_is_never_inverted():
    secret = 50
    for guess in range(1, 101):
        outcome, message = check_guess(guess, secret)
        if guess > secret:
            assert outcome == "Too High", guess
            assert "LOWER" in message, guess
        elif guess < secret:
            assert outcome == "Too Low", guess
            assert "HIGHER" in message, guess
        else:
            assert outcome == "Win", guess


@pytest.mark.parametrize("guess", [1, 25, 49, 50, 51, 75, 100])
def test_outcome_is_one_of_three_values(guess):
    outcome, _ = check_guess(guess, 50)
    assert outcome in {"Win", "Too High", "Too Low"}


@pytest.mark.xfail(
    strict=True,
    reason="GLITCH: the TypeError fallback compares str to int and raises again.",
)
def test_string_guess_does_not_crash():
    outcome, _ = check_guess("50", 50)
    assert outcome in {"Win", "Too High", "Too Low"}


# ---------------------------------------------------------------------------
# update_score
# ---------------------------------------------------------------------------

def test_win_on_first_attempt():
    assert update_score(current_score=0, outcome="Win", attempt_number=1) == 80


def test_win_on_second_attempt():
    assert update_score(current_score=0, outcome="Win", attempt_number=2) == 70


def test_win_points_are_floored_at_ten():
    assert update_score(current_score=0, outcome="Win", attempt_number=20) == 10


def test_win_points_shrink_as_attempts_grow():
    first = update_score(0, "Win", 1)
    second = update_score(0, "Win", 2)
    third = update_score(0, "Win", 3)
    assert first > second > third


def test_win_adds_to_the_existing_score():
    assert update_score(current_score=100, outcome="Win", attempt_number=1) == 180


def test_too_low_subtracts_five():
    assert update_score(current_score=50, outcome="Too Low", attempt_number=3) == 45


def test_too_high_on_even_attempt_adds_five():
    # A wrong guess on an even-numbered attempt currently rewards the player.
    assert update_score(current_score=50, outcome="Too High", attempt_number=2) == 55


def test_too_high_on_odd_attempt_subtracts_five():
    assert update_score(current_score=50, outcome="Too High", attempt_number=3) == 45


def test_unknown_outcome_leaves_score_unchanged():
    assert update_score(current_score=50, outcome="Banana", attempt_number=1) == 50


def test_score_can_go_negative():
    assert update_score(current_score=0, outcome="Too Low", attempt_number=1) == -5


@pytest.mark.xfail(
    strict=True,
    reason="GLITCH: 'Too High' on an even attempt increases the score.",
)
def test_wrong_guess_never_increases_score():
    for outcome in ("Too High", "Too Low"):
        for attempt_number in range(1, 9):
            assert update_score(50, outcome, attempt_number) < 50, (
                outcome,
                attempt_number,
            )
