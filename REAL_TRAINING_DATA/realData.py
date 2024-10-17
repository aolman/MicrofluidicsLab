import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from helpers import *

# FIND WAY TO FIND PEAKS MORE ACCURATELY, NOT COUNTING THE ASCENT AND DESCENT ON EITHER SIDE
# FIND WAY TO CALCULATE THRESHOLD FOR COUNTING A PEAK
# FIND WAY TO CALCULATE THRESHOLD FOR MERGED DROPLETS
# INCORPORATE MOLECULE C TO GET MORE ACCURATE RATIOS
# FIND dt OF EACH TIME INTERVAL

# get data from excel sheet
# spreadsheetName = input("Spreadsheet Name: ")
df = pd.read_excel("realDataTraining.xlsx", sheet_name="S1", usecols=['Time (min)', 'Isomer 77', 'Isomer 57', 'Internal standard'])
time = df['Time (min)'].to_numpy()
IsoA = df['Isomer 57'].to_numpy()
IsoB = df['Isomer 77'].to_numpy()
IntStand = df['Internal standard'].to_numpy()
IntStandAverage = np.nanmean(IntStand)

# set any places where the reading is zero to one for sake of taking log later

IsoA = np.where(IsoA <= 0, 1, IsoA)
IsoB = np.where(IsoB <= 0, 1, IsoB)

# take log of both isomers to even out peaks

loggedA = np.log10(IsoA)
loggedB = np.log10(IsoB)

#sum them together into one array and find the indices of the peaks

loggedSum = loggedA + loggedB
min = findMinAboveThreshold(loggedSum, 4)
THRESHOLD = 8
peakInd = np.where(loggedSum > THRESHOLD, 1, 0)

# find the start and end of each peak

peakS = findPeakStart(peakInd.copy())
peakE = findPeakEnd(peakInd.copy())

#combine start and end into one array

peakEdges = peakS + peakE

# iterate through the array to find how long each peak is and the avg intensity

# returns intensity for each peak   

IsoAIntensities = findPeakIntensities(peakEdges, IsoA, time)
IsoBIntensities = findPeakIntensities(peakEdges, IsoB, time)

# returns duration and center for each peak

peakDurations = findPeakDurations(peakEdges, time)
peakCenters = getTimesOfPeakCenters(peakEdges, time)

# based on duration of peak, remove peaks with very low durations (spikes)

peakDurations, IsoAIntensities, IsoBIntensities, peakCenters = removeSpikes(peakDurations, IsoAIntensities, IsoBIntensities, peakCenters)

potentialMerged = findPotentialMergedDrops(peakDurations)
calibratedAIntensities = calibrateData(IsoAIntensities)
calibratedBIntensities = calibrateData(IsoBIntensities)
print(IntStandAverage)

dataOut = {'Peak Number' : range(1, peakCenters.size + 1),
           'Peak Center' : peakCenters,
           'Peak Duration' : peakDurations,
           'Calibrated 57 Intensity' : calibratedAIntensities,
           'Calibrated 77 Intensity' : calibratedBIntensities,
           'Internal Standard' : np.array(peakCenters.size, IntStandAverage),
           'Uncalibrated 57 Intensity' : IsoAIntensities,
           'Uncalibrated 77 Intensity' : IsoBIntensities,
           'Calibrated Ratio' : calibratedAIntensities / (calibratedAIntensities + calibratedBIntensities),
           'Yield' : (calibratedAIntensities + calibratedBIntensities) / IntStandAverage,
           'Calibrated 57 / Internal Standard Ratio' : calibratedAIntensities / IntStandAverage,
           'Calibrated 77 / Internal Standard Ratio' : calibratedBIntensities / IntStandAverage}

dfOut = pd.DataFrame(dataOut)
dfOut.to_excel('S1output.xlsx', index=False, engine='openpyxl')

with open('SHEET1OUTPUT.txt', 'w') as file:
    file.write(f'Total Peaks: {peakCenters.size}\n\n')
    if potentialMerged.size > 0:
        file.write('POTENTIAL MERGED PEAKS\n')
        for i in range(potentialMerged.size):
            file.write(f'Peak {potentialMerged[i]+1}\n')
        file.write('\n')
    for i in range(peakCenters.size):
        file.write(f'Peak {i + 1}:\n')
        file.write(f'Time of Peak Center: {round(peakCenters[i], 3)} minutes\n')
        file.write(f'Duration: {round(peakDurations[i], 3)} minutes\n')
        file.write(f'Isomer A Intensity: {round(IsoAIntensities[i], 3)}\n')
        file.write(f'Isomer B Intensity: {round(IsoBIntensities[i], 3)}\n')
        file.write(f'A to B Ratio: {round(IsoAIntensities[i] / IsoBIntensities[i], 3)}\n\n')


# plt.subplot(2, 1,1)
# plt.plot(time,loggedSum)
# ax = plt.gca()
# ax.set_xlim([6.3, 6.5])
# ax.set_ylim([0, 15])

# plt.subplot(2,1,2)
# plt.plot(time,IsoA)
# ax = plt.gca()
# ax.set_xlim([6.3, 6.5])
# ax.set_ylim([0, 200000])
# plt.show()
