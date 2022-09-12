import math
import os
from glob import iglob


def repair_dir(subdir, files):
    if "records.txt" not in files: return
    if len(list(map(lambda x: x.endswith(".mp3"), files))) == 0: return
    with open(subdir + "/records.txt", "r") as f:
        for line in f:
            line_split = line.split(" ")
            if len(line_split) != 4 or (line_split[0].isdigit() and int(line_split[0]) > 100) or not line_split[
                0].isdigit(): continue
            try:
                rename(line_split, subdir)
            except Exception:
                pass #xd
            # print(line, end="")


def rename(line_split, subdir):
    line_split[3] = line_split[3][:len(line_split[3]) - 1]

    text_number = get_text_number(int(line_split[0]))
    telegram_id = line_split[1]
    emotion = line_split[2]
    timestamp = line_split[3]
    timestamp = timestamp.replace(":", "_")

    old_file = os.path.join(subdir, line_split[0] + ".mp3")
    new_file = os.path.join(subdir,  "{}+{}+{}+{}.mp3".format(telegram_id, timestamp, emotion, text_number))
    os.rename(old_file, new_file)


def get_text_number(x):  # 0 1 => 1, 2 3 => 2
    return str(math.ceil(float(x + 1) / 2))


def iterate_all_dir(root_dir: str):
    for subdir, dirs, files in os.walk(root_dir):
        repair_dir(subdir, files)


def repair():
    iterate_all_dir(".")


if __name__ == "__main__":
    repair()
