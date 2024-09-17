import pandas as pd

def combine_comments(csv_files):
    combined_df = pd.concat(csv_files, ignore_index=True)
    return combined_df
