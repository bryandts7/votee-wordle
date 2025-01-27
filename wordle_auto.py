import argparse
import random
import string
import requests

BASE_URL = "https://wordle.votee.dev:8000/"
LIMIT_ATTEMPTS = 100

class WordleSolver:
    def __init__(self, size):
        self.size = size
        self.correct = [None] * self.size
        self.present = {}
        self.absent = set()
        self.attempts = []
    
    def process_feedback(self, feedback):
        new_absent = set()
        for res in feedback:
            char = res['guess'].lower()
            slot = res['slot']
            result =res['result']

            if result == 'correct':
                self.correct[slot] = char
                #if char in self.present:
                #    del self.present[char]
            
            elif result == 'present':
                if char not in self.present:
                    self.present[char] = set()
                self.present[char].add(slot)
                if char in self.absent:
                    self.absent.remove(char)
            
            elif result == 'absent':
                if all(char != c for c in self.correct if c) and char not in self.present:
                    new_absent.add(char)
            
        self.absent.update(new_absent)

    def generate_guess(self):
        # Start with the correct letters
        guess = list(self.correct)
        remaining_slots = [i for i, c in enumerate(guess) if c is None]

        # Shuffle for avoiding patterns
        random.shuffle(remaining_slots)
        present_chars = [c for c in self.present if c not in guess]

        # Place present characters
        for char in present_chars:
            allowed_slots = [s for s in remaining_slots if s not in self.present.get(char, set())]
            if allowed_slots:
                slot = random.choice(allowed_slots)
                guess[slot] = char
                remaining_slots.remove(slot)

        # Fill remaining slots with valid alphabets
        for slot in remaining_slots:
            valid_chars = [c for c in string.ascii_lowercase if c not in self.absent and c not in guess]
            try:
                guess[slot] = random.choice(valid_chars) if valid_chars else random.choice([i for i in self.correct if i is not None])
            except:
                guess[slot] = random.choice(valid_chars) if valid_chars else random.choice(string.ascii_lowercase)
        return ''.join(guess)

    def solve_daily(self):
        attempts = 0
        while attempts < LIMIT_ATTEMPTS:
            attempts += 1
            guess = self.generate_guess().lower()

            # Skip duplicate guesses
            if guess in self.attempts:
                continue

            print(f"Attempt {attempts}: {guess}")
            
            response = requests.get(f"{BASE_URL}/daily", params={"guess": guess, "size":self.size})

            if response.status_code == 200:
                feedback = response.json()
                self.attempts.append(guess)
                self.process_feedback(feedback)

                if all(c is not None for c in self.correct):
                    print(f"\nSolved in {attempts} attempts!")
                    print(f"Final Answer: {''.join(self.correct).lower()}")
                    return True
            
            else:
                print(f"Error Status Code: {response.status_code}")
                print(f"Error detail: {response.content}")
                break
        
        print(f"\nFailed to solve within {attempts} attempts")
        return False


    def solve_random(self):
        seed = random.randint(0,1000)
        attempts = 0
        while attempts < LIMIT_ATTEMPTS:
            attempts += 1
            guess = self.generate_guess().lower()

            # Skip duplicate guesses
            if guess in self.attempts:
                continue

            print(f"Attempt {attempts}: {guess}")
            
            response = requests.get(f"{BASE_URL}/random", params={"guess": guess, "size":self.size, "seed":seed})

            if response.status_code == 200:
                feedback = response.json()
                self.attempts.append(guess)
                self.process_feedback(feedback)

                if all(c is not None for c in self.correct):
                    print(f"\nSolved in {attempts} attempts!")
                    print(f"Final Answer: {''.join(self.correct).lower()}")
                    return True
            
            else:
                print(f"Error Status Code: {response.status_code}")
                print(f"Error detail: {response.content}")
                break
        
        print(f"\nFailed to solve within {attempts} attempts")
        return False


    def solve_word(self, word):
        attempts = 0
        while attempts < LIMIT_ATTEMPTS:
            attempts += 1
            guess = self.generate_guess().lower()

            # Skip duplicate guesses
            if guess in self.attempts:
                continue

            print(f"Attempt {attempts}: {guess}")
            response = requests.get(f"{BASE_URL}/word/{word}", params={"guess": guess, "size":self.size})

            if response.status_code == 200:
                feedback = response.json()
                self.attempts.append(guess)
                self.process_feedback(feedback)

                if all(c is not None for c in self.correct):
                    print(f"\nSolved in {attempts} attempts!")
                    print(f"Final Answer: {''.join(self.correct).lower()}")
                    return True
            
            else:
                print(f"Error Status Code: {response.status_code}")
                print(f"Error detail: {response.content}")
                break
        
        print(f"\nFailed to solve within {attempts} attempts")
        return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Wordle Solver CLI")
    parser.add_argument("--size", type=int, default=5, help="Size of the Wordle puzzle")
    subparsers = parser.add_subparsers(dest="mode", help="Mode to run the solver in")

    # Daily mode
    daily_parser = subparsers.add_parser("daily", help="Solve the daily Wordle")

    # Random mode
    random_parser = subparsers.add_parser("random", help="Solve a random Wordle")

    # Word mode
    word_parser = subparsers.add_parser("word", help="Solve a specific Wordle word")
    word_parser.add_argument("word", type=str, help="The word to solve")

    args = parser.parse_args()

    solver = WordleSolver(args.size)

    if args.mode == "daily":
        solver.solve_daily()
    elif args.mode == "random":
        solver.solve_random()
    elif args.mode == "word":
        solver.solve_word(args.word)
    else:
        parser.print_help()

