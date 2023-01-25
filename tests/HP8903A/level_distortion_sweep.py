from PyAR488.PyAR488 import AR488
from PyAR488.HP8903A import HP8903A

import numpy as np
import matplotlib.pyplot as plt

interface = AR488('COM5', debug=False)
analyzer = HP8903A(20, interface)

start_level = 0.1
stop_level = 1.1
test_points = 3
test_frequency = 1000
meas_delay = 2
load_impedance = 8

analyzer.push(  # pack all configuration parameters in a single command and send
    (analyzer.set_source_frequency, test_frequency),  # set test level
    (analyzer.set_read_display, 'MEASUREMENT'),  # configure the pointed display for a read command
    (analyzer.set_trigger, 'FREE_RUN'),  # configure trigger mode
    (analyzer.set_source_frequency, test_frequency),  # set source frequency
    (analyzer.enable_srq, None),  # enable srq requests
)

points = np.linspace(start_level, stop_level, test_points)  # build frequency test points
measurements = []

for i in points:
    analyzer.set_source_amplitude(i)  # set new amplitude

    analyzer.set_measurement('DISTORTION')  # set measurement to distortion
    analyzer.await_measurement()  # wait for SRQ (measurement ready)
    d = analyzer.read()  # get measurement result

    analyzer.set_measurement('AC')
    analyzer.await_measurement()
    a = analyzer.read()

    measurement = (a, d)
    measurements.append(measurement)
    print(f'source level : {i} -> {measurement}')

analyzer.set_source_amplitude(start_level)  # return to low level

distortion_point = [i[0] for i in measurements]  # separate all X points
meas_points = [i[1] for i in measurements]  # separate all Y points

plt.plot(distortion_point, meas_points)
plt.xlabel('output voltage [Vrms]')
plt.ylabel('THD+N %')
plt.grid(True)
plt.show()