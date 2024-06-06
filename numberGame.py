import random
import json


def generate_random_number():
    return str(random.randint(0, 9999)).zfill(4)


def get_user_guess():
    while True:
        try:
            guess = input("Enter your 4-digit guess (or type 'give up' to reveal the answer): ")
            if guess.lower() == 'give up':
                return None
            elif not guess.isdigit() or len(guess) != 4:
                raise ValueError("Invalid input. Please enter a 4-digit number.")
            return guess.zfill(4)
        except ValueError as e:
            print(e)


def evaluate_guess(secret_number, user_guess):
    correct_position = sum(a == b for a, b in zip(secret_number, user_guess))
    correct_number = sum(secret_number.count(num) for num in set(user_guess))
    correct_not_position = correct_number - correct_position
    return correct_position, correct_not_position


def create_account():
    user_name = input("Enter a username (letters only): ")
    while not user_name.isalpha():
        print("This is not a valid username try again")
        user_name = input("Enter a username (letters only): ")

    password = input("Enter a 3 digit PIN number: ")
    while not password.isdigit() or len(password) != 3:
        print("This is not a valid PIN number try again")
        password = input("Enter a 3 digit PIN number: ")

    return user_name, password


def login():
    with open("user_data.json", "r") as file:
        users = json.load(file)

    username = input("Do you have an account? Enter your username (or type 'new' to create an account): ")

    if username.lower == "new":
        new_username, new_password = create_account()
        users[new_username] = {"password": new_password, "high_score": float('inf')}
        print("Account created successfully! You can now login")
        login()
    elif username in users:
        password = input("Enter your PIN: ")
        if password == users[username]["password"]:
            print("Login successful!")
            return username, users[username]["high_score"]
        else:
            print("Incorrect PIN try again: ")
            login()
    else:
        print("User not found. Please enter a valid username.")
        login()


def update_high_score(username, total_guesses, user_data):
    if total_guesses < user_data[username]["high_score"]:
        user_data[username]["high_score"] = total_guesses

    with open("user_data.json", "w") as file:
        json.dump(user_data, file)


def play_game():
    username, high_score = login()
    secret_number = generate_random_number()
    total_guesses = 0

    while True:
        user_guess = get_user_guess()

        if user_guess is None:
            print(f"The answer was: {secret_number}. Thanks for playing!")
            break

        total_guesses += 1

        if user_guess == secret_number:
            print(f"Congrats! You guessed the number. It took you {total_guesses} guesses.")
            break
        else:
            correct_position, correct_not_position = evaluate_guess(secret_number, user_guess)
            print(f"Correct position: {correct_position}")
            print(f"Correct number but not in the correct position: {correct_not_position}")
            print("Try again.")


if __name__ == "__main__":
    try:
        with open("user_data.json", "r") as file:
            user_data = json.load(file)
    except FileNotFoundError:
        user_data = {}

    main_menu = True
    while main_menu:
        play_game()
        play_again = input("Do you want to play again? (y/n): ").lower()
        if play_again != 'y':
            main_menu = False
