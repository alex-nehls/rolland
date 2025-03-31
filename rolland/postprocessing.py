"""Postprocessing classes.

.. autosummary::
    :toctree: postprocessing

    PostProcessing
    AnalyticPP
    RollandPP
    Response
"""
import abc

import matplotlib.pyplot as plt
from numpy import ones, pi, squeeze, zeros
from numpy.fft import fft, fftfreq
from traitlets import Float, Instance, List, observe
from traittypes import Array

from rolland import ABCHasTraits, Deflection
from rolland.methods import AnalyticalMethods


class PostProcessing(ABCHasTraits):
    r"""Abstract base class for postprocessing classes."""

    @abc.abstractmethod
    def validate_postprocessing(self):
        """Validate the postprocessing methods."""

    @staticmethod
    def fast_fourier_tr(tsignal, dt):
        """Calculate the Fast Fourier Transform (FFT) of a time signal.

        Parameters
        ----------
        tsignal : numpy.ndarray
            Time signal to transform.
        dt : float
            Time step between samples.

        Returns
        -------
        tuple
            Frequencies and FFT of the signal.
        """
        samples = len(tsignal)
        window = ones(samples)
        fftrans = 2.0 / samples * fft(tsignal[:samples] * window)
        fftfre = fftfreq(samples, dt)
        return fftfre[0 : samples // 2], fftrans[0 : samples // 2]

    @staticmethod
    def plot(
        arrays, labels, title='Universal Plot', x_label='X-axis', y_label='Y-axis', colors=None, plot_type='loglog',
    ):
        """Universal plot function for multiple data sets.

        Parameters
        ----------
        arrays : list of tuple
            List of tuples, where each tuple contains two numpy.ndarray (x and y data).
        labels : list of str
            List of labels for each array.
        title : str, optional
            Title of the plot. Default is 'Universal Plot'.
        x_label : str, optional
            Label for the x-axis. Default is 'X-axis'.
        y_label : str, optional
            Label for the y-axis. Default is 'Y-axis'.
        colors : list of str, optional
            List of colors for each array. Default is None.
        plot_type : str, optional
            Type of plot (e.g., 'loglog', 'plot'). Default is 'loglog'.
        """
        plt.figure(figsize=(10, 6))
        if colors is None:
            colors = ['k', 'r', 'b', 'g', 'c', 'm', 'y']

        for (x, y), label, color in zip(arrays, labels, colors, strict=False):
            if plot_type == 'loglog':
                plt.loglog(x, abs(y), label=label, color=color)
            else:
                plt.plot(x, abs(y), label=label, color=color)

        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.title(title)
        plt.legend()
        plt.grid(True)
        plt.show()


class AnalyticPP(PostProcessing):
    r"""Analytic postprocessing class.

    This class is used to perform postprocessing on analytical methods.

    Attributes
    ----------
    results : AnalyticalMethods
        Instance of the AnalyticalMethods class containing the results.
    """

    results = Instance(AnalyticalMethods)

    def validate_postprocessing(self):
        """Validate the postprocessing methods."""

    @property
    def f(self):
        """Frequency vector."""
        return self.results.f

    @property
    def vb(self):
        """Velocity vector."""
        return self.results.mobility * self.results.force

    @property
    def ub(self):
        """Displacement vector."""
        return self.vb / (self.results.omega * 1j)


class RollandPP(PostProcessing):
    r"""Rolland postprocessing base class.

    This class is used to perform postprocessing on Rolland methods.

    Attributes
    ----------
    results : Deflection
        Instance of the Deflection class containing the results.
    f_min : float
        Minimum frequency for response calculation :math:`[Hz]`.
    f_max : float
        Maximum frequency for response calculation :math:`[Hz]`.
    """

    results = Instance(Deflection)
    f_min = Float(default_value=100.0, min=0.0)
    f_max = Float(default_value=3000.0, min=0.0)

    def validate_postprocessing(self):
        """Validate the postprocessing methods."""


class Response(RollandPP):
    r"""Postprocessing class for Rolland response quantities.

    This class calculates and stores response quantities such as receptance,
    mobility, and accelerance based on the results of the Deflection class.

    Attributes
    ----------
    results : Deflection
        Instance of the Deflection class containing the results.
    x_resp : list of float
        List of response points in meters :math:`[m]` (default value is x_excit).
    freq : numpy.ndarray
        Frequency vector :math:`[Hz]`.
    rez : numpy.ndarray
        Receptance vector :math:`[m/N]`.
    mob : numpy.ndarray
        Mobility vector :math:`[m/Ns]`.
    accel : numpy.ndarray
        Accelerance vector :math:`[m/Ns^2]`.
    """

    x_resp = List(default_value=None, allow_none=True)
    freq = Array()
    rez = Array()
    mob = Array()
    accel = Array()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.calculate_response()
        self.observe(self._on_results_change, names='results')

    @observe('results')
    def _on_results_change(self, change):
        self.calculate_response()

    def calculate_response(self):
        """Calculate and store response quantities (Receptance, Mobility, Accelerance)."""
        if self.x_resp is None:
            self.x_resp = [self.results.excit.x_excit]

        # Get response indices
        ind_resp = [int(x / self.results.discr.dx) for x in self.x_resp]

        # Compute force FFT once
        fftfre, ffft = self.fast_fourier_tr(self.results.force, self.results.discr.dt)

        # Initialize arrays for results
        n_points = len(ind_resp)
        n_freq = len(fftfre)
        ufft = zeros((n_points, n_freq), dtype=complex)

        # Compute deflection FFTs separately for each point
        for i, ind in enumerate(ind_resp):
            defl = self.results.deflection[ind, : self.results.discr.nt]
            _, ufft[i] = self.fast_fourier_tr(defl, self.results.discr.dt)

        # Calculate quantities for all points
        rez = ufft / ffft  # Receptance
        mob = 1j * fftfre * 2 * pi * rez  # Mobility
        accel = -((fftfre * 2 * pi) ** 2) * rez  # Accelerance

        # Frequency range
        mask = (fftfre > self.f_min) & (fftfre <= self.f_max)

        # Store results as attributes
        self.freq = fftfre[mask]
        self.rez = squeeze(rez[:, mask])
        self.mob = squeeze(mob[:, mask])
        self.accel = squeeze(accel[:, mask])
