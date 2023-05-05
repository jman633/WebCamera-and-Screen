import cv2
from flask import Flask, render_template, Response

app = Flask(__name__,template_folder='templates')

camera = cv2.VideoCapture(0)

def generate_frames():
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)  
            frame = buffer.tobytes()  
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n') 

@app.route('/')
def index():
    return render_template('index.html')  

@app.route('/video_feed/<string:camera>')
def video_feed(source):
    # код для получения видео потока
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='192.168.1.36', port=5000, debug=True) # Стандарт - 192.168.1.36 , port=5000
