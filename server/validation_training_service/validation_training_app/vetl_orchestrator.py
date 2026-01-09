import os

# ===== import fix from gemini in below block ==========
# This ensures we can import 'utils' regardless of where 
# ---------------------------------------------------------
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
# =================== end of gemini fix ================


print("Hello1")

from .dataset_validation import validate_dataset
from .merge_datasets import merge_mcgill_dataset_directories

# returning paths independently of platform run on
DEFAULT_MCGILL_PATH = os.path.join(project_root, 'resources', 'The-McGill-Billboard')

def vetl_orchestrator(dataset_version,path=DEFAULT_MCGILL_PATH, val_threshold=0.65):
    
    print("inside the orchestrator??! or?")

    # # Check the resources directory
    # resources_path = os.path.join(project_root, 'resources')
    # if os.path.exists(resources_path):
    #     print(f"Contents of resources directory:")

    chordino_path = os.path.join(path, "billboard-2.0-chordino")
    mirex_path = os.path.join(path, "billboard-2.0.1-mirex")

    if not os.path.exists(chordino_path):
        print(f"Error: folder at {chordino_path} is missing")
        return None
    
    if not os.path.exists(mirex_path):
        print(f"Error: folder at {mirex_path} is missing")
        return None
    
    print("The data directories are available for validation. . .")

    #Get common song folders
    chroma_subdirs = {f for f in os.listdir(chordino_path)
                    if os.path.isdir(os.path.join(chordino_path, f)) and not f.startswith('.')}
    majmin_subdirs = {f for f in os.listdir(mirex_path)
                 if os.path.isdir(os.path.join(mirex_path, f)) and not f.startswith('.')}

    total_submitted = max(len(chroma_subdirs), len(majmin_subdirs))

    val_results = validate_dataset(chordino_path, mirex_path)

    valid_songs = []

    valid = 0
    for element in val_results:
        result = val_results[element]
        is_valid = result[0]
    
        if is_valid == True:
            valid += 1
            valid_songs.append(element)
    
    if total_submitted > 0: 
        validity = valid / total_submitted
        percentage_val = validity * 100

        if validity >= val_threshold:
            print(f"we have enough valid data.\n{percentage_val}% valid\nContinuing validation. . . ")
            
            # ============= Merging into the combined data directory ==================
            print("\nMerging the valid data into a combined folder...")
            combined_path = merge_mcgill_dataset_directories(chordino_path, mirex_path, valid_songs)

            if not os.path.exists(combined_path):
                print(f"Error: Combined directory was not created at {combined_path}")
                return None
            
            merged_subdirs = {f for f in os.listdir(combined_path)
                             if os.path.isdir(os.path.join(combined_path, f)) and not f.startswith('.')}
            
            if len(merged_subdirs) == 0:
                print("Error: No song directories found in combined folder")
                return None
            
            expected_count = len(valid_songs)
            actual_count = len(merged_subdirs)

            merge_success_rate = (actual_count / expected_count) * 100 if expected_count > 0 else 0
            print(f"Merge validation complete: {actual_count}/{expected_count} songs merged ({merge_success_rate:.1f}%)")
            
            if actual_count >= expected_count * 0.95:  # 95% threshold
                
                
                # ============= Generating the SQLite database ==================
                print("\nGenerating SQLite database from combined data. . .")
                try:
                    from .sqlite_dataset_builder import build_sqlite_from_dataset
                    
                    # Get parent directory of combined 
                    combined_parent = os.path.dirname(combined_path)
                    db_name = 'billboard_data.db'
                    db_path = os.path.join(combined_parent, db_name) # save in McGill
                    
                    db_path = build_sqlite_from_dataset(
                        dataset_version,
                        combined_path=combined_path,
                        valid_songs=valid_songs,
                        database_name=db_path,
                        chunksize=10000
                    )
                    
                    print(f"The database was successfully created at: {db_path}")
                    
                    return {
                        'valid_songs': valid_songs,
                        'combined_path': combined_path,
                        'db_path': db_path,
                        'merge_count': actual_count
                    }
                    
                except Exception as e:
                    print(f"Error encountered while generating database: {e}")
                    return None
            else:
                print(f"Merge validation failed")
                return None

        else:
            print(f"not enough valid data for retraining only ({percentage_val})% valid data.")
        return None
    else: 
        print("Data not vaailable")
        return None
    
if __name__ == "__main__":
    # Get the results by running the orchestrator
    results = vetl_orchestrator()
    
    # Check if we got data back
    if results:
        print(f"Pipeline completed successfully!")
        print(f"Processed {len(results['valid_songs'])} valid songs")
        print(f"merged {results['merge_count']} song directories")
        print(f"sqlite database: {results['db_path']}")
    else:
        print("Pipeline stopped. Something broke alone the way.")