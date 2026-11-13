# Dynamic Binning For Data Streams

## Implementation of part 3 of the Algorithm of "Differential privacy histogram publishing method based on dynamic sliding window"
**Input:** Tuple of (time, personId, energyConsumption)
**Output:** histogram

K ... Number of cluster
M ... Maximum number of clusters

for K=1 --> M do  
    Cluster data through k-means++;  
    Calculate the SSE (square sum of errors) of clustering;  
end  
Draw the relationship graph of K and SSE;  
Obtain the optimal K value by calculating the adjacent slope change degree based on the graph;  
Select the clustering result corresponding to the optimal K for forming the group to be released;  
Add Laplace noise to the group for publishing histogram.

### k-means++ Algo
**Input:** All data points
**Output:** All selected centers
1. First center: choose the first cluster centrum random from the data points
2. Subsequent centers: For each remaining center:
    - calculate the distance from each data point to its nearest existing center
    - choose the next center with probability proportional to the square of this distance (square is important to ensure that point far from existing centers are much more likely to be chosen) $P(x)={(D(x)^2)\over(\sum_{x'}D(x')^2)}$
    - points farther from existing centers have a higher chance of being selected
3. Standard K-means: Once all k centers are initialized, procees with the standard K-means 


### k-means Algo
**Input:** All centers
**Output:** All clusters

1. Each data point is assigned to the nearest centroid
    - Distance between a data point x and a centroid c is calculated: $d(x,c)=\sqrt{\sum^n_{i=1}(x_i-c_i)^2}$
2. After the assignment, we recalculate the centroid of each cluster by averaging the points within it
    - the mean of a centroid is calculated: $c_j={1\over|C_j|} \sum_{x_i \in C_j} x_i$
3. Repeat this process until the centroids no longer change or the maximum number of iterations is reached


## Our implementation
**Input:** Tuple of (time, personId, energyConsumption)
**Output:** histogram

K ... Number of cluster
M ... Maximum number of clusters

for K=1 --> M do  
    Cluster data through k-means++;  
    Calculate the SSE (square sum of errors) of clustering;  
end  
Draw the relationship graph of K and SSE;  
Obtain the optimal K value by calculating the adjacent slope change degree based on the graph;  
Select the clustering result corresponding to the optimal K for forming the group to be released; 
Fill gaps with intervalls to get a complete range. 
Add by coin choice a 1 size intervall into every filling intervalls to divide the intervalls.
Add Laplace noise to the group for publishing histogram.

### Distance calculation of two histogramms

We check distribution of a histogram by calculate the percentage of each bin to the total count of datapoints.
By using theTotal Variation Distance (TVD): $1/2 * \sum((\abs p_2 -p_1)) we calculate the shift from the older hist to the newer.
We define a threshold. If this threshold is reached we need to recalculate the Intervalls for the new histogram. If not we output the histogram with the old bins.