# -*- coding: utf-8 -*-
import os
import math
import random
import glob
import numpy as np
from scipy import misc
from PIL import Image
# from __future__ import print_function
import argparse
import cv2


# 画像の中心を正方形に切り抜き，size X sizeにリサイズ
def crop(img, size):
    w, h = img.size
    assert w >= 100 or h >= 100, "画像サイズが小さすぎます"
    p = (w - h) / 2 if w > h else (h - w) / 2
    box = (p, 0, p + h, h)
    return img.crop(box).resize((size, size))


def lrtb(img):
    lr1 = img.transpose(Image.FLIP_LEFT_RIGHT)
    tb1 = img.transpose(Image.FLIP_TOP_BOTTOM)
    lr2 = tb1.transpose(Image.FLIP_LEFT_RIGHT)
    tb2 = lr1.transpose(Image.FLIP_TOP_BOTTOM)
    return lr1, lr2, tb1, tb2


def rotate(img):
    r90 = img.transpose(Image.ROTATE_90)
    r270 = img.transpose(Image.ROTATE_270)
    return r90, r270


def main():
    parser = argparse.ArgumentParser(description='画像ファイルのデータ拡張')
    parser.add_argument('--outdir', '-o', default='.',
                        help='拡張した画像データの保存場所')
    parser.add_argument('--indir', '-i', default='.',
                        help='元画像のあるディレクトリ')
    parser.add_argument('--size', '-s', type=int, default=100,
                        help='クロップサイズ')
    args = parser.parse_args()

    images = glob.glob(os.path.join(args.indir, "*.jpg"))
    ix = 0
    for f in images:
        print(f)
        img = crop(Image.open(f), 100)
        outimg = args.outdir + "/" + str(ix).zfill(4) + ".jpg"
        img.save(outimg)
        ix += 1
        for i in rotate(img):
            outimg = args.outdir + "/" + str(ix).zfill(4) + ".jpg"
            i.save(outimg)
            ix += 1
        for i in lrtb(img):
            outimg = args.outdir + "/" + str(ix).zfill(4) + ".jpg"
            i.save(outimg)
            ix += 1
            for j in rotate(i):
                outimg = args.outdir + "/" + str(ix).zfill(4) + ".jpg"
                j.save(outimg)
                ix += 1


def cap(i):
    # VideoCaptureクラスのインスタンスを生成
    # 内蔵webカメラ使用時は0を指定
    cap = cv2.VideoCapture(0)

    # 正常に読み込めなかった場合
    if cap.isOpened() is False:
        print("IO Error")
    # 正常に読み込まれた場合
    else:
        # readメソッド
        # 返り値１　ret: フレームの画像が読み込めたか　/  返り値２  frame: 画像の配列（ndarray)
        ret, frame = cap.read()
        image_path = "date/raw_face/"
        if (ret):
            # imwriteメソッド
            # 引数１：画像のパス　引数２：画像を表すndarrayオブジェクト
            # 画像パスの拡張子は.jpgや.pngが使用できる。
            cv2.imwrite(image_path + "image" + str(i) + ".jpg", frame)
        else:
            print("Read Error")

    cap.release()  # カメラデバイスを終了する


if __name__ == '__main__':
    # カメラで写真４５枚ほど撮りたいときは以下のcommentoutはずす
    # for i in range(45):
    #    cap(i)

    main()
