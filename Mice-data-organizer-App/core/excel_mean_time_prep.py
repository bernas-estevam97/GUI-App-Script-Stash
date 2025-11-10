import os
import pandas as pd
import time
from multiprocessing import Pool
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor, as_completed

pd.set_option('future.no_silent_downcasting', True)

def create_new_excel_mean_time(idx, file, total_files, output_folder, experiment):
    """Extract mean/time information from a filtered Excel file and append to summary file."""
    try:
        # Read the sheet once
        df_filtered = pd.read_excel(file, sheet_name='Calculated Data', header=None)

        # Extract file ID
        file_id = os.path.basename(file)
        parts = file_id.split("_")
        file_id_split = "_".join(parts[:parts.index("out")]) if "out" in parts else os.path.splitext(file_id)[0]

        # First row = headers / ids
        df_av_ids = df_filtered.iloc[[0]].copy()
        df_av_ids.insert(0, "Ids", "Ids")

        # Last row = averages
        df_av_values = df_filtered.iloc[[-1]].copy()
        df_av_values.insert(0, "Ids", file_id_split)

        # Construct output filename
        parts_path = os.path.normpath(file).split(os.path.sep)
        parent_folder_1 = parts_path[-3] if len(parts_path) > 2 else "Unknown1"
        parent_folder_2 = parts_path[-2] if len(parts_path) > 1 else "Unknown2"
        output_filename = f"{experiment.upper()}_Averages_{parent_folder_1}_{parent_folder_2}.xlsx"
        output_path = os.path.join(output_folder, output_filename)

        # Write to Excel
        if idx == 0 or not os.path.exists(output_path):
            with pd.ExcelWriter(output_path, engine='openpyxl', mode='w') as writer:
                df_av_ids.to_excel(writer, sheet_name='Averages and Time', startrow=0, index=False, header=False)
                df_av_values.to_excel(writer, sheet_name='Averages and Time', startrow=1, index=False, header=None)
        else:
            with pd.ExcelWriter(output_path, engine='openpyxl', mode='a', if_sheet_exists="overlay") as writer:
                # startrow = idx + 1 keeps all rows sequentially
                df_av_values.to_excel(writer, sheet_name='Averages and Time', startrow=idx + 1, index=False, header=None)

        return f"Processed file {idx + 1} of {total_files}: {file_id} → {os.path.basename(output_path)}"

    except Exception as e:
        return f"[ERROR] File '{file}': {e}"



def run(folder_input, folder_output=None, experiment_name="", log_fn=print):
    """Sequential processing of filtered Excel files without threading."""
    
    if not folder_input:
        log_fn("❌ No input path provided.")
        return
    if not os.path.isdir(folder_input):
        log_fn(f"❌ Invalid input directory: {folder_input}")
        return

    # Default output folder
    if not folder_output or not os.path.isdir(folder_output):
        folder_output = folder_input
        log_fn("📁 No output folder selected. Using input folder as output.")
    os.makedirs(folder_output, exist_ok=True)

    log_fn(f"📂 Input folder: {os.path.normpath(folder_input)}")
    log_fn(f"📦 Output folder: {os.path.normpath(folder_output)}")

    # Validate experiment name
    if not experiment_name:
        log_fn("⚠️ No experiment name provided — using 'EXPERIMENT'.")
        experiment_name = "EXPERIMENT"

    # Collect filtered Excel files
    file_paths = [
        os.path.join(folder_input, f)
        for f in os.listdir(folder_input)
        if f.lower().endswith('filtered.xlsx') and not f.startswith('~$')
    ]

    if not file_paths:
        log_fn(f"⚠️ No filtered Excel files found in:\n   {folder_input}")
        return

    total_files = len(file_paths)
    log_fn(f"📊 Found {total_files} filtered Excel file(s) to process")

    start = time.perf_counter()

    # Sequential processing
    for idx, file in enumerate(file_paths):
        try:
            result = create_new_excel_mean_time(idx, file, total_files, folder_output, experiment_name)
            if result:
                log_fn(f"✅ {result}")
        except Exception as exc:
            log_fn(f"❌ Error while processing file '{file}': {exc}")

    finish = time.perf_counter()
    log_fn(f"🎉 All files processed in {round(finish - start, 2)} seconds.")


