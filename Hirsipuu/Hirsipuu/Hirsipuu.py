# TIE-02100 Johdatus ohjelmointiin
# Viktor Mykrä, viktor.mykra@student.tut.fi, opiskelijanumero: 274391
# Eero Mäkiranta, eero.makiranta@student.tut.fi, opiskelijanumero: 274514
# Hangman game
# Status: READY
"""
This program is Hangman-game. In the game you have to guess letters of a word
which the game chooses based on the difficulty you set in main menu. There are
three difficulty levels. EASY: *, chooses a word between 1 to 5 letters long.
HARD: ***, chooses a word between 5 to 8 letters long and PUNISHER: *****
creates 8 letters long nonsense word. You can choose the difficulty from the
 drop down menu in main menu. In the game you have six tries to guess
all the letters in the word. To guess a letter you have to click button with
the letter you want to guess on it. If the guessed letter is in the word, it
will appear on the right slot(s). If you fail to guess all the letters in
six tries, you will lose and die (in the game of course). If you do, you will
win. In the main menu there is also info, help and quit buttons. Info button
gives you some information about the program. Help button gives you the rules
of the game. Quit button shuts down the program. We hope you have fun time
playing our little game. We poured our hearts and souls into making it.

While making this program we aimed for the ease of use and portability for
touch screens. Thats why we made it playable by only a mouse. Also the
program is very robust because there is no action user can make that we didn't
think about. We aimed for the scalable level in this project. Scalability can
be seen in the game screen with the keyboard, answer slots and pictures. For
example there is always a correct amount of answer slots.
"""


from tkinter import *
import random
import string


def read_file(filename):
    """
    Reads file with words in it. Words are separated by ','. Makes a list of
    all the words.
    :param filename: str
    :return words: list
    """
    words = []

    with open(filename,'r') as f:
        for rivi in f:
            words_list = rivi.split(",")
            words_list = [word.strip() for word in words_list]
            for word in words_list:
                word_upper = word.upper()
                words.append(word_upper)
            for i in range(len(words)):
                if words[i] == "":
                    del words[i]

    return words


def random_word(words):
    """
    Takes the list of all words and picks a random one. Returns that random
    word.
    :param words: list
    :return word_random: str
    """
    rnd_seed = random.randint(0, len(words)-1)
    word_random = words[rnd_seed]
    return word_random


def nonsense_word():
    """
    This function generates random nonsensical word that is 8 letters long.
    :return word: str
    """
    letters = list(string.ascii_uppercase)
    word = ""
    for i in range(7):
        rnd_seed = random.randint(0, len(letters) - 1)
        word += letters[rnd_seed]
    return word


def set_difficulty_and_get_word(words, difficulty):
    """
    Generates a word with difficulty set by difficulty param.
    :param words: str
    :param difficulty: str
    :return word: str
    """

    if difficulty == "EASY: *":
        word = random_word(words)
        while len(word) > 5:
            word = random_word(words)
        return word

    if difficulty == "HARD: ***":
        word = random_word(words)
        while len(word) < 5 or len(word) > 8:
            word = random_word(words)
        return word

    if difficulty == "PUNISHER: *****":
        word = nonsense_word()
        return word


def word_processor(word):
    """
    Takes a word, and makes a dict with letters and their index in the word.
    :param word: str a word.
    :return: dict with letters and their index in the word.
    """
    letters = list(word)
    letters_dict = {}
    for letter in letters:
        letters_dict[letter] = []
    for i in range(len(letters)):
        letters_dict[letters[i]].append(i)
    return letters_dict


def quess(quess, print_list,word_dict, method):
    """
    Takes dict of randomly selected word and guess. If quess
    letter is in random word, puts guessed letter on its right place. Else
    does not change print_list and returns 1 to be reduced from tries left
    :param quess: str, character of the button player pressed
    :param word_dict: dict
    :param print_list: list
    :return:int,list
    """

    print_info = print_list
    if quess in word_dict:
        for i in range(len(word_dict[quess])):
            print_info[word_dict[quess][i]] = quess
        method.game(0, print_info)
    else:
        method.game(1, print_info)


def get_answer_x(print_list):
    """
    Calculates approximation of coordinates for printing answer blocks
    so that its always more or less centered
    :param print_list: List of letters that you have guessed right and
        under scores in the places of letters you have not quessed yet.
    :return: approximation of coordinates for printing answer blocks
    so that its always more or less centered
    """
    starting_point = int((640-(len(print_list)*40))/2)-len(print_list)/2
    return starting_point


