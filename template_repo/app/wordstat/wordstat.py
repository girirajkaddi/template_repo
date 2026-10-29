import argparse
import re
from collections import Counter
from pathlib import Path


def count_words(file_path):
    """Read a text file and return word frequencies."""
    path = Path(file_path)

    if not path.is_file():
        raise FileNotFoundError(f"Error: File not found: {file_path}")

    text = path.read_text(encoding="utf-8")

    words = re.findall(r"[^\W_]+", text.casefold(), flags=re.UNICODE)

    return Counter(words)


def main():
    parser = argparse.ArgumentParser(
        description="Count words in a text file and display the top N"
    )

    parser.add_argument("file", help="Path to the text file")

    parser.add_argument(
        "-n", "--top", type=int, default=10, help="Number of top words to display (default: 10)"
    )

    args = parser.parse_args()

    if args.top < 1:
        parser.error("N must be greater than 0.")

    try:
        word_counts = count_words(args.file)
    except (FileNotFoundError, PermissionError, UnicodeDecodeError, OSError) as error:
        parser.exit(status=1, message=f"{error}\n")

    if not word_counts:
        print("The file is empty or contains no words.")
        return

    print(f"Top {args.top} words:")
    for word, count in word_counts.most_common(args.top):
        print(f"{word}: {count}")


if __name__ == "__main__":
    main()
