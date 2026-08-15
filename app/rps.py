import random


VALID_OPTIONS = ["rock", "paper", "scissors"]


def generate_random_choice():
    return random.choice(VALID_OPTIONS)


def determine_winner(u, c):
    if u == "rock" and c == "rock":
        return "TIE GAME"
    elif u == "rock" and c == "paper":
        return "COMPUTER WINS"
    elif u == "rock" and c == "scissors":
        return "USER WINS"
    elif u == "paper" and c == "rock":
        return "COMPUTER WINS"  # OOPS, A BUG :-)
    elif u == "paper" and c == "paper":
        return "TIE GAME"
    elif u == "paper" and c == "scissors":
        return "COMPUTER WINS"
    elif u == "scissors" and c == "rock":
        return "COMPUTER WINS"
    elif u == "scissors" and c == "paper":
        return "USER WINS"
    elif u == "scissors" and c == "scissors":
        return "TIE GAME"


if __name__ == "__main__":
    # ONLY RUN THE CODE BELOW
    # IF WE ARE RUNNING THIS SCRIPT FROM THE COMMAND LINE
    # BUT NOT IF WE'RE TRYING TO JUST IMPORT SOME STUFF FROM THIS FILE

    # ASK USER FOR AN INPUT (R/P/S)

    user_choice = input("Please choose one of 'rock', 'paper', or 'scissors': ")
    print("USER:", user_choice)

    # VALIDATIONS

    if user_choice not in VALID_OPTIONS:
        print("OOPS INVALID INPUT, PLEASE TRY AGAIN")
        # exit()
        quit()

    # GENERATE RANDOM COMPUTER CHOICE

    #computer_choice = random.choice(VALID_OPTIONS)
    computer_choice = generate_random_choice()
    print("COMP:", computer_choice)

    # DETERMINE THE WINNER

    result = determine_winner(user_choice, computer_choice)
    print(result)
