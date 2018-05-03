import json
import cv2
import numpy as np
from sklearn.model_selection import train_test_split
def load():
    path = "D:/kaggle/png/"
    #path = "/home/burke/song/png/"
    img_path = path + "train"
    img = []
    for i in range(1,5000):
        tmp = img_path + "/" + str(i) + ".jpg"
        tmpval = cv2.imread(tmp)
        tmpval = cv2.resize(tmpval,(227,227))
        img.append(tmpval)
    
    label = []
    with open (path+"train_label.json", 'r') as f:
        data = json.load(f)
    for i in range(1,5000):
        label.append(data[str(i)])
    img = np.array(img)
    label = np.array(label)
    x_train , x_test, y_train, y_test = train_test_split(img,label,test_size=0.2,random_state=100)
    return x_train, x_test, y_train, y_test

def prep():
    path = "D:/kaggle/png/"
    dic = {}
    with open(path + "train.json") as f:
        data = json.load(f)
    max_v = 0
    for i in data["annotations"]:
        for j in range(len(i['labelId'])):
            if max_v < int(i['labelId'][j]):
                max_v = int(i['labelId'][j])
    print(max_v)
    
    for i in data["annotations"]:
        tmp = [0]*max_v
        for j in i["labelId"]:
            tmp[int(j)-1] = 1
        dic[i["imageId"]] = tmp
    with open(path + "train_label.json", 'w') as f:
        f.write(json.dumps(dic))
if __name__ == '__main__':
    prep()