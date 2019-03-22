# HANGMAN GAME

from random import randint
from string import ascii_lowercase

# Reads files and returns lists.
class Textfile:
    def __init__(self, filename):
        # with calls __exit__ function
        with open(filename, 'r') as inputfile:
            self.content = inputfile.read()
            self.words_list = self.content.split(',')

    # Returns a random word for a player
    def random_word(self):
        return self.words_list[randint(0, len(self.words_list) - 1)]

    # Returns a gallow state
    def return_gallow(self, l_left):
        return self.words_list[l_left]

# Play the game
def play_the_game_again():
    answer = input('\nWhould you like to play again? (YES/NO): ')
    if answer.lower() == 'yes':
        hangman_game()
    elif answer.lower() == 'no':
        exit()
    else:
        print('Please enter YES/NO: ')

# Hides letters
def hide_letters(random_word):
    secret_word = []
    for i in range(len(random_word)):
        secret_word.append('_')
    return secret_word

# Open letters in a secret word
def show_letters(x, random_word, secret_word):
    for i in range(len(random_word)):
        if x == random_word[i]:
            secret_word[i] = x
    return ' '.join(secret_word)

# User guessing a letter
def get_letter(remaining_letters, guessed_letters):
    while True:
        letter = input('\nGuess the letter: ').lower()
        if len(letter) != 1:
            if letter.lower() == 'quit':
                exit()
            else:
                print(letter.lower() + ' is not a single character.')
        elif letter not in ascii_lowercase:
            print(letter.lower() + ' is not a letter.')
        elif letter not in remaining_letters:
            print(letter.lower() + ' has been guessed before.')
        else:
            remaining_letters.remove(letter)
            guessed_letters.append(letter)
            return letter


# Begin the game
def hangman_game():

    print('\nLet\'s start the game!\n')

    # Get a random word for a player
    word = Textfile('words.txt').random_word()

    # Hide a random word
    hidden_word = hide_letters(word)

    # Initialize state variables
    remaining_letters = list(ascii_lowercase)
    guessed_letters = []
    correct_guess = []
    failed_guess = []
    letter = ''

    # Main game loop
    while len(failed_guess) < 6 and len(correct_guess) != len(set(word)):

        # Print current game state
        print(Textfile('gallows.txt').return_gallow(len(failed_guess)))
        print('Word: ' + show_letters(letter, word, hidden_word))
        # test
        #print('Word_test: ' + word)
        print('Lives left: ' + str(6-len(failed_guess)))
        print('Previous Guesses: ' + ' '.join(guessed_letters))

        letter = get_letter(remaining_letters, guessed_letters)
        if letter in word:
            show_letters(letter, word, hidden_word)
            correct_guess.append(letter)
        else:
            failed_guess.append(letter)

    # Player has guessed the word
    print(Textfile('gallows.txt').return_gallow(len(failed_guess)))
    print('Word: ' + show_letters(letter, word, hidden_word))
    # test
    #print('Word_test: ' + word)
    print('Lives left: ' + str(6-len(failed_guess)))
    print('Previous Guesses: ' + ' '.join(guessed_letters))

    # The end of the game
    if len(failed_guess) == 6:
        print('\nGAME OVER! YOU LOST!')
    else:
        print('\nGAME OVER! YOU WON!')

    # Repeat the game/leave
    play_the_game_again()

hangman_game()