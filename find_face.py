import cv2
import time
import base64

import similar_face

import win32api
import win32con


def contrastFace(img_dict):
    # 调用电脑本地摄像头，所以参数为0，如果有其他的摄像头可以调整参数为1，2
    capture = cv2.VideoCapture(0)
    # 使用内open cv内置的人脸识别分类器，缺点：智能检测正脸
    face_detector = cv2.CascadeClassifier('./face_xml/haarcascade_frontalface_default.xml')

    while True:
        # 获取一帧
        ret, frame = capture.read()
        # 将这帧转换为灰度图
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # 检测人脸
        faces = face_detector.detectMultiScale(gray, 1.3, 3)
        # faces = face_detector.detectMultiScale(gray)

        if len(str(faces)) > 2:

            image_jpg = cv2.imencode('.jpg', gray)[1]
            image_code = str(base64.b64encode(image_jpg), 'utf-8')

            img_dict_2 = {'image': image_code, 'image_type': 'BASE64', 'face_type': 'LIVE', 'quality_control': 'LOW'}

            res = similar_face.checkFace(img_dict, img_dict_2)
            result = res.get('result')
            if result:
                score = result.get('score')
                # 设定人脸相似度阈值
                if score >= 80:
                    print('检测到设定的人脸')
                    # 按下 win+d
                    win32api.keybd_event(0x5B, 0, 0, 0)  # win键位码是0x5B
                    win32api.keybd_event(68, 0, 0, 0)  # d键位码是86
                    win32api.keybd_event(68, 0, win32con.KEYEVENTF_KEYUP, 0)  # 释放按键
                    win32api.keybd_event(0x5B, 0, win32con.KEYEVENTF_KEYUP, 0)
                    break

        for (x, y, w, h) in faces:
            res = cv2.rectangle(gray, (x, y), (x + w, y + w), (255, 0, 0))
            # print(res)

        # 显示摄像头图像
        # cv2.imshow('frame', gray)

        time.sleep(1)
        # 按下按键 q 退出
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # 关闭摄像头
    capture.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    # 设定目标人脸
    file_path_1 = './face_base/ymg001.png'

    img_dict_1 = similar_face.encodeImg(file_path_1)

    contrastFace(img_dict=img_dict_1)
