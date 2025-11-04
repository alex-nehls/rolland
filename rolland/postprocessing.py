"""Postprocessing classes.

.. autosummary::
    :toctree: postprocessing

    PostProcessing
    AnalyticPP
    RollandPP
    Response
    TDR
"""
import abc

import matplotlib.pyplot as plt
from numpy import array, convolve, ones, pi, rint, round, squeeze, where, zeros  # noqa: A004
from numpy.fft import fft, fftfreq
from traitlets import Float, Instance, List, Unicode
from traittypes import Array

from .abstract_traits import ABCHasTraits
from .deflection import Deflection
from .methods import AnalyticalMethods
from .track import (
    ArrangedBallastedSingleRailTrack,
    ArrangedSlabSingleRailTrack,
)


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
            arrays,
            title       = 'Universal Plot',
            x_label     = 'X-axis',
            y_label     = 'Y-axis',
            colors      = None,
            plot_type   = 'loglog',
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

        for (x, y), color in zip(arrays, colors, strict=False):  # NOTE: why does this work? Should be grouping the first and second list elements into two respective tuples.
            if plot_type == 'loglog':
                plt.loglog(x, y, color=color)
            else:
                plt.plot(x, y, color=color)

        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.title(title)
        # plt.legend()
        plt.grid(True)


    @staticmethod
    def plot_mobility_receptance(
        freq,
        mob,
        rez,
        title='Mobility & Receptance',
        x_label='Frequency [Hz]',
        mob_label='Mobility [m/Ns]',
        rez_label='Receptance [m/N]',
        colors=None,
        plot_type='loglog',
    ):
        # TODO : Docstring
        import matplotlib.pyplot as plt
        import numpy as np
        plt.figure(figsize=(10, 8))
        ax1 = plt.subplot(211)
        if plot_type == 'loglog':
            ax1.loglog(freq, np.abs(mob), color=colors[0] if colors else 'b', label=mob_label)
        else:
            ax1.plot(freq, np.abs(mob), color=colors[0] if colors else 'b', label=mob_label)
        ax1.set_ylabel(mob_label)
        ax1.set_title(title)
        ax1.grid(True)
        ax1.legend()

        ax2 = plt.subplot(212, sharex=ax1)
        if plot_type == 'loglog':
            ax2.loglog(freq, np.abs(rez), color=colors[1] if colors else 'r', label=rez_label)
        else:
            ax2.plot(freq, np.abs(rez), color=colors[1] if colors else 'r', label=rez_label)
        ax2.set_xlabel(x_label)
        ax2.set_ylabel(rez_label)
        ax2.grid(True)
        ax2.legend()
        plt.tight_layout()
        plt.show()

    @staticmethod
    def plotMatrix(
        deflection, 
        track,
        simulation_time,
    ):
        # TODO: put parameters in description
        """Plot function for visualizing the deflection of the track over time in an array.
        x_axis : represents spatial dimension of track
        y_axis : represents time dimension of process

        Parameters
        ----------
        arrays : list of tuple
            List of tuples, where each tuple contains two numpy.ndarray (x and y data).


        """
        plt.figure(figsize=(10, 6))

        skip_x      = 1
        skip_y      = 1

        plt.imshow(
            # deflection[::skip_y, ::skip_x],   # NOTE: 
            X           = deflection,
            aspect      ='auto',
            cmap        ='viridis',
            extent      =[
                0, track.l_track,
                simulation_time, 0
            ])
        plt.title('Displacement')
        plt.ylabel('Time Step [s]')
        plt.xlabel('Beam Pos. [m]')
        plt.ylim(simulation_time, 0)
        plt.colorbar(label='Displacement [m]')
        plt.clim(-1e-6, 1e-6)

        plt.tight_layout()
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
    ind_resp : list of int
        List of response indices (None if x_resp is provided).
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
    ind_resp = List(default_value=None, allow_none=True)
    freq = Array()
    rez = Array()
    mob = Array()
    accel = Array()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.calculate_response()
        #self.observe(self._on_results_change, names='results')

    #@observe('results')
    #def _on_results_change(self, change):
    #    self.calculate_response()

    def calculate_response(self):
        """Calculate and store response quantities (Receptance, Mobility, Accelerance)."""
        if self.x_resp is None and self.ind_resp is None:
            # Handle both excitation_indices (plural, list) and excitation_index (singular)
            if hasattr(self.results, 'excitation_indices') and self.results.excitation_indices:
                exc_ind = int(self.results.excitation_indices[0])
            elif hasattr(self.results, 'excitation_index'):
                exc_ind = int(self.results.excitation_index)
            else:
                raise AttributeError('No excitation index found on results (expected excitation_indices or excitation_index)')
            
            self.x_resp = [self.results.discr.dx * exc_ind]
            self.ind_resp = [int(x / self.results.discr.dx) for x in self.x_resp]

        elif self.x_resp is None and self.ind_resp is not None:
            self.x_resp = [(x * self.results.discr.dx) for x in self.ind_resp]

        else:
            self.ind_resp = [int(x / self.results.discr.dx) for x in self.x_resp]

        # Compute force FFT once
        fftfre, ffft = self.fast_fourier_tr(self.results.force, self.results.discr.dt)

        # Initialize arrays for results
        n_points = len(self.ind_resp)
        n_freq = len(fftfre)
        ufft = zeros((n_points, n_freq), dtype=complex)

        # Compute deflection FFTs separately for each point
        for i, ind in enumerate(self.ind_resp):
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