class Ui:

    def __init__(self):


        self.__window = Tk()
        self.__window.title("Hangman")
        self.__window.geometry("{}x{}".format(640, 500))
        self.__window.resizable(width=0, height=0)

        # Difficulty drop menu for main menu:
        self.__choises = StringVar(self.__window)
        self.__choises.set("EASY: *")

        # Reads the file with words in it:
        self.__word_list = read_file("WORDS.txt")

        # Word processing for the hangman game:
        self.__word = set_difficulty_and_get_word(self.__word_list,
                                                  self.__choises.get())
        self.__word_dict = word_processor(self.__word)
        self.__turns_left = 6

    def main_menu(self):
        """
        Creates a window with main menu. Options: New Game: Starts a new game.
        Difficulty: You can choose the difficulty with the drop down menu.
        Info: You will see some info about the program.
        Help: You will get help.
        Quit: You will quit.
        :return:
        """
        try:
            # Clears window, if window has been closed
            # by the user before that, returns to main(): and closes the
            # program.
            for widget in self.__window.winfo_children():
                widget.destroy()
        except TclError:
            return

        try:
            # Catches some problem with closing the program in main menu.
            # Photo for main menu:
            photo = PhotoImage(file="Hangman.gif")
        except RuntimeError:
            return


        hardness_list = ["EASY: *", "HARD: ***", "PUNISHER: *****"]
        # Main menu:
        # Buttons for main menu:
        button_new_game = Button(self.__window, text="New Game",
                                 command= self.new_game)
        button_help = Button(self.__window, text="Help", command=self.help)
        button_info = Button(self.__window, text="Info", command=self.info)
        button_exit = Button(self.__window, text="Quit", command = quit)
        # Image for main menu:
        image_label = Label(self.__window, image=photo)
        # Difficulty drop down menu for main menu:
        difficulty_label = Label(self.__window, text="Difficulty:")
        difficulty = OptionMenu(self.__window, self.__choises,
                                       * hardness_list)

        button_exit.pack(fill=X, side=BOTTOM)
        button_info.pack(fill=X, side=BOTTOM)
        button_help.pack(fill=X, side=BOTTOM)
        difficulty.pack(fill=X, side=BOTTOM)
        difficulty_label.pack(fill=X, side=BOTTOM)
        button_new_game.pack(fill=X, side=BOTTOM)
        image_label.pack(fill=X, side= BOTTOM)

        self.__window.mainloop()

    def info(self):
        """
        Opens a window with info about the program in it.
        :return:
        """
        try:
            for widget in self.__window.winfo_children():
                # Clears window, if window has been closed
                # by the user before that, returns to main(): and closes the
                # program.
                widget.destroy()
        except TclError:
            return

        # Text for info screen:
        info_label = Label(self.__window, text= "This game was developed by "
                                                "Viktor Mykrä and Eero Mäkiranta in "
                                                "December 2017.")
        license_label = Label(self.__window, text= "This programm is under CC BY-NC-SA license")


        back_button = Button(self.__window, text="Main menu", command=self.main_menu)
        back_button.pack(side=BOTTOM, fill=X)
        info_label.pack(fill="none", expand=True)
        license_label.pack()

    def help(self):
        """
        Opens a window with rules of the game in it.
        :return: none
        """
        try:
            for widget in self.__window.winfo_children():
                # Clears window, if window has been closed
                # by the user before that, returns to main(): and closes the
                # program.
                widget.destroy()
        except TclError:
            return

        # Text for help screen
        help_text = Text(self.__window)
        help_text.pack()
        help_string = """
        This program is Hangman-game. In the game you have to 
        guess letters of a word which the game chooses based on the difficulty 
        you set in main menu. There are three difficulty levels. EASY: *, 
        chooses a word between 1 to 5 letters long. HARD: ***, chooses a word 
        between 5 to 8 letters long and PUNISHER: ***** creates 8 letters long 
        nonsense word. You can choose the difficulty from the drop down menu in
        main menu. In the game you have six tries to guess all the letters in 
        the word. To guess a letter you have to click button with the letter 
        you want to guess on it. If the guessed letter is in the word, it
        will appear on the right slot(s). If you fail to guess all the letters 
        in six tries, you will lose and die (in the game of course). If you do,
        you will win. We hope you have fun time playing our little game. We 
        poured our hearts and souls into making it."""
        help_text.insert(END,help_string)
        back_button = Button(self.__window, text="Main menu",
                             command=self.main_menu)

        back_button.pack(side=BOTTOM, fill=X)


    def new_game(self):
        """
        Initializes a new game and clears the window before it starts.
        :return:
        """

        try:
            # Clears window, if window has been closed
            # by the user before that, returns to main(): and closes the
            # program.
            for widget in self.__window.winfo_children():
                widget.destroy()
        except TclError:
            return

        # Starts new game, gets word to be guessed and sets turns left to 6
        self.__turns_left = 6
        # Picks a random word based on the difficulty level you set.
        self.__word = set_difficulty_and_get_word(self.__word_list,
                                                  self.__choises.get())
        # Figures out the letters and their position inside the word.
        self.__word_dict = word_processor(self.__word)
        # Starts the game.
        self.game()

    def game(self, game_turn=0, print_list=""):
        """
        This method runs the game in side UI class. When called for the first
        time in a new game, turns_left will no be subtracted and a new print
        list will be generated. Has a loop that runs until you win or lose.
        :param game_turn: int, if you guessed wrong, one turn will be deleted
        from turns_left.
        :param print_list: List of letters that you have guessed right and
        under scores in the places of letters you have not quessed yet.
        :return: none
        """

        # Keeps track of turns left.
        self.__turns_left = self.__turns_left - game_turn

        while self.__turns_left > 0:
            # Game instance, will be looping until all the turns are used or
            # player has guessed all the letters in the word
            try:
                # Clears window, if window has been closed
                # by the user before that, returns to main(): and closes the
                # program.
                for widget in self.__window.winfo_children():
                    widget.destroy()
            except TclError:
                return


            if print_list == "":
                # Makes new print_list if there isn't already one in place.
                print_list = ["__"] * len(self.__word)

            if "__" not in print_list:
                # Checks if you have guessed all the letters. If so calls
                # method win_screen
                self.win_screen()
                break

            self.draw_game_screen(print_list, self.__word_dict,
                                  self.__turns_left)

        if self.__turns_left == 0:
            # If you have no more turns, you lose. Calls the method
            # losing_screen()
            self.losing_screen()

    def draw_game_screen(self, print_list, word_dict, turns_left):
        """
        Draws the game screen with keyboard, answer slots and pictures.
        :param print_list: List of letters that you have guessed right and
        under scores in the places of letters you have not guessed yet.
        :param word_dict: dict with index of every letter in the word.
        :param turns_left: int, amount of turns you have left.
        :return: none
        """

        # Photos for the game:
        photos = [PhotoImage(file="Hangman-1.gif"),
                  PhotoImage(file="Hangman-2.gif"),
                  PhotoImage(file="Hangman-3.gif"),
                  PhotoImage(file="Hangman-4.gif"),
                  PhotoImage(file="Hangman-5.gif"),
                  PhotoImage(file="Hangman-6.gif"),
                  PhotoImage(file="Hangman-7.gif")]


        buttons = list(string.ascii_uppercase)
        # Starting coordinates for keyboard and answer slots.
        x_keyb = 120
        y_keyb = 400
        x_asw = get_answer_x(print_list)
        y_asw = 370

        for character in print_list:
            # Prints the answer slots based on the print_list. If there has
            # been correct answers previously, those are already in print_list.
            char = Label(self.__window, text=character)
            char.place(x=x_asw, y=y_asw)
            x_asw += 40

        for button in buttons:
            # Prints the buttons to the game screen and if button is pressed
            # send that letter to function quess()

            command = lambda x=button: quess(x, print_list, word_dict, self)
            key = Button(self.__window, text=button, command=command)
            key.place(x=x_keyb, y=y_keyb)
            key.config(width=4)
            x_keyb += 40
            if x_keyb == 520:
                x_keyb = 120
                y_keyb += 30

        # Prints info of turns left to game screen.
        turns_left_string = "You have " + str(turns_left) + " turns left."
        turns_left_label = Label(self.__window, text=turns_left_string)
        turns_left_label.place(x=385, y=462)

        # Photo of game screen, changes depending on turns left.
        photo = photos[self.__turns_left]
        image_label = Label(self.__window, image=photo)
        image_label.pack()

        self.__window.mainloop()

    def win_screen(self):
        try:
            # Clears window, if window has been closed
            # by the user before that, returns to main(): and closes the
            # program.
            for widget in self.__window.winfo_children():
                widget.destroy()
        except TclError:
            return

        # Prints info about you winning, correct word and buttons to take you
        # back to main screen or to play a new game.
        win_string = "Nice escape dude! Word was: " + self.__word
        win_label = Label(self.__window,text= win_string)
        back_button = Button(self.__window, text="Main menu",
                             command=self.main_menu)
        new_game_button = Button(self.__window,text="New Game",
                                 command=self.new_game)
        # Photo of you winning:
        photo = PhotoImage(file="Hangman-7.gif")
        image_label = Label(self.__window, image=photo)

        image_label.pack()
        win_label.pack()
        new_game_button.pack()
        new_game_button.config(width=20)
        back_button.pack()
        back_button.config(width=20)

        self.__window.mainloop()
    def losing_screen(self):
        try:
            # Clears window, if window has been closed
            # by the user before that, returns to main(): and closes the
            # program.
            for widget in self.__window.winfo_children():
                widget.destroy()
        except TclError:
            return

        # Prints info about you losing, correct word and buttons to take you
        # back to main screen or to play a new game.
        lose_string = "Why didn't you try " + self.__word + \
                      "? Now you're dead as a rock!"
        lose_label = Label(self.__window, text=lose_string)
        back_button = Button(self.__window, text="Main menu",
                             command=self.main_menu)
        new_game_button = Button(self.__window, text="New Game",
                                 command=self.new_game)
        # Photo of you losing
        photo = PhotoImage(file="Hangman_lose.gif")
        image_label = Label(self.__window, image=photo)

        image_label.pack()
        lose_label.pack()
        new_game_button.pack()
        new_game_button.config(width=20)
        back_button.pack()
        back_button.config(width=20)

        self.__window.mainloop()



def main():
    window = Ui()
    window.main_menu()

main()