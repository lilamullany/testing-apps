import cv2
import edgeiq
import time
import numpy as np
import cv2 as cv
"""
Use semantic segmentation to determine a class for each pixel of an image.
The classes of objects detected can be changed by selecting different models.
This particular starter application uses a model on the cityscape
dataset (https://www.cityscapes-dataset.com/).
The Cityscapes Dataset focuses on semantic understanding of urban street scenes,
and is a favorite dataset for building autonomous car machine learning models.

Different images can be used by updating the files in the *images/*
directory. Note that when developing for a remote device, removing
images in the local *images/* directory won't remove images from the
device. They can be removed using the `aai app shell` command and
deleting them from the *images/* directory on the remote device.

To change the computer vision model, follow this guide:
https://dashboard.alwaysai.co/docs/application_development/changing_the_model.html

To change the engine and accelerator, follow this guide:
https://dashboard.alwaysai.co/docs/application_development/changing_the_engine_and_accelerator.html
"""


def main():
    semantic_segmentation = edgeiq.SemanticSegmentation(
            "alwaysai/fcn_alexnet_pascal_voc")
    semantic_segmentation.load(engine=edgeiq.Engine.DNN)

    obj_detect = edgeiq.ObjectDetection("alwaysai/mobilenet_ssd")
    obj_detect.load(engine=edgeiq.Engine.DNN)

    labels_to_mask = ['person']

    print("Engine: {}".format(semantic_segmentation.engine))
    print("Accelerator: {}\n".format(semantic_segmentation.accelerator))
    print("Model:\n{}\n".format(semantic_segmentation.model_id))
    print("Labels:\n{}\n".format(semantic_segmentation.labels))

    # descriptions printed to console
    print("Engine: {}".format(obj_detect.engine))
    print("Accelerator: {}\n".format(obj_detect.accelerator))
    print("Model:\n{}\n".format(obj_detect.model_id))

    fps = edgeiq.FPS()

    try:
        with edgeiq.WebcamVideoStream(cam=0) as video_stream, \
                edgeiq.Streamer() as streamer:

            # Allow Webcam to warm up
            time.sleep(2.0)
            fps.start()

            last_non_detection = None


            # loop detection
            while True:


                # read in the video stream
                frame = video_stream.read()


                detector_results = obj_detect.detect_objects(frame, confidence_level=.1)

                if last_non_detection is None:
                    last_non_detection = np.zeros(frame.shape)


                segmentation_results = semantic_segmentation.segment_image(frame)



                # Generate text to display on streamer
                text = ["Model: {}".format(semantic_segmentation.model_id)]
                text.append("Inference time: {:1.3f} s".format(segmentation_results.duration))
                text.append("Legend:")
                text.append(semantic_segmentation.build_legend())

                label_map = np.array(semantic_segmentation.labels)[segmentation_results.class_map]

                filtered_class_map = np.zeros(segmentation_results.class_map.shape).astype(int)

                for label in labels_to_mask:
                    filtered_class_map += segmentation_results.class_map * (label_map == label).astype(int)



                # map that is people
                detection_map = (filtered_class_map != 0)


                # blur the background:
                blur_frame = cv.blur(frame, (50, 50))

                # create a new frame and replace pixels corresponding to the detected face
                new_frame = blur_frame
                new_frame[detection_map] = frame[detection_map].copy()
                #out_frame = edgeiq.blend_images(blur_frame, new_frame, 0.5)


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
