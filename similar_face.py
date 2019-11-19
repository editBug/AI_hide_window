import requests
import json
import base64
import imghdr


# 获取人脸相似度检测接口 token
def getToken():
    # client_id 为官网获取的AK， client_secret 为官网获取的SK
    # host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=【官网获取的AK】&client_secret=【官网获取的SK】'
    # 百度AI人脸相似度检测，免费接口需要自己申请
    url = 'https://aip.baidubce.com/oauth/2.0/token'
    header = {
        'Content-Type': 'application/json',
    }

    data = {
        'grant_type': 'client_credentials',
        'client_id': '替换为自己的 client_id',
        'client_secret': '替换为自己的 client_secret'
    }
    res_raw = requests.post(url=url, data=data, headers=header).content.decode('utf-8')
    if (res_raw):
        content = json.loads(res_raw)
        # print(content)

        access_token = content.get('access_token')
        if access_token:
            return {'access_token': access_token, 'res': 1}
        else:
            return {'res': 0}
    else:
        return {'res': 0}


# 将本地图像文件转换成 base64 编码
def encodeImg(file_path):
    with open(file_path, 'rb') as f:
        data = f.read()

    encodestr = base64.b64encode(data)
    base64_img = str(encodestr, 'utf-8')

    img_dict = {
        'image': base64_img,
        'image_type': 'BASE64',
        'face_type': 'LIVE',
        'quality_control': 'LOW',
    }

    return img_dict


# 检验脸部相似度
def checkFace(img_dict_1, img_dict_2):
    token_dict_res = getToken()
    access_token = token_dict_res.get('access_token')

    request_url = "https://aip.baidubce.com/rest/2.0/face/v3/match" + "?access_token=" + access_token
    # print(request_url)

    header = {
        'Content-Type': 'application/json',
    }

    img_list = [img_dict_1, img_dict_2]

    data = json.dumps(img_list)

    res_raw = requests.post(url=request_url, data=data, headers=header).content.decode('utf-8')
    res_dict = json.loads(res_raw)

    if res_dict:
        return res_dict
    else:
        return {'res': False}


if __name__ == '__main__':
    file_path_1 = './face_base/001.png'
    file_path_2 = './face_base/002.png'

    img_dict_1 = encodeImg(file_path_1)
    img_dict_2 = encodeImg(file_path_2)

    checkFace(img_dict_1, img_dict_2)
