import io
import socket
import struct
import time
import picamera
import cv2
import numpy as np
import threading
import multiprocessing as mp
DETE_DATA = []
def  Client_(ip,port,open_ret=1):
    global DETE_DATA
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  #TCP的模式进行
    client_socket.connect((ip,port))                                   #连接服器
    connection = client_socket.makefile('wb')                          #创建二进制文件
    start = time.time()
    try:
        with picamera.PiCamera() as camera:
            camera.resolution = (416, 416)  # 图片的像数
            camera.framerate = 15  # 15 帧帲 帧/秒
            time.sleep(2)  # give 2 secs for camera to initilize

            stream = io.BytesIO()    #创建字节流
            threading.Thread(target=show_photo_inPI,name="得到数据",args=(client_socket,)).start()
            # mp.Process(target=show_photo_inPI,name= "显示图片",args=(client_socket,stream)).start()
            for foo in camera.capture_continuous(stream, 'jpeg', use_video_port=True):
                # 将数据写进流中
                connection.write(struct.pack('<L', stream.tell()))
                connection.flush()
                # threading.Thread(target=show_photo_inPI,name= "显示图片",args=(client_socket,stream)).start()
                data = np.fromstring(stream.getvalue(), dtype=np.uint8)
                # 通过opencv解码numpy

                img = cv2.imdecode(data, 1)
                #img =cvDrawBoxes(DETE_DATA,img)
                if 1 == open_ret:
                    cv2.imshow("video", img)
                    cv2.moveWindow("video", 50, 50)
                    cv2.waitKey(50)
                stream.seek(0)
                # 将数据流的指针指向起始位置
                connection.write(stream.read())
                if time.time() - start > 600:
                    break
                # 重置捕获流，等待下一次捕获图像
                stream.seek(0)
                stream.truncate()
            connection.write(struct.pack('<L', 0))
    finally:
        connection.close()
        client_socket.close()

def convertBack(x, y, w, h):
    xmin = int(round(x - (w / 2)))
    xmax = int(round(x + (w / 2)))
    ymin = int(round(y - (h / 2)))
    ymax = int(round(y + (h / 2)))
    return xmin, ymin, xmax, ymax


def cvDrawBoxes(detections, img):
    for detection in detections:
        x, y, w, h = detection[2][0],\
            detection[2][1],\
            detection[2][2],\
            detection[2][3]
        xmin, ymin, xmax, ymax = convertBack(
            float(x), float(y), float(w), float(h))
        pt1 = (xmin, ymin)
        pt2 = (xmax, ymax)
        cv2.rectangle(img, pt1, pt2, (0, 255, 0), 1)
        cv2.putText(img,
                    detection[0] +
                    " [" + str(round(detection[1] * 100, 2)) + "]",
                    (pt1[0], pt1[1] - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                    [0, 255, 0], 2)
    return img
def show_photo_inPI(client_socket):
    global DETE_DATA
    while True:
        data = client_socket.recv(1024)
        detection_res = str(data,encoding="utf-8")
        detection_res = detection_res.split(',')
        detections = []
        for p in range(int(len(detection_res) / 6)):
            temp1 = (
                detection_res[0 + p * 6][4:-1],
                float(detection_res[1 + p * 6]),
                (float(detection_res[2 + p * 6].replace('(', '')), float(detection_res[3 + p * 6]),
                 float(detection_res[4 + p * 6]),
                 float(detection_res[5 + p * 6].replace(')', '').replace(']', ''))))
            detections.append(temp1)

        DETE_DATA = detections





# ip ='192.168.219.32'
# port =  8000
# Client_(ip,port)
