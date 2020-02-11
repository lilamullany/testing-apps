import time
import edgeiq
"""
Simultaneously utilize two object detection models and present results to shared
output stream.

To change the computer vision model, follow this guide:
https://dashboard.alwaysai.co/docs/application_development/changing_the_model.html

To change the engine and accelerator, follow this guide:
https://dashboard.alwaysai.co/docs/application_development/changing_the_engine_and_accelerator.html
"""


def main():

    models = ["alwaysai/mobilenet_ssd", "alwaysai/ssd_inception_v2_coco_2018_01_28"]
    
    colors = [(52, 64, 235), (82, 235, 52)]

    objects = []

    # load all the models
    for model in models:

        # start up a first object detection model
        obj_detect = edgeiq.ObjectDetection(model)
        obj_detect.load(engine=edgeiq.Engine.DNN)

        # track the generated object detection items by storing them in objects
        objects.append(obj_detect)

        print("Model:\n{}\n".format(obj_detect.model_id))
        print("Engine: {}".format(obj_detect.engine))
        print("Accelerator: {}\n".format(obj_detect.accelerator))
        print("Labels:\n{}\n".format(obj_detect.labels))

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

                text = [""]

                # gather data from the all the objects 
                for i in range(0, len(objects)):
                    results = objects[i].detect_objects(
                        frame, confidence_level=.5)
                    frame = edgeiq.markup_image(
                        frame, results.predictions, show_labels=False, colors=colors[i]) 
                    
                    #text.append("Model: {}".format(objects[i].model_id))
                    #text.append(
                            #"Inference time: {:1.3f} s".format(results.duration))
                    #text.append("Objects:")

                    # append each prediction
                    for prediction in results.predictions:
                        text.append("({}) {}: {:2.2f}%".format(objects[i].model_id,
                            prediction.label, prediction.confidence * 100))

                
                # send the image frame and the predictions for both 
                # prediction models to the output stream
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
