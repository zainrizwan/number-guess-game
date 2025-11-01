import streamlit as st
import random

# --- Title and Intro ---
st.set_page_config(page_title="Number Guessing Game", page_icon="🎯", layout="wide")

st.title("🎯 Number Guessing Game")
st.write("I'm thinking of a number between **1 and 100**. Can you guess it?")

# --- Initialize State ---
if "secret_number" not in st.session_state:
    st.session_state.secret_number = random.randint(1, 100)
if "attempts_left" not in st.session_state:
    st.session_state.attempts_left = 0
if "total_attempts" not in st.session_state:
    st.session_state.total_attempts = 0
if "game_started" not in st.session_state:
    st.session_state.game_started = False
if "message" not in st.session_state:
    st.session_state.message = ""
if "guess_history" not in st.session_state:
    st.session_state.guess_history = []

# --- Functions ---
def start_game(difficulty):
    st.session_state.secret_number = random.randint(1, 100)
    st.session_state.total_attempts = 10 if difficulty == "easy" else 5
    st.session_state.attempts_left = st.session_state.total_attempts
    st.session_state.guess_history = []
    st.session_state.game_started = True
    st.session_state.message = f"Game started! You have {st.session_state.attempts_left} attempts."

def reset_game():
    st.session_state.game_started = False
    st.session_state.message = ""
    st.session_state.secret_number = random.randint(1, 100)
    st.session_state.attempts_left = 0
    st.session_state.guess_history = []

# --- Difficulty Selection ---
if not st.session_state.game_started:
    difficulty = st.radio("Choose a difficulty:", ["easy", "hard"], horizontal=True)
    if st.button("Start Game 🎮"):
        start_game(difficulty)

# --- Game Section ---
else:
    # Two-column layout
    left_col, right_col = st.columns([2, 1])

    with left_col:
        st.subheader("🎯 Make Your Guess")

        # Progress bar at top
        st.progress(st.session_state.attempts_left / st.session_state.total_attempts)

        # Guess input
        guess = st.number_input("Enter your guess:", min_value=1, max_value=100, step=1)

        # Submit button
        if st.button("Submit Guess"):
            st.session_state.attempts_left -= 1

            if guess < st.session_state.secret_number:
                feedback = "📉 Too low!"
                st.session_state.message = f"{feedback} Attempts left: {st.session_state.attempts_left}"
            elif guess > st.session_state.secret_number:
                feedback = "📈 Too high!"
                st.session_state.message = f"{feedback} Attempts left: {st.session_state.attempts_left}"
            else:
                feedback = "🎉 Correct!"
                st.session_state.message = f"{feedback} The number was {st.session_state.secret_number}."
                st.session_state.game_started = False

            st.session_state.guess_history.append((guess, feedback))

            # Out of attempts
            if st.session_state.attempts_left == 0 and guess != st.session_state.secret_number:
                st.session_state.message = f"😢 Out of guesses! The number was {st.session_state.secret_number}."
                st.session_state.game_started = False

        # Feedback styling
        if "Correct" in st.session_state.message:
            st.success(st.session_state.message)
        elif "Out of guesses" in st.session_state.message:
            st.error(st.session_state.message)
        elif "Too" in st.session_state.message:
            st.warning(st.session_state.message)
        else:
            st.info(st.session_state.message)

        # Progress bar bottom
        st.progress(st.session_state.attempts_left / st.session_state.total_attempts)

        # Play Again button
        if not st.session_state.game_started:
            if st.button("Play Again 🔁"):
                reset_game()

    # --- Right Column: Guess History ---
    with right_col:
        st.subheader("📜 Guess History")
        if st.session_state.guess_history:
            for i, (num, fb) in enumerate(st.session_state.guess_history, 1):
                st.markdown(f"**{i}.** You guessed **{num}** → {fb}")
        else:
            st.write("No guesses yet! Start playing 👉")

