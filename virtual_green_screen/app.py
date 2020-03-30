import edgeiq
import time
import numpy as np
import cv2 as cv
import os
import json
"""
Use semantic segmentation to determine a class for each pixel of an image.
This particular example app uses semantic segmentation to cut a person out
of a frame and either blur the background or replace the background with an
image.

To change the computer vision model, follow this guide:
https://dashboard.alwaysai.co/docs/application_development/changing_the_model.html
To change the engine and accelerator, follow this guide:
https://dashboard.alwaysai.co/docs/application_development/changing_the_engine_and_accelerator.html
"""
CONFIG_FILE = "config.json"
SEGMENTER = "segmenter"
MODEL_ID = "model_id"
BACKGROUND_IMAGES = "background_images"
IMAGE = "image"
TARGETS = "target_labels"
BLUR = "blur"

def load_json(filepath):
    # check that the file exsits and return the loaded json data
    if os.path.exists(filepath) == False:
        raise Exception('File at {} does not exist'.format(filepath))

    with open(filepath) as data:
        return json.load(data)

def main():
    # load the configuration data from config.json
    config = load_json(CONFIG_FILE)
    labels_to_mask = config.get(TARGETS)
    model_id = config.get(MODEL_ID)
    background_image = config.get(BACKGROUND_IMAGES) + config.get(IMAGE)
    blur = config.get(BLUR)

    semantic_segmentation = edgeiq.SemanticSegmentation(model_id)
    semantic_segmentation.load(engine=edgeiq.Engine.DNN)

    print("Engine: {}".format(semantic_segmentation.engine))
    print("Accelerator: {}\n".format(semantic_segmentation.accelerator))
    print("Model:\n{}\n".format(semantic_segmentation.model_id))
    print("Labels:\n{}\n".format(semantic_segmentation.labels))

    fps = edgeiq.FPS()

    try:
        with edgeiq.WebcamVideoStream(cam=0) as video_stream, \
                edgeiq.Streamer() as streamer:

            # Allow Webcam to warm up
            time.sleep(2.0)
            fps.start()

            # loop detection
            while True:
                # read in the video stream
                frame = video_stream.read()

                segmentation_results = semantic_segmentation.segment_image(frame)

                # Generate text to display on streamer
                text = ["Model: {}".format(semantic_segmentation.model_id)]
                text.append("Inference time: {:1.3f} s".format(segmentation_results.duration))

                label_map = np.array(semantic_segmentation.labels)[segmentation_results.class_map]

                filtered_class_map = np.zeros(segmentation_results.class_map.shape).astype(int)

                for label in labels_to_mask:
                    filtered_class_map += segmentation_results.class_map * (label_map == label).astype(int)

                # just the part of the map that is people
                detection_map = (filtered_class_map != 0)

                if blur:
                    # blur the background:
                    new_frame = cv.blur(frame, (100, 100))

                else:
                    # read in the image
                    img = cv.imread(background_image)

                    # get 2D the dimensions of the frame (need to reverse for compatibility with cv2)
                    shape = frame.shape[:2]

                    # resize the image
                    new_frame = cv.resize(img, (shape[1], shape[0]), interpolation=cv.INTER_NEAREST)

                # replace the area of the new frame that corresponds to the person in the original
                new_frame[detection_map] = frame[detection_map].copy()
                streamer.send_data(new_frame, text)

                fps.update()

                if streamer.check_exit():
                    break

    finally:
        fps.stop()
        print("elapsed time: {:.2f}".format(fps.get_elapsed_seconds()))
        print("approx. FPS: {:.2f}".format(fps.compute_fps()))

        print("Program Ending")


if __name__ == "__main__":
    main()