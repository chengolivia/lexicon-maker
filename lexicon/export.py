import pandas as pd

def export_to_excel(vocab_list, file_name_no_ext):
    df = pd.DataFrame.from_dict(vocab_list, "index")
    file_name = f"{file_name_no_ext}.xlsx"
    df.to_excel(file_name)
    print(f"Saved to {file_name}")

def export_to_txt(vocab_list, file_name_no_ext):
    file_name = f"{file_name_no_ext}.txt"
    with open(file_name, 'a') as output:
        for key, value in vocab_list.items():
            output.write('%s:%s\n' % (key, value))
    print(f"Saved to {file_name}")