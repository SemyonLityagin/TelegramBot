import os
from glob import iglob

import opensmile
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
    y.insert(0, "user_id", int(user_id))
    y.insert(0, "emotions", emotions)
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
            frames.append(y)
    result = pd.concat(frames)

    return result


# Пример получения
extract_features_from_all_users_folders(".").to_csv(
    path_or_buf="./csv_files/{}.csv".format("Emobase_extracted_features"), index=True)
