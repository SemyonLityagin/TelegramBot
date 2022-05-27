import os
from glob import iglob

import opensmile
import pandas
import pandas as pd


def get_feature_extractor():
    # Выбираем извлекаемые параметры
    return opensmile.Smile(
        feature_set=opensmile.FeatureSet.emobase,  # Используемый набор фич.
        feature_level=opensmile.FeatureLevel.Functionals,
        # low-Level descriptors или Functionals (statistical, polynomial regression, and transformations). Подробнее:
        # https://mediatum.ub.tum.de/doc/1082431/1082431.pdf
    )


def get_features(file_name: str, feature_extractor):
    """
    На вход получает путь к файлу На выход выдаёт dataframe из одной строки Имя файла содержит в себе данные,
    перечисленные через + (Пример: ./1070122155/1070122155+09_02_2022_19_32_43+покинутость_беспомощность_грусть+1.mp3
    ) Эти данные добавляются в датафрэйм, полученный от обработки аудиофайла библиотекой opnesmile.
    """
    user_id, date, emotions, text_number = file_name.split("/")[2].split("+")
    y = feature_extractor.process_file(file_name)

    y.insert(0, "emotions", emotions)

    y.insert(0, "user_id", int(user_id))
    y.insert(0, "text_number", text_number.split(".")[0])

    return y


def extract_features_from_all_users_folders(root_dir: str):
    """
    Функция итерируется по папкам пользователей и запускает извлечение фич для каждой из найденных аудиозаписей.
    :param root_dir: Путь до папки с базой данных. Пример: /home/tyoma/PycharmProjects/TelegramBot или если код из
    папки с проектом rootdir = '.'
    :return: Dataframe, с колонками: file, start, end, text_number, emotions, date,
    user_id, ...(features).
    """
    root_dir += "/**/*"
    file_list = [f for f in iglob(root_dir, recursive=True) if os.path.isfile(f)]
    frames = []
    fe = get_feature_extractor()
    for file in file_list:
        if file.endswith(".mp3"):
            print(file)
            y = get_features(str(file), feature_extractor=fe)
            for emotion in y["emotions"].array[0].split("_"):
                row = y.copy()
                row["emotions"] = emotion
                frames.append(row)



    result = pd.concat(frames)
    return result

def extract_features_from_all_users_folders_old(root_dir: str):
    """
    Функция итерируется по папкам пользователей и запускает извлечение фич для каждой из найденных аудиозаписей.
    :param root_dir: Путь до папки с базой данных. Пример: /home/tyoma/PycharmProjects/TelegramBot или если код из
    папки с проектом rootdir = '.'
    :return: Dataframe, с колонками: file, start, end, text_number, emotions, date,
    user_id, ...(features).
    """
    root_dir += "/**/*"
    file_list = [f for f in iglob(root_dir, recursive=True) if os.path.isfile(f)]
    frames = []
    fe = get_feature_extractor()
    couner = 0
    for file in file_list:
        if file.endswith(".mp3"):
            print(file)
            y = get_features(str(file), feature_extractor=fe)
            frames.append(y)





    result = pd.concat(frames)
    return result


def get_pretty_dataframe(file_name = "Emobase_extracted_features") -> pandas.DataFrame:
    df = pd.read_csv("./csv_files/{}.csv".format(file_name))
    df = df.iloc[:, 5:]  # Убрали первые 5 колонок
    return df


def save_to_csv_file(df, file_path="./csv_files/{}.csv", file_name="Emobase_extracted_features"):
    df.to_csv(
        path_or_buf=(file_path).format("%s" % file_name), index=True)


def change_dataframe_one_emotion_per_row(df):
    df = df.reset_index()  # make sure indexes pair with number of rows
    for index, row in df.iterrows():
        print(row['c1'], row['c2'])



if "__main__" == __name__:
    # Пример получения
    save_to_csv_file(extract_features_from_all_users_folders_old(".."), file_name="old_table")
    save_to_csv_file(get_pretty_dataframe(file_name="old_table"), file_name="old_table_pretty")
