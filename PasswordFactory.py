import os
import itertools
import time
import sys
from tqdm import tqdm

def clear_terminal():
    os.system('clear' if os.name == 'posix' else 'cls')

def estimate_total_combinations(chars, min_len, max_len):
    total = 0
    for length in range(min_len, max_len + 1):
        total += len(chars) ** length
    return total

def estimate_file_size(lines, avg_length):
    return lines * (avg_length + 1)

def generate_wordlist(chars, min_len, max_len, filename, total_estimate):
    try:
        with open(filename, "w") as f:
            with tqdm(total=total_estimate, desc="Generating", unit="pwd") as progress:
                for length in range(min_len, max_len + 1):
                    for combo in itertools.product(chars, repeat=length):
                        word = ''.join(combo)
                        f.write(word + "\n")
                        progress.update(1)
    except KeyboardInterrupt:
        print("\n\n[!] Generation interrupted by user. Partial wordlist saved.")
        sys.exit()

def wordlist_loop():
    while True:
        clear_terminal()

        chars = input("Enter characters to include (e.g., abc123): ").strip()
        if not chars:
            print("Error: No characters provided.")
            continue

        try:
            min_len = int(input("Enter minimum password length: "))
            max_len = int(input("Enter maximum password length: "))
            if min_len > max_len or min_len <= 0:
                raise ValueError
        except ValueError:
            print("Error: Invalid length values. Minimum must be <= maximum and > 0.")
            continue

        filename_input = input("Enter output file name (e.g., wordlist.txt): ").strip()
        if not filename_input:
            filename_input = "wordlist.txt"

        home_dir = os.path.expanduser("~")
        filename = os.path.join(home_dir, filename_input)

        total = estimate_total_combinations(chars, min_len, max_len)
        avg_len = (min_len + max_len) / 2
        size_bytes = estimate_file_size(total, avg_len)
        size_gb = size_bytes / (1024 ** 3)
        estimated_time = total * 0.0001

        print(f"\nEstimated total passwords: {total:,}")
        print(f"Estimated file size: {size_gb:.2f} GB")
        print(f"Estimated time to complete: {estimated_time:.2f} seconds")

        if size_gb > 2:
            warn = input(f"Warning: File size is very large ({size_gb:.2f} GB). Continue? (y/n): ").strip().lower()
            if warn != 'y':
                print("Cancelled by user due to large file size.")
                continue

        confirm = input("Proceed with generation? (y/n): ").strip().lower()
        if confirm != 'y':
            print("Cancelled by user.")
            continue

        print(f"\nStarting generation... Wordlist will be saved to: {filename}\n")
        start_time = time.time()
        generate_wordlist(chars, min_len, max_len, filename, total)
        end_time = time.time()

        elapsed = end_time - start_time
        print(f"\nCompleted in {elapsed:.2f} seconds.")
        print(f"Wordlist saved as '{filename}'.")

        again = input("\nDo you want to generate another wordlist? (y/n): ").strip().lower()
        if again != 'y':
            print("Goodbye!")
            break

if __name__ == "__main__":
    wordlist_loop()