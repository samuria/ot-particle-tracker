from __future__ import division, unicode_literals, print_function

import base64
from io import BytesIO
import os
import utilities

import matplotlib as mpl
import numpy as np
import pims
import trackpy as tp

mpl.use('Agg')

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import matplotlib.pyplot as plt


class VideoAnalyser:
    def __init__(self):
        self.micron_per_pixel = 0.15192872980868
        self.feature_diameter = 2.8  # um
        self.radius = int(np.round(self.feature_diameter / 2.0 / self.micron_per_pixel))
        if self.radius % 2 == 0:
            self.radius + 1

        self.frames = pims.as_gray(pims.Video('core/sample.mp4'))

    def set_tracking_properties(self, mpp, fd):
        self.micron_per_pixel = mpp
        self.feature_diameter = fd
        self.radius = int(np.round(float(fd) / 2.0 / float(mpp)))

    def get_tracking_properties(self):
        return {
            'mpp': self.micron_per_pixel,
            'fd': self.feature_diameter,
            'radius': self.radius
        }

    def create_figure(self, frame_id):
        fig, ax = plt.subplots()
        # for frame in np.arange(0, len(frames), 50):  # show every 50th frame to keep file size low
        f_locate = tp.locate(self.frames[frame_id], self.radius + 2, minmass=600, invert=True)
        tp.annotate(f_locate, self.frames[frame_id], plot_style={'markersize': self.radius}, ax=ax)

        canvas = FigureCanvas(fig)
        output = BytesIO()
        canvas.print_png(output)

        return base64.b64encode(output.getvalue()).decode('utf8')

    def set_video(self, video):
        print(os.path.join(utilities.UPLOAD_DIR, video))
        self.frames = pims.as_gray(pims.Video(os.path.join(utilities.UPLOAD_DIR, video)))
