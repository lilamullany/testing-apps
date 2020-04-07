import time
import numpy as np

class ContrabandSummary:
    def __init__(self):
        self.contraband_detections = []


    def contraband_alert(self, contraband, frame):
        """
        Prints the detection to the console. Input frame can be saved to disk.

        Parameters
        -------
        contraband : string
            The label of the detected object

        frame: []
            A numpy array of the moment the contraband was detected
        """
        detect_time = time.localtime()
        self.contraband_detections.append((contraband, detect_time, frame))
        items = self.get_contraband_string()
        
        print(*items)


    def get_contraband_string(self):
        """
        Returns a list of strings describing all of the detected contraband

        Returns
        -------
        []
            A list of text describing all of the detected contraband and the time of detection
        """
        contraband_string = [""]
        for contraband, detect_time, frame in self.contraband_detections:
            string_time = time.strftime('%Y-%m-%d %H:%M:%S', detect_time)
            contraband_string.append(contraband + " detected at " + string_time + "\n")
        return contraband_string


