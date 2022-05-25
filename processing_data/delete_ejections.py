import math

import pandas as pd
from Extracting_features import get_pretty_dataframe
from Extracting_features import save_to_csv_file
def delete_ejections(df: pd.DataFrame):
    columns = df.columns[1:]
    q25 = []
    q75 = []
    index_25 = math.floor(0.15 * df.shape[0])
    index_75 = math.floor(0.85 * df.shape[0])

    for column in columns:
        list_of_single_column = df[column].tolist()
        q25.append(sorted(list_of_single_column)[index_25])
        q75.append(sorted(list_of_single_column)[index_75])

    good_rows = []

    for index, row in df.iterrows():
        ok = True
        for index, param in enumerate(row[1:]):
            if param > q75[index] + 1.5*(q75[index]-q25[index]) or param < q25[index] - 1.5*(q75[index]-q25[index]):
                ok = False
        if ok:
            good_rows.append(row)
        print(row)

    return pd.DataFrame(data=good_rows)


if __name__ == "__main__":
    df = get_pretty_dataframe(file_name="Emobase_extracted_features")

    save_to_csv_file(delete_ejections(df), file_name="without_ejections")