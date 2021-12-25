# import module
from pdf2image import convert_from_path
import os


def get_size():
	# assign size
	size = 0
	
	try:
		# assign folder path
		Folderpath = 'images'  
		# get size
		for base, dires, files in os.walk(Folderpath):
			print('Searching in: ',base)
			for Files in files:
				size += 1
	except:
		return 0
	return size

# Store Pdf with convert_from_path function
def pdf_converter(pdf):
	pdf_name = 'pdf/' + pdf + '.pdf'
	images = convert_from_path(pdf_name)
	max_size = get_size()
	for i in range(len(images)):
		try:
			images[i].save('images/'+ str(max_size + i + 1) +'.jpeg', 'JPEG')
		except:
			print("not saved")

pdf_converter("mainetti")

# def store():


