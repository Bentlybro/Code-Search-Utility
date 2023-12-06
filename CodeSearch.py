import os
import re
import multiprocessing

def search_file(file_path, pattern):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return [line.strip() for line in f if pattern.search(line)]
    except UnicodeDecodeError:
        return []

def process_file(file_tuple):
    file_path, pattern = file_tuple
    matching_lines = search_file(file_path, pattern)
    if matching_lines:
        return file_path, matching_lines
    return None

def main(root_dir, pattern_str):
    try:
        pattern = re.compile(pattern_str)
    except re.error:
        print("Invalid search pattern. Please ensure your pattern is a valid regular expression.")
        return

    pool = multiprocessing.Pool()
    file_paths = [
        (os.path.join(dirpath, filename), pattern)
        for dirpath, _, filenames in os.walk(root_dir)
        for filename in filenames if filename.endswith(".py")
    ]

    matching_code_snippets = dict(filter(None, pool.map(process_file, file_paths)))

    if matching_code_snippets:
        print("Matching code snippets:")
        for file_path, code_snippets in matching_code_snippets.items():
            print(f"File: {file_path}\nCode snippets:")
            for code_snippet in code_snippets:
                print(code_snippet)
            print()
    else:
        print(f"No matching code snippets found for pattern '{pattern_str}'.")

if __name__ == "__main__":
    root_dir = os.path.dirname(os.path.realpath(__file__))
    pattern_str = input("Enter the search pattern: ")
    main(root_dir, pattern_str)
