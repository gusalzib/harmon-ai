import os

# Add this function to your tools.py file:
def equalize_tone(tone):
    """Convert flat notes to their sharp equivalents."""
    if tone in tones_normalized_equiv:
        return tones_normalized_equiv[tone]
    else:
        return tone

# Turn flats into sharps/naturals
tones_normalized_equiv = {
    # Flat notes
    "Cb": "B",
    "Db": "C#",
    "Eb": "D#",
    "Fb": "E",
    "Gb": "F#",
    "Ab": "G#",
    "Bb": "A#",
    # Maybe Sharp notes too for future data updates
}

chord_map = {
    "N": 1,
    "X": 2,
    "C": 3,
    "C#": 4,
    "D": 5,
    "D#": 6,
    "E": 7,
    "F": 8,
    "F#": 9,
    "G": 10,
    "G#": 11,
    "A": 12,
    "A#": 13,
    "B": 14,
}

quality_map = {"N": 1, "X": 2, "maj": 3, "min": 4, "7": 5, "maj7": 6}


def count_folders(path):
    num_of_folders = 0
    for item in os.listdir(path):
        if os.path.isdir(f"{path}/{item}"):
            num_of_folders += 1

    return num_of_folders


### Verification


def verify_count(path, count):
    total = 0
    correct = 0
    incorrect = 0

    # For each folder...
    for item in os.listdir(path):
        full_path = f"{path}/{item}"
        if os.path.isdir(full_path):

            # ... Count each file
            num_of_files = 0
            for file in os.listdir(full_path):
                if os.path.isfile(f"{full_path}/{file}"):
                    num_of_files += 1
            if num_of_files == count:
                correct += 1
            else:
                incorrect += 1
            total += 1

    print(f"Subfolders with {count} files: {correct}/{total}")


def grab_all(data_path):
    return os.listdir(data_path)


# Load data from directory
# With specified .lab file (majmin, full, etc)
def load_sets_paths(path, load_alg=grab_all):
    # Load sets and prepend full relative path
    sets = load_alg(path)
    for i in range(len(sets)):
        sets[i] = os.path.join(path, sets[i])

    return sets


def main_lmao():
    # Paths
    lab_file = "majmin.lab"
    path = os.path.join("..", "McGill-Billboard")
    N = count_folders(path)
    print(f"{N} sets available")

    # Data load and prep
    data = load_sets_paths(path)
    print(f"Loaded {len(data)} sets")
    prepare_data(data, lab_file)

    # Validation
    # validate()
