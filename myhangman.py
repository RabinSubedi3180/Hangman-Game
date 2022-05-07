from pickle import load, dump
import random
from os import system, name
from prettytable import PrettyTable


class Hangman:
    def __init__(self, word=None):
        self.trials = 6
        self.secret_word = word.lower()
        self.player = ("_" * len(self.secret_word))
        self.used_letters = set()

    @classmethod
    # To clear screen
    def clear_screen(cls):
        if name == 'nt':
            _ = system('cls')

        else:
            _ = system('cls')

    # To check if the player has won
    def _is_word_guessed(self):
        if set(self.secret_word) == self.used_letters:
            return True

    # To print the blank spaces for letter to be guessed
    def _blank_string(self):
        return " ".join(self.player)

    # To print players progress by inserting correct guessed letters in blanks
    def _player_progress(self, letters_guessed):
        progress = ''
        for letter in self.secret_word:
            if letter in letters_guessed:
                progress += letter
            else:
                progress += " _"
        print(progress)

    # To check if the guessed letter is vowel
    # The guess is decreased by 2 if the player incorrectly guesses vowels
    @staticmethod
    def _check_vowels(guessed_letter):
        vowels = "aeiou"
        if guessed_letter in set(vowels):
            return True

    # To load words from the Word file and choose one randomly
    @classmethod
    def _load_words(cls):
        try:
            with open("words.pkl", "rb") as f:
                word_list = load(f)
                word = random.choice(word_list)
            return word
        except FileNotFoundError:
            print("Make sure that you have downloaded the 'words.pkl' file as well")

    # To display the leader board and also fetch individual score if needed
    @staticmethod
    def get_score(player_name=None):
        # fetches individual score
        if player_name is not None:
            with open(f"leaderboard.pkl", "rb") as f:
                score_details = load(f)
                return score_details.get(f"{player_name}")

        # To display leader board
        else:
            try:
                with open(f"leaderboard.pkl", "rb") as f:
                    score_details = load(f)
                    my_table = PrettyTable(["Player Name", "Highest Score"])
                    for key, value in score_details.items():
                        my_table.add_row([key, value])
                    print(my_table)
            except FileNotFoundError:
                print("No leaderboard has been created yet!!")

    # To save and update player score
    @staticmethod
    def save_score(player_name, score, update_choice=None):
        score_details = {}
        flag = False
        # updates player score
        if update_choice is not None:
            with open(f"leaderboard.pkl", "rb") as f:
                score_details = load(f)
                score_details.update({f"{player_name}": f"{score}"})
            with open(f"leaderboard.pkl", "wb+") as f:
                dump(score_details, f)
        # saves player score
        else:
            try:
                with open(f"leaderboard.pkl", "rb") as f:
                    score_details = load(f)
                if player_name in score_details.keys():
                    flag = True
                else:
                    with open(f"leaderboard.pkl", "rb") as f:
                        score_details = load(f)
                        score_details[f"{player_name}"] = f"{score}"
                    with open(f"leaderboard.pkl", "wb+") as f:
                        dump(score_details, f)
        # creates leaderboard if it does not exist
            except FileNotFoundError:
                with open(f"leaderboard.pkl", "wb+") as f:
                    score_details[f"{player_name}"] = f"{score}"
                    dump(score_details, f)

        return flag

    @classmethod
    def main(cls, player_name):
        word = Hangman._load_words()
        Hangman.clear_screen()
        print(f'I am thinking of a word that is {len(word)} letters long.')
        player = Hangman(word)
        print(player._blank_string())
        while player.trials > 0:
            print(f'\nYou have {player.trials} guesses left.')
            print("Guessed letters")
            print(*player.used_letters)
            your_guess = input(str('Please guess a letter: ')).lower()
            Hangman.clear_screen()
            try:
                assert your_guess.isalpha(), "Warning!!!Please enter only alphabets"
            except Exception as msg:
                print(msg)
            if your_guess in player.used_letters:
                Hangman.clear_screen()
                print(f'You have already guessed {your_guess}')

            elif your_guess not in player.used_letters:
                player.used_letters.add(your_guess)
                if your_guess in word:
                    print("Good guess")
                elif your_guess not in word:
                    if Hangman._check_vowels(your_guess):
                        player.trials -= 2
                    else:
                        player.trials -= 1
                    print(f"Oops! That letter is not in the word:")
                    Hangman.clear_screen()
            print("Your Progress:")
            player._player_progress(player.used_letters)

            if player._is_word_guessed():
                Hangman.clear_screen()
                score = len(set(word)) * player.trials
                print(f'''Congratulations, you won!
Your total score for this game is: {score}''')

                flag = True
                while flag:
                    save_choice = input(
                        str('Would you like to save your score?(y/n) '))
                    if save_choice == 'y':
                        print(
                            f'Ok {player_name}, your score has been saved.')
                        if player.save_score(player_name, score) is False:
                            flag = False
                        else:
                            print(
                                f"You already have a previous high score of {player.get_score(player_name)}.")
                            update_choice = input(
                                "Would you like to update it?? (y/n): ").lower()
                            if update_choice == 'y':
                                player.save_score(
                                    player_name, score, 1)
                                print(
                                    f'Ok {player_name}, your score has been updated.')
                                break
                            elif update_choice == 'n':
                                print(
                                    f'Ok {player_name}, your score has not been updated.')
                                break
                            flag = False
                    elif save_choice == 'n':
                        print('Your score is not saved.')
                        flag = False
                    else:
                        print('The input is not valid. Try again.')
                break
        if player.trials <= 0:
            Hangman.clear_screen()
            print(f'''Game Over!!!
            Sorry you ran out of guesses. The word was: {word}''')


if __name__ == '__main__':
    print("Welcome to Hangman Ultimate Edition")
    while True:
        choice = input('Would you like to play(p), view leaderboard(l) or quit(q): ')[
            0].lower()
        Hangman.clear_screen()
        match choice:
            case 'p':
                name = input(str('Please enter your name: ')).title()
                Hangman.main(name)
            case 'l':
                print("LeaderBoard Table")
                Hangman.get_score()

            case 'q':
                print(f'Thank you for playing. Goodbye.')
                break

            case default:
                print('Please enter valid input.')
            