class TDR(RollandPP):
    r"""Postprocessing class for TDR (Track-Decay-Rate).

    This class calculates and stores the Track-Decay-Rate (TDR) based on :cite:`EN15461:2008`.

    Attributes
    ----------
    results : Deflection
        Instance of the Deflection class containing the results.
    tdr : numpy.ndarray
        Track-Decay-Rate vector :math:`[dB/m]`.
    ind_tdr : list of int
        Indices of the TDR points.
    x_tdr : numpy.ndarray
        Distances of the TDR points from the excitation point :math:`[m]`.
    filter : str
        Filter type (default is '1/3 Octave').
    freq : numpy.ndarray
        Frequency vector :math:`[Hz]`.
    """

    tdr = Array()
    filter = Unicode(default_value=None, allow_none=True)
    freq = Array()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.find_tdr_points()
        self.calculate_tdr()
        # self.observe(self._on_results_change, names='results')

    def find_tdr_points(self):
        """Find the corresponding measurement points depending on track type."""
        # Determine excitation index robustly
        if hasattr(self.results, 'excitation_indices') and self.results.excitation_indices:
            exc_ind = int(self.results.excitation_indices[0])
        elif hasattr(self.results, 'excitation_index'):
            exc_ind = int(self.results.excitation_index)
        else:
            raise AttributeError('No excitation index found on results (expected excitation_indices or excitation_index)')
        
        if isinstance(self.results.track, ArrangedSlabSingleRailTrack | ArrangedBallastedSingleRailTrack):
            # TDR for non-uniform mounting positions
            #   Identification of TDR positions

            # Determination of mounting positions
            x_mp = array(list(self.results.track.mount_prop.keys()))    # Position
            ind_mp = (x_mp / self.results.discr.dx).astype(int)         # Index
            # Left sleeper Index
            idx_s = int(where(ind_mp < exc_ind)[0][-1])
            # Calculate distance from excitation point
            x_s = x_mp[idx_s:] - x_mp[idx_s]  # Sleeper distances from excitation point.
            x_sc = convolve(x_s, ones(2) / 2, mode='valid')  # Sleeper centers from excitation point.

            def tdr_points_betw1(idx):
                """Calculate of theoretical measurement points (1st part)."""
                return ((x_s[idx + 1] - x_sc[idx]) / 2) + x_sc[idx]

            def tdr_points_betw2(dx):
                """Calculate of theoretical measurement points (2nd part)."""
                return ((x_sc[dx] - x_s[dx]) / 2) + x_s[dx]

            # Theoretical measurement points
            self.x_tdr = array([x_sc[0], tdr_points_betw1(0), x_s[1], tdr_points_betw2(1), x_sc[1], tdr_points_betw1(1),
                         x_s[2], tdr_points_betw2(2), x_sc[2], tdr_points_betw1(2), x_s[3], x_sc[3], x_s[4], x_sc[4],
                         x_sc[5], x_sc[6], x_sc[7], x_sc[8], x_sc[10], x_sc[12], x_sc[16], x_sc[20], x_sc[24], x_sc[30],
                         x_sc[36], x_sc[42], x_sc[48], x_sc[54], x_sc[66]]) - x_sc[0]

            # Determination of measurement position indices
            ind_tdr = rint(round(self.x_tdr, 5) / self.results.discr.dx) + exc_ind
            self.ind_tdr = list(ind_tdr.astype(int))

        else:
            # TDR for continuous slab and ballasted tracks
            # Identification of TDR positions
            excitation_index = exc_ind              # Start index.
            l_s = 0.6                                       # Theoretical Sleeper distance.
            x_tdr = array([0.5, 0.75, 1, 1.25, 1.5, 1.75, 2, 2.25, 2.5, 2.75, 3, 3.5, 4, 4.5, 5.5, 6.5, 7.5, 8.5,
                         10.5, 12.5, 16.5, 20.5, 24.5, 30.5, 36.5, 42.5, 48.5, 54.5, 66.5]) * l_s

            self.x_tdr = x_tdr - l_s / 2
            ind_tdr = rint(self.x_tdr / self.results.discr.dx) + excitation_index # NOTE: excitation_indices not defined
            self.ind_tdr = list(ind_tdr.astype(int))


    def calculate_tdr(self):
        """Calculate the Track-Decay-Rate (TDR) based on the results."""
        # Calculation of mobilities
        resp = Response(results=self.results, ind_resp=self.ind_tdr)
        mob = resp.mob

        # Calculation of TDR (according to DIN)
        sum_tdr = abs(mob[1, 1:]) ** 2 / abs(mob[0, 1:]) ** 2 * (self.x_tdr[1])
        for n in range(2, len(self.ind_tdr)):
            sum_tdr = sum_tdr + abs(mob[n, 1:]) ** 2 / abs(mob[0, 1:]) ** 2 * (self.x_tdr[n])

        self.tdr = 4.343 / sum_tdr
        self.freq = resp.freq[1:]


