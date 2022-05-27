from sklearn.preprocessing import MinMaxScaler

from processing_data.Extracting_features import get_pretty_dataframe, save_to_csv_file
import pandas as pd
from sklearn import preprocessing

def normalize_csv(file_name="Emobase_extracted_features"):
    df = pd.read_csv("./csv_files/{}.csv".format(file_name))
    df[df.columns[2:]] = df[df.columns[2:]].apply(lambda x: (x - x.min()) / (x.max() - x.min()))
    save_to_csv_file(df, file_name="normalized_one_emotion_per_row")

if __name__ == "__main__":
    normalize_csv("without_ejections")