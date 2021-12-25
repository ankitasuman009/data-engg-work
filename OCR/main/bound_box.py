from datetime import date
import cv2
import pytesseract
from pytesseract import Output
import matplotlib.pyplot as plt
import re

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def boundBoxAllText(page):
    image = cv2.imread(page, cv2.IMREAD_GRAYSCALE)
    d = pytesseract.image_to_data(image, output_type=Output.DICT)
    n_boxes = len(d['level'])
    boxes = cv2.cvtColor(image.copy(), cv2.COLOR_BGR2RGB)
    for i in range(n_boxes):
        (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])    
        boxes = cv2.rectangle(boxes, (x, y), (x + w, y + h), (0, 255, 0), 2)
    
    plt.figure(figsize=(16,10))
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    cv2.imwrite('output/output' + page + '.jpg', boxes)
    cv2.waitKey(0)



def boundBoxDate(page):
    img = cv2.imread('images/' + (page) + '.jpeg')

    d = pytesseract.image_to_data(img, output_type=Output.DICT)
    keys = list(d.keys())
    # date_pattern = '^(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[012])/(19|20)\d\d$'
    date_pattern2 = '^(0?[1-9]|[12][0-9]|3[01])[\/\-\.](0?[1-9]|1[012])[\/\-\.]\d{4}$'
    n_boxes = len(d['text'])
    for i in range(n_boxes):
        if int(float(d['conf'][i])) > 60:
            if re.match(date_pattern2, d['text'][i]):
                # print(d['text'][i])
                (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
                img = cv2.rectangle(img, (x - 5, y - 5), (x + w + 5, y + h + 5), (255, 0, 0), 2)


    img = cv2.resize(img, (0,0), fx=0.5, fy=0.5) 
    cv2.imshow('img', img)
    cv2.waitKey(0)
# print(d.keys())

boundBoxDate("5")



