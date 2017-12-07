# coding=utf-8
from flask import Flask, request, make_response
from utils.calculateColorSimilarity import calculateColorSimilarity
from utils.pickMostUsedColor import pickMostUsedColor
from utils.imageResize import resizeImage
import json
import csv

app = Flask(__name__)


@app.route("/resize", methods=['POST'])
def resize():
    """
    画像をリサイズした結果を ./tmp/dst/に保存する
    """
    image_name = request.form["image_name"]
    if not resizeImage(image_name):
        response = make_response()
        response.data = json.dumps({"resize": "fault"})
        response.headers["Content-Type"] = "application/json"
        return response
    else:
        response = make_response()
        response.data = json.dumps({"resize": "success"})
        response.headers["Content-Type"] = "application/json"
        return response


@app.route("/pick", methods=['POST'])
def pick():
    """
    画像名から最も使われいる色を多い順に三色をjsonで返す

    ex
    {
    "red", "blue", "yellow"}
    """
    image_name = request.form["image_name"]
    color_dict = pickMostUsedColor(image_name)
    response = make_response()
    response.data = json.dumps(color_dict)
    response.headers["Content-Type"] = "application/json"
    return response


@app.route("/similarity", methods=['POST'])
def similarity():
    """
    画像名から２枚の画像の類似度を返す
    """
    f = open('all_pattern_of_Similarity.csv2', 'a')
    writer = csv.writer(f, lineterminator='\n')

    ranking_data = readCsv("tools/ranking.csv")

    for r in ranking_data:
        user_id = request.form["user_id"]
        user_clothe = request.form["user_clothe"]
        user_clothe_type = request.form["user_clothe_type"]
        year = r[0]
        month = r[1]
        rank = r[2]
        for i, item in enumerate(r[3:]):
            if item != "" and user_clothe_type == "Tops" and i < 3:
                ranking_tops = item
                simi = calculateColorSimilarity(ranking_tops, user_clothe)
                writer.writerow([user_id, user_clothe, ranking_tops, user_clothe_type, year, month, rank, simi])
            elif item != "" and user_clothe_type == "Bottoms" and i == 3:
                ranking_bottoms = item
                simi = calculateColorSimilarity(ranking_bottoms, user_clothe)
                writer.writerow([user_id, user_clothe, ranking_bottoms, user_clothe_type, year, month, rank, simi])

    f.close()
    response = make_response()
    response.data = json.dumps({"write_csv": "done"})
    response.headers["Content-Type"] = "application/json"
    return response


def readCsv(csvfile):
    f = open(csvfile, 'r')

    reader = csv.reader(f)
    header = next(reader)

    data = [r for r in reader]

    f.close()
    return data


if __name__ == '__main__':
    app.debug = True
    app.run(port=8050)
