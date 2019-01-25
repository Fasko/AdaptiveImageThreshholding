# Michael Fasko Jr
# Term Project CIS 465
# Fall 2018

from PIL import Image
from PIL import ImageOps
import statistics
threshold = 0 # Global, so we can use to normalize for APT

def otsu(grayImage):
    global threshold
    pixelEditor = grayImage.load()
    width,height = grayImage.size
    imageSize = width * height
    meanWeight = 1/imageSize
    imgHistogram = grayImage.histogram() # Compute Image Histogram
    varmax,sum,sumB,q1,q2,mu1,mu2 = 0,0,0,0,0,0,0

    for i in range(0,256):
        sum += i * imgHistogram[i]
    for j in range(0,255):
        q1 += imgHistogram[j] # Dark
        q2 = imageSize - q1   # Light
        if q1 == 0: continue
        if q2 == 0: continue
        sumB += j * imgHistogram[j]
        mu1 = sumB/q1   # Avg Dark
        mu2 = (sum-sumB) /q2    # Avg Lights
        varSquared = q1*q2 * ((mu1 - mu2)*(mu1 - mu2)) # Interclass Difference
        if varSquared > varmax:
            threshold = j
            varmax = varSquared
    return threshold, pixelEditor

def imageCreator(threshold,pixelEditor,image):
    width,height = image.size
    # Create binary image
    for a in range(0,width):
        for b in range(0,height):
            grayValue = pixelEditor[a,b]
            if grayValue > threshold:
                pixelEditor[a,b] = 255
            else:
                pixelEditor[a, b] = 0

def APT(grayImage):
    global threshold
    pixelEditor = grayImage.load()
    width,height = grayImage.size
    imageCreator(threshold,pixelEditor,grayImage)


# Run's otsu's method and APT for the input image
def createImages(imagePath):
    global threshold
    imgOTSU = Image.open(imagePath).convert('L')
    threshold, pixelEditor = otsu(imgOTSU)
    print('Otsu Threshold:', threshold)
    imageCreator(threshold,pixelEditor,imgOTSU)
    imgOTSU.show()
    imgAPT = Image.open(imagePath).convert('L')
    imgAPT = imgAPT.quantize(threshold)
    otsu(imgAPT)
    imgAPT = Image.open(imagePath).convert('L')
    APT(imgAPT)
    print('APT Threshold: ', threshold)
    imageCreator(threshold,pixelEditor,imgAPT)
    imgAPT.show()


print("1 = coins\n2 = room with clock\n3 = color palette \n4 = lena")
userImagePath = str(input("Enter in the number of the image you want:"))
if userImagePath == '1':
    createImages('Project-Data/coins.bmp')
elif(userImagePath == '2'):
    createImages('Project-Data/image1.jpg')
elif(userImagePath == '3'):
    createImages('Project-Data/image2.jpg')
elif(userImagePath == '4'):
    createImages('Project-Data/lena.png')
else:
    print("ERROR: not accepted value")
    exit(1)



