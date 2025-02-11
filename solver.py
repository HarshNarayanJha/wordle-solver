class WordleSolver:
    def __init__(self) -> None:
        self.words: list[str] = []

    def _load_data(self) -> None:
        with open('./data/wordlist.txt', 'r') as f:
            self.words = [w for w in f.read().splitlines()]

solver = WordleSolver()
solver._load_data()
print(solver.words)
