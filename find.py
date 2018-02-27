import cv2 as cv
import numpy as np
#class to hold the min and max rows/columns
class Points:
    minRow = 0
    maxRow = 0
    minCol = 0
    maxCol = 0
    def setRowAndCol(self, minR, maxR, minC, maxC):
        self.minRow = minR
        self.maxRow = maxR
        self.minCol = minC
        self.maxCol = maxC
        return;

#function to find the max and min rows/columns
def findMinMax(rows,cols):
    x = Points()
    minRow = rows[0]
    maxRow = 0
    minCol = cols[0]
    maxCol = 0
    for i in rows:
        if i < minRow:
            minRow = i
        elif i > maxRow:
            maxRow = i
    for i in cols:
        if i < minCol:
            minCol = i
        elif i > maxCol:
            maxCol = i
    x.setRowAndCol(minRow, maxRow, minCol, maxCol)
    return x;

#function to tell if the point is already been found
def isIn(r,c,shapes):
    flag = False
    for i in shapes:
        if (r >= i.minRow and r <= i.maxRow) and (c >= i.minCol and c <= i.maxCol):
            flag = True
            return flag;
    return flag;

#Function to find the whole green object
#This still needs to be improved as it does not handle green objects
#that are right next to each other well
def findEdge(startRow, numRows, numCols, image, shapes):
    x = Points()
    rows = []
    cols = []
    for i in range(startRow, numRows):
        emptyRow = False
        for j in range(numCols):
            flag = False
            isInflag = isIn(i,j,shapes)
            if (image[i,j] == 255) and not(isIn(i,j,shapes)):
                rows.append(i)
                cols.append(j)
                k = j
                while image[i,k] == 255:
                    k = k + 1
                cols.append(k)
                flag = True
            if flag:
                break
            elif (j+1) == numCols:
                emptyRow = True
        if emptyRow:
            break
    if not rows:
        return x;
    x = findMinMax(rows,cols)
    return x;

img = cv.imread('green3.jpg')
img = cv.resize(img,None,fx=0.25,fy=0.25, interpolation = cv.INTER_AREA)
#owl = cv.imread('owl.jpg')
greenObjects = []
hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV )
#owlhsv = cv.cvtColor(owl, cv.COLOR_BGR2HSV)
lower = np.array([40, 150, 72])
upper = np.array([90, 255, 255])

mask = cv.inRange(hsv,lower,upper)
#owlMask = cv.inRange(owlhsv,lower,upper)
maskInv = cv.bitwise_not(mask,mask=None)
#owlMaskInv = cv.bitwise_not(owlMask,mask=None)

#numRows, numCols = maskInv.shape[:2]
numRows, numCols = mask.shape[:2]
maskImage = []
maskInvImage = []
image = []
count = 0
for i in range(numRows):
    for j in range(numCols):
        if (mask[i,j] == 255) and not(isIn(i,j,greenObjects)):
            greenObjects.append(findEdge(i,numRows,numCols,mask,greenObjects))
            image.append(img[greenObjects[count].minRow:greenObjects[count].maxRow,greenObjects[count].minCol:greenObjects[count].maxCol])
            maskImage.append(mask[greenObjects[count].minRow:greenObjects[count].maxRow,greenObjects[count].minCol:greenObjects[count].maxCol])
            maskInvImage.append(maskInv[greenObjects[count].minRow:greenObjects[count].maxRow,greenObjects[count].minCol:greenObjects[count].maxCol])
            count = count + 1
title = 'Green_Image_'
number = 0
for i in image:
    cv.imshow(title + str(number), i)
    cv.imwrite(title + str(number) + ".jpg", i)
    number += 1







#This will be the basis of my code to show an image in front of the green object
#owl = cv.bitwise_and(owl,owl,mask=owlMaskInv)
#owlRows, owlCols = owl.shape[:2]
#imgPiece = img[:owlRows,:owlCols]
#imgPiece = cv.bitwise_and(imgPiece,imgPiece,mask=owlMask)
#imgPiece = cv.add(owl,imgPiece)
#img[:owlRows,:owlCols] = imgPiece
#cv.imshow('imgPiece',img)
#img3 = cv.add(owl,owlMaskInv)
#cv.imshow('test',owl)
cv.waitKey(0)
cv.destroyAllWindows()
