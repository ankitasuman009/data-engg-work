import cv2
import pytesseract
from pytesseract import Output
import json
import pandas as pd

# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# img = cv2.imread('images/page0.jpg')


# extracted_text = pytesseract.image_to_string(img)
# print(extracted_text)

# df = pd.DataFrame.from_dict(pd.json_normalize("json/outputfile1.json"), orient='columns')

# df.head()

# with open('json/outputfile1.json') as json_file:
#     data = json.load(json_file)
#     print(data)

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

img = cv2.imread('images/' + 'page0' + '.jpg')
d = pytesseract.image_to_data(img, output_type=Output.DICT)
n_boxes = len(d['text'])

for i in range(n_boxes):
    if (d['text'][i]).lower() == 'gst':
        if (len(d['text'][i+1])) == 15:
            gst = d['text'][i+1]
        else:
            gst = d['text'][i+2]