from vidgear.gears import ScreenGear
import cv2
from flask import Flask, render_template, Response

app = Flask(__name__,template_folder='templates')

camera = cv2.VideoCapture(0)

options = {"top": 0, "left": 0, "width": 1920, "height": 1080}
screen_stream = ScreenGear(monitor=1, logging=True, **options).start()

def generate_screen_frames():
    while True:
        frame = screen_stream.read()
        if frame is not None and frame.shape[0] > 0 and frame.shape[1] > 0:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        else:
            break

def generate_camera_frames():
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

@app.route('/screen_feed')
def screen_feed():
    return Response(generate_screen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/camera_feed')
def camera_feed():
    return Response(generate_camera_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
     app.run(host='localhost', port=5500, debug=True)