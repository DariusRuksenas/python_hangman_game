# HANGMAN GAME

from random import randint
from string import ascii_lowercase

# Reads files and returns lists.
class Textfile:
    def __init__(self, filename):
        with open(filename, "r") as inputfile:
            self.content_lang = inputfile.readlines()

    def list_lang(self, language):
        self.inputfile = self.content_lang
        self.dictionary_lang = {}
        for line in self.inputfile:
            key = line[:2]
            value = line[3:-1]
            if key in self.dictionary_lang:
                self.dictionary_lang[key].append(value)
            else:
                self.dictionary_lang[key] = [value]
        self.words_list_lang = self.dictionary_lang.get(language[0])
        return self.words_list_lang

    # Make word lists with different difficulty level
    def list_difficulty(self, difficulty_level, words_list_lang):
        self.words_list_level = []

        level = {"easy": [1, 4], "medium": [4, 7], "hard": [7, 10], "expert": [10, 26]}

        for word in words_list_lang:
            if len(set(word)) in range(
                level.get(difficulty_level)[0], level.get(difficulty_level)[1]
            ):
                self.words_list_level.append(word)
        return self.words_list_level

    # Returns a random word for a player
    def random_word(self, words_list_level):
        return words_list_level[randint(0, len(words_list_level) - 1)]


class Gallowsfile:
    def __init__(self, filename):
        with open(filename, "r") as inputfile:
            self.content = inputfile.read()
            self.words_list = self.content.split(",")

    # Returns a gallow state
    def return_gallow(self, l_left):
        return self.words_list[l_left]


translation = {
    "start": [
        "\nLet's start the game!\n",
        "\nНачнём игру!\n",
        "\nPradėkime žaidimą!\n",
    ],
    "guess": ["\nGuess the letter: ", "\nВведите букву: ", "\nSpėkite raidę: "],
    "ex_guess": ["Previous guesses: ", "Прежние угадки: ", "Buvę spėjimai: "],
    "yes_no": [
        "Please respond with YES/NO: ",
        "Пожалуйста введите YES/NO: ",
        "Prašau atsakyti YES/NO: ",
    ],
    "won": [
        "\nGAME OVER! YOU WON!",
        "\nИГРА ОКОНЧЕНА! Вы победили!",
        "\nŽAIDIMAS BAIGTAS! TU LAIMĖJAI!",
    ],
    "lost": [
        "\nGAME OVER! YOU LOST!",
        "\nИГРА ОКОНЧЕНА! ВЫ ПРОИГРАЛИ!",
        "\nŽAIDIMAS BAIGTAS! TU PRALOŠEI!",
    ],
    "word": ["Word: ", "Слово: ", "Žodis: "],
    "word_show": [
        "\nThe secret word: ",
        "\nБыло загадано слово: ",
        "\nŽodis, kurio neatspėjai: ",
    ],
    "lives": ["Lives left: ", "Оставшиеся жизни: ", "Gyvybių skaičius: "],
    "difficult": [
        "Choose game difficulty [easy/medium/hard/expert]: ",
        "Выберите сложность игры easy/medium/hard/expert]: ",
        "Pasirink sudėtingumo lygį [easy/medium/hard/expert]: ",
    ],
    "exit": [
        "\nWhould you like to play again? [yes/no]: ",
        "\nХотите попробовать еще раз? [yes/no]: ",
        "\nAr norėtum sužaisti dar kartą? [yes/no]: ",
    ],
    "no_letter": [" is not a letter.", " это не буква с кириллицы.", " yra ne raidė."],
    "played": [
        " has been guessed before.",
        " букву уже пробовали.",
        " raidę jau spėjai anksčiau.",
    ],
    "char": [
        " is not a single character.",
        " это не одина буква.",
        " yra ne vienas raidė.",
    ],
}


# Player choosing a language
def choose_language():
    game_language = ""
    answer = ["1", "2", "3"]
    while not game_language in answer:
        game_language = input(
            "\nChoose game language [1:English 2:Русский 3:Lietuvių]\nType a number [1/2/3]: "
        )
    if game_language == "1":
        return ("EN", 1)
    elif game_language == "2":
        return ("RU", 2)
    elif game_language == "3":
        return ("LT", 3)


