import os
import pandas as pd
import time
from multiprocessing import Pool
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor, as_completed

pd.set_option('future.no_silent_downcasting', True)

def create_new_excel_mean_time(idx, file, total_files, output_folder, experiment):
    #index, file, total_files = index_file_total_tuple
    list_path_directories = os.path.normpath(file).split(os.path.sep)
    df_filtered = pd.read_excel(file, sheet_name='Calculated Data', header=None)
    file_id = os.path.basename(file)
    parts = file_id.split("_")
    file_id_split = "_".join(parts[:parts.index("out")]) if "out" in parts else ""

    #file_id_split = file_id.split("_")[0] + "_" + file_id.split("_")[1] + "_" + file_id.split("_")[2]
    averages_id_row = df_filtered.iloc[0]
    #averages_id_row.iloc[0]= "Ids"
    df_av_ids = pd.DataFrame(averages_id_row).T
    df_av_ids.insert(0, "Ids", "Ids")
    average_values = df_filtered.iloc[-1]
    #average_values.iloc[0] = file_id_split
    df_av_values = pd.DataFrame(average_values).T
    df_av_values.insert(0, "Ids", file_id_split)
    if idx==0:
        with pd.ExcelWriter(output_folder+ f'/{experiment.upper()}_Averages_'+list_path_directories[-3]+'_'+list_path_directories[-2]+'.xlsx', engine='openpyxl', mode='w') as writer:
        #This is for Joana --> with pd.ExcelWriter(output_folder+ f'/{experiment.upper()}_Averages_'+list_path_directories[-3]+'_OLD_vS_NEW.xlsx', engine='openpyxl', mode='w') as writer:
            df_av_ids.to_excel(writer, sheet_name='Averages and Time', startrow=0, index=False, header=False)
            df_av_values.to_excel(writer, sheet_name='Averages and Time', startrow=1, index=False, header=None)
    else:
        #This is for Joana --> with pd.ExcelWriter(output_folder+f'/{experiment.upper()}_Averages_'+list_path_directories[-3]+'_OLD_vS_NEW.xlsx', engine='openpyxl', if_sheet_exists="overlay", mode='a') as writer:    
        with pd.ExcelWriter(output_folder+f'/{experiment.upper()}_Averages_'+list_path_directories[-3]+'_'+list_path_directories[-2]+'.xlsx', engine='openpyxl', if_sheet_exists="overlay", mode='a') as writer:
            df_av_values.to_excel(writer, sheet_name='Averages and Time', startrow=idx+1, index=False, header=None)
    


    return f"Added info to Averages Excel from file {idx + 1} of {total_files}: {os.path.basename(file)} info added"




def run(folder_input, folder_output, experiment_name, log_fn=print):
    if os.path.isdir(folder_input):
        log_fn(f'Folder selected: {folder_input}')
        #folder_files = os.listdir(folder_input)
        
        
        #for file in folder_files:
        #    if file.endswith('.xlsx'):
        #        excel_files.append(file)
        #    else:
        #        pass
    elif folder_input == "":
        log_fn("You didn't input any path.")
        return
        
    else:
        log_fn('Invalid path input.')
        return

    if os.path.isdir(folder_output):
        log_fn(f'File destination: {folder_output}')
        #folder_files = os.listdir(folder_output)
        
        
        #for file in folder_files:
        #    if file.endswith('.xlsx'):
        #        excel_files.append(file)
        #    else:
        #        pass
    elif folder_output == "":
        log_fn("You didn't input any path.")
        return
        
    else:
        log_fn('Invalid path input.')
        return
    
    # Get the list of files in the folder (filtering only filtered xlsx files)
    file_paths = [os.path.join(folder_input, str(p)) for p in os.listdir(folder_input) if p.endswith('filtered.xlsx')]
    if not file_paths:
       log_fn(f"No files found in the folder '{folder_input}'.")
       return
    total_files = len(file_paths)
    #indexed_files = [(index, file_path, total_files) for index, file_path in enumerate(file_paths)]
    for idx, file in enumerate(file_paths):
        create_new_excel_mean_time(idx, file, total_files, folder_output, experiment_name)
    
    
    # -------------------------------------------- #            


def main():
    # Get folder path input from user
    folder_input = input('Which folder has your filtered xlsx files? ')
    if os.path.isdir(folder_input):
        print('Folder selected: ', folder_input)
        #folder_files = os.listdir(folder_input)
        
        
        #for file in folder_files:
        #    if file.endswith('.xlsx'):
        #        excel_files.append(file)
        #    else:
        #        pass
    elif folder_input == "":
        print("You didn't input any path.")
        return
        
    else:
        print('Invalid path input.')
        return
    
    folder_output = input('In which folder do you want your excel file to be at: ')

    if os.path.isdir(folder_output):
        print('File destination: ', folder_output)
        #folder_files = os.listdir(folder_output)
        
        
        #for file in folder_files:
        #    if file.endswith('.xlsx'):
        #        excel_files.append(file)
        #    else:
        #        pass
    elif folder_output == "":
        print("You didn't input any path.")
        return
        
    else:
        print('Invalid path input.')
        return
        
    experiment_name = input('What experiment are these files from (footprint, beam, swimming, gridwalk)? ')
    
    # Get the list of files in the folder (filtering only filtered xlsx files)
    file_paths = [os.path.join(folder_input, str(p)) for p in os.listdir(folder_input) if p.endswith('filtered.xlsx')]
    if not file_paths:
       print(f"No files found in the folder '{folder_input}'.")
       return
    total_files = len(file_paths)
    #indexed_files = [(index, file_path, total_files) for index, file_path in enumerate(file_paths)]
    for idx, file in enumerate(file_paths):
        create_new_excel_mean_time(idx, file, total_files, folder_output, experiment_name)
    
    
    # -------------------------------------------- #            
                
                
                
if __name__ == '__main__':
    main()
    