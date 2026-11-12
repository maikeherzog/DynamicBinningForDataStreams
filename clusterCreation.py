import numpy as np
import random
import math

data=[(1,1,20), (1,2,22), (1,3,25), (1,4,27), (1,5,30), (1,6,89)]
numOfClusters=2
wholeDomain =  (0, 100)

def preproces_stream(data):
    # Extract the third element from each tuple in the stream
    processed_data = [item[2] for item in data]
    return processed_data

def find_clusters(data, numOfClusters):
    different_k = {}
    for k in range (1, len(data)):
        clusters=k_means_plus_plus(data, k) #Dict mit cluster als key und liste der zugehörigen Punkte als value
        different_k[k] = sse(clusters) # returns a number, the sum of squared errors for the clustering

    #draw_relationship_graph() #TODO: Brauchen wir das? Ich denke nicht
    optimal_k = calc_optimal_k(different_k)
    get_best_clustering(data,optimal_k) 
    add_noise()
    return 0

def k_means_plus_plus(values, numOfClusters):
    clusters = []
    c1 = np.random.choice(values) #values has to be a list
    clusters.append(c1)
    while len(clusters) < numOfClusters:
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
        p = random.randint(low+1, high-1)
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

data = preproces_stream(data)
print("data:", data)
erg = k_means_plus_plus(data, 2)
print("erg:", erg)
erg2=sse(erg)
print("erg2:", erg2)

print(calc_optimal_k({1: 3497.5, 2: 62.8, 3: 17.17, 4: 4, 5: 2}))
histogram =get_best_clustering(data, 2)
print("get_best_clustering:", histogram) 
print("add_noise:", add_noise(histogram))