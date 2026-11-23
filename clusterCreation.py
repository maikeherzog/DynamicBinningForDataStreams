import numpy as np
import pandas as pd
import random
import math
from load_london import load_london
import time
from collections import defaultdict

#data=[(1,1,20), (1,2,22), (1,3,25), (1,4,27), (1,5,30), (1,6,89)]
#data=[(1,1,20), (1,2,21), (1,3,22), (1,4,21), (1,5,20), (1,6,22)] #(time, person_id, value)
data = [
    # Phase 1: Werte überwiegend um 20–30, einzelne um 85–90
    (1, 1, 21), (1, 2, 88),
    (2, 3, 24), (2, 1, 22),
    (3, 2, 90), (3, 4, 27),
    (4, 3, 25),
    (5, 1, 23), (5, 4, 86),
    (6, 2, 28),
    # Phase 2: Verteilung verschiebt sich nach 50–60
    (7, 1, 52), (7, 3, 55),
    (8, 4, 58), (8, 2, 87),
    (9, 1, 54),
    (10, 3, 57), (10, 4, 60),
    (11, 2, 53),
    (12, 1, 89), (12, 3, 56),
]
data2 = [
    # Phase 1: Werte überwiegend um 20–30, einzelne um 85–90
    (1, 1, 21), (1, 2, 88),
    (1, 3, 24), (1, 1, 22),
    (1, 2, 90), (1, 4, 27),
    (1, 3, 25),
    (1, 1, 23), (1, 4, 86),
    (1, 2, 28),
    # Phase 2: Verteilung verschiebt sich nach 50–60
    (2, 1, 52), (2, 3, 55),
    (2, 4, 58), (2, 2, 87),
    (2, 1, 54),
    (2, 3, 57), (2, 4, 60),
    (2, 2, 53),
    (2, 1, 89), (2, 3, 56),
    # Phase 3: Werte überwiegend um 20–30, einzelne um 85–90
    (3, 1, 21), (3, 2, 88),
    (3, 3, 24), (3, 1, 22),
    (3, 2, 90), (3, 4, 27),
    (3, 3, 25),
    (3, 1, 23), (3, 4, 86),
    (3, 2, 28),
    # Phase 4: Verteilung verschiebt sich nach 50–60
    (4, 1, 52), (4, 3, 55),
    (4, 4, 58), (4, 2, 87),
    (4, 1, 54),
    (4, 3, 57), (4, 4, 60),
    (4, 2, 53),
    (4, 1, 89), (4, 3, 56),
]

data3 = [
    # Phase 1: Werte überwiegend um 20–30, einzelne um 85–90
    (1, 1, 21), (1, 2, 88),
    (1, 3, 24), (1, 1, 22),
    (1, 2, 90), (1, 4, 27),
    (1, 3, 25),
    (1, 1, 23), (1, 4, 86),
    (1, 2, 28),
    # Phase 2: Verteilung verschiebt sich nach 50–60
    (2, 1, 52), (2, 3, 55),
    (2, 4, 58), (2, 2, 87),
    (2, 1, 54),
    (2, 3, 57), (2, 4, 60),
    (2, 2, 53),
    (2, 1, 89), (2, 3, 56),
    # Phase 3: Werte überwiegend um 20–30, einzelne um 85–90
    (3, 1, 52), (3, 3, 55),
    (3, 4, 58), (3, 2, 87),
    (3, 1, 54),
    (3, 3, 57), (3, 4, 60),
    (3, 2, 53),
    (3, 1, 89), (3, 3, 56),
    # Phase 4: Verteilung verschiebt sich nach 50–60
    (4, 1, 21), (4, 2, 88),
    (4, 3, 24), (4, 1, 22),
    (4, 2, 90), (4, 4, 27),
    (4, 3, 25),
    (4, 1, 23), (4, 4, 86),
    (4, 2, 28),
]
wholeDomain =  (0, 17)
threshold = 1
windowSize = 1
maxClusters = 8 
currentPlace = 0

def preproces_stream(data):
    # Extract the third element from each tuple in the stream
    processed_data = [item[2] for item in data]
    return processed_data

def find_clusters(data, max_clusters):
    n_distinct = len(np.unique(data))
    upper = min(max_clusters, n_distinct)
    
    different_k = {}
    for k in range (1, upper +1): 
        clusters=k_means_plus_plus(data, k) #Dict mit cluster als key und liste der zugehörigen Punkte als value
        different_k[k] = sse(clusters) # returns a number, the sum of squared errors for the clustering

    #draw_relationship_graph() #TODO: Brauchen wir das? Ich denke nicht
    optimal_k = calc_optimal_k(different_k)
    histogram = get_best_clustering(data,optimal_k) 
    noisy_histogram = add_noise(histogram)
    return noisy_histogram

