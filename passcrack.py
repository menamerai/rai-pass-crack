import threading


class PassCrack:
    def __init__(self, enc="iso-8859-15"):
        self.dictionary = []
        self.enc = enc
        self.found = [False, -1, ""]
        self.brute_set = set()

    def dict_search(self, password, portion_start, portion_end):
        print("Searching in range [{start}:{end}]".format(start=portion_start, end=portion_end))
        try:
            self.found[1] = self.dictionary.index(password, portion_start, portion_end)
        except ValueError:
            pass

    def thread_logic(self, password, threads):
        step = len(self.dictionary) // threads
        step_list = []
        for i in range(step):
            step_list.append([i * step, i * step + (step - 1)])
        for i in range(threads):
            if i == threads - 1:
                args = (password, step_list[i][0], len(self.dictionary))
            else:
                args = (password, step_list[i][0], step_list[i][1])
            thread = threading.Thread(target=self.dict_search, args=args, daemon=True)
            thread.start()
        if self.found[1] != -1:
            self.found[0] = True
            return "Match found. {password} at index {index}"\
                .format(password=self.dictionary[self.found[1]], index=self.found[1])

    def dict_crack(self, dictionary="dictionaries/nuclearfusion.txt", password="Input Mode", threads=10):
        try:
            self.dictionary = open(dictionary, "rt", encoding=self.enc).read().splitlines()
            print("Importation complete.\nInitiate dictionary attack...")
            if password == "Input Mode":
                password = input("Enter password: ")
            return self.thread_logic(password, threads)
        except UnicodeDecodeError as e:
            print(e)

    def brute_crack(self, password, mode=None):
        print("Initiate brute force attack...")
        if mode is None:
            mode = input("1 for digits only, 2 for characters only. Leave blank for both.\n"
                         "Enter mode: ")
        from itertools import product
        from string import ascii_letters, digits
        if mode == "1":
            chars = digits
        elif mode == "2":
            chars = ascii_letters
        else:
            chars = ascii_letters + digits
        guesses = 0
        for length in range(1, 6):
            for guess in product(chars, repeat=length):
                guesses += 1
                guess = "".join(guess)
                if guess == password:
                    self.found[0] = True
                    self.found[2] = guess
                    return "Password is {password}, found in {guesses} guesses."\
                        .format(password=guess, guesses=guesses)

    def crack(self, password, threads=10):
        try:
            return self.dict_crack(password=password, threads=threads)
        finally:
            if not self.found[0] and len(password) < 6:
                return self.brute_crack(password, mode=0)
            if not self.found[0]:
                return "You defeated me. Congrats"
