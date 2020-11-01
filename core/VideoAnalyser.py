from __future__ import division, unicode_literals, print_function

import base64
import os
import timeit
from io import BytesIO

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pims
import trackpy as tp
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import utilities

mpl.use('Agg')


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

        start_time = timeit.default_timer()
        f_locate = tp.locate(self.frames[frame_id], self.radius + 2, minmass=600, invert=True)
        elapsed = timeit.default_timer() - start_time

        tp.annotate(f_locate, self.frames[frame_id], plot_style={'markersize': self.radius}, ax=ax)

        canvas = FigureCanvas(fig)
        output = BytesIO()
        canvas.print_png(output)

        return {"image": base64.b64encode(output.getvalue()).decode('utf8'), "time_elapsed": elapsed,
                "feature_count": len(f_locate.index)}

    def set_video(self, video):
        print(os.path.join(utilities.UPLOAD_DIR, video))
        self.frames = pims.as_gray(pims.Video(os.path.join(utilities.UPLOAD_DIR, video)))

    def export_csv(self):
        data = tp.batch(self.frames, self.radius + 2, minmass=600, invert=True)
        return data.to_csv()
