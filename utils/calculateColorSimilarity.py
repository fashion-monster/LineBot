# coding=utf-8
import cv2
import numpy as np

import itertools


def decleaseColor(val):
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

            output_image.itemset((h, w, 0), decleaseColor(b))
            output_image.itemset((h, w, 1), decleaseColor(g))
            output_image.itemset((h, w, 2), decleaseColor(r))

    return output_image


# ２枚の画像から色の類似度を返す
def calculateColorSimilarity(posterize_clothe_img, rank_img_path):
    rank_img = cv2.imread("tmp/cropped/" + str(rank_img_path))
    print("tmp/cropped/" + str(rank_img_path))
    if rank_img is None:
        return 0

    posterize_rank_img = posterize_image(rank_img)

    hist1 = cv2.calcHist([posterize_rank_img], [0, 1, 2], None, [256, 256, 256], [0, 256, 0, 256, 0, 256])
    hist2 = cv2.calcHist([posterize_clothe_img], [0, 1, 2], None, [256, 256, 256], [0, 256, 0, 256, 0, 256])

    corr = cv2.compareHist(hist1, hist2, cv2.HISTCMP_CORREL)

    print(corr)
    return corr
