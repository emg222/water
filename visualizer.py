#!/usr/bin/env python

"""
Visualize shallow water simulation results.

NB: Requires a modern Matplotlib version; also needs
 either FFMPeg (for MP4) or ImageMagick (for GIF)
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as manimation
import sys


def main(infile="waves.out", outfile="out.mp4", startpic="start.png"):
    """Visualize shallow water simulation results.

    Args:
        infile: Name of input file generated by simulator
        outfile: Desired output file (mp4 or gif)
        startpic: Name of picture generated at first frame
    """

    u = np.fromfile(infile, dtype=np.dtype('f4'))
    nx = int(u[0])
    ny = int(u[1])
    x = range(0,nx)
    y = range(0,ny)
    u = u[2:]
    nframe = len(u) // (nx*ny)
    stride = nx // 20
    u = np.reshape(u, (nframe,nx,ny))
    X, Y = np.meshgrid(x,y)

    fig = plt.figure(figsize=(10,10))

    def plot_frame(i, stride=5):
        ax = fig.add_subplot(111, projection='3d')
        ax.set_zlim(0, 2)
        Z = u[i,:,:];
        ax.plot_surface(X, Y, Z, rstride=stride, cstride=stride)
        return ax

    if startpic:
        ax = plot_frame(0)
        plt.savefig(startpic)
        plt.delaxes(ax)

    metadata = dict(title='Wave animation', artist='Matplotlib')
    if outfile[-4:] == ".mp4":
        Writer = manimation.writers['ffmpeg']
        writer = Writer(fps=15, metadata=metadata,
                        extra_args=["-r", "30",
                                    "-c:v", "libx264",
                                    "-pix_fmt", "yuv420p"])
    elif outfile[-4:] == ".gif":
        Writer = manimation.writers['imagemagick']
        writer = Writer(fps=15, metadata=metadata)

    with writer.saving(fig, outfile, nframe):
        for i in range(nframe):
            ax = plot_frame(i)
            writer.grab_frame()
            plt.delaxes(ax)


if __name__ == "__main__":
    main(*sys.argv[1:])
