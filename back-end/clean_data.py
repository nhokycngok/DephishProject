
#importing pandas package
import pandas as pd
  
def remove_duplicate_row_in_csv_file(input_file_name, output_file_name):
    try:
        data = pd.read_csv(input_file_name)                        
        data = pd.DataFrame.drop_duplicates(data)
        data = data.drop_duplicates()
        data.to_csv(output_file_name, index=False)
        return 1
    except:
        return "An exception occurred"

print(remove_duplicate_row_in_csv_file("csv/data.csv", "csv/newdata.csv"))
