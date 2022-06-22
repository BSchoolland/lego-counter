import os
import sys
import cv2
from PIL import Image
#
sys.setrecursionlimit(5000)
def groupPixels(Map,H,W):
    Map[H][W] = '0'
    global Pixels_in_piece
    Pixels_in_piece += 1
    if H == 0 or H == len(Map)-1 or W == 0 or W == len(Map[H])-1:
        global not_on_edge
        not_on_edge = False
        return
    if Map[H+1][W] == '#' or Map[H+1][W] == '?':
        groupPixels(Map, H+1, W)
    if Map[H-1][W] == '#' or Map[H-1][W] == '?':
        groupPixels(Map, H-1, W)
    if Map[H][W-1] == '#' or Map[H][W-1] == '?':
        groupPixels(Map, H, W-1)
    if Map[H][W+1] == '#' or Map[H][W+1] == '?':
        groupPixels(Map,H,W+1)
cwd = os.getcwd()
tuning_input = 1
threshhold = 50




cap = cv2.VideoCapture(1)
if not cap.isOpened():
    print("Cannot open webcam")
print("camera ready")
while True:
    while True:
        ret, frame = cap.read()
        frame = cv2.resize(frame, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
        cv2.imshow('Input', frame)


        if cv2.waitKey(1) & 0xFF == ord(' '):
            break
    lego_num_list = []
    lego_groups_num_list = []
    normal_pixel_list = []
    edgePieces = 0
    for n in range(3):
        ret, frame = cap.read()
        frame = cv2.resize(frame, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
        cv2.imshow('Input', frame)
        cv2.imwrite("image.png", frame)

        img = cwd + '/image.png'
        im = cv2.imread(img)
        img = Image.open(img)
        screenW, screenH = im.shape[1] - 1, im.shape[0] - 1

        skip = 1
        black_pixels = 0
        white_pixels = 0
        red_pixels = 0

        mostOff = [0, 0, 0]
        mostOff2 = [255, 255, 255]
        Map = []
        for h in range(int(screenH / skip)):
            Line = []
            row = []
            for w in range(int(screenW / skip)):
                R, G, B = (img.getpixel((w * skip, h * skip)))
                if R < threshhold and G < threshhold and B < threshhold:
                    if R+G+B > mostOff[0] + mostOff[1] + mostOff[2]:
                        mostOff = [R,G,B]
                    black_pixels += 1

                    row.append("#")

                elif R < threshhold+25 and G < threshhold+25 and B < threshhold+25:
                    if R+G+B > mostOff[0] + mostOff[1] + mostOff[2]:
                        mostOff = [R,G,B]

                    row.append("?")
                else:
                    red_pixels += 1

                    row.append(".")
            Map.append(row)
        """for H in range(len(Map)):
            if H//3 == H/3:
                for W in range(len(Map[H])):
                    if W//3 == W/3:
                        print(Map[H][W],"   ",end='')
                print()
                """
        legos = 0
        leastPixels= 99999999999
        list_of_pixels = []

        for H in range(len(Map)):
            for W in range(len(row)):
                if Map[H][W] == '#':
                    Pixels_in_piece = 0
                    not_on_edge = True
                    groupPixels(Map, H, W)
                    if not_on_edge:
                        list_of_pixels.append(Pixels_in_piece)
                        if Pixels_in_piece < leastPixels:
                            leastPixels = Pixels_in_piece
                    else:
                        edgePieces += 1
        Normal_pixel_calc = 999999999999
        Normal_pixel = 0
        for num_pixels in list_of_pixels:
            new_normal_pixel = 0
            for num_pixels2 in list_of_pixels:
                new_normal_pixel += (abs(num_pixels2-num_pixels))
            if new_normal_pixel<Normal_pixel_calc:
                Normal_pixel = num_pixels
                Normal_pixel_calc = new_normal_pixel
        legos_by_least = 0
        for num_pixels in list_of_pixels:
            ratio = round(num_pixels/leastPixels)
            legos_by_least = legos_by_least + ratio
        legos_by_normal = 0

        for num_pixels in list_of_pixels:
            ratio = round(num_pixels/Normal_pixel)
            legos_by_normal = legos_by_normal + ratio
        for num_pixels in list_of_pixels:
            legos +=1

        lego_num_list.append(legos_by_normal)
        lego_groups_num_list.append(legos)
        normal_pixel_list.append(Normal_pixel)
    average = 0
    for legos in lego_num_list:
        average += legos
    average/=len(lego_num_list)
    avg_groups = 0
    for n in lego_groups_num_list:
        avg_groups += n
    avg_groups /= len(lego_groups_num_list)

    avg_normal_pixel = 0
    for n in normal_pixel_list:
        avg_normal_pixel += n
    avg_normal_pixel /= len(normal_pixel_list)
    print("\n")
    print("Lego groups:", avg_groups)
    # print("least_pixel", leastPixels)
    # print("Legos by least:", legos_by_least)

    print("normal_pixel", avg_normal_pixel)
    print("legos:", average)
    if average > avg_groups / 0.4:
        print("CRITICAL group warning!!! (move the legos and try again)")
    elif average > avg_groups / 0.6:
        print("group warning! (number may be off by a slight amount)")
    elif average > avg_groups / 0.9:
        print("slight group warning")
    if edgePieces > 0:
        print("CRITICAL warning!", edgePieces, "objects on edge")