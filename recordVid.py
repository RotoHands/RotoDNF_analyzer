import cv2

import cv2

def recordVid():
    vidNum = open('vidNum.txt').readline()
    fourcc = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')
    savePath = "C:\\Python\\PythonWork\\BLD\\RotoBLD\\RotoDNF\\videos\\solve" +vidNum+ ".avi"
    cap = cv2.VideoCapture(0)
    out = cv2.VideoWriter(savePath, fourcc, 30.0, (640, 480))
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    cap.set(15, -8.0)
    f = open('StartRec.txt','w')
    f.write('T')
    f.close()
    while(open('boolVid.txt').read(1) == 'T'):
        _, frame = cap.read()
        out.write(frame)
    cv2.destroyAllWindows()
    f = open('StartRec.txt','w')
    f.write('F')
    f.close()

recordVid()


