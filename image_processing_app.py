# coding=utf-8
from flask import Flask, request, make_response
from utils.calculateColorSimilarity import calculateColorSimilarity
from utils.pickMostUsedColor import pickMostUsedColor
from utils.imageResize import resizeImage
import json

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
    image1_name = request.form["image1_name"]
    image2_name = request.form["image2_name"]
    simi = calculateColorSimilarity(image1_name, image2_name)
    response = make_response()
    response.data = json.dumps({"similarity": simi})
    response.headers["Content-Type"] = "application/json"
    return response


if __name__ == '__main__':
    app.debug = True
    app.run(port=8050)