def k_means_plus_plus(values, num_of_clusters):
    clusters = []
    c1 = np.random.choice(values) #values has to be a list
    clusters.append(c1)
    while len(clusters) < num_of_clusters:
        distances = distancePoints(values, clusters)
        if sum(distances) == 0:
            brak
        selection_probabilitys = selection_probability(distances)
        nextCluster = rouletteWheel(values, selection_probabilitys)
        clusters.append(nextCluster)
    bestClusters = k_means(values, clusters)
    return bestClusters



def distancePoints(dataPoints, clusterCenters):
    distances = []
    for value in dataPoints:
        shortestDistances = min([abs(value - cluster) for cluster in clusterCenters]) ** 2
        distances.append(shortestDistances)
    return distances

def selection_probability(listDistances):
    sumOfDistances = sum(listDistances)
    return [d/sumOfDistances for d in listDistances]

def rouletteWheel(values, probability):
    return random.choices(values, weights=probability, k=1)[0]

def k_means(dataPoints, currentClusterCenters, max_iter=100):
    newCenters = []
    iterations = 0
    while sorted(currentClusterCenters) != sorted(newCenters) and iterations < max_iter:
        if newCenters:
            currentClusterCenters = newCenters
        closestCluster = [min(currentClusterCenters, key=lambda c: abs(p-c))for p in dataPoints]
        clusterAssignment = assignPointsToCluster(dataPoints, closestCluster)
        newCenters = list(calculateClusterMean(clusterAssignment).keys())
        iterations += 1
    return clusterAssignment
    
def assignPointsToCluster(dataPoints, closestCluster):
    clusterAssignment = {}
    for point, cluster in zip(dataPoints, closestCluster):
        if cluster not in clusterAssignment:
            clusterAssignment[cluster] = []
        clusterAssignment[cluster].append(point)
    return clusterAssignment

def calculateClusterMean(clusterAssignment):
    newCenters = {}
    for cluster, points in clusterAssignment.items():
        mean = sum(points)/ len(points)
        newCenters[mean] = points
    return newCenters

def sse(clusters):
    total_sse = 0
    for predicted in clusters.keys():
        actualNumbers = clusters[predicted]
        total_sse += sum((actual - predicted) ** 2 for actual in actualNumbers)
    return total_sse

def calc_optimal_k(different_k):
    # calc gradients from k to k'
    gradients = {}
    for k in different_k.keys():
        if k+1 in different_k:
            gradients[(k, k+1)] = different_k[k+1] - different_k[k]
    
    #bending
    bending = {}
    for (k_before, k), bending_before in gradients.items():
        if (k, k+1) in gradients:
            bending_after = gradients[(k, k+1)]
            if bending_before != 0:
                bending[k] = (bending_after - bending_before) / different_k[k]

    best_k = max(bending, key=bending.get)
    return best_k

def add_gap(histogram, low, high, closed="neither"):
    flip = random.randint(0,1)
    if flip < 0.5 and high - low > 1:
        histogram[pd.Interval(low, high, closed="neither")] = 0
    else: 
        p = random.uniform(low, high)
        left_closed = "left" if closed in ("left", "both") else "neither"
        right_closed = "right" if closed in ("right", "both") else "neither"
        histogram[pd.Interval(low, p, closed=left_closed)] = 0
        histogram[pd.Interval(p, p, closed="both")] = 0
        histogram[pd.Interval(p, high, closed=right_closed)] = 0
    return histogram

def get_best_clustering(data,optimal_k):
    clusters = k_means_plus_plus(data, optimal_k)
    histogram = {}
    for cluster in clusters:
        points = clusters[cluster]
        histogram[pd.Interval(min(points), max(points), closed="both")] = len(points)

    # define start and end
    bins = sorted(histogram.keys(), key=lambda iv: (iv.left, iv.right))
    if wholeDomain is not None:
        start, end = wholeDomain
    else:
        start, end = bins[0].left, bins[-1].right

    #fill gaps
    filled_histogram = {}
    current = start
    for i, iv in enumerate(bins):
        if iv.left > current: 
            closed = "left" if i == 0 else "neither"
            add_gap(filled_histogram, current, iv.left, closed)
        filled_histogram[iv] = histogram[iv]
        current = iv.right
    if current < end:
        add_gap(filled_histogram, current, end, "right")
    
    return filled_histogram

def add_noise(histogram):
    epsilon = 1.0
    sensitivity = 1
    scale = sensitivity / epsilon

    noisy_histogram = {key: value + np.random.laplace(0, scale) for key, value in histogram.items()}
    return noisy_histogram

def calc_distribution(histogram):
    total_count = sum(histogram.values())
    distribution = {key: value / total_count for key, value in histogram.items()}
    return distribution

def compare_distributions(dist1, dist2):
    total_difference = 0
    total_difference = 0.5*sum(abs(dist1.get(key, 0) - dist2.get(key, 0)) for key in set(dist1.keys()).union(set(dist2.keys())))
    return total_difference

