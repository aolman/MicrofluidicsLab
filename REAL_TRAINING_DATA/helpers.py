import pandas as pd
import numpy as np

# Finds all of the starts to the peaks

def findPeakStart(Ind):
    for i in range(Ind.size - 1):
        if Ind[i] == 0 and Ind[i+1] == 1:
            Ind[i+1] = 2
    Ind = np.where(Ind == 2, 1, 0)
    return Ind

# Finds all of the ends of the peaks

def findPeakEnd(Ind):
    for i in range(Ind.size - 1):
        if Ind[i] == 1 and Ind[i+1] == 0:
            Ind[i] = 2
    Ind = np.where(Ind == 2, 1, 0)
    return Ind

# Calculates peak duration and intensities

def findPeakIntensities(peakEdges, Iso, time):
    peakIntensities = []
    intensity = 0
    count = 0
    isPeak = False
    
    for i in range(peakEdges.size):
        if (isPeak):
            count += 1
            intensity += Iso[i]
        
        if peakEdges[i] == 1 and isPeak:
            avgIntensity = intensity / count
            peakIntensities.append(avgIntensity)
            intensity = 0
            count = 0
            isPeak = False
            continue
        if peakEdges[i] == 1 and not isPeak:
            isPeak = True
            
    peakIntensities = np.array(peakIntensities)
    return peakIntensities

def findPeakDurations(peakEdges, time):
    peakDurations = []
    isPeak = False
    begin = 0
    end = 0
    duration = 0
    
    for i in range(peakEdges.size):
        if peakEdges[i] == 1 and isPeak:
            end = time[i]
            duration = end - begin
            peakDurations.append(duration)
            isPeak = False
            continue
        
        if peakEdges[i] == 1 and not isPeak:
            begin = time[i]
            isPeak = True
    return peakDurations

# Finds the center of each peak

def getTimesOfPeakCenters(peakEdges, time):
    peakCenters = []
    isPeak = False
    startOfPeakIndex = 0
    for i in range(peakEdges.size):
        if (not isPeak and peakEdges[i] == 1):
            startOfPeakIndex = i
            isPeak = True
            continue
            
        if(isPeak and peakEdges[i] == 1):
            peakCenter = (time[startOfPeakIndex] + time[i]) / 2
            peakCenters.append(peakCenter)
            isPeak = False
    peakCenters = np.array(peakCenters)
    return peakCenters

# Finds the minimum above a given threshold

def findMinAboveThreshold(arr, threshold):
    filtered = arr[arr > threshold]
    minVal = np.min(filtered)
    return minVal

# Calculates moving average of a data set

def moving_average(data, window_size):
    return np.convolve(data, np.ones(window_size) / window_size, mode='valid')

# Finds any potential drops that have been merged

def findPotentialMergedDrops(durations):
    MIN_DURATION = 0.05
    potentialMerged = []
    for d in range(len(durations)):
        if durations[d] >= MIN_DURATION:
            potentialMerged.append(d)
    return np.array(potentialMerged)

def removeSpikes(durations, intensitiesA, intensitiesB, centers):
    indList = []
    for i in range(len(durations) - 1, -1, -1):
        if durations[i] < 0.01:
            indList.append(i)
    durations = np.delete(durations, indList)
    intensitiesA = np.delete(intensitiesA, indList)
    intensitiesB = np.delete(intensitiesB, indList)
    centers = np.delete(centers, indList)
    return durations, intensitiesA, intensitiesB, centers

def calibrateData(IsoIntensities):
    calibrated = IsoIntensities.copy()
    min = np.min(calibrated)
    for i in range(calibrated.size):
        calibrated[i] = calibrated[i] - min
    return calibrated
    
    