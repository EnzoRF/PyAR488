from PyAR488.PyAR488 import AR488
from PyAR488.HP8903A import HP8903A

import numpy as np
import matplotlib.pyplot as plt

from math import log10

interface = AR488('COM5', debug=True)
analyzer = HP8903A(20, interface)

test_level = 0.1
start_freq = 100
stop_freq = 100000
points_per_decade = 100

analyzer.push(
    (analyzer.set_measurement, 'AC'),  # set measurement
    (analyzer.set_source_amplitude, test_level),  # set test level
    (analyzer.enable_srq, {
        'data_ready': True,
        'HPIB_error': True,
        'instrument_error': True
    }),
    (analyzer.set_read_display, 'MEASUREMENT')
)

#generate logarythmic test points
n_decades = log10(stop_freq) - log10(start_freq)
n_points = (int(n_decades) + 1) * points_per_decade
frequency_test_points = np.logspace(log10(start_freq), log10(stop_freq), num=n_points, endpoint=True, base=10)

measurements = []
error_points = []

for i in frequency_test_points:
    try:
        analyzer.set_source_frequency(i)

        analyzer.await_measurement()
        level = analyzer.read()

        measurement = (i, level)
        measurements.append(measurement)
        print(measurement)

    except analyzer.InstrumentError:
        print(f'instrument error on frequency {i}')
        error_points.append(i)
        analyzer.clear()

    except analyzer.ReadError:
        print(f'invalid reading on frequency {i}')

# print error frequency

open('error points', 'w+').writelines([str(i) + ';' for i in error_points])

# plot results
freq_point = [i[0] for i in measurements]
meas_points = [i[1] for i in measurements]

plt.plot(freq_point, meas_points)
plt.xlabel('frequency')
plt.ylabel('AC')
plt.xscale('log')
plt.grid(True)
plt.show()
