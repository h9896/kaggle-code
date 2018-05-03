import json
import cv2
import numpy as np
from sklearn.model_selection import train_test_split
def load():
    #path = "C:/Users/h124036822/Desktop/kaggle/png/"
    path = "/home/burke/song/png/"
    img_path = path + "train"
    img = []
    for i in range(1,4001):
        tmp = img_path + "/" + str(i) + ".jpg"
        tmpval = cv2.imread(tmp)
        tmpval = cv2.resize(tmpval,(100,100))
        tmpval = tmpval.transpose((2,0,1))
        img.append(tmpval)
    
    label = []
    with open (path+"train_label.json", 'r') as f:
        data = json.load(f)
    for i in range(1,4001):
        label.append(data[str(i)])
    img = np.array(img)
    label = np.array(label)
    x_train , x_test, y_train, y_test = train_test_split(img,label,test_size=0.2,random_state=100)
    return x_train, x_test, y_train, y_test