def check_for_recalculation(dist1, dist2, threshold): # True: we dont need to recalculate, False: we need to recalculate
    difference = compare_distributions(dist1, dist2)
    #print("difference:", difference)
    # print(f"TVD = {difference:.3f}")
    return difference <= threshold

def get_window(dataStream, windowSize, currentPlace):
    return [tuple for tuple in dataStream if currentPlace <= tuple[0] < currentPlace + windowSize]

def build_histogram_with_old_interval(data, bins):
    bins = sorted(bins, key=lambda iv: (iv.left, iv.right))
    histogram = {b: 0 for b in bins}
    outside_bin = 0

    for value in data:
        for b in bins:
            if value in b:
                histogram[b] += 1
                break
        else:
            outside_bin += 1
    return histogram, outside_bin

def output_histogram(histogram):
    #print("Histogram:", histogram)
    pass

def get_window(by_day, start, windowSize):
    return [tup for day in range(start, start + windowSize) for tup in by_day[day]]

def process_window(dataStream, windowSize, currentPlace, threshold, max_clusters, timeStep=1): # windowsize should not be smaller than 4
    by_day = defaultdict(list)
    for tup in dataStream:
        by_day[tup[0]].append(tup)

    currentPlace = min(by_day)
    max_time = max(by_day)

    currentPlace = min(tup[0] for tup in dataStream)
    #data = dataStream[currentPlace:currentPlace + windowSize]
    #data = [tup for tup in dataStream if currentPlace <= tup[0] < currentPlace + windowSize]
    preprocessed_data = preproces_stream(get_window(by_day, currentPlace, windowSize))
    noisy_histogram = find_clusters(preprocessed_data, max_clusters) # here we have the noisy histogram
    current_bins = noisy_histogram.keys()
    currentPlace += 1
    max_time = max([tuple[0] for tuple in dataStream])
    #print("------------------------------------------------------")
    #print("first Histogram:")
    output_histogram(noisy_histogram)
    recalculations = 0
    while currentPlace + windowSize <= max_time + timeStep: #TODO: hier wäre eine andere Abbruchbedingung sinnvoll, da wir ja eigentlich die letzte Zeit nicht kennen
        #print("currentPlace:", currentPlace)
        #next_data = get_window(dataStream, windowSize, currentPlace)
        preprocessed_data = preproces_stream(get_window(by_day, currentPlace, windowSize))
        next_histogram, outside = build_histogram_with_old_interval(preprocessed_data, current_bins)
        #print("Outside", outside)
        next_noisy_histogram = add_noise(next_histogram)
        #next_noisy_histogram = find_clusters(preprocessed_data, max_clusters) # here we have the noisy histogram
        check = check_for_recalculation(calc_distribution(noisy_histogram), calc_distribution(next_noisy_histogram), threshold)
        if not check:
            noisy_histogram = find_clusters(preprocessed_data, max_clusters)
            current_bins = noisy_histogram.keys()
            #print("------------------------------------------------------")
            #print("Recalculation needed. New histogram:")
            #output_histogram(noisy_histogram)
            recalculations += 1
        if check:
            #print("------------------------------------------------------")
            #print("No recalculation needed. Histogram remains the same.")
            #output_histogram(next_noisy_histogram)
            pass
        currentPlace += 1
    print(f"Neu berechnet an {recalculations} von {currentPlace - min(by_day) - 1} Tagen")  
    return True


#data = preproces_stream(data)
#print("data:", data)
#erg = k_means_plus_plus(data, 2)
#print("erg:", erg)
#erg2=sse(erg)
#print("erg2:", erg2)

#print(calc_optimal_k({1: 3497.5, 2: 62.8, 3: 17.17, 4: 4, 5: 2}))
#histogram =get_best_clustering(data, 2)
#print("get_best_clustering:", histogram) 
#print("add_noise:", add_noise(histogram))
#print("calc_distribution:", calc_distribution(histogram))
#hist = calc_distribution(histogram)
#print("compare_distributions:", compare_distributions(hist, add_noise(histogram)))
#print("check_for_recalculation:", check_for_recalculation(hist, hist, threshold))

#print("find_clusters:", find_clusters(data))
#print("process_window:", process_window(data3, windowSize, currentPlace, threshold, maxClusters))

if __name__ == "__main__":
    data = load_london(max_users=None, end_date="2012-01-31") 

    wholeDomain = (0, 17)
    windowSize = 1          # 1 Tag pro Fenster
    maxClusters = 8
    threshold = 0.1
    currentPlace = 0        # wird in process_window überschrieben

    for i in range(1,10):
        start = time.perf_counter()
        print("Durchgang: ", i)
        process_window(data, windowSize, currentPlace, threshold, maxClusters)
        print(f"Laufzeit: {time.perf_counter() - start:.1f} s")
