#!/usr/bin/python3
import time
import sys
import cv2
import socket
IP = '127.0.0.1'
PORT = 12345
import os
from pathlib import Path

def recordVid():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((IP, PORT))
    print("opening connection ")
    print("cv2 version {}".format(cv2.__version__))
    print("python version:\n {} \n {} ".format(sys.prefix, sys.base_prefix))

    server.listen(1)

    session_socket, client_socket_name = server.accept()
    data = session_socket.recv(1024).decode('utf-8')
    vidNum = data
    fourcc = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')

    savePath = os.path.join(Path(os.getcwd()).parent.absolute(),"Videos","{}{}".format(vidNum, ".mkv"))
    print(savePath)
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cap.set(15, -3.0)
    out = cv2.VideoWriter(savePath, fourcc, 30.0, (640, 480))
    session_socket.send(bytearray("Started", 'utf-8'))
    session_socket.setblocking(False)
    a = time.time()
    count_frames = 0
    while True:
        count_frames += 1
        _, frame = cap.read()
        out.write(frame)
        try:
            data = session_socket.recv(1024).decode('utf-8')
            break
        except Exception as e:
            pass
    cv2.destroyAllWindows()
    print("here {}".format(str(count_frames/(time.time()-a))))
    session_socket.send(bytearray(str(count_frames/(time.time()-a)), 'utf-8'))
    session_socket.send(bytearray(str((time.time()-a)), 'utf-8'))

def main():
    recordVid()

if __name__ == '__main__':
    main()
