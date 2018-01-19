# coding=utf-8
import cv2
import numpy as np

# 減色した色をWearのサンプルカラーと照らし合わせて作ったカラーチャート
# たまに合ってない可能性があるw
COLOR_CHART = ["black", "brown", "red", "red", "green", "yellow", "brown", "orange", "green", "green", "yellow",
               "orange", "green", "green", "green", "yellow"
    , "blue", "purple", "purple", "pink", "green", "gray", "pink", "pink", "green", "green", "beige", "orange", "green",
               "green", "green", "yellow"
    , "blue", "purple", "purple", "pink", "blue", "blue", "purple", "pink", "green", "green", "gray", "pink", "green",
               "green", "green", "beige"
    , "blue", "purple", "purple", "pink", "blue", "blue", "purple", "pink", "blue", "blue", "purple", "pink", "blue",
               "blue", "blue", "white"]


# rgb(３チャンネル)を数値に変換
def rgb2bin(red, green, blue):
    red_no = int(red / 64)
    green_no = int(green / 64)
    blue_no = int(blue / 64)
    return 16 * red_no + 4 * green_no + blue_no


# 画像から最も使われている(WEARで定義されている)色を３色リストで返す
def pickMostUsedColor(src_img_path):
    src_img = cv2.imread("./tmp/cropped/" + src_img_path)
    histogram = [0] * 64

    height = src_img.shape[0]
    width = src_img.shape[1]

    step_count = 1
    
    for h in range(0,height,step_count):
        for w in range(0,width,step_count):
            b = src_img.item(h, w, 0)
            g = src_img.item(h, w, 1)
            r = src_img.item(h, w, 2)
            bin = int(rgb2bin(b, g, r))
            histogram[bin] += 1

    tmp_arr = np.array(histogram)
    sorted_histgram = tmp_arr.argsort()[::-1]
    first_index = sorted_histgram[0]
    second_index = sorted_histgram[1]
    third_index = sorted_histgram[2]
    return {"first_color": COLOR_CHART[first_index], "second_color": COLOR_CHART[second_index],
            "third_color": COLOR_CHART[third_index]}
