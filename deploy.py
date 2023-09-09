from flask import Flask
from main import Extract
from flask import request
from PIL import Image
import io
import base64
import requests
import mysql.connector
from config import user, pwd, host

app = Flask(__name__)
model = Extract()

db = mysql.connector.connect(user=user, password = pwd, host=host)
mycursor = db.cursor()

def create_respone(result_json, errorCode, errorMessage):
    result = {
        'data': result_json,
        'errorCode': errorCode,
        'errorMessage': errorMessage
    }
    return result


@app.route("/hello")
def hello():
    return "Hello, Welcome to GeeksForGeeks"


@app.route('/predict', methods=['POST', 'GET'])
def predict():
    format_type = request.args.get('format_type', default='file')
    get_thumb = request.args.get('get_thumb', default='false')
    ret = {}
    if format_type in ['file', 'url']:
        if format_type == 'file':
            try:
                image = Image.open(io.BytesIO(request.files["img1"].read()))
            except:
                ret = create_respone({}, '3', 'Incorrect image format')
                return ret
        else:
            try:
                img1 = request.args.get('url')
                image = Image.open(requests.get(img1, stream=True).raw)
            except:
                ret = create_respone("", '2', 'Url is unavailable')
                return ret

        ret['data'], lst_img = model.predict(image)

        if lst_img is not None:
            code = 'INSERT INTO `INFO`.`info_cccd` (`id`, `name`, `address`, `residence`, `date`, `nationality`, `sex`) VALUES (%s, %s, %s, %s, %s, %s, %s)'
            val = [(ret['data']['id'], ret['data']['name'], ret['data']['add'], ret['data']['residence'],
                    ret['data']['date'], ret['data']['nationality'], ret['data']['sex'])]
            mycursor.executemany(code, val)
            db.commit()
            if get_thumb == 'true':
                for i in range(len(lst_img)):
                    img_base64 = base64.b64encode(lst_img[i])
                    ret['data']['image_' + str(i)] = img_base64.decode()
            else:
                ret['data']['image'] = ''
            ret['errorCode'] = '0'
            ret['errorMessage'] = 'Success'
        else:
            ret = create_respone("", '1', 'The photo does not contain content')
    else:
        ret = create_respone("", '6', 'Incorrect format type')
    return ret


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=False)
