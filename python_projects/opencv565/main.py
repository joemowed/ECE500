IMG_PATH = "imgs/2026-03-25-090151.jpg"
import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

img = cv.imread(IMG_PATH, cv.IMREAD_COLOR_RGB)
assert img is not None, "file could not be read, check with os.path.exists()"
original_img = img
img_contour = img.copy()
img = cv.medianBlur(img, 5)
canny = cv.Canny(img, 15, 60, L2gradient=True)  #


# 4. Find contours
# Output format is slightly different in older OpenCV versions, but this works for current ones.
contours, hierarchy = cv.findContours(canny, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
# cv.RETR_TREE retrieves all contours and their hierarchy
# cv.CHAIN_APPROX_SIMPLE compresses horizontal, vertical, and diagonal segments

# 5. Draw all contours on the original image copy
cv.drawContours(
    img_contour, contours, -1, (0, 255, 0), 3
)  # -1 draws all contours, (0, 255, 0) is green, 3 is thickness

titles = [
    "Original Image",
    "canny edge",
    "contour",
    "Adaptive Gaussian Thresholding",
]
images = [original_img, canny, img_contour, img_contour]

for i in range(4):
    plt.subplot(2, 2, i + 1), plt.imshow(images[i], "gray")
    plt.title(titles[i])
    plt.xticks([]), plt.yticks([])
plt.show()
