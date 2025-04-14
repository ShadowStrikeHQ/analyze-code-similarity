import argparse
import logging
import os
import sys
from collections import Counter

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def setup_argparse():
    """
    Sets up the argument parser for the command-line interface.
    Returns:
        argparse.ArgumentParser: The configured argument parser.
    """
    parser = argparse.ArgumentParser(description="Compares two files or snippets of code and reports a similarity score.")
    parser.add_argument("file1", help="Path to the first file or code snippet.")
    parser.add_argument("file2", help="Path to the second file or code snippet.")
    parser.add_argument("-m", "--mode", choices=['token', 'line'], default='token', help="Comparison mode: 'token' (default) or 'line'.")
    parser.add_argument("-t", "--threshold", type=float, default=0.7, help="Similarity threshold (0.0 to 1.0).  Similarity scores below this threshold will be reported as dissimilar.")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose logging.")
    return parser


def read_file(filepath):
    """
    Reads the content of a file.

    Args:
        filepath (str): The path to the file.

    Returns:
        str: The content of the file.

    Raises:
        FileNotFoundError: If the file does not exist.
        IOError: If an error occurs while reading the file.
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        logging.error(f"File not found: {filepath}")
        raise
    except IOError as e:
        logging.error(f"Error reading file {filepath}: {e}")
        raise

def tokenize(text):
    """
    Tokenizes the given text by splitting it into words.

    Args:
        text (str): The text to tokenize.

    Returns:
        list: A list of tokens.
    """
    return text.split()


def calculate_similarity(content1, content2, mode='token'):
    """
    Calculates the similarity between two strings based on token or line overlap.

    Args:
        content1 (str): The first string.
        content2 (str): The second string.
        mode (str): 'token' or 'line'.  Determines the method of comparison.

    Returns:
        float: The similarity score (0.0 to 1.0).
    """
    try:
        if mode == 'token':
            tokens1 = tokenize(content1)
            tokens2 = tokenize(content2)
            counter1 = Counter(tokens1)
            counter2 = Counter(tokens2)
            common_tokens = sum((counter1 & counter2).values())
            total_tokens = len(set(tokens1 + tokens2)) # Total unique tokens
            if total_tokens == 0:
                return 0.0
            similarity = common_tokens / total_tokens
            return similarity
        elif mode == 'line':
            lines1 = content1.splitlines()
            lines2 = content2.splitlines()
            common_lines = set(lines1) & set(lines2)
            total_lines = len(set(lines1 + lines2))
            if total_lines == 0:
                return 0.0
            similarity = len(common_lines) / total_lines
            return similarity
        else:
            logging.error(f"Invalid mode: {mode}.  Must be 'token' or 'line'.")
            raise ValueError(f"Invalid mode: {mode}.  Must be 'token' or 'line'.")
    except Exception as e:
        logging.error(f"Error calculating similarity: {e}")
        raise


def main():
    """
    Main function to execute the code similarity analysis.
    """
    parser = setup_argparse()
    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
        logging.debug("Verbose mode enabled.")

    try:
        content1 = read_file(args.file1)
        content2 = read_file(args.file2)

        similarity_score = calculate_similarity(content1, content2, args.mode)

        print(f"Similarity score: {similarity_score:.4f}")
        if similarity_score >= args.threshold:
            print("The files are considered similar.")
        else:
            print("The files are considered dissimilar.")


    except FileNotFoundError:
        sys.exit(1)  # Exit with an error code
    except ValueError as e:
        print(e)
        sys.exit(1)
    except IOError:
        sys.exit(1)
    except Exception as e:
        logging.exception("An unexpected error occurred:")
        sys.exit(1)


if __name__ == "__main__":
    main()