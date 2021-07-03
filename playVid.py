import cv2
import keyboard
import socket

def playVideo():
    IP = "127.0.0.1"
    PORT = 12321
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((IP, PORT))
    server.listen(1)
    session_socket, client_socket_name = server.accept()
    session_socket.send(bytearray("start", 'utf-8'))
    data = session_socket.recv(1024).decode('utf-8').split(":")
    sec_mistake = int(float(data[0]))
    row = int(data[1])
    frame_rate = int(float(data[2]))
    video_time = int(float(data[3]))

    with open("log.txt", "w") as f:
        f.write("{},{} : {},{} : {},{} : {},{}".format(video_time, type(video_time), sec_mistake, type(sec_mistake), row, type(row) , frame_rate , type(frame_rate)))

    openPath = "{}\\{}{}".format(r'C:\Users\rotem\PycharmProjects\Roto_DNF_Analyzer\Videos',str(row), ".mkv")
    cap1 = cv2.VideoCapture(openPath)
    cap1.set(cv2.CAP_PROP_POS_MSEC, round(sec_mistake*1000-500,2))
    times = 2
    c1=0
    c2=0
    c3=0
    c4=0
    m = 0
    e = 0
    t = 0
    n = 0
    corrected = False
    while(cap1.isOpened()):
        ret, frame = cap1.read()
        if(ret == True):
            # print(cap1.get(cv2.CAP_PROP_POS_MSEC)
            res = cv2.resize(frame, (640,480))
            cv2.imshow('m: memo, e: exe, t: trace, s:Success, mistake:{}'.format(sec_mistake),res)
            cv2.moveWindow('m: memo, e: exe, t: trace, s:Success, mistake:{}'.format(sec_mistake), 210, 20)

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
                    cap1.set(cv2.CAP_PROP_POS_MSEC, round(sec_mistake * 1000-500, 2))
            # memo : m, trace : t, execution : e, no_error : n

            if (keyboard.is_pressed('m') == True):
                m += 1
                if (m >= times):
                    session_socket.send(bytearray("{}:{}".format(str(int(cv2.CAP_PROP_POS_MSEC/1000)), "memo_forgot_error"),'utf-8'))
                    corrected = True
                    break
            if (keyboard.is_pressed('t') == True):
                t += 1
                if (t >= times):
                    session_socket.send(bytearray("{}:{}".format(str(int(cv2.CAP_PROP_POS_MSEC/1000)), "trace_error"),'utf-8'))
                    corrected = True
                    break
            if (keyboard.is_pressed('e') == True):
                e += 1
                if (e >= times):
                    session_socket.send(bytearray("{}:{}".format(str(int(cv2.CAP_PROP_POS_MSEC/1000)), "exe_error"),'utf-8'))
                    corrected = True
                    print("exe_errrrror")
                    break
            if (keyboard.is_pressed('s') == True):
                n += 1
                if (n >= times):
                    session_socket.send(bytearray("{}:{}".format(str(int(cv2.CAP_PROP_POS_MSEC/1000)), "Success"),'utf-8'))
                    corrected = True
                    break

        else:
            break

    cap1.release()
    cv2.destroyAllWindows()
    if not corrected:
        session_socket.send(bytearray("finish", 'utf-8'))
def main():
    playVideo()
if __name__ == '__main__':
    main()
