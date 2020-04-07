import time
import numpy as np

class ContrabandSummary:
	def __init__(self):
		self.contraband_detections = []


	def contraband_alert(self, contraband, frame):
		"""
        Appends the contraband item, the time the alert was called, and the frame
        to the list of detected contraband.

        Parameters
        -------
        contraband : string
            The label of the detected object

        frame: []
        	A numpy array of the moment the contraband was detected
        """
		new_tuple = (contraband, time.localtime(), frame)
		self.contraband_detections.append(new_tuple)


	def get_contraband_frame_summary(self):
		"""
        Returns all of the frames when a contraband item was detected

        Returns
        -------
        []
            The concatenated numpy array of all stored detection frames
        """
		if self.contraband_detections:
			new_frame = self.contraband_detections[0][2]
			for contraband, time, frame in self.contraband_detections:
				new_frame = np.concatenate((new_frame, frame))
			return new_frame


	def get_contraband_objects_summary(self):
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


