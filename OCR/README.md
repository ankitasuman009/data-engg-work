#### converter.py

- convert pdf file into images and store them inside 'images' folder

#### bound_box.py

- bound box all the dates in the images

#### upload.py

- upload new modified images into s3 bucket.
- these images have date, gst no., invoice no., address, amount etc texts bound-boxed

#### get_data.py

- for every image we are calling fetchData() function
- that function again calling three functions: fetchDate(), fetchGST(), fetchInvoice()
- storing all the values in a list first
- and at last storing the values inside a dictionary, with key value as image number and value as the list contains all the fetched value.

