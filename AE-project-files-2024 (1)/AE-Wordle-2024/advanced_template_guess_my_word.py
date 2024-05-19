#!/usr/bin/env python3
"""Guess-My-Word is a game where the player has to guess a word.
WORDLE GAME
Author: Arvand Eftekhar
Company: NMTAFE, 20108797
Copyright: 2024"""

import random

MISS = 0  # _-.: letter not found ⬜
MISSPLACED = 1  # O, ?: letter in wrong place 🟨
EXACT = 2  # X, +: right letter, right place 🟩

MAX_ATTEMPTS = 6
WORD_LENGTH = 5

ALL_WORDS = 'all_words.txt'  # Update with actual file path
TARGET_WORDS = 'target_words.txt'  # Update with actual file path


def register_user():
    username = input("Enter a username: ")
    password = input("Enter a password: ")
    with open("users.txt", "a") as f:
        f.write(f"{username},{password}\n")
    print("Registration successful!\n")


def login_user():
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    with open("users.txt", "r") as f:
        users = f.readlines()
    for user in users:
        saved_username, saved_password = user.strip().split(",")
        if username == saved_username and password == saved_password:
            print("Login successful!")
            print("Input 'help' for game rules.\n")
            return True
    print("Login failed. Please try again.\n")
    return False


def get_valid_words(file_path=ALL_WORDS):
    """returns a list containing all valid words."""
    with open(file_path, 'r') as file:
        return [line.strip() for line in file.readlines()]


def get_target_word(file_path=TARGET_WORDS, seed=None):
    """Picks a random word from a file of words."""
    with open(file_path, 'r') as file:
        words = [line.strip() for line in file.readlines()]
    if seed is not None:
        random.seed(seed)
    return random.choice(words)


def ask_for_guess(valid_words):
    """Requests a guess from the user directly from stdout/in."""
    while True:
        guess = input(f"Enter your {WORD_LENGTH}-letter guess: ").strip().lower()
        if guess == 'help':
            print("GAME RULES:")
            print("- You have to guess a 5-letter word.")
            print("- You have a maximum of 6 attempts.")
            print("- After each guess, you will receive feedback:")
            print("    ⬜ : Letter not found")
            print("    🟨 : Letter in wrong place")
            print("    🟩 : Right letter, right place")
            print("- The game ends when you correctly guess the word or run out of attempts.")
            continue
        if len(guess) == WORD_LENGTH and guess in valid_words:
            return guess
        print(f"Invalid guess. Ensure it's a {WORD_LENGTH}-letter word from the valid words list.")


def score_guess(guess, target_word):
    """given two strings of equal length, returns a tuple of ints representing the score of the guess against the target word."""
    score = []
    for g_char, t_char in zip(guess, target_word):
        if g_char == t_char:
            score.append(EXACT)
        elif g_char in target_word:
            score.append(MISSPLACED)
        else:
            score.append(MISS)
    return tuple(score)


def is_correct(score):
    """Checks if the score is entirely correct and returns True if it is."""
    return all(s == EXACT for s in score)


def format_score(guess, score):
    """Formats a guess with a given score as output to the terminal."""
    guess_display = " ".join(guess.upper())
    score_display = " ".join(["⬜" if s == MISS else "🟨" if s == MISSPLACED else "🟩" for s in score])
    return f"{guess_display}\n{score_display}"


def play():
    """Code that controls the interactive game play."""
    word_of_the_day = get_target_word()
    valid_words = get_valid_words()
    attempts = 0
    while attempts < MAX_ATTEMPTS:
        remaining_attempts = MAX_ATTEMPTS - attempts
        print(f"\nAttempts left: {remaining_attempts}")
        guess = ask_for_guess(valid_words)
        score = score_guess(guess, word_of_the_day)
        print("Result of your guess:")
        print(format_score(guess, score))
        if is_correct(score):
            print("Congratulations! You've guessed the word correctly!")
            break
        attempts += 1
    else:
        print(f"Sorry, you've used all your attempts. The word was: {word_of_the_day}")



def main():
    while True:
        choice = input("Do you want to [L]ogin or [R]egister? (L/R): ").strip().upper()
        if choice == 'L':
            if login_user():
                break
        elif choice == 'R':
            register_user()
        else:
            print("Invalid choice. Please enter 'L' to login or 'R' to register.")

    play()


if __name__ == '__main__':
    main()
