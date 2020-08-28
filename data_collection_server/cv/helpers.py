
import os
import time

def file_set_up(sample_type):
    folder = "Images" if sample_type == "image" else "Videos"
    date_time = time.strftime("%d%H%M%S", time.localtime())
    
    if not os.path.exists('samples'):
        os.mkdir('samples')

    if not os.path.exists('samples/{}'.format(folder)):
        os.mkdir('samples/{}'.format(folder))

    os.mkdir('samples/{}/{}'.format(folder, date_time))

    file_name = 'samples/{}/{}/{}'.format(folder, date_time, time.asctime().replace(" ", "_") + ".avi")
    return file_name