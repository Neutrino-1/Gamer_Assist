try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract
import cv2

img_cv = cv2.imread('images/HealthY.png')
pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract'
img_rgb = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)
gray_image = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
#blur the gray image to remove noise and to averaging the color
blurred = cv2.bilateralFilter(gray_image,15,100,100)
#converting the blurred image to pure black(0) and white(255) binary image
thresh = cv2.threshold(blurred, 100,200, cv2.THRESH_BINARY)[1]
print(pytesseract.image_to_string(thresh,config='--psm 7 -c tessedit_char_whitelist=0123456789'))
cv2.imshow("test",thresh)
cv2.waitKey(0)
cv2.destroyAllWindows()