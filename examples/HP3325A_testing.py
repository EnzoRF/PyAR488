from PyAR488.PyAR488 import AR488
from PyAR488.HP3325A import HP3325A
import time

interface = AR488('COM4')
gen = HP3325A(interface,10)

# address instrument to start comunication
gen.address()

print('set waveform to 123.456 Hz sine wave with amplitude 2.5V')
gen.set_function('sine')
gen.set_frequency(123.456)
gen.set_amplitude(2.5, 'V')
time.sleep(10)


print('set waveform to 10200.50 Hz square wave with amplitude 10dBm')
gen.set_function('square')
gen.set_frequency(10200.50)
gen.set_amplitude(10, 'dBm')
time.sleep(10)


print('set waveform triangle wave for 1 to 10Hz log sweep with amplitude 1Vrms')
gen.set_function('triangle')
gen.set_frequency_sweep(1,10)
gen.set_amplitude(1, 'Vrms')
time.sleep(10)
