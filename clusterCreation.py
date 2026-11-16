import numpy as np
import random
import math

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
wholeDomain =  (0, 100)
threshold = 2
windowSize = 4
maxClusters = windowSize 
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
        selection_probabilitys = selection_probability(distances)
        nextCluster = rouletteWheel(values, selection_probabilitys)
        clusters.append(nextCluster)
    bestClusters = k_means(values, clusters)
    return bestClusters



def distancePoints(dataPoints, clusterCenters):
    distances = []
    for value in dataPoints:
        shortestDistances = min([abs(value - cluster) for cluster in clusterCenters])
        distances.append(shortestDistances)
    return distances

def selection_probability(listDistances):
    sumOfDistances = sum(listDistances)
    return [d/sumOfDistances for d in listDistances]

def rouletteWheel(values, probability):
    return random.choices(values, weights=probability, k=1)[0]

def k_means(dataPoints, currentClusterCenters):
    newCenters = []
    while sorted(currentClusterCenters) != sorted(newCenters):
        if newCenters:
            currentClusterCenters = newCenters
        closestCluster = [min(currentClusterCenters, key=lambda c: abs(p-c))for p in dataPoints]
        clusterAssignment = assignPointsToCluster(dataPoints, closestCluster)
        newCenters = calculateClusterMean(clusterAssignment)
        newCentersList = list(newCenters.keys())
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

def add_gap(histogram, low, high):
    flip = random.randint(0,1)
    if flip < 0.5 and high - low > 1:
        histogram[(low, high)] = 0
    else: 
        p = random.uniform(low, high)
        histogram[(low, p)] = 0
        histogram[(p, p)] = 0
        histogram[(p, high)] = 0
    return histogram

def get_best_clustering(data,optimal_k):
    clusters = k_means_plus_plus(data, optimal_k)
    histogram = {}
    for cluster in clusters:
        histogram[(clusters[cluster][0], clusters[cluster][-1])] = len(clusters[cluster])

    # define start and end
    bins = sorted(histogram.keys())
    if wholeDomain is not None:
        start, end = wholeDomain
    else:
        start, end = bins[0][0], bins[-1][1]

    #fill gaps
    filled_histogram = {}
    current = start
    for (a,b) in bins:
        if a > current: 
            add_gap(filled_histogram, current, a)
        filled_histogram[(a,b)] = histogram[(a,b)]
        current = b
    if current < end:
        add_gap(filled_histogram, current, end)
    
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
    print("difference:", difference)
    return difference < threshold

def get_window(dataStream, windowSize, currentPlace):
    return [tuple for tuple in dataStream if currentPlace <= tuple[0] < currentPlace + windowSize]

def process_window(dataStream, windowSize, currentPlace, threshold, max_clusters): # windowsize should not be smaller than 4
    data = dataStream[currentPlace:currentPlace + windowSize]
    preprocessed_data = preproces_stream(data)
    noisy_histogram = find_clusters(preprocessed_data, max_clusters) # here we have the noisy histogram
    currentPlace += 1
    max_time = max([tuple[0] for tuple in dataStream])
    while currentPlace + windowSize <= max_time: #TODO: hier wäre eine andere Abbruchbedingung sinnvoll, da wir ja eigentlich die letzte Zeit nicht kennen
        print("currentPlace:", currentPlace)
        next_data = get_window(dataStream, windowSize, currentPlace)
        preprocessed_data = preproces_stream(next_data)
        next_noisy_histogram = find_clusters(preprocessed_data, max_clusters) # here we have the noisy histogram
        check = check_for_recalculation(calc_distribution(noisy_histogram), calc_distribution(next_noisy_histogram), threshold)
        if not check:
            noisy_histogram = next_noisy_histogram
            print("Recalculation needed. New histogram:", noisy_histogram)
        if check:
            print("No recalculation needed. Histogram remains the same.")
        currentPlace += 1
        data = next_data
    return noisy_histogram


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
print("process_window:", process_window(data, windowSize, currentPlace, threshold, maxClusters))