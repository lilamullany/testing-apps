import time
import numpy as np

class ContrabandSummary:
    def __init__(self):
        self.contraband = ""


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
        self.contraband = contraband
        print(self.get_contraband_string())


    def get_contraband_string(self):
        """
        Returns a string describing all of the detected contraband

        Returns
        -------
        String
            A string describing all of the detected contraband and the time of detection
        """
        contraband_string = "contraband " + self.contraband + " detected at " + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        return contraband_string


