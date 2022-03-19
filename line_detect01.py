#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import cv2 as cv
import numpy as np
src = cv.imread("lane.jpg", cv.IMREAD_COLOR)
cv.imshow("src", src)
cv.waitKey(0)


# In[ ]:


gray = cv.cvtColor(src, cv.COLOR_BGR2GRAY)
cv.imshow("src_gray", gray)
cv.waitKey(0)


# In[ ]:


gray = cv.bitwise_not(gray)
bw = cv.adaptiveThreshold(gray, 255, cv.ADAPTIVE_THRESH_MEAN_C,                                cv.THRESH_BINARY, 15, -2)
cv.imshow("src_gray_binary", bw)
cv.waitKey(0)


# In[ ]:


# Create the images that will use to extract the horizontal and vertical lines
horizontal = np.copy(bw)
vertical = np.copy(bw)


# In[ ]:


cols = horizontal.shape[1]
horizontal_size = cols // 30
    # Create structure element for extracting horizontal lines through morphology operations
horizontalStructure = cv.getStructuringElement(cv.MORPH_RECT, (horizontal_size, 1))
    # Apply morphology operations
horizontal = cv.erode(horizontal, horizontalStructure)
horizontal = cv.dilate(horizontal, horizontalStructure)
    # Show extracted horizontal lines
cv.imshow("horizontal", horizontal)
cv.waitKey(0) # Specify size on vertical axis


# In[ ]:


rows = vertical.shape[0]
verticalsize = rows // 30
# Create structure element for extracting vertical lines through morphology operations
verticalStructure = cv.getStructuringElement(cv.MORPH_RECT, (1, verticalsize))
# Apply morphology operations
vertical = cv.erode(vertical, verticalStructure)
vertical = cv.dilate(vertical, verticalStructure)
# Show extracted vertical lines
cv.imshow("vertical", vertical)
cv.waitKey(0)


# In[ ]:




