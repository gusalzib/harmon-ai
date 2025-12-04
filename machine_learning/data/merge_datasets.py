import os
import shutil

# For this parsing function to work you need to place the 
# Main McGill folder in resources, inside it you will have 
# 1. billboard-2.0-chordino
# 2. billboard-2.0.1-mirex

# results in combined folders, while dropping any mismatches

def merge_mcgill_dataset_folders(): 
    base_path = "machine_learning/resources/The-McGill-Billboard"
    chordino_path = os.path.join(base_path, "billboard-2.0-chordino")
    mirex_path = os.path.join(base_path, "billboard-2.0.1-mirex")
    merged_dataset_path = os.path.join(base_path, "combined")

    # Checking if source folders exist
    if not os.path.exists(chordino_path) or not os.path.exists(mirex_path):
        print("Error: Source folders not found.")
        return

    # get a list of the subfolders
    subfolders_chordino = {name for name in os.listdir(chordino_path) if os.path.isdir(os.path.join(chordino_path, name))}
    subfolders_mirex = {name for name in os.listdir(mirex_path) if os.path.isdir(os.path.join(mirex_path, name))}

    # check subfolder matches
    print("Verifying Folder Structure")
    if subfolders_chordino == subfolders_mirex:
        print("Success: Both archives have identical subfolder structures.")
        common_folders = subfolders_chordino
    else:
        print("Warning: subfolders are mismatched!")
        only_in_chordino = subfolders_chordino - subfolders_mirex
        only_in_mirex = subfolders_mirex - subfolders_chordino
        
        if only_in_chordino:
            print(f"These folders are only in chordino: {only_in_chordino}")
        if only_in_mirex:
            print(f"these folders only in mirex: {only_in_mirex}")
            
        print("\nProceeding with common folders only...")
        common_folders = subfolders_chordino.intersection(subfolders_mirex)
    
    print(f"Merging {len(common_folders)} folders...\n")


    os.makedirs(merged_dataset_path, exist_ok=True)

    print("Copying chordino files (bothchroma.csv, tuning.csv)...")

    for folder in os.listdir(chordino_path): 
        src = os.path.join(chordino_path, folder)
        dst = os.path.join(merged_dataset_path, folder)
        if os.path.isdir(src):
            shutil.copytree(src, dst, dirs_exist_ok=True)

    print("Copying lab files into folders...")

    for folder in os.listdir(mirex_path):
        src_folder = os.path.join(mirex_path, folder)
        dst_folder = os.path.join(merged_dataset_path, folder)

        if os.path.isdir(src_folder):
            # create one if it doesn't exist
            os.makedirs(dst_folder, exist_ok=True)

            for file in os.listdir(src_folder):
                if file.endswith('.lab'):
                    shutil.copy(
                        os.path.join(src_folder, file),
                        os.path.join(dst_folder, file)
                    )
    print(f"Merge complete! combined dataset in: {merged_dataset_path}")

merge_mcgill_dataset_folders()
