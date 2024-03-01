import sys
from inspect import currentframe


def get_ln():
    cf = currentframe()
    return cf.f_back.f_lineno


def file_to_list(file_path):
    l_list = []

    with open(file_path, 'r', encoding="utf-8") as file:
        for line in file:
            l_list.append(line.strip())

    return l_list


class WeightedLetter:
    def __init__(self):
        self.letter = ""
        self.counter = 0
        self.weight = 0.0

    def set_letter(self, letter):
        self.letter = letter

    def get_letter(self):
        return self.letter

    def increment_counter(self):
        self.counter += 1

    def get_counter_val(self):
        return self.counter

    def calculate_weight(self, aggregated_counters):
        if aggregated_counters != 0:
            self.weight = 1 - (self.counter / aggregated_counters)
        else:
            self.weight = 1
        # print(get_ln(), self.__class__.__name__, "letter = ", self.letter,
        #       "counter = ", self.counter, "counter = ", self.counter, "weight = ", self.weight)

    def get_weight(self):
        return self.weight


class MainAlgorithm:
    def __init__(self):
        self.letters_list = []
        self.weighted_letters_list = []
        self.input_words_list = []
        self.output_words_list = []

    def set_letters_list(self, letters_list):
        print(get_ln(), self.__class__.__name__, ": set_letters_list :", letters_list)
        self.letters_list = letters_list
        for letter in letters_list:
            curr_counted_letter = WeightedLetter()
            curr_counted_letter.set_letter(letter)
            self.weighted_letters_list.append(curr_counted_letter)

    def set_words_list(self, words_list):
        print(get_ln(), self.__class__.__name__, ": set_words_list", words_list[:4] + ["..."])
        self.input_words_list = words_list

    def run(self):
        self.assert_arrays_not_empty()
        counter = 0
        while len(self.output_words_list) < 200:
            counter += 1
            self.add_new_word_to_output_list()
            print(get_ln(), self.__class__.__name__, "Iteration = ", counter)
        print(get_ln(), self.__class__.__name__, self.output_words_list)

    def assert_arrays_not_empty(self):
        if not self.letters_list or not self.input_words_list:
            print(get_ln(), self.__class__.__name__, ": Some array is empty")
            sys.exit(1)

    def find_new_best_word_to_add_to_list(self):
        print(get_ln(), self.__class__.__name__, "Finding best word")
        highest_score_word_length = 0
        highest_score = 0
        curr_word_length = 0
        curr_score = 0
        word_to_return = "goo"
        for word in self.input_words_list:
            curr_score = self.get_word_score(word)
            curr_word_length = len(word)
            if (curr_score > highest_score) or \
                    ((curr_score == highest_score) and (curr_word_length < highest_score_word_length)):
                highest_score = curr_score
                word_to_return = word
        return word_to_return

    def get_output_word_list(self):
        return self.output_words_list

    def add_new_word_to_output_list(self):
        self.calculate_letters_weight()
        new_word = self.find_new_best_word_to_add_to_list()
        self.increment_letter_counters(new_word)
        self.output_words_list.append(new_word)
        self.remove_word_from_input_list(new_word)

    def calculate_letters_weight(self):
        total_count = 0
        for letter in self.weighted_letters_list:
            total_count += letter.get_counter_val()
        print(get_ln(), self.__class__.__name__, ": calculate_letters_weight : total_count = ", total_count)
        for letter in self.weighted_letters_list:
            letter.calculate_weight(total_count)

    def increment_letter_counters(self, new_word):
        for char in new_word:
            for letter in self.weighted_letters_list:
                if char == letter.get_letter():
                    letter.increment_counter()

    def get_word_score(self, word):
        word_score = 0
        for char in word:
            for letter in self.weighted_letters_list:
                if char == letter.get_letter():
                    word_score += letter.get_weight()
        # print(get_ln(), self.__class__.__name__, ": get_word_score : word = ", word, "score = ", word_score)
        return word_score

    def remove_word_from_input_list(self, new_word):
        print(get_ln(), self.__class__.__name__, "Removing word '", new_word, "' from input_words_list")
        self.input_words_list.remove(new_word)


class InputHandler:
    def __init__(self):
        self.letter_list = []
        self.word_list = []
        self.words_filename = ""

    def get_filename_from_user(self):
        self.words_filename = sys.argv[1]
        print(get_ln(), self.__class__.__name__, ": get_filename_from_user : ", self.words_filename)

    def get_letters_from_user(self):
        self.letter_list = sys.argv[2:]
        if not self.sanitize_input():
            print(get_ln(), self.__class__.__name__, ": Input sucks:", sys.argv[1:])
        print(get_ln(), self.__class__.__name__, ": Input from user:", sys.argv[1:])

    def get_letters_list(self):
        if len(self.letter_list) == 0:
            self.get_letters_from_user()
        print(get_ln(), self.__class__.__name__, ": letter_list is :", self.letter_list)
        return self.letter_list

    def sanitize_input(self):
        if len(self.letter_list) == 0:
            return False
        for letter in self.letter_list:
            if len(letter) > 1:
                return False
            if not letter.isalpha():
                return False
        return True

    def get_words_list(self):
        if len(self.word_list) == 0:
            self.get_filename_from_user()
            self.word_list = file_to_list(self.words_filename)
        return self.word_list


class Main:
    def __init__(self):
        self.input_handler = InputHandler()
        self.main_algorithm = MainAlgorithm()
        self.letters = []

    def run(self):
        print(get_ln(), self.__class__.__name__, ":run")
        self.get_letters_from_user()
        self.get_words_list()
        self.run_algorithm()
        self.print_output_words_list_to_file()

    def get_letters_from_user(self):
        self.letters = self.input_handler.get_letters_list()
        self.main_algorithm.set_letters_list(self.letters)

    def print_output_words_list_to_file(self):
        filename = ''.join(self.letters) + ".txt"
        print(get_ln(), self.__class__.__name__, "Printing to file", filename)
        with open(filename, "w") as file:
            file.write(" ".join(map(str, self.main_algorithm.get_output_word_list())))

    def get_best_words(self):
        print(get_ln(), self.__class__.__name__)
        self.main_algorithm.run()

    def get_words_list(self):
        print(get_ln(), self.__class__.__name__, ":get_words_list")
        self.main_algorithm.set_words_list(self.input_handler.get_words_list())

    def run_algorithm(self):
        print(get_ln(), self.__class__.__name__)
        self.main_algorithm.run()


if __name__ == '__main__':
    print(get_ln())
    main = Main()
    main.run()
