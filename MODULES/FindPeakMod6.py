import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from helpers import *

def moving_average(data, window_size):
    return np.convolve(data, np.ones(window_size) / window_size, mode='valid')

df = pd.read_excel("mockData.xlsx", sheet_name='Module 6', usecols=['Time (min)', 'Isomer A', 'Isomer B'])
time = df['Time (min)'].to_numpy()
IsoA = df['Isomer A'].to_numpy()
IsoB = df['Isomer B'].to_numpy()

IsoA = np.where(IsoA <= 0, 1, IsoA)
IsoB = np.where(IsoB <= 0, 1, IsoB)

loggedA = np.log10(IsoA)
loggedB = np.log10(IsoB)

loggedSum = loggedA + loggedB
min = findMinAboveThreshold(loggedSum, 4)
peakInd = np.where(loggedSum > 6, 1, 0)

peakCount = 0

# iterate through the data and find the amount of peaks there are

for i in range(peakInd.size - 1):
    if (peakInd[i] == 0 and peakInd[i+1] == 1):
        peakCount += 1

# find the start and end of each peak

peakS = findPeakStart(peakInd.copy())
peakE = findPeakEnd(peakInd.copy())

#combine start and end into one array

peakEdges = peakS + peakE

# iterate through the array to find how long each peak is and the avg intensity

# returns a tuple of length amd intensity for each peak    

IsoALengths, IsoAIntensities = findPeakLengthsAndIntensities(peakEdges, IsoA)
IsoBLengths, IsoBIntensities = findPeakLengthsAndIntensities(peakEdges, IsoB)

peakCenters = getTimesOfPeakCenters(peakEdges, time)

IsoALengths = np.array(IsoALengths)
IsoBLengths = np.array(IsoBLengths)
IsoAIntensities = np.array(IsoAIntensities)
IsoBIntensities = np.array(IsoBIntensities)


with open('mockDataOutput.txt', 'w') as file:
    file.write(f'Total Peaks: {IsoALengths.size}\n\n')
    for i in range(IsoALengths.size):
        file.write(f'Peak {i + 1}:\n')
        file.write(f'Time of Peak Center: {peakCenters[i]} minutes\n')
        file.write(f'Duration: {IsoALengths[i]} minutes\n')
        file.write(f'Isomer A Intensity: {IsoAIntensities[i]}\n')
        file.write(f'Isomer B Intensity: {IsoBIntensities[i]}\n')
        file.write(f'A to B Ratio: {IsoAIntensities[i] / IsoBIntensities[i]}\n\n')


# plt.figure(figsize=(12,8))
# plt.subplot(4, 1, 1)
# plt.plot(time, smoothedA, 'r')
# plt.title('Isomer A Smoothed')

# plt.subplot(4,1,2)
# plt.plot(time, smoothedB, 'g')
# plt.title('Isomer B Smoothed')

# plt.subplot(4,1,3)
# plt.plot(time,IsoA, 'r')
# plt.title('Isomer A')

# plt.subplot(4,1,4)
# plt.plot(time, IsoB, 'g')
# plt.title('Isomer B')
# plt.show()
