# license: unlicense
# author: Falto
# created: June 13th, 2024

from rotational_invariance_pred import pred
from ultralytics import YOLO
from ultralytics.engine.results import Results, Boxes
import numpy as np
import cv2
import os
import math
import sys
from cv2.typing import MatLike

dirname = os.path.dirname(__file__)
assets = os.path.join(dirname, "images")
assets_list = os.listdir(assets)
model_path = os.path.join(dirname, "yolov8s_playing_cards.pt")

def get_xyxy(box:Boxes) -> list:
    ret = [*map(float, box.xyxy[0])]
    
    assert len(ret) == 4
    for i in ret:
        assert i >= 0

    return ret

def show_result(result:Results) -> None:
    """
    Show result. If the user press q key, return 1.
    Otherwise, return 0.
    """
    plot = result.plot()
    plot:np.ndarray

    # Resize plot if it is too big to display
    while plot.shape[0] > 1000 or plot.shape[1] > 1900:
        plot = cv2.resize(plot, (plot.shape[1]//2, plot.shape[0]//2))
    
    
    key = imshow(plot) & 0xFF

    if key == ord("q"):
        return 1

def imshow(im:MatLike) -> int:
    cv2.imshow("imshow", im)
    return cv2.waitKey(0)

def main():
    yolo = YOLO(model_path)

    abspath = os.path.join(assets, "0.jpg")

    im = cv2.imread(abspath)
    
    result = pred(yolo, im)

    show_result(result)

    boxes = result.boxes
    print("boxes.shape=", boxes.shape)

    orig_img = result.orig_img

    writedir = os.path.join(dirname, "crop_images")
    if not os.path.isdir(writedir):
        os.mkdir(writedir)

    i = 0

    for box in boxes:
        xyxy = get_xyxy(box)
        crop_img = orig_img[int(xyxy[1]):math.ceil(xyxy[3]), int(xyxy[0]):math.ceil(xyxy[2])]
        cv2.imwrite(os.path.join(writedir, "%d.jpg"%i), crop_img)
        imshow(crop_img)
        i += 1
        
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()