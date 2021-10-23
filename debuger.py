import sys
import cv2
import numpy as np

if __name__ == "__main__":
    f = open("solution.txt", "r")
    solution = f.read().split("\n")

    FILE = sys.argv[1]
    height = int(sys.argv[2])
    width = int(sys.argv[3])

    img    = cv2.imread(FILE)

    PIECE_SIZE = img.shape[0] // height

    pieces = [ piece for piece in np.reshape([np.hsplit(h, width) for h in np.vsplit(img.astype(np.int16), height)],(-1, PIECE_SIZE, PIECE_SIZE, 3))]

    n = int(solution[1])
    print(n)

    h = -1
    for i in range(n):
        h+=3
        print(h)
        posi = solution[h]
        x = int(posi[0], 16)
        y = int(posi[1], 16)
        t = int(solution[h+1])
        acts = solution[h+2]
        for act in acts:
            if act=="R":
                if x==width-1:
                    tmp = pieces[y*width + x]
                    pieces[y*width + x] = pieces[y*width]
                    pieces[y*width] = tmp
                    x=0
                else:
                    tmp = pieces[y*width + x]
                    pieces[y*width + x] = pieces[y*width + x + 1]
                    pieces[y*width + x + 1] = tmp
                    x+=1
            elif act=="U":
                if y==0:
                    tmp = pieces[y*width + x]
                    pieces[y*width + x] = pieces[(height-1)*width + x]
                    pieces[(height-1)*width + x] = tmp
                    y=height-1
                else:
                    tmp = pieces[y*width + x]
                    pieces[y*width + x] = pieces[(y-1)*width + x]
                    pieces[(y-1)*width + x] = tmp
                    y-=1
            elif act=="L":
                if x==0:
                    tmp = pieces[y*width + x]
                    pieces[y*width + x] = pieces[y*width + width - 1]
                    pieces[y*width + width - 1] = tmp
                    x=width-1
                else:
                    tmp = pieces[y*width + x]
                    pieces[y*width + x] = pieces[y*width + x - 1]
                    pieces[y*width + x - 1] = tmp
                    x-=1
            elif act=="D":
                if y==height-1:
                    tmp = pieces[y*width + x]
                    pieces[y*width + x] = pieces[x]
                    pieces[x] = tmp
                    y=0
                else:
                    tmp = pieces[y*width + x]
                    pieces[y*width + x] = pieces[(y+1)*width + x]
                    pieces[(y+1)*width + x] = tmp
                    y+=1

    for i in range(len(solution[0])):
        r = (4-int(solution[0][i]))%4
        pieces[i] = np.rot90(pieces[i],r)

    pic = np.zeros(img.shape)
    for y in range(height):
        for x in range(width):
            pic[y*PIECE_SIZE:(y+1)*PIECE_SIZE, x*PIECE_SIZE:(x+1)*PIECE_SIZE] = pieces[y*width+x]
    cv2.imwrite("debug.png", pic)

def debug(height, width):
    f = open("solution.txt", "r")
    solution = f.read().split("\n")

    img    = cv2.imread("problem.ppm")

    PIECE_SIZE = img.shape[0] // height

    pieces = [ piece for piece in np.reshape([np.hsplit(h, width) for h in np.vsplit(img.astype(np.int16), height)],(-1, PIECE_SIZE, PIECE_SIZE, 3))]

    n = int(solution[1])
    print(n)

    h = -1
    for i in range(n):
        h+=3
        print(h)
        posi = solution[h]
        x = int(posi[0], 16)
        y = int(posi[1], 16)
        t = int(solution[h+1])
        acts = solution[h+2]
        for act in acts:
            if act=="R":
                if x==width-1:
                    tmp = pieces[y*width + x]
                    pieces[y*width + x] = pieces[y*width]
                    pieces[y*width] = tmp
                    x=0
                else:
                    tmp = pieces[y*width + x]
                    pieces[y*width + x] = pieces[y*width + x + 1]
                    pieces[y*width + x + 1] = tmp
                    x+=1
            elif act=="U":
                if y==0:
                    tmp = pieces[y*width + x]
                    pieces[y*width + x] = pieces[(height-1)*width + x]
                    pieces[(height-1)*width + x] = tmp
                    y=height-1
                else:
                    tmp = pieces[y*width + x]
                    pieces[y*width + x] = pieces[(y-1)*width + x]
                    pieces[(y-1)*width + x] = tmp
                    y-=1
            elif act=="L":
                if x==0:
                    tmp = pieces[y*width + x]
                    pieces[y*width + x] = pieces[y*width + width - 1]
                    pieces[y*width + width - 1] = tmp
                    x=width-1
                else:
                    tmp = pieces[y*width + x]
                    pieces[y*width + x] = pieces[y*width + x - 1]
                    pieces[y*width + x - 1] = tmp
                    x-=1
            elif act=="D":
                if y==height-1:
                    tmp = pieces[y*width + x]
                    pieces[y*width + x] = pieces[x]
                    pieces[x] = tmp
                    y=0
                else:
                    tmp = pieces[y*width + x]
                    pieces[y*width + x] = pieces[(y+1)*width + x]
                    pieces[(y+1)*width + x] = tmp
                    y+=1

    for i in range(len(solution[0])):
        r = (4-int(solution[0][i]))%4
        pieces[i] = np.rot90(pieces[i],r)

    pic = np.zeros(img.shape)
    for y in range(height):
        for x in range(width):
            pic[y*PIECE_SIZE:(y+1)*PIECE_SIZE, x*PIECE_SIZE:(x+1)*PIECE_SIZE] = pieces[y*width+x]
    cv2.imwrite("debug.png", pic)