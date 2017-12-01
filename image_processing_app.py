from flask import Flask, request
from utils.calculateColorSimilarity import calculateColorSimilarity
from utils.pickMostUsedColor import pickMostUsedColor
from utils.resizeImage import resizeImage

app = Flask(__name__)

"""
画像をリサイズした結果を ./tmp/dst/に保存する
"""
@app.route("/resize", methods=['PUT'])
def resize():
    image_name = request.args.get("image_name")
    resizeImage(image_name)

"""
画像名から最も使われいる色を多い順に三色をリストで返す

ex
["red", "blue", "yellow"]
"""
@app.route("/pick", methods=['PUT'])
def pick():
    image_name = request.args.get("image_name")
    color_list = pickMostUsedColor(image_name)
    return color_list

"""
画像名から２枚の画像の類似度を返す
"""
@app.route("/similarity", methods=['PUT'])
def similarity():
    image1_name = request.args.get("image1_name")
    image2_name = request.args.get("image2_name")
    simi = calculateColorSimilarity(image1_name, image2_name)
    return simi


if __name__ == '__main__':
    app.run(port=8050)