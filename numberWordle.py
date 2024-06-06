import random
import json
import sys


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


def create_account(users_data):
    username = input("Enter your username (letters only): ")
    while not username.isalpha():
        print("Invalid username. Please use letters only.")
        username = input("Enter your username (letters only): ")
        password = input("Enter your 3-digit PIN: ")

    while username in users_data:
        print("This username is already in use. Please choose a different username.")
        username = input("Enter your username (letters only): ")

    while not password.isdigit() or len(password) != 3:
        print("Invalid PIN. Please enter a 3-digit number.")
        password = input("Enter your 3-digit PIN: ")

    return username, password


def save_user_data(user_data):
    with open("user_data.json", "w") as file:
        json.dump(user_data, file)


def login():
    try:
        with open("user_data.json", "r") as file:
            users = json.load(file)
    except FileNotFoundError:
        users = {}

    username = input("Do you have an account? Enter your username (or type 'new' to create an account or 'quit'): ")

    if username.lower() == 'new':
        new_username, new_password = create_account(users)
        users[new_username] = {"password": new_password, "high_score": float('inf')}
        save_user_data(users)
        print("Account created successfully! Now please log in.")
        username = new_username
    elif username.lower() == 'quit':
        sys.exit()
    elif username in users:
        password = input("Enter your PIN: ")
        if password == users[username]["password"]:
            print("Login successful!")
            print("Your high score is:", users[username]["high_score"])

            if admin_login() is True:
                print("Admin options:")
                print("1. Delete a user")
                admin_choice = input("Enter the number of your choice: ")

                if admin_choice == '1':
                    display_user_list(users)
                    target_user = input("Enter the username to delete (or type 'cancel' to cancel): ")
                    if target_user.lower() != 'cancel':
                        delete_user(users, target_user)

        else:
            print("Incorrect PIN. Please try again.")
            return login()
    else:
        print("User not found. Please enter a valid username.")
        return login()

    return username, users


def admin_login():
    admin_username = "admin"
    admin_password = "123"

    entered_username = input("If admin enter username else hit enter: ")
    entered_password = input("If admin enter pin else hit enter: ")

    if entered_username == admin_username and entered_password == admin_password:
        print("Admin login successful!")
        return True
    else:
        print("Incorrect admin credentials.")
        return False


def display_user_list(users):
    print("List of Users:")
    for username in users:
        print(username)


def delete_user(users, target_user):
    if target_user in users:
        del users[target_user]
        print(f"User '{target_user}' deleted successfully.")
        save_user_data(users)
    else:
        print(f"User '{target_user}' not found.")


def update_high_score(username, total_guesses, user_data):
    if total_guesses < user_data[username]["high_score"]:
        user_data[username]["high_score"] = total_guesses

    with open("user_data.json", "w") as file:
        json.dump(user_data, file)


def evaluate_guess(secret_number, user_guess):
    correct_position = sum(a == b for a, b in zip(secret_number, user_guess))
    correct_number = sum(secret_number.count(num) for num in set(user_guess))
    correct_not_position = correct_number - correct_position
    return correct_position, correct_not_position


def play_game(username, user_data):
    secret_number = generate_random_number()
    total_guesses = 0

    while True:
        user_guess = get_user_guess()

        if user_guess is None:
            print(f"The answer was: {secret_number}")
            break

        total_guesses += 1

        if user_guess == secret_number:
            print(f"Congrats! You guessed the number. It took you {total_guesses} guesses.")
            update_high_score(username, total_guesses, user_data)
            break
        else:
            correct_position, correct_not_position = evaluate_guess(secret_number, user_guess)
            print(f"Correct position: {correct_position}")
            print(f"Correct number but not in the correct position: {correct_not_position}")


if __name__ == "__main__":
    try:
        with open("user_data.json", "r") as file:
            user_data = json.load(file)
    except FileNotFoundError:
        user_data = {}

    while True:
        user_input = input("Welcome to the game, press enter to start: ")

        if user_input.lower() == 'quit':
            break

        is_admin = admin_login()
        if is_admin:
            print("Admin login successful!")
            print("Admin options:")
            print("1. Display user list")
            print("2. Delete a user")
            admin_choice = input("Enter the number of your choice (or hit enter to continue): ")

            if admin_choice == '1':
                display_user_list(user_data)
            elif admin_choice == '2':
                display_user_list(user_data)
                target_user = input("Enter the username to delete (or type 'cancel' to cancel): ")
                if target_user.lower() != 'cancel':
                    delete_user(user_data, target_user)
        else:
            username, user_data = login()
            if username:
                print("Welcome, {}!".format(username))
                play_game(username, user_data)
                play_again = input("Do you want to play again? (y/n): ").lower()
                if play_again != 'y':
                    print("Thanks for playing")
                    break
