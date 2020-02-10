import time
import edgeiq
"""
Use object detection to detect human faces and to classification to classify 
detected faces in terms of age groups simultaneously, and output results to 
shared output stream.

To change the computer vision model, follow this guide:
https://dashboard.alwaysai.co/docs/application_development/changing_the_model.html

To change the engine and accelerator, follow this guide:
https://dashboard.alwaysai.co/docs/application_development/changing_the_engine_and_accelerator.html
"""


def main():

    # first make a detector to detect facial objects
    facial_detector = edgeiq.ObjectDetection(
            "alwaysai/res10_300x300_ssd_iter_140000")
    facial_detector.load(engine=edgeiq.Engine.DNN)

    # make a classifer to classify the age of the image
    classifier = edgeiq.Classification("alwaysai/agenet")
    classifier.load(engine=edgeiq.Engine.DNN)

    print("Engine: {}".format(facial_detector.engine))
    print("Accelerator: {}\n".format(facial_detector.accelerator))
    print("Model:\n{}\n".format(facial_detector.model_id))

    fps = edgeiq.FPS()

    try:
        with edgeiq.WebcamVideoStream(cam=0) as video_stream, \
                edgeiq.Streamer() as streamer:
            # Allow Webcam to warm up
            time.sleep(2.0)
            fps.start()

            # loop detection
            while True:
                frame = video_stream.read()

                # detect human faces
                results = facial_detector.detect_objects(
                        frame, confidence_level=.5)
                frame = edgeiq.markup_image(
                        frame, results.predictions, show_labels=False)  

                # generate labels to display the facial detections on the streamer output
                text = ["Model: {}".format(facial_detector.model_id)]
                text.append(
                        "Inference time: {:1.3f} s".format(results.duration))
                text.append("Objects:")

                # append each predication 
                for prediction in results.predictions:
                    text.append("{}: {:2.2f}%".format(
                        prediction.label, prediction.confidence * 100))

                # attempt to classify the image in terms of age
                age_results = classifier.classify_image(frame)

                # if there are predictions for the age classification,
                # generate these labels for the output stream
                if age_results.predictions:
                    text.append("Label: {}, {:.2f}".format(
                        age_results.predictions[0].label,
                        age_results.predictions[0].confidence))
                else:
                    text.append("No age predication")    
                
                # send the image frame and the predictions to the output stream
                streamer.send_data(frame, text)

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
