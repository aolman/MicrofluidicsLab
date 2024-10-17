import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt

def moving_average(data, window_size):
    return np.convolve(data, np.ones(window_size) / window_size, mode='valid')

def log10All(Iso, time):
    for dt in range(time.size - 1):
        Iso[dt] = math.log10(Iso[dt])
    return Iso
    
    
def smoothie(Iso, time):
    for dt in range(1, time.size - 2):
        if (abs(Iso[dt - 1] - Iso[dt + 1]) > 5000):
            Iso[dt] = (Iso[dt - 1] + Iso[dt + 1]) / 2
    return Iso

df = pd.read_excel("mockData.xlsx", sheet_name='Module 6', usecols=['Time (min)', 'Isomer A', 'Isomer B'])
time = df['Time (min)'].to_numpy()
IsoA = df['Isomer A'].to_numpy()
IsoB = df['Isomer B'].to_numpy()

loggedA = log10All(IsoA.copy(), time)
loggedB = log10All(IsoB.copy(), time)

logged_sum = loggedA + loggedB

smoothedA = smoothie(IsoA.copy(), time)
smoothedB = smoothie(IsoB.copy(), time)

peakInd = np.where(logged_sum > 6, 1, 0)

plt.plot(time, peakInd)
ax = plt.gca()
ax.set_ylim([0, 2])
plt.show()



# plt.figure(figsize=(12,8))
# plt.subplot(2, 1, 1)
# plt.plot(time, loggedA, 'r') 
# plt.title('Isomer A Smoothed')
# ax = plt.gca()
# ax.set_ylim([0, 10])

# plt.subplot(4,1,2)
# plt.plot(time, IsoA, 'r')
# plt.title('Isomer A')

# plt.subplot(2,1,2)
# plt.plot(time, loggedB, 'g')
# plt.title('Isomer B Smoothed')
# ax = plt.gca()
# ax.set_ylim([0, 10])

# plt.subplot(4,1,4)
# plt.plot(time, IsoB, 'g')
# plt.title('Isomer B')
#plt.show()
#smoothedA = moving_average(IsoA, window_size=3)
#smoothedB = moving_average(IsoB, window_size=3)

#pad_length = len(IsoA) - len(smoothedA)
#smoothedA = np.pad(smoothedA, (pad_length, 0), mode='constant')
#smoothedB = np.pad(smoothedB, (pad_length, 0), mode='constant')

