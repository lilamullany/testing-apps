
import time
import cv2
import edgeiq
import base64

class CVClient(object):
    def __init__(self, server_addr, stream_fps, socket, writer):
        """The original code was created by Eric VanBuhler
        (https://github.com/alwaysai/video-streamer) and is modified here.

        Initializes a customizable streamer object that 
        communicates with a flask server via sockets. 

        Args:
            server_addr (string): The IP address or hostname of the SocketIO server.
            stream_fps (float): The rate to send frames to the server.
            socket (socketio.Client): [description]
            writer (Writer): [description]
        """
        self.server_addr = server_addr
        self.server_port = 5001
        self._stream_fps = stream_fps
        self._last_update_t = time.time()
        self._wait_t = (1/self._stream_fps)
        # give the cv client access to the socket and 
        # writer used in the cv application
        self.socket = socket
        self.writer = writer

    def setup(self):
        """[summary]

        Returns:
            CVClient: The CVClient object
        """
        print('[INFO] Connecting to server http://{}:{}...'.format(
            self.server_addr, self.server_port))
        self.socket.connect(
                'http://{}:{}'.format(self.server_addr, self.server_port),
                transports=['websocket'],
                namespaces=['/cv'])
        time.sleep(1)
        return self

    def _convert_image_to_jpeg(self, image):
        """Converts a numpy array image to JPEG

        Args:
            image (numpy array): The input image

        Returns:
            string: base64 encoded representation of the numpy array
        """
        # Encode frame as jpeg
        frame = cv2.imencode('.jpg', image)[1].tobytes()
        # Encode frame in base64 representation and remove
        # utf-8 encoding
        frame = base64.b64encode(frame).decode('utf-8')
        return "data:image/jpeg;base64,{}".format(frame)

    def send_data(self, frame, text):
        """Sends image and text to the flask server.

        Args:
            frame (numpy array): the image
            text (string): the text
        """
        cur_t = time.time()
        if cur_t - self._last_update_t > self._wait_t:
            self._last_update_t = cur_t
            frame = edgeiq.resize(
                    frame, width=640, height=480, keep_scale=True)
            self.socket.emit(
                    'cv2server',
                    {
                        'image': self._convert_image_to_jpeg(frame),
                        'text': '<br />'.join(text)
                    })

    def check_exit(self):
        """Checks if the writer object has had
        the 'close' variable set to True.

        Returns:
            boolean: value of 'close' variable
        """
        return self.writer.close

    def close(self):
        """Disconnects the cv client socket.
        """
        self.socket.disconnect()