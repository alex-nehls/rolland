"""Postprocessing classes.

.. autosummary::
    :toctree: postprocessing


"""
import matplotlib.pyplot as plt
from numpy import ones, pi, where
from numpy.fft import fft, fftfreq


def fast_fourier_transform(tsignal, dt):
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


def response(defl, f_min=100, f_max=3000):
    """Calculate point or transfer quantities (Receptance, Mobility, Accelerance).

    Parameters
    ----------
    defl : numpy.ndarray
        Deflection array :math:`[m]`.
    f_min : float, optional
        Minimum frequency :math:`[Hz]`. Default is 100.
    f_max : float, optional
        Maximum frequency :math:`[Hz]`. Default is 3000.

    Returns
    -------
    tuple
        Frequencies, Receptance, Mobility, and Accelerance.
    """
    fftfre, ffft = fast_fourier_transform(defl.force, defl.dt)
    fftfre, ufft = fast_fourier_transform(defl, defl.dt)

    rez = ufft / ffft
    mob = 1j * fftfre * 2 * pi * rez
    accel = -((fftfre * 2 * pi) ** 2) * rez
    ind_fmin = int(where(fftfre > f_min)[0][0])
    ind_fmax = int(where(fftfre > f_max)[0][0])
    return fftfre[ind_fmin:ind_fmax], rez[ind_fmin:ind_fmax], mob[ind_fmin:ind_fmax], accel[ind_fmin:ind_fmax]

def response_fdm(defl, dist = 0, f_min=100, f_max=3000):
    """Calculate point or transfer quantities (Receptance, Mobility, Accelerance).

    Parameters
    ----------
    defl : Deflection
        Deflection instance.
    f_min : float, optional
        Minimum frequency :math:`[Hz]`. Default is 100.
    f_max : float, optional
        Maximum frequency :math:`[Hz]`. Default is 3000.

    Returns
    -------
    tuple
        Frequencies, Receptance, Mobility, and Accelerance.
    """
    discr = defl.discr
    force = defl.force
    ind_trans = defl.ind_excit + int(dist // discr.dx + 1)
    defl = defl.deflection[ind_trans, 0 : discr.nt]

    fftfre, ffft = fast_fourier_transform(force, discr.dt)
    fftfre, ufft = fast_fourier_transform(defl, discr.dt)

    rez = ufft / ffft
    mob = 1j * fftfre * 2 * pi * rez
    accel = -((fftfre * 2 * pi) ** 2) * rez
    ind_fmin = int(where(fftfre > f_min)[0][0])
    ind_fmax = int(where(fftfre > f_max)[0][0])
    return fftfre[ind_fmin:ind_fmax], rez[ind_fmin:ind_fmax], mob[ind_fmin:ind_fmax], accel[ind_fmin:ind_fmax]



def plot(arrays, labels, title='Universal Plot', x_label='X-axis', y_label='Y-axis', colors=None, plot_type='loglog'):
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
