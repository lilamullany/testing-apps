
import os
import time

"""
Helper functions not associated with a particular
class are defined here for modularity.
"""


def file_set_up(sample_type):
    """Takes in a file type, either
    'image' or 'video', creates a new folder for the
    data to be stored and returns the name of the file.

    Args:
        sample_type (string): either 'image' or 'video'

    Returns:
        string: name of newly created folder and filename
    """
    folder = "Images" if sample_type == "image" else "Videos"
    date_time = time.strftime("%d%H%M%S", time.localtime())
    
    if not os.path.exists('samples'):
        os.mkdir('samples')

    if not os.path.exists('samples/{}'.format(folder)):
        os.mkdir('samples/{}'.format(folder))

    os.mkdir('samples/{}/{}'.format(folder, date_time))

    file_name = 'samples/{}/{}/{}'.format(folder, date_time, time.asctime().replace(" ", "_") + ".avi")
    return file_name