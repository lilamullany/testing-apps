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

    labels_to_mask = ['person']

    print("Engine: {}".format(semantic_segmentation.engine))
    print("Accelerator: {}\n".format(semantic_segmentation.accelerator))
    print("Model:\n{}\n".format(semantic_segmentation.model_id))
    print("Labels:\n{}\n".format(semantic_segmentation.labels))

    fps = edgeiq.FPS()

    blur = False

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
                text.append("Legend:")
                text.append(semantic_segmentation.build_legend())

                label_map = np.array(semantic_segmentation.labels)[segmentation_results.class_map]

                filtered_class_map = np.zeros(segmentation_results.class_map.shape).astype(int)

                for label in labels_to_mask:
                    filtered_class_map += segmentation_results.class_map * (label_map == label).astype(int)


                # just the part of the map that is people
                detection_map = (filtered_class_map != 0)

                if blur:
                    # blur the background:
                    new_frame = cv.blur(frame, (50, 50))

                else:
                    # read in the image
                    img = cv.imread('./images/mountain_pic.jpg')

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