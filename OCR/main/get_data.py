from datetime import date
import cv2
import pytesseract
from pytesseract import Output
import re
import os
import json

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def get_size():
	# assign size
	size = 0
	
	try:
		# assign folder path
		Folderpath = 'json'  
		# get size
		for base, dires, files in os.walk(Folderpath):
			for Files in files:
				size += 1
	except:
		return 0
	return size


def addressOfJson(name):
    return 'json/outputfile' + str(name) + '.json'


def fetchDate(pageno):
    date_list = []
    img = cv2.imread('images/' + str(pageno) + '.jpeg')
    d = pytesseract.image_to_data(img, output_type=Output.DICT)
    n_boxes = len(d['text'])
    date_pattern2 = '^(0?[1-9]|[12][0-9]|3[01])[\/\-\.](0?[1-9]|1[012])[\/\-\.]\d{4}$'
    for i in range(n_boxes):
        if int(float(d['conf'][i])) > 60:
            if re.match(date_pattern2, d['text'][i]):
                date_list.append(d['text'][i])
    return (date_list)


def fetchGST(data):
    if data['Type'] == 'LINE':
        if 'gst' in data['DetectedText'].lower():   # checking if it is a line and contains the term gst
           return(data['DetectedText'])
    


def fetchInvoice(data):
    checkList = ['invoice number', 'invoice no', 'inv no', 'invoice num', 'inv num']
    if data['Type'] == 'LINE':
        for check in checkList:
            if check in data['DetectedText'].lower():   # checking if it is a line and contains the term gst
                return(data['DetectedText'])



def fetchData(pageno, dataToShow):
    '''
    gets the image details as parameter
    opens corresponding json file and checks for date, gst, etc
    '''
    filename = addressOfJson(pageno)                    # for every json file in the directory
    f = open(filename)
    detections = json.load(f)                   # accessing the detections from the json file
    li = []
    for data in dataToShow:
        if 'date' in data:
            li.append(fetchDate(pageno))
        if 'gst' in data:
            for text in detections['TextDetections']:
                if (fetchGST(text)):                     # checking for gst number
                    li.append(fetchGST(text))
                    break
        if 'invoice' in data:
            for text in detections['TextDetections']:
                if (fetchInvoice(text)):                     # checking for invoice number
                    li.append(fetchInvoice(text))
                    break
                    # splitstr = fetchInvoice(text).split(' ')
                    # for i in range(len(splitstr)):
                    #     if 'invoice' in splitstr[i].lower():
                    #         print(splitstr[i]+" "+splitstr[i+1]+":"+splitstr[i+2])
                    #         break
                    
    return li


def main():
    max_size = get_size()
    dict = {}
    
    for num in range(1, max_size):
        print("fetching data in image", num)
        dataToShow = ['date', 'gst', 'invoice']
        dict[num] = fetchData(num, dataToShow)
    # print(dict)
    for key, value in dict.items():
        print(key, value)
        

if __name__ == "__main__":
    main()