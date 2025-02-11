import operator
from collections import Counter
from itertools import chain
from pathlib import Path
from string import ascii_lowercase


class WordleSolver:
    def __init__(self, attempts: int = 6, word_length: int = 5) -> None:
        self.WORDS: set[str] = set()
        self.LETTER_COUNTS: dict[str, int] = {}
        self.LETTER_FREQUENCIES: dict[str, float] = {}

        self.ALLOWABLE_CHARACTERS = set(ascii_lowercase)
        self.ALLOWED_ATTEMPTS = attempts
        self.WORD_LENGTH = word_length

        self.word_vector = [set(ascii_lowercase) for _ in range(self.WORD_LENGTH)]

    def match_word_vector(self, word: str, word_vector: list[set[str]]) -> bool:
        assert len(word) == len(word_vector)
        for letter, v_letter in zip(word, word_vector):
            if letter not in v_letter:
                return False

        return True

    def update_possible_words(self, guess: str, result: str) -> None:
        for idx, letter in enumerate(result):
            match letter:
                case "=":
                    self.word_vector[idx] = {guess[idx]}
                case "+":
                    try:
                        self.word_vector[idx].remove(guess[idx])
                    except KeyError:
                        pass

                case "-":
                    for vector in self.word_vector:
                        try:
                            vector.remove(guess[idx])
                        except KeyError:
                            pass

        self.possible_words = solver.match(self.word_vector, self.possible_words)

    def match(self, word_vector: list[set[str]], possible_words: list[str]) -> list[str]:
        return [word for word in possible_words if self.match_word_vector(word, word_vector)]

    def calculate_word_commonality(self, word: str) -> float:
        score = 0.0
        for char in word:
            score += self.LETTER_FREQUENCIES[char]
        return score / (self.WORD_LENGTH - len(set(word)) + 1)

    def sort_by_commonality(self, words: list[str]) -> list[tuple[str, float]]:
        sort_by = operator.itemgetter(1)
        return sorted([(word, self.calculate_word_commonality(word)) for word in words], key=sort_by, reverse=True)

    def display_word_table(self, word_commonalities: list[tuple[str, float]]) -> None:
        for word, freq in word_commonalities:
            print(f"{word:<10} | {freq:<5.2}")

    def load_data(self) -> None:
        self.WORDS = {
            word.strip().lower()
            for word in Path("./data/wordlist.txt").read_text().splitlines()
            if len(word) == self.WORD_LENGTH and set(word).issubset(self.ALLOWABLE_CHARACTERS)
        }
        self.possible_words = list(self.WORDS.copy())
        self.LETTER_COUNTS = Counter(chain.from_iterable(self.WORDS))
        self.LETTER_FREQUENCIES = {character: value / self.LETTER_COUNTS.total() for character, value in self.LETTER_COUNTS.items()}


if __name__ == "__main__":
    print("Welcome to the Wordle Solver")
    solver = WordleSolver(6, 5)
    solver.load_data()

    for c in range(solver.ALLOWED_ATTEMPTS):
        print(f"Attempt {c} with {len(solver.possible_words)} possible words")
        solver.display_word_table(solver.sort_by_commonality(solver.possible_words)[:15])

        guess = input("Guess the word: ").lower()
        result = input("Enter the result (XXXXX fill with +-=): ").lower()

        if result == "=" * solver.WORD_LENGTH:
            print(f'\nToday\'s Wordle Solution is: "{guess}", solved in {c + 1} guesses')
            break

        solver.update_possible_words(guess, result)
        print()
