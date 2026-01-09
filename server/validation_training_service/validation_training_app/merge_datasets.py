# Authors of code:
# -

import os
import shutil
from os.path import join, isdir

# For this parsing function to work you need to place the 
# Main McGill folder in resources, inside it you will have 
# 1. billboard-2.0-chordino
# 2. billboard-2.0.1-mirex
# results in combined folders, while dropping any mismatches

def merge_mcgill_dataset_directories(chroma_path, majmin_path, valid_list):
    subdirectories_path = os.path.dirname(chroma_path) 
    merged_dataset_path = os.path.join(subdirectories_path, "combined")
    # Checking if source folders exist
    if not os.path.exists(chroma_path) or not os.path.exists(majmin_path):
        print("Error: directories not found.")
        return False

    # get a list of the subfolders
    content_chordino = set(os.listdir(chroma_path))
    subdirs_chordino = {
        item for item in content_chordino & set(valid_list) 
        if os.path.isdir(os.path.join(chroma_path, item))
    }

    content_mirex = set(os.listdir(majmin_path))
    subdirs_mirex = {
        item for item in content_mirex & set(valid_list)
        if os.path.isdir(os.path.join(majmin_path, item))
    }

    # check subfolder matches
    print("Verifying Folder Structure")
    if subdirs_chordino == subdirs_mirex:
        print("Both subdirectories have identical songs.")
        common_folders = subdirs_chordino
    else:
        print("the subdirectories are mismatched!")
        dirs_only_chordino = subdirs_chordino - subdirs_mirex
        dirs_only_mirex = subdirs_mirex - subdirs_chordino
        
        if dirs_only_chordino:
            print(f"These directories are only in chordino folder: {dirs_only_chordino}")
        if dirs_only_mirex:
            print(f"these directories are only in mirex folder: {dirs_only_mirex}")
            
        print("\nProceeding with common folders only...")
        common_folders = subdirs_chordino.intersection(subdirs_mirex)
    
    print(f"Merging {len(common_folders)} folders...\n")

    os.makedirs(merged_dataset_path, exist_ok=True)

    for dir in common_folders:
        chordino_orig = os.path.join(chroma_path, dir)
        mirex_orig = os.path.join(majmin_path, dir)

        both_dest = os.path.join(merged_dataset_path, dir)

        # Check if source folders exist (they should, since they're in common_folders)
        if not (os.path.isdir(chordino_orig) and os.path.isdir(mirex_orig)):
            continue 

        chordino_file = 'bothchroma.csv'
        mirex_file = 'majmin.lab'
        chordino_file_path = os.path.join(chordino_orig, chordino_file)
        mirex_file_path = os.path.join(mirex_orig, mirex_file)
        if os.path.exists(chordino_file_path) and os.path.exists(mirex_file_path):
            os.makedirs(both_dest, exist_ok=True)
            shutil.copy(chordino_file_path,
                        os.path.join(both_dest, chordino_file))
            shutil.copy(mirex_file_path,
                        os.path.join(both_dest, mirex_file))
            # print(f"both files for folder: {dir} are copied")
        else:
            print(f"Skipping folder {dir} - missing required file(s)")
        if not os.path.exists(chordino_file_path):
            print(f"Missing: {chordino_file}")
        if not os.path.exists(mirex_file_path):
            print(f"Missing: {mirex_file}")

    print(f"Merge complete! combined dataset in: {merged_dataset_path}")
    return merged_dataset_path
