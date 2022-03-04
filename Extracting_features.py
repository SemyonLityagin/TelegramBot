import opensmile

# Выбрали параметры, которые хотим извлекать.
import pandas as pd

smile = opensmile.Smile(
    feature_set=opensmile.FeatureSet.emobase,
    feature_level=opensmile.FeatureLevel.Functionals,
)


# Выбираем аудиозапись
def get_features(file_name: str):
    user_id, date, emotions, text_number = file_name.split("/")[2].split("+")
    y = smile.process_file(file_name)
    y.insert(0, "user_id", int(user_id))
    y.insert(0, "date", date)
    y.insert(0, "emotions", emotions)
    y.insert(0, "text_number", text_number.split(".")[0])
    return y


# compression_opts = dict(folder_name='out.csv')



# Итерируемся по пользователям
import os
from glob import iglob

rootdir_glob = './**/*'  # Note the added asterisks
# This will return absolute paths
file_list = [f for f in iglob(rootdir_glob, recursive=True) if os.path.isfile(f)]
counter = 100
frames = []
for file in file_list:
    if file.endswith(".mp3"):
        print(file)
        y = get_features(str(file))
        frames.append(y)
        counter -= 1
        if counter == 0:
            break
result = pd.concat(frames)
print(result)

result.to_csv(path_or_buf="./csv_files/{}.csv".format("Emobase_extracted_features"), index=True)