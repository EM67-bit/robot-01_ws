import cv2
from flask import Flask, Response

app = Flask(__name__)

def gen_frames():
    cap = cv2.VideoCapture(0, cv2.CAP_V4L2)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))

    while True:
        success, frame = cap.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    return '''
    <html>
        <head>
            <title>Robot-01 Live Stream</title>
            <style>
                body { 
                    background-color: #111; 
                    margin: 0; 
                    display: flex; 
                    flex-direction: column;
                    align-items: center; 
                    justify-content: center;
                    height: 100vh;
                    color: #0f0;
                    font-family: 'Courier New', Courier, monospace;
                }
                h1 { margin-bottom: 10px; font-size: 24px; text-transform: uppercase; letter-spacing: 2px; }
                .stream-container {
                    width: 90%;
                    max-width: 1200px;
                    border: 4px solid #333;
                    box-shadow: 0 0 20px rgba(0, 255, 0, 0.2);
                    line-height: 0;
                }
                img {
                    width: 100%;
                    height: auto;
                }
            </style>
        </head>
        <body>
            <h1>SYSTEM ACTIVE: ROBOT-01 FEED</h1>
            <div class="stream-container">
                <img src="/video_feed">
            </div>
        </body>
    </html>
    '''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)