# USE IN CASE OF VARIOUS FILES (HUNDREDS) TRY THREADING POOL

# from concurrent.futures import ThreadPoolExecutor, as_completed

# def run(folder_input, folder_output=None, experiment_name="", log_fn=print):
#     """Main entry point for Excel mean time preparation using threads."""
#     if not folder_input:
#         log_fn("❌ No input path provided.")
#         return
#     if not os.path.isdir(folder_input):
#         log_fn(f"❌ Invalid input directory: {folder_input}")
#         return

#     # Default output = input folder
#     if not folder_output or not os.path.isdir(folder_output):
#         folder_output = folder_input
#         log_fn("📁 No output folder selected. Using input folder as output.")
#     os.makedirs(folder_output, exist_ok=True)

#     log_fn(f"📂 Input folder: {os.path.normpath(folder_input)}")
#     log_fn(f"📦 Output folder: {os.path.normpath(folder_output)}")

#     # Validate experiment name
#     if not experiment_name:
#         log_fn("⚠️ No experiment name provided — using 'EXPERIMENT'.")
#         experiment_name = "EXPERIMENT"

#     # Collect all filtered Excel files
#     file_paths = [
#         os.path.join(folder_input, f)
#         for f in os.listdir(folder_input)
#         if f.lower().endswith('filtered.xlsx') and not f.startswith('~$')
#     ]

#     if not file_paths:
#         log_fn(f"⚠️ No filtered Excel files found in:\n   {folder_input}")
#         return

#     total_files = len(file_paths)
#     log_fn(f"📊 Found {total_files} filtered Excel file(s) to process")

#     start = time.perf_counter()

#     # Threaded processing
#     max_threads = min(8, total_files)  # Limit threads to avoid excessive disk contention
#     with ThreadPoolExecutor(max_workers=max_threads) as executor:
#         futures = [
#             executor.submit(create_new_excel_mean_time, idx, file, total_files, folder_output, experiment_name)
#             for idx, file in enumerate(file_paths)
#         ]
#         for future in as_completed(futures):
#             try:
#                 result = future.result()
#                 if result:
#                     log_fn(f"✅ {result}")
#             except Exception as exc:
#                 log_fn(f"❌ Error while processing file: {exc}")

#     finish = time.perf_counter()
#     log_fn(f"🎉 All files processed in {round(finish - start, 2)} seconds.")


# def main():
#     # Get folder path input from user
#     folder_input = input('Which folder has your filtered xlsx files? ')
#     if os.path.isdir(folder_input):
#         print('Folder selected: ', folder_input)
#         #folder_files = os.listdir(folder_input)
        
        
#         #for file in folder_files:
#         #    if file.endswith('.xlsx'):
#         #        excel_files.append(file)
#         #    else:
#         #        pass
#     elif folder_input == "":
#         print("You didn't input any path.")
#         return
        
#     else:
#         print('Invalid path input.')
#         return
    
#     folder_output = input('In which folder do you want your excel file to be at: ')

#     if os.path.isdir(folder_output):
#         print('File destination: ', folder_output)
#         #folder_files = os.listdir(folder_output)
        
        
#         #for file in folder_files:
#         #    if file.endswith('.xlsx'):
#         #        excel_files.append(file)
#         #    else:
#         #        pass
#     elif folder_output == "":
#         print("You didn't input any path.")
#         return
        
#     else:
#         print('Invalid path input.')
#         return
        
#     experiment_name = input('What experiment are these files from (footprint, beam, swimming, gridwalk)? ')
    
#     # Get the list of files in the folder (filtering only filtered xlsx files)
#     file_paths = [os.path.join(folder_input, str(p)) for p in os.listdir(folder_input) if p.endswith('filtered.xlsx')]
#     if not file_paths:
#        print(f"No files found in the folder '{folder_input}'.")
#        return
#     total_files = len(file_paths)
#     #indexed_files = [(index, file_path, total_files) for index, file_path in enumerate(file_paths)]
#     for idx, file in enumerate(file_paths):
#         create_new_excel_mean_time(idx, file, total_files, folder_output, experiment_name)
    
    
#     # -------------------------------------------- #            
                
                
                
# if __name__ == '__main__':
#     main()
    