import pandas as pd
from openpyxl import load_workbook
import os
from datetime import datetime

# All possible target labels in Excel
RAW_STRINGS = [
    "Stride length left front average in cm:",
    "Stride length right front average in cm:",
    "Stride length left hind average in cm:",
    "Stride length right hind average in cm:",
    "Overlap left average in cm:",
    "Overlap Right average in cm:",
    "Stride Width Front(L) average in cm:",
    "Stride Width Front(R) average in cm:",
    "Stride Width Hind(L) average in cm:",
    "Stride Width Hind(R) average in cm:"
]

# Map specific labels to unified output names
RENAME_MAP = {
    "Stride Width Front(L) average in cm:": "Stride Width Front average in cm:",
    "Stride Width Front(R) average in cm:": "Stride Width Front average in cm:",
    "Stride Width Hind(L) average in cm:": "Stride Width Hind average in cm:",
    "Stride Width Hind(R) average in cm:": "Stride Width Hind average in cm:"
}

def find_table_data(workbook_path):
    wb = load_workbook(workbook_path, data_only=True)
    result_data = []

    for sheet_name in wb.sheetnames:
        ws = wb[sheet_name]
        for row in ws.iter_rows():
            for cell in row:
                if isinstance(cell.value, str) and cell.value.strip().startswith("Table ID"):
                    # Extract clean Table ID
                    table_id = cell.value.strip().replace("Table ID:", "").strip()
                    table_data = {"Table ID": table_id}

                    col_index = cell.column
                    row_index = cell.row

                    for r in range(row_index + 1, ws.max_row + 1):
                        label_cell = ws.cell(row=r, column=col_index)
                        value_cell = ws.cell(row=r, column=col_index + 1)

                        label = label_cell.value
                        value = value_cell.value

                        if label in RAW_STRINGS:
                            #This line uses the .get() method of Python dictionaries. It does the following:
                            #Checks if the current label is a key in the RENAME_MAP dictionary.
                            #If it is, return the corresponding renamed label.
                            #If it isn’t, return the original label as-is.
                            output_label = RENAME_MAP.get(label, label) 
                            table_data[output_label] = value

                    result_data.append(table_data)

    return result_data


#Info

# table_data = {
#     "Table ID": "2199_1R_T1_4W",
#     "Stride length left front average in cm:": 7.416,
#     "Stride Width Front average in cm:": 1.45,
#     ...
# }

# This is a single row of data, where:
# keys = column names (like headers in Excel)
# values = values under each column



# result_data = [
#     table_data_1,
#     table_data_2,
#     ...
# ]

#Each key (from the dictionaries) becomes a column.
#Each dictionary becomes a row.
#The dictionary’s key-value pairs are aligned horizontally in Excel or when printed.




# def save_to_excel(data, base_output_dir):
#     # Better formatted timestamp
#     timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
#     output_file = os.path.join(base_output_dir, f"MFrame_clean_output_{timestamp}.xlsx")
#     df = pd.DataFrame(data)
#     df.to_excel(output_file, index=False)
#     return output_file


# 🚀 This is the entrypoint callable from GUI
def run(input_file):
    #This gets the path of the excel file in main app and I only want the directory. Change below!
    if not os.path.isfile(input_file):
        raise FileNotFoundError(f"File not found: {input_file}")

    data = find_table_data(input_file)

    if not data:
        raise ValueError("No 'Table ID' entries found in the provided file.")

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    output_file = os.path.join(os.path.dirname(input_file), f"MFrame_clean_output_{timestamp}.xlsx")
    df = pd.DataFrame(data)
    df.to_excel(output_file, index=False)
    return output_file

# Keep CLI usability for testing
if __name__ == "__main__":
    input_file = input("Enter the path to the Excel file: ").strip()
    try:
        output_path = run(input_file)
        print(f"✅ Extracted data has been written to: {output_path}")
    except Exception as e:
        print(f"❌ Error: {e}")
