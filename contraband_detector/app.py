import time
import edgeiq
from contraband_summary import ContrabandSummary 
"""
Detect items that are considered contraband for working or learning 
from home, namely cell phones, headphones, books, etc. 

This example app uses two detection models in order to increase the
number of detections as well as the types of detections. The models this 
app uses are "alwaysai/ssd_mobilenet_v2_oidv4" and 
"alwaysai/ssd_inception_v2_coco_2018_01_28".

Additionally, this app uses a object tracker, which reduces the overhead 
associated with inference time and lessens the strain on your deployment device. 

To change the computer vision model, follow this guide:
https://dashboard.alwaysai.co/docs/application_development/changing_the_model.html

To change the engine and accelerator, follow this guide:
https://dashboard.alwaysai.co/docs/application_development/changing_the_engine_and_accelerator.html
"""

def main():

    # The current frame index
    frame_idx = 0

    # The number of frames to skip before running detector
    detect_period = 50

    # if you would like to test an additional model, add one to the list below:
    models = ["alwaysai/ssd_mobilenet_v2_oidv4","alwaysai/ssd_inception_v2_coco_2018_01_28"]

    # include any labels that you wish to detect from any models (listed above in 'models') here in this list
    detected_contraband = ["Pen", "cell phone", "backpack", "book", "Book", "Ring binder", "Headphones", "Calculator", "Mobile phone", 
    "Telephone", "Microphone", "Ipod", "Remote control"]

    # load all the models (creates a new object detector for each model)
    detectors = []
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
    contraband_summary = ContrabandSummary()

    try:
        with edgeiq.WebcamVideoStream(cam=0) as video_stream, \
                edgeiq.Streamer() as streamer:
            
            # Allow Webcam to warm up
            time.sleep(2.0)
            fps.start()

            # loop detection
            while True:
                frame = video_stream.read()
                predictions_to_markup = []
                text = [""]

                # only analyze every 'detect_period' frame (i.e. every 50th in original code)
                if frame_idx % detect_period == 0:

                    # gather data from the all the detectors 
                    for i in range(0, len(detectors)):
                        results = detectors[i].detect_objects(
                            frame, confidence_level=.2)

                        # Stop tracking old objects
                        if tracker.count:
                            tracker.stop_all()

                        # append each prediction
                        predictions = results.predictions
                        for prediction in predictions:

                            if (prediction.label.strip() in detected_contraband):
                                contraband_summary.contraband_alert(prediction.label, frame)
                                predictions_to_markup.append(prediction)
                                tracker.start(frame, prediction) 
                else:

                    # if there are objects being tracked, update the tracker with the new frame
                    if tracker.count:

                        # get the new predictions for the objects being tracked, used to markup the frame
                        predictions_to_markup = tracker.update(frame)

                # mark up the frame with the predictions for the contraband objects
                frame = edgeiq.markup_image(
                        frame, predictions_to_markup, show_labels=True,
                        show_confidences=False, colors=obj_detect.colors)
                   
                # send the collection of contraband detection points (string and video frame) to the streamer
                text = contraband_summary.get_contraband_string()
                
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
