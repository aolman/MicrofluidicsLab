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
    meanDuration = np.mean(durations)
    potentialMerged = []
    for d in range(len(durations)):
        if durations[d] >= meanDuration * 1.5:
            potentialMerged.append(d)
    potentialMerged = np.array(potentialMerged)
    return np.array(potentialMerged)

def findPotentialSpikes(durations, intensitiesA, intensitiesB, centers):
    meanDuration = np.mean(durations)
    indList = []
    for i in range(len(durations) - 1, -1, -1):
        if durations[i] < meanDuration * 0.55:
            indList.append(i)
    # durations = np.delete(durations, indList)
    # intensitiesA = np.delete(intensitiesA, indList)
    # intensitiesB = np.delete(intensitiesB, indList)
    # centersOfRemovedSpikes = centers[indList]
    # centers = np.delete(centers, indList)
    # return durations, intensitiesA, intensitiesB, centers, indList
    indList.sort()
    indList = np.array(indList)
    return indList

def calibrateData(IsoIntensities):
    calibrated = IsoIntensities.copy()
    min = np.min(calibrated)
    for i in range(calibrated.size):
        calibrated[i] = calibrated[i] - min
    return calibrated
  
  # OMITTED TIME MUST NOT BE IN MIDST OF PEAK 
  # MAYBE PASS PEAK START AND END TO ENSURE THAT IT IS NOT IN PEAK
            
def omitTimes(time, IsoA, IsoB, intStand, omittedStart, omittedEnd):
    indList = []
    for i in range(time.size - 1, -1, -1):
        if time[i] < omittedStart or time[i] > omittedEnd:
            indList.append(i)
    IsoA = np.delete(IsoA, indList)
    IsoB = np.delete(IsoB, indList)
    intStand = np.delete(intStand, indList)
    time = np.delete(time, indList)
    return time, IsoA, IsoB, intStand

def deleteRandomNoise(intStandIntensities, durations, centers, AIntensities, BIntensities):
    indList = []
    for i in range(len(durations) - 1, -1, -1):
        if intStandIntensities[i] == 0:
            indList.append(i)
    intStandIntensities = np.delete(intStandIntensities, indList)
    durations = np.delete(durations, indList)
    AIntensities = np.delete(AIntensities, indList)
    BIntensities = np.delete(BIntensities, indList)
    centers = np.delete(centers, indList)
    return intStandIntensities, durations, centers, AIntensities, BIntensities