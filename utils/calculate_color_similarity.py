# coding=utf-8
import cv2
import numpy as np

import itertools

def declease_color(val):
    if val < 64:
        return 32
    elif val < 128:
        return 96
    elif val < 196:
        return 160
    else:
        return 224


# 各画素値を減色する
def posterize_image(src_img):
    output_image = src_img.copy()

    height = src_img.shape[0]
    width = src_img.shape[1]

    for h in range(height):
        for w in range(width):
            b = src_img.item(h, w, 0)
            g = src_img.item(h, w, 1)
            r = src_img.item(h, w, 2)

            output_image.itemset((h, w, 0), declease_color(b))
            output_image.itemset((h, w, 1), declease_color(g))
            output_image.itemset((h, w, 2), declease_color(r))

    return output_image


# ２枚の画像から色の類似度を返す
def calculate_color_similarity(posterize_clothe_img, rank_img_path):
    rank_img = cv2.imread("tmp/cropped/" + str(rank_img_path))
    if rank_img is None:
        return 0
    resize_retio = 4
    img1_height = rank_img.shape[0]
    img1_width = rank_img.shape[1]
    resize_img1 = cv2.resize(rank_img, (round(img1_height/resize_retio), round(img1_width/resize_retio)))

    posterize_clothe_img_resize = cv2.resize(posterize_clothe_img, (round(img1_height/resize_retio), round(img1_width/resize_retio)))

    posterize_rank_img = posterize_image(resize_img1)

    hist1 = cv2.calcHist([posterize_rank_img], [0, 1, 2], None, [256, 256, 256], [0, 256, 0, 256, 0, 256])
    hist2 = cv2.calcHist([posterize_clothe_img_resize], [0, 1, 2], None, [256, 256, 256], [0, 256, 0, 256, 0, 256])

    corr = cv2.compareHist(hist1, hist2, cv2.HISTCMP_CORREL)

    return corr
