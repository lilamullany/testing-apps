import cv2 as cv
import edgeiq
import time
import numpy as np
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

                results = semantic_segmentation.segment_image(frame)

                # Generate text to display on streamer
                text = ["Model: {}".format(semantic_segmentation.model_id)]
                text.append("Inference time: {:1.3f} s".format(results.duration))
                text.append("Legend:")
                text.append(semantic_segmentation.build_legend())


                # build the color mask, making all colors the same except for background
                semantic_segmentation.colors = [ (0,0,0) for i in semantic_segmentation.colors]

                index = semantic_segmentation.labels.index("person")
                semantic_segmentation.colors[index] = (255,255,255)
                mask = semantic_segmentation.build_image_mask(results.class_map)

                # apply smoothing to the mask
                blurred_mask = cv.blur(mask, (100, 100))

                # apply the color mask to the image
                blended = edgeiq.blend_images(frame, blurred_mask, alpha=0.5)

                # threshold to get back to a two-color mask and cut out the image where color != black
                blended[blended > 128] = 1

                # just the part of the map that is people
                detection_map = (blended == 1)

                if blur:
                    new_frame = cv.blur(frame, (100, 100))

                else:
                    # read in the image
                    img = cv.imread('./images/mountain_pic.jpg')

                    # get 2D the dimensions of the frame (need to reverse for compatibility with cv2)
                    shape = frame.shape[:2]

                    # resize the image
                    new_frame = cv.resize(img, (shape[1], shape[0]), interpolation=cv.INTER_NEAREST)

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
