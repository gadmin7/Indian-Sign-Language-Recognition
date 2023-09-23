#importing necessary libraries
import flask_restful as fr
from flask import Flask, render_template, make_response, request,Response
from werkzeug.utils import secure_filename
import flask

import cv2
import detection
from eng2isl import english_to_isl
from trans import lang_trans
from trans import pdf_trans
from trans import ocr_core


app = flask.Flask(__name__)
api = fr.Api(app)

camera = cv2.VideoCapture(0)

def gen_frames():  # generate frame by frame from camera
    while True:
        # Capture frame-by-frame
        success, frame = camera.read()  # read the camera frame
        if not success:
            break
        else:
            image=detection.detect(frame)#returned image
            ret, buffer = cv2.imencode('.jpg', image)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result

@app.route('/video_feed')
def video_feed():
    #Video streaming route. Put this in the src attribute of an img tag
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace;boundary=frame')

@app.route('/s2t')
def index():
    """Video streaming home page."""
    return render_template('signlangui.html')

class Home(fr.Resource):
    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('home.html'),200,headers)

class Text2sign(fr.Resource):
    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('text2sign.html'),200,headers)
    def post(self):
        headers = {'Content-Type': 'text/html'}
        text = flask.request.form['message']
        ret = english_to_isl(text)
        return make_response(render_template('text2sign.html',prediction = ret,input_message=text),200,headers)

class Translate(fr.Resource):
    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('trans.html'),200,headers)

    def post(self):
        headers = {'Content-Type': 'text/html'}
        string = flask.request.form['message']
        print(string)
        lang = flask.request.form['languages']
        print(lang)
        ret = lang_trans(string,lang)
        print(ret)
        return make_response(render_template('trans.html',prediction = ret,input_message=string,language=lang),200,headers)

class PdfTranslate(fr.Resource):
    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('pdftranslate.html'),200,headers)

    def post(self):
        headers = {'Content-Type': 'text/html'}
        pdf = request.files['file']
        pdf.save(secure_filename("test.pdf"))
        lang = request.form.get("languages")
        print("---------------------",lang)
        ans = pdf_trans("test.pdf",lang)
        print(ans)
        return make_response(render_template('pdftranslate.html',prediction = ans),200,headers)

class OCR(fr.Resource):
    def get(self):
        headers={'Content-Type':'text/html'}
        return make_response(render_template('ocrtranslate.html'),200,headers)
    def post(self):
        headers={'Content-Type':'text/html'}
        file=request.files['photo']
        file.save(secure_filename('test.jpg'))
        print(file)
        lang=request.form.get('languages')
        print(lang)
        ret=ocr_core("test.jpg",lang)
        print(ret)
        return make_response(render_template('ocrtranslate.html',prediction=ret),200,headers)

api.add_resource(Home,"/home")
api.add_resource(Text2sign,"/t2s")
api.add_resource(Translate,"/translate")
api.add_resource(PdfTranslate,"/pdftranslate")
api.add_resource(OCR,"/ocrtranslate")

if __name__ == "__main__":
    app.run(debug=True)
