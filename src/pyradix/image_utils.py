import numpy as np
import cv2

def create_arrows_sub(src2, moves2, word):
    frames = []
    currentImg = np.zeros((560, 560, 3), np.uint8)
    moves = moves2.copy()
    lastPoint = moves[0]
    moves = moves[1:len(moves)-1]
    src = src2.copy()
    for move in moves:
        arrowedLine = cv2.arrowedLine(src, (lastPoint[1]*140+70, lastPoint[0]*140+70), (move[1]*140+70, move[0]*140+70), (0, 255, 0), 5)
        currentImg = cv2.addWeighted(src, 0, arrowedLine, 1, 0)
        lastPoint = move
    wordlen = word[0:len(moves2)-1]
    font = cv2.FONT_HERSHEY_SIMPLEX
    text = wordlen
    fontsize = 2
    textsize = cv2.getTextSize(text, font, fontsize, 2)[0]
    textX = int((currentImg.shape[1] - textsize[0]) / 2)
    textY = int((currentImg.shape[0] + textsize[1]) / 2)
    cv2.putText(currentImg, text, (textX, textY ), font, fontsize, (0, 0, 0), 2)
    frames.append(currentImg)
    #if(len(moves)>1):
        #frames = frames+create_arrows_sub(src2, moves2[0:len(moves2)-1], word)
    return currentImg

def create_arrows(src, moves, word):
    var = create_arrows_sub(src, moves, word)
    return (var, word)

def create_img(letter):
    image = np.ones((140, 140, 3), np.uint8)
    image[:] = (255, 255, 255)
    font = cv2.FONT_HERSHEY_SIMPLEX
    text = letter
    fontsize = 4
    textsize = cv2.getTextSize(text, font, fontsize, 2)[0]
    textX = int((image.shape[1] - textsize[0]) / 2)
    textY = int((image.shape[0] + textsize[1]) / 2)
    cv2.putText(image, text, (textX, textY ), font, fontsize, (0, 0, 0), 2)
    return image

def create_imgs(text):
    u = 0
    fullimg = np.ones((560,560,3), np.uint8)
    for i in range(4):
        tempimg = np.ones((140, 560, 3), np.uint8)
        for z in range (4):
            img = create_img(text[u:u+1])
            tempimg[:,z*140:z*140+140] = img
            u+=1
        fullimg[i*140:i*140+140, :] = tempimg
    return fullimg