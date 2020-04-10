import time
import edgeiq
import numpy
from contraband_summary import ContrabandSummary 
"""
Simultaneously utilize two object detection models and present the results to
a single output stream.

The models used in this app are ssd_inception_v2_coco_2018_01_28, which can detect
numerous inanimate objects, such as bikes, utensils, animals, etc., and the
the mobilenet_ssd, which is a smaller library but detects some larger objects that
ssd_inception_v2_coco_2018_01_28 does not, such as a sofa, a train, or an airplane.

To change the computer vision model, follow this guide:
https://dashboard.alwaysai.co/docs/application_development/changing_the_model.html

To change the engine and accelerator, follow this guide:
https://dashboard.alwaysai.co/docs/application_development/changing_the_engine_and_accelerator.html
"""

def main():
    # The current frame index
    frame_idx = 0
    # The number of frames to skip before running detector
    detect_period = 30

    # if you would like to test an additional model, add one to the list below:
    models = ["alwaysai/ssd_mobilenet_v2_oidv4","alwaysai/ssd_inception_v2_coco_2018_01_28"]

    detected_contraband = ["Pen", "cell phone", "backpack", "book", "Book", "Ring binder", "Headphones", "Calculator", "Mobile phone", 
    "Telephone", "Microphone", "Ipod", "Remote control"]

    detectors = []

    contraband_summary = ContrabandSummary()

    # load all the models (creates a new object detector for each model)
    for model in models:

        # start up a first object detection model
        obj_detect = edgeiq.ObjectDetection(model)
        obj_detect.load(engine=edgeiq.Engine.DNN)

        # track the generated object detection items by storing them in detectors
        detectors.append(obj_detect)

        # print the details of each model to the console
        print("Model:\n{}\n".format(obj_detect.model_id))
        print("Engine: {}".format(obj_detect.engine))
        print("Accelerator: {}\n".format(obj_detect.accelerator))
        print("Labels:\n{}\n".format(obj_detect.labels))

    tracker = edgeiq.CorrelationTracker(max_objects=5)
    fps = edgeiq.FPS()

    try:
        with edgeiq.WebcamVideoStream(cam=0) as video_stream, \
                edgeiq.Streamer() as streamer:
            
            # Allow Webcam to warm up
            time.sleep(2.0)
            fps.start()
            frame_count = 0

            # loop detection
            while True:
                frame = video_stream.read()

                text = [""]

                predictions_to_markup = []

                if frame_idx % detect_period == 0:

                    # gather data from the all the detectors 
                    for i in range(0, len(detectors)):
                        results = detectors[i].detect_objects(
                            frame, confidence_level=.2)

                        # Stop tracking old objects
                        if tracker.count:
                            tracker.stop_all()

                        # append each prediction
                        for prediction in results.predictions:

                            if (prediction.label.strip() in detected_contraband):
                                contraband_summary.contraband_alert(prediction.label, frame)
                                predictions_to_markup.append(prediction)

                                #frame = edgeiq.markup_image(frame, predictions_to_markup) 
                                tracker.start(frame, prediction) 

                else:
                    if tracker.count:
                        predictions_to_markup = tracker.update(frame)

                frame = edgeiq.markup_image(
                        frame, predictions_to_markup, show_labels=True,
                        show_confidences=False, colors=obj_detect.colors)
                   
                # send the collection of contraband detection points (string and video frame) to the streamer
                text =contraband_summary.get_contraband_string()
                
                streamer.send_data(frame, text)
                frame_idx += 1
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
