import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from helpers import *

# FIND WAY TO FIND PEAKS MORE ACCURATELY, NOT COUNTING THE ASCENT AND DESCENT ON EITHER SIDE
# FIND WAY TO CALCULATE THRESHOLD FOR COUNTING A PEAK
# FIND WAY TO CALCULATE THRESHOLD FOR MERGED DROPLETS

# get data from excel sheet
# spreadsheetName = input("Spreadsheet Name: ")
df = pd.read_excel("20241111 for Aidan redo.xlsx", usecols=['Time (min)', '77 iso', '57 iso', 'IS'])
time = df['Time (min)'].to_numpy()
IsoA = df['57 iso'].to_numpy()
IsoB = df['77 iso'].to_numpy()
intStand = df['IS'].to_numpy()

#omit any times that may not be a part of the data we want to look at

time, IsoA, IsoB, intStand = omitTimes(time, IsoA, IsoB, intStand, 1.7, time[time.size - 1])

# set any places where the reading is  <= 0 to one for sake of taking log later

IsoA = np.where(IsoA <= 0, 1, IsoA)
IsoB = np.where(IsoB <= 0, 1, IsoB)

# take log of both isomers to even out peaks

# loggedA = np.log10(IsoA)
# loggedB = np.log10(IsoB)

# sum them together into one array and find the indices of the peaks

# loggedSum = loggedA + loggedB
# THRESHOLD = 3
# determining whether I want to use a logged sum or molecule C for finding peaks
# peakInd = np.where(loggedSum > THRESHOLD, 1, 0)
intStandMean = np.nanmean(intStand)
peakInd = np.where(intStand > (intStandMean / 4), 1, 0)
# find the start and end of each peak

peakStart = findPeakStart(peakInd.copy())
peakEnd = findPeakEnd(peakInd.copy())

#combine start and end into one array

peakEdges = peakStart + peakEnd
# iterate through the array to find how long each peak is and the avg intensity

# returns intensity for each peak   

IsoAIntensities = findPeakIntensities(peakEdges, IsoA, time)
IsoBIntensities = findPeakIntensities(peakEdges, IsoB, time)
intStandIntensities = findPeakIntensities(peakEdges, intStand, time)

# returns duration and center for each peak

peakDurations = findPeakDurations(peakEdges, time)
peakCenters = getTimesOfPeakCenters(peakEdges, time)

intStandIntensities, peakDurations, peakCenters, IsoAIntensities, IsoBIntensities = deleteRandomNoise(intStandIntensities, peakDurations, peakCenters, IsoAIntensities, IsoBIntensities)

# based on duration of peak, remove peaks with very low durations (spikes) or very long durations (merged)

potentialSplit = findPotentialSpikes(peakDurations, IsoAIntensities, IsoBIntensities, peakCenters)
potentialMerged = findPotentialMergedDrops(peakDurations)

# calibrate the data based on the zero values
calibratedAIntensities = calibrateData(IsoAIntensities)
calibratedBIntensities = calibrateData(IsoBIntensities)

# create a dataframe and make it an excel sheet

dataOut = {'Peak Number' : range(1, peakCenters.size + 1),
           'Peak Center' : np.round(peakCenters, 3),
           'Peak Duration' : np.round(peakDurations, 3),
           'Calibrated 57 Intensity' : np.round(calibratedAIntensities),
           'Calibrated 77 Intensity' : np.round(calibratedBIntensities),
           'Internal Standard' : np.round(intStandIntensities),
           'Uncalibrated 57 Intensity' : np.round(IsoAIntensities),
           'Uncalibrated 77 Intensity' : np.round(IsoBIntensities),
           'Calibrated Ratio' : np.round(calibratedAIntensities / (calibratedAIntensities + calibratedBIntensities), 3),
           'Yield' : np.round((calibratedAIntensities + calibratedBIntensities) / intStandIntensities, 3),
           'Calibrated 57 / Internal Standard Ratio' : np.round(calibratedAIntensities / intStandIntensities, 3),
           'Calibrated 77 / Internal Standard Ratio' : np.round(calibratedBIntensities / intStandIntensities, 3),
           'Potential Merged Peaks' : potentialMerged + 1,
           'Potential Split Peaks' : potentialSplit + 1}

dfOut = pd.DataFrame.from_dict(dataOut, orient='index').transpose()
dfOut.to_excel('20241111output.xlsx', index=False, engine='openpyxl')

# with open('SHEET1OUTPUT.txt', 'w') as file:
#     file.write(f'Total Peaks: {peakCenters.size}\n\n')
#     if potentialMerged.size > 0:
#         file.write('POTENTIAL MERGED PEAKS\n')
#         for i in range(potentialMerged.size):
#             file.write(f'Peak {potentialMerged[i]+1}\n')
#         file.write('\n')
#     for i in range(peakCenters.size):
#         file.write(f'Peak {i + 1}:\n')
#         file.write(f'Time of Peak Center: {round(peakCenters[i], 3)} minutes\n')
#         file.write(f'Duration: {round(peakDurations[i], 3)} minutes\n')
#         file.write(f'Isomer A Intensity: {round(IsoAIntensities[i], 3)}\n')
#         file.write(f'Isomer B Intensity: {round(IsoBIntensities[i], 3)}\n')
#         file.write(f'A to B Ratio: {round(IsoAIntensities[i] / IsoBIntensities[i], 3)}\n\n')


plt.plot(time,IsoA)
ax = plt.gca()
ax.set_xlim([8, 10])
ax.set_ylim([0, 15000])
plt.show()

