import random

def generate_random_number():
    return str (random.randint(0,9999)).zfill(4)

#print(generate_random_number())

def user_guess():
    while True:
        try:
            guess = input("Enter your 4-digit guess (or type 'give up' to reveal the answer): ")
            if guess.lower() == 'give up':
                return None
            elif not guess.isdigit() or len(guess) != 4:
                raise ValueError ("Invalid input, try again");