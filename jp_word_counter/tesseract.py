from PIL import Image
import pytesseract
from pytesseract import Output
import cv2
import numpy as np
import matplotlib.pyplot as plt

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
#######################################################################################

# Page segmentation modes:
#   0    Orientation and script detection (OSD) only.
#   1    Automatic page segmentation with OSD.
#   2    Automatic page segmentation, but no OSD, or OCR. (not implemented)
#   3    Fully automatic page segmentation, but no OSD. (Default)
#   4    Assume a single column of text of variable sizes.
#   5    Assume a single uniform block of vertically aligned text.
#   6    Assume a single uniform block of text.
#   7    Treat the image as a single text line.
#   8    Treat the image as a single word.
#   9    Treat the image as a single word in a circle.
#  10    Treat the image as a single character.
#  11    Sparse text. Find as much text as possible in no particular order.
#  12    Sparse text with OSD.
#  13    Raw line. Treat the image as a single text line,
#        bypassing hacks that are Tesseract-specific.

def image_window(filename):
    image = cv2.imread(filename)

    if image is None:
        print("Error: Could not load image.")
        exit()
    else:
        cv2.imshow('My Image', image)

        cv2.waitKey(0)

        cv2.destroyAllWindows()


# print(pytesseract.image_to_string(Image.open('image_data/jpn1.png'), lang='jpn'))
# print(pytesseract.image_to_string(Image.open('image_data/jpn2.png'), lang='jpn'))
# print(pytesseract.image_to_string(Image.open('image_data/jpn3.png'), lang='jpn'))
# print(pytesseract.image_to_string(Image.open('image_data/jpn4.png'), lang='jpn'))
# print(pytesseract.image_to_string(Image.open('image_data/jpn5.png'), lang='jpn'))
# print(pytesseract.image_to_string(Image.open('image_data/jpn6.png'), lang='jpn'))
# print(pytesseract.image_to_string(Image.open('image_data/engimage1.png')))

image = cv2.imread('image_data/jpn6.png')

filtered = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) # grayscale
filtered = cv2.bilateralFilter(filtered, 10, 85, 75) # denoise 10 75 75
kernel = np.ones((2,2), np.uint8)
filtered = cv2.morphologyEx(filtered, cv2.MORPH_CLOSE, kernel)
# kernel = np.array([[0, -1, 0],
#                    [-1, 5, -1],
#                    [0, -1, 0]])
# filtered = cv2.filter2D(filtered, -1, kernel)
# filtered = cv2.adaptiveThreshold(filtered, 255,
#                                  cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
#                                  cv2.THRESH_BINARY, 11, 2)  # strictly B&W

cv2.imwrite('filtered_images/filter.png', filtered)

print(pytesseract.image_to_string(Image.open('filtered_images/filter.png'), lang='jpn', config='--psm 11 --oem 3'))
# print(pytesseract.image_to_data(Image.open('filtered_images/filter.png'), lang='jpn', config='--psm 6'))
data = pytesseract.image_to_data(Image.open('filtered_images/filter.png'), lang='jpn', config='--psm 11 --oem 3', output_type=Output.DICT)

image_rgb = cv2.cvtColor(filtered, cv2.COLOR_BGR2RGB)
fig, ax = plt.subplots(figsize=(10, 10))

ax.imshow(image_rgb)

n_boxes = len(data['level'])
for i in range(n_boxes):
    if int(data['conf'][i]) > 0:
        (x, y, w, h) = (data['left'][i], data['top'][i], data['width'][i], data['height'][i])
        
        rect = plt.Rectangle((x, y), w, h, fill=False, color='red', linewidth=1)
        ax.add_patch(rect)
        ax.text(x, y-5, data['conf'][i]/100, color='blue', fontsize=8)

plt.show()

# image_window('grayscale_images/jpn1gray.png')
