"""
Experiment at KWS-3 1300mm, March 2019
"""
import matplotlib
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.patches as patches
import bornagain as ba
from bornagain import nm

matplotlib.rcParams['image.cmap'] = 'jet'

wavelength = 12.8*ba.angstrom
alpha_i = 0.56*ba.degree

# detector setup as given from instrument responsible
npx, npy = 256, 256
pixel_size = 0.351  # in mm
detector_distance = 1300  # in mm
beam_xpos, beam_ypos = 129.05, 85.185# in pixels
xmin, ymin, xmax, ymax = 29, 48, 61, 80

f65569 = '00065569_0000_p15749_S3087-1.2dgr-rot0dgr_HRD_standard.det'
sensitivity_matrix = "sens.sens"

matplotlib.rcParams['xtick.labelsize'] = 16
matplotlib.rcParams['ytick.labelsize'] = 16
matplotlib.rcParams['axes.labelsize'] = 16


def create_detector():
    """
    Creates and returns KWS=3 detector
    """
    u0 = beam_xpos * pixel_size  # in mm
    v0 = beam_ypos * pixel_size  # in mm
    detector = ba.RectangularDetector(npx, npx * pixel_size, npy, npy * pixel_size)
    detector.setPerpendicularToDirectBeam(detector_distance, u0, v0)

    return detector


def get_simulation():
    """
    Creates and returns GISAS simulation with beam and detector defined
    """
    simulation = ba.GISASSimulation()
    simulation.setBeamParameters(wavelength, alpha_i, 0.0)
    simulation.setDetector(create_detector())
    simulation.setRegionOfInterest(xmin, ymin, xmax, ymax)
    return simulation


def load_data(fname):
    rawdata = np.loadtxt(fname)
    sens = np.loadtxt(sensitivity_matrix)
    data = rawdata * sens
    data = np.rot90(data, 3)
    simulation = get_simulation()

    return ba.ConvertData(simulation, data, True)

def plot_data():
    """
    Load data and plot results
    """
    data = load_data(f65569)
    plt.figure(figsize=(10, 10))
    ba.plot_simulation_result(data, units=ba.AxesUnits.QSPACE, intensity_min=0.1, intensity_max=8e+01)
    plt.show()


if __name__ == '__main__':
    plot_data()
