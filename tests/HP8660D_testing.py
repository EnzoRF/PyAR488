from PyAR488.PyAR488 import AR488
from PyAR488.HP8660D import HP8660D

interface = AR488('COM5', debug = True)

gen = HP8660D(interface, 19)

gen.source(1.23456789 * 10**6, -25)  #1.23456789 GHz @ -25dBm

interface.close()
print('done')

