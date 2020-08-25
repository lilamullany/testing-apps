import time
import edgeiq
import argparse
import socketio
import cv2
import base64
import os
"""
Use object detection to detect objects in the frame in realtime. The
types of objects detected can be changed by selecting different models.

To change the computer vision model, follow this guide:
https://dashboard.alwaysai.co/docs/application_development/changing_the_model.html

To change the engine and accelerator, follow this guide:
https://dashboard.alwaysai.co/docs/application_development/changing_the_engine_and_accelerator.html
"""

class SampleWriter(object):
    def __init__(self):
        self.write = False
        self.text = ""

sio = socketio.Client()
writer = SampleWriter()
SAMPLE_RATE = 5
streamer = None


@sio.event
def connect():
    print('[INFO] Successfully connected to server.')


@sio.event
def connect_error():
    print('[INFO] Failed to connect to server.')


@sio.event
def disconnect():
    print('[INFO] Disconnected from server.')

@sio.on('write_data', namespace='/cv')
def write_data(data):
    writer.write = True
    writer.text = 'Data Collection Started!'
    time.sleep(0.5)
    print('start signal received')
    file_name = file_set_up()

    with edgeiq.WebcamVideoStream(cam=0) as video_stream, edgeiq.VideoWriter(
            file_name, fps=SAMPLE_RATE) as video_writer:
        
        if SAMPLE_RATE > video_stream.fps:
            raise RuntimeError(
                "Sampling rate {} cannot be greater than the camera's FPS {}".
                format(SAMPLE_RATE, video_stream.fps))

        time.sleep(2.0)

        print('Data Collection Started!')
        while True:
            t_start = time.time()
            frame = video_stream.read()
            video_writer.write_frame(frame)
            #streamer.send_data(frame, None)
            t_end = time.time() - t_start
            t_wait = (1 / SAMPLE_RATE) - t_end
            if t_wait > 0:
                time.sleep(t_wait)

            if not writer.write:
                writer.text = 'Data Collection Ended'
                time.sleep(0.5)
                print('Data Collection Ended')
                break

@sio.on('stop_writing', namespace='/cv')
def stop_writing(data):
    writer.write = False
    print('stop signal received')

@sio.on('take_snapshot', namespace='/cv')
def take_snapshot(data):
    print('snapshot signal received')
    file_name = file_set_up()
    with edgeiq.WebcamVideoStream(cam=0) as video_stream, edgeiq.VideoWriter(
            file_name, fps=SAMPLE_RATE) as video_writer:

        time.sleep(2.0)
        writer.text = 'Taking Snapshot'
        time.sleep(1.0)
        print('Taking Snapshot')
        frame = video_stream.read()
        video_writer.write_frame(frame)
        writer.text = 'Snapshot Saved'
        time.sleep(0.5)
        print('Snapshot Saved')

def file_set_up():
    if not os.path.exists('samples'):
        os.mkdir('samples')

    date_time = time.strftime("%d%H%M%S", time.localtime())

    os.mkdir('samples/{}'.format(date_time))

    file_name = 'samples/{}/{}'.format(date_time, time.asctime().replace(" ", "_") + ".avi")
    return file_name

class CVClient(object):
    def __init__(self, server_addr, stream_fps):
        self.server_addr = server_addr
        self.server_port = 5001
        self._stream_fps = stream_fps
        self._last_update_t = time.time()
        self._wait_t = (1/self._stream_fps)

    def setup(self):
        print('[INFO] Connecting to server http://{}:{}...'.format(
            self.server_addr, self.server_port))
        sio.connect(
                'http://{}:{}'.format(self.server_addr, self.server_port),
                transports=['websocket'],
                namespaces=['/cv', '/web'])
        time.sleep(1)
        return self

    def _convert_image_to_jpeg(self, image):
        # Encode frame as jpeg
        frame = cv2.imencode('.jpg', image)[1].tobytes()
        # Encode frame in base64 representation and remove
        # utf-8 encoding
        frame = base64.b64encode(frame).decode('utf-8')
        return "data:image/jpeg;base64,{}".format(frame)

    def send_data(self, frame, text):
        cur_t = time.time()
        if cur_t - self._last_update_t > self._wait_t:
            self._last_update_t = cur_t
            frame = edgeiq.resize(
                    frame, width=640, height=480, keep_scale=True)
            sio.emit(
                    'cv2server',
                    {
                        'image': self._convert_image_to_jpeg(frame),
                        'text': '<br />'.join(text)
                    })

    def check_exit(self):
        pass

    def close(self):
        sio.disconnect()


def main(camera, use_streamer, server_addr, stream_fps):
    obj_detect = edgeiq.ObjectDetection(
            "alwaysai/mobilenet_ssd")
    obj_detect.load(engine=edgeiq.Engine.DNN)

    print("Loaded model:\n{}\n".format(obj_detect.model_id))
    print("Engine: {}".format(obj_detect.engine))
    print("Accelerator: {}\n".format(obj_detect.accelerator))
    print("Labels:\n{}\n".format(obj_detect.labels))

    fps = edgeiq.FPS()

    try:
        if use_streamer:
            streamer = edgeiq.Streamer().setup()
        else:
            streamer = CVClient(server_addr, stream_fps).setup()

        with edgeiq.WebcamVideoStream(cam=camera) as video_stream:
            # Allow Webcam to warm up
            time.sleep(2.0)
            fps.start()
            
            # loop detection
            while True:
                frame = video_stream.read()
                #results = obj_detect.detect_objects(frame, confidence_level=.5)
                #frame = edgeiq.markup_image(
                        #frame, results.predictions, colors=obj_detect.colors)

                # Generate text to display on streamer
                text = [""]
                #text.append(
                        #"Inference time: {:1.3f} s".format(results.duration))
                text.append(writer.text)

                #for prediction in results.predictions:
                    #text.append("{}: {:2.2f}%".format(
                        #prediction.label, prediction.confidence * 100))

                streamer.send_data(frame, text)

                fps.update()

                if streamer.check_exit():
                    break

    finally:
        if streamer is not None:
            streamer.close()
        fps.stop()
        print("elapsed time: {:.2f}".format(fps.get_elapsed_seconds()))
        print("approx. FPS: {:.2f}".format(fps.compute_fps()))

        print("Program Ending")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='alwaysAI Video Streamer')
    parser.add_argument(
            '--camera', type=int, default='0',
            help='The camera index to stream from.')
    parser.add_argument(
            '--use-streamer',  action='store_true',
            help='Use the embedded streamer instead of connecting to the server.')
    parser.add_argument(
            '--server-addr',  type=str, default='localhost',
            help='The IP address or hostname of the SocketIO server.')
    parser.add_argument(
            '--stream-fps',  type=float, default=20.0,
            help='The rate to send frames to the server.')
    args = parser.parse_args()
    main(args.camera, args.use_streamer, args.server_addr, args.stream_fps)
