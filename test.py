import socket
import numpy
import cv2
def test_play():
    cap = cv2.VideoCapture(r'C:\Users\rotem\PycharmProjects\Roto_DNF_Analyzer\RotoDNF_analyzer\Videos\134.mkv')

    while (cap.isOpened()):
        ret, frame = cap.read()

        cv2.imshow('frame', frame)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def init_ws(ip, port):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((ip, port))

    client.send(bytearray(str(123),'utf-8'))
    print(client.recv(1024).decode('utf-8'))
    a = input("press enter to finish")
    client.send(bytearray("STOP", 'utf-8'))

def main():
    test_play()
if __name__ == '__main__':
    main()