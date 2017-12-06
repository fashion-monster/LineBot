# coding=utf-8
import csv
from utils.calculateColorSimilarity import calculateColorSimilarity


# all_pattern_of_Similarity.csv

def readCsv(csvfile):
    f = open(csvfile, 'r')

    reader = csv.reader(f)
    header = next(reader)

    data = [r for r in reader]

    f.close()
    return data


def writeCsv(csvfile, data_list):
	f = open(csvfile, 'a')

	writer = csv.writer(f, lineterminator='\n')
	for list in data_list:
		writer.writerow(list)

	f.close()


champ_data = readCsv("tools/ranking.csv")
clothe_data = readCsv("clothe_types.csv")
user_list = readCsv("follower.csv")

output_data = []

for clothe in clothe_data:
	for champ in champ_data:
		user_id = clothe[0]
		user_clothe = clothe[1]
		user_clothe_type = clothe[2]
		rank = champ[0]
		for i,item in enumerate(champ[1:]):

			if item != "" and user_clothe_type == "Tops" and i<3:
				ranking_tops = item
				simi = calculateColorSimilarity(ranking_tops, user_clothe)
				output_data.append([user_id, user_clothe, ranking_tops, user_clothe_type, rank, simi])
			elif item != "" and user_clothe_type == "Bottoms" and i==3:
				ranking_bottoms = item
				simi = calculateColorSimilarity(ranking_bottoms, user_clothe)
				output_data.append([user_id, user_clothe, ranking_bottoms, user_clothe_type, rank, simi])

with open('all_pattern_of_Similarity.csv', 'a') as f:
    writer = csv.writer(f, lineterminator='\n') # 改行コード（\n）を指定しておく
    writer.writerows(output_data) # 2次元配列も書き込める
    