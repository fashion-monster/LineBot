# coding=utf-8
import csv
import json

import cv2
import requests
from flask import Flask, request

from utils.calculate_color_similarity import calculate_color_similarity
from utils.calculate_color_similarity import posterize_image

app = Flask(__name__)


@app.route("/similarity", methods=['POST'])
def similarity():
    """
    画像名から２枚の画像の類似度を返す
    """
    f = open('all_pattern_of_Similarity2.csv', 'a')
    writer = csv.writer(f, lineterminator='\n')

    ranking_data = read_csv("tools/ranking.csv")

    res_json = json.loads(request.data.decode("UTF-8"))

    user_id = res_json["user_id"]
    user_cloth = res_json["img_path"]
    user_cloth_type = res_json["cloth_type"]

    user_cloth_img = cv2.imread("tmp/cropped/" + str(user_cloth))
    posterize_user_cloth_image = posterize_image(user_cloth_img)

    next(ranking_data)

    for r in ranking_data:

        year = r[0]
        month = r[1]
        rank = r[2]
        for i, item in enumerate(r[3:]):
            if item != "" and user_cloth_type == "Tops" and i < 3:
                ranking_tops = item
                simi = calculate_color_similarity(posterize_user_cloth_image, ranking_tops)
                writer.writerow([user_id, user_cloth, ranking_tops, user_cloth_type, year, month, rank, simi])
            elif item != "" and user_cloth_type == "Bottoms" and i == 3:
                ranking_bottoms = item
                simi = calculate_color_similarity(posterize_user_cloth_image, ranking_bottoms)
                writer.writerow([user_id, user_cloth, ranking_bottoms, user_cloth_type, year, month, rank, simi])

    f.close()

    header = {'Content-Type':'application/json'}
    requests.post(url='http://127.0.0.1:5001/',
                  headers=header,
                  data=(json.dumps({"action": "similarity"})))
    
    return "ok"


def read_csv(csv_file):
    f = open(csv_file, 'r')
    reader = csv.reader(f)
    data = [r for r in reader]
    f.close()
    return data


if __name__ == '__main__':
    app.debug = True
    app.run(port=8050)