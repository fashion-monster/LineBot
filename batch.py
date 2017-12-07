# coding=utf-8
import csv
from utils.calculateColorSimilarity import calculateColorSimilarity


# all_pattern_of_Similarity.csv

def read_csv(csv_file):
    f = open(csv_file, 'r')

    reader = csv.reader(f)
    header = next(reader)

    data = [r for r in reader]

    f.close()
    return data


def write_csv(csv_file, data_list):
    f = open(csv_file, 'a')

    writer = csv.writer(f, lineterminator='\n')
    for list in data_list:
        writer.writerow(list)

    f.close()


ranking_data = read_csv("tools/ranking.csv")
clothe_data = read_csv("clothe_types.csv")
user_list = read_csv("follower.csv")

output_data = []

for clothe in clothe_data:
    for r in ranking_data:
        user_id = clothe[0]
        user_clothe = clothe[1]
        user_clothe_type = clothe[2]
        year = r[0]
        month = r[1]
        rank = r[2]
        for i, item in enumerate(r[1:]):

            if item != "" and user_clothe_type == "Tops" and i < 3:
                ranking_tops = item
                simi = calculateColorSimilarity(ranking_tops, user_clothe)
                output_data.append([user_id, user_clothe, ranking_tops, user_clothe_type, year, month, rank, simi])
            elif item != "" and user_clothe_type == "Bottoms" and i == 3:
                ranking_bottoms = item
                simi = calculateColorSimilarity(ranking_bottoms, user_clothe)
                output_data.append([user_id, user_clothe, ranking_bottoms, user_clothe_type, year, month, rank, simi])

with open('all_pattern_of_Similarity.csv', 'a') as f:
    writer = csv.writer(f, lineterminator='\n')  # 改行コード（\n）を指定しておく
    writer.writerows(output_data)  # 2次元配列も書き込める