# Language's alphabet
def choose_alphabet(language):
    if language[0] == "EN":
        return ascii_lowercase
    elif language[0] == "RU":
        return "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
    else:
        return "aąbcčdeęėfghiįyjklmnoprsštuųūvzž"


# Player choosing a difficulty level
def choose_difficulty(language):
    difficulty_level = ""
    answer = ("easy", "medium", "hard", "expert")
    while not difficulty_level in answer:
        difficulty_level = input(translation["difficult"][language[1] - 1]).lower()
    return difficulty_level.lower()


# Hides letters
def hide_letters(random_word):
    secret_word = []
    for i in range(len(random_word)):
        secret_word.append("_")
    return secret_word


# Open letters in a secret word
def show_letters(x, random_word, secret_word):
    for i in range(len(random_word)):
        if x == random_word[i]:
            secret_word[i] = x
    return " ".join(secret_word)


# User guessing a letter
def get_letter(remaining_letters, guessed_letters, alphabet, language):
    while True:
        letter = input(translation["guess"][language[1] - 1]).lower()
        if len(letter) != 1:
            if letter.lower() == "quit":
                exit()
            else:
                print(letter.lower() + translation["char"][language[1] - 1])
        elif letter not in alphabet:
            print(letter.lower() + translation["no_letter"][language[1] - 1])
        elif letter not in remaining_letters:
            print(letter.lower() + translation["played"][language[1] - 1])
        else:
            remaining_letters.remove(letter)
            guessed_letters.append(letter)
            return letter


# Play the game
def play_the_game_again(language):
    yes = ("yes", "y", "ye", "")
    no = ("no", "n")
    answer = "none"
    while not answer in yes or answer in no:
        answer = input(translation["exit"][language[1] - 1])
        if answer.lower() in yes:
            hangman_game()
        elif answer.lower() in no:
            exit()
        else:
            answer = input(translation["yes_no"][language[1] - 1])


# Begin the game
def hangman_game():

    # Player chooses language
    language = choose_language()
    alphabet = choose_alphabet(language)
    list_language = Textfile("words.txt").list_lang(language)

    print(translation["start"][language[1] - 1])

    # Player chooses difficulty
    difficulty_level = choose_difficulty(language)
    list_level = Textfile("words.txt").list_difficulty(difficulty_level, list_language)

    # Get a random word for a player
    word = Textfile("words.txt").random_word(list_level)

    # Hide a random word
    hidden_word = hide_letters(word)

    # Initialize state variables
    remaining_letters = list(alphabet)
    lives_number = 6
    guessed_letters = []
    correct_guess = []
    failed_guess = []
    letter = ""

    # Main game loop
    while len(failed_guess) < lives_number and len(correct_guess) != len(set(word)):

        # Print current game state
        print(Gallowsfile("gallows.txt").return_gallow(len(failed_guess)))
        print(
            translation["word"][language[1] - 1]
            + show_letters(letter, word, hidden_word)
        )
        ## test
        ## print('Word_test: ' + word)
        print(
            translation["lives"][language[1] - 1]
            + str(lives_number - len(failed_guess))
        )
        print(translation["ex_guess"][language[1] - 1] + " ".join(guessed_letters))

        letter = get_letter(remaining_letters, guessed_letters, alphabet, language)
        if letter in word:
            show_letters(letter, word, hidden_word)
            correct_guess.append(letter)
        else:
            failed_guess.append(letter)

    # Player has guessed the word
    print(Gallowsfile("gallows.txt").return_gallow(len(failed_guess)))
    print(
        translation["word"][language[1] - 1] + show_letters(letter, word, hidden_word)
    )
    ## test
    ## print('Word_test: ' + word)
    print(translation["lives"][language[1] - 1] + str(lives_number - len(failed_guess)))
    print(translation["ex_guess"][language[1] - 1] + " ".join(guessed_letters))

    # The end of the game
    if len(failed_guess) == lives_number:
        print(translation["word_show"][language[1] - 1] + word)
        print(translation["lost"][language[1] - 1])
    else:
        print(translation["won"][language[1] - 1])

    # Repeat the game/leave
    play_the_game_again(language)


hangman_game()
