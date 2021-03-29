import cv2
import keyboard
import pyautogui
def playVid():
    row = open('vidNum.txt').readline()
    sec = float(open('playVid.txt').readline())
    openPath = "C:\\Python\\PythonWork\\BLD\\RotoBLD\\RotoDNF\\videos\\solve" + str(row) +".avi"
    cap1 = cv2.VideoCapture(openPath)

    cap1.set(cv2.CAP_PROP_POS_MSEC, round(sec*1000-500,2))
    times = 2
    c1=0
    c2=0
    c3=0
    while(cap1.isOpened()):
        ret, frame = cap1.read()
        if(ret == True):
            res = cv2.resize(frame, (0,0), fx=1.4, fy=1.4)
            cv2.imshow('frame',res)
            cv2.moveWindow('frame', 210, 20)

            if cv2.waitKey(30)& 0xFF == ord(' '):
                break
            if(keyboard.is_pressed('left arrow') == True):
                c1+=1
                if(c1>=times):
                    c1=0
                    cap1.set(cv2.CAP_PROP_POS_MSEC, cap1.get(cv2.CAP_PROP_POS_MSEC)-5000.0)
            if(keyboard.is_pressed('right arrow') == True):
                c2 += 1
                if (c2 >= times):
                    c2 = 0
                    cap1.set(cv2.CAP_PROP_POS_MSEC, cap1.get(cv2.CAP_PROP_POS_MSEC)+5000.0)
            if (keyboard.is_pressed('down arrow') == True):
                c3 += 1
                if (c3 >= times):
                    c3 = 0
                    cap1.set(cv2.CAP_PROP_POS_MSEC, round(sec * 1000-500, 2))
        else:
            break
    cap1.release()
    cv2.destroyAllWindows()
playVid()