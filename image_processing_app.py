# coding=utf-8
from flask import Flask, request, Response
from utils.calculate_color_similarity import calculate_color_similarity
from utils.calculate_color_similarity import posterize_image

import json
import csv
import time
import cv2
import numpy
import requests
from models.state import ActionState

app = Flask(__name__)


@app.route("/similarity", methods=['POST'])
def similarity():
    """
    画像名から２枚の画像の類似度を返す
    """
    f = open('all_pattern_of_Similarity2.csv', 'a')
    writer = csv.writer(f, lineterminator='\n')

    ranking_data = read_csv("tools/ranking.csv")

    user_id = request.form["user_id"]
    user_cloth = request.form["img_path"]
    user_cloth_type = request.form["cloth_type"]

    user_cloth_img = cv2.imread("tmp/cropped/" + str(user_cloth))
    posterize_user_cloth_image = posterize_image(user_cloth_img)

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
    header = {'content-type': 'application/json'}
    requests.post(url='http://127.0.0.1:5001/img_process_queue',header=header, data=(json.dumps({"action": "similarity"})))
    return


def read_csv(csvfile):
    f = open(csvfile, 'r')

    reader = csv.reader(f)
    header = next(reader)

    data = [r for r in reader]

    f.close()
    return data


if __name__ == '__main__':
    app.debug = True
    app.run(port=8050)
