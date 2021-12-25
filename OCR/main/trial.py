# from datetime import date
# import cv2
# import pytesseract
# from pytesseract import Output
# import re

# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# def find_amounts(page):
#     date_list = []
#     img = cv2.imread('images/' + page + '.jpg')
#     d = pytesseract.image_to_data(img, output_type=Output.DICT)
#     n_boxes = len(d['text'])
#     date_pattern2 = '^(\d*\.?\d+|\d(,\d{3})|\d{1,3}(,\d{3})*(\.\d+)?)$'
#     for i in range(n_boxes):
#         if int(float(d['conf'][i])) > 60:
#             if re.match(date_pattern2, d['text'][i]):
#                 date_list.append(d['text'][i])
#     return date_list

# amounts = find_amounts("page2")
# print(amounts)



import json
import cv2
from PIL import Image


def addressOfJson(name):
    '''
    gets the name of the json file as parameter
    builds and returns the address of the json file
    '''
    temp = 'output/json_files/outputfile'
    address = temp + str(name) + '.json'
    return address


def getPolygon(data, imgSize = [1700,2200]):
    '''
    the function gets the data and the image size as parameters
    extracts the bounding box dimensions into variables
    returns the corner points of the bounding box for the data
    '''
    geometry = data['Geometry']
    (tl, tr, br, bl) = geometry['Polygon']
    tl = (int(tl['X']*imgSize[0]),int(tl['Y']*imgSize[1]))
    tr = (int(tr['X']*imgSize[0]),int(tr['Y']*imgSize[1]))
    br = (int(br['X']*imgSize[0]),int(br['Y']*imgSize[1]))
    bl = (int(bl['X']*imgSize[0]),int(bl['Y']*imgSize[1]))
    return tl,tr,br,bl


def printTermAndAfter(textLine,term):
    '''
    gets a line of text and a string term as parameters
    checks for the presence of the term in that line
    prints the term and the characters following that term in that line
    '''
    for i in range(len(textLine)-len(term)):
        if textLine[i:i+len(term)].lower() == term.lower():
            print(textLine[i:])
            return


def checkForDate(data):
    '''
    gets a dictionary data containing DetectedText, Type, etc
    checks if the Type is a line and if 'date' is present
    calls the printTermAndAfter to print the date
    '''
    if data['Type'] == 'LINE':
        if 'date' in data['DetectedText'].lower():   # checking if it is a line and contains the term date
            boundingDataList.append(data)
            printTermAndAfter(data['DetectedText'],'date')
    

def checkForGST(data):
    '''
    gets a dictionary data containing DetectedText, Type, etc
    checks if the Type is a line and if 'date' is present
    calls the printTermAndAfter to print the gst
    '''
    if data['Type'] == 'LINE':
        if 'gst' in data['DetectedText'].lower():   # checking if it is a line and contains the term gst
            boundingDataList.append(data)
            printTermAndAfter(data['DetectedText'],'gst')

def checkForInvoice(data):
    '''
    gets a dictionary data containing DetectedText, Type, etc
    checks if the Type is a line and if 'date' is present
    calls the printTermAndAfter to print the gst
    '''
    checkList = ['invoice number', 'invoice no', 'inv no', 'invoice num', 'inv num']

    if data['Type'] == 'LINE':
        for check in checkList:
            if check in data['DetectedText'].lower():   # checking if it is a line and contains the term gst
                boundingDataList.append(data)
                printTermAndAfter(data['DetectedText'],check)


def makeBoundingBox(data,imgDetails,box = True,text = True):
    '''
    the data and the image is passed as parameters to the function
    the function gets the bounding box dimensions and position
    builds a bounding box and shows image with it
    '''
    imageAddress = imageDetails[2]
    billImage = imageDetails[3]

    image = Image.open(imageAddress)
    x,y = image.size
    tl, tr, br, bl = getPolygon(data,[x,y])

    if box == True:
        cv2.rectangle(billImage,tl,br,(0,0,255),2)
    if text == True:
        cv2.putText(billImage,data['DetectedText'],(br[0],br[1]-10),
                    cv2.FONT_HERSHEY_SIMPLEX,0.5,(20,20,20),2)
    
def getImageDetails(number):
    '''
    gets a number as the function parameter
    gathers the details of the image from that number
    returns the image number, name, address and the image itself
    '''
    imagenumber = number
    imageName = str(imagenumber)+'.jpeg'
    imageAddress = 'images/'+str(imagenumber)+'.jpg'
    billImage = cv2.imread(imageAddress)
    imageDetails = [imagenumber, imageName, imageAddress, billImage]
    return imageDetails


def boundData(imageDetails,dataToShow):
    '''
    gets the image details as parameter
    opens corresponding json file and checks for date, gst, etc
    '''
    imagenumber = imageDetails[0]
    filename = addressOfJson(imagenumber)                    # for every json file in the directory
    f = open(filename)
    detections = json.load(f)                   # accessing the detections from the json file
    for data in detections['TextDetections']:
        if 'date' in dataToShow:
            checkForDate(data)                      # checking for date in every text detection
        if 'gst' in dataToShow:
            checkForGST(data)                       # checking for gst number
        if 'invoice' in dataToShow:
            checkForInvoice(data)                   # checking for invoice number


def showData(imageDetails, boundingDataList,box = True, text = True):
    '''
    gets the list of data that needs to be bounded, bool values for the box and text to show
    builds a bounding box for each data using makeboundingbox and shows image
    '''
    for data in boundingDataList:
        makeBoundingBox(data,imageDetails,box,text)
    billImage = imageDetails[3]
    cv2.imshow("image",billImage)
    cv2.waitKey(0)

def outputModifiedImages(imageDetails):
    imageName = imageDetails[1]
    imageAddress = 'output/modified_images/' + str(imageName)
    billImage = imageDetails[3]
    cv2.imwrite(imageAddress, billImage)

for num in range(1,20):
    imageDetails = getImageDetails(num)
    dataToShow = ['date', 'gst', 'invoice']
    boundingDataList = []
    boundData(imageDetails,dataToShow)
    showData(imageDetails, boundingDataList, text = False)
    outputModifiedImages(imageDetails)