from PIL import Image
import numpy as np
import random

"""
K-Means Clustering Strategy from Lecture: 
1. Pick k random points 
2. Partition by closeness (choose a center) 
3. Re-center (take the spatial average of all of the points) 
4. Repeat 
"""

class Classifier:
    def __init__(self, num_clusters):
        self.num_clusters = num_clusters

    # Groups pixels based on central pixel
    def group_pixels(self, clusters, pixels):
        groupings = []
        for i in range(self.num_clusters):
            groupings.append([])
        for p in pixels:
            minimum_distance = float('inf')
            for i in range(self.num_clusters):
                distance = find_euclidean_distance(p, clusters[i].center)
                if distance < minimum_distance:
                    minimum_distance = distance
                    index = i
            groupings[index].append(p)

        return groupings

    # Returns central pixel of cluster
    def find_central_pixel(self, pixels):
        n = len(pixels[0].coordinates)
        values = []
        for i in range(n):
            values.append(0)
        for p in pixels:
            for i in range(n):
                values[i] = values[i] + p.coordinates[i]
        total_pixels = len(pixels)
        central_pixel_values = []
        for v in values:
            central_pixel_values.append((v / total_pixels))
        central_pixel = Pixel(central_pixel_values)
        return central_pixel

# Finds euclidean distance between non-central points and central point
# Euclidean distance between points x and y = Sqrt(Sum for i = 1 to n of (yi - xi)^2)
def find_euclidean_distance(x, y):
    n = len(x.coordinates)
    for i in range(n):
        return np.sqrt(np.sum([(x.coordinates[i] - y.coordinates[i]) ** 2]))

# Extracts pixels from image given in path
def extract_pixels(num_images, path):
    print("Analyzing " + str(num_images) + " image(s)")
    img = Image.open(path)
    img = img.convert("RGB")
    width = img.size[0]
    height = img.size[1]
    product = width * height
    print("Image size: " + str(img.size))
    pixels = []
    for count, color in img.getcolors(product):
        for _ in range(count):
            pixels.append(Pixel(color))
    return pixels

# Finds n representative colors given filename
def find_rep_colors(filename, num_colors=5):
    pixels = extract_pixels(1, filename) # Extract pixels
    k_means_classifier = Classifier(num_colors) # Create classifier
    # Find clusters
    clusters = [Cluster(p, [p]) for p in random.sample(pixels, num_colors)]
    while True:
        dist = 0
        groupings = k_means_classifier.group_pixels(clusters, pixels)
        for i in range(num_colors):
            if not groupings[i]:
                continue
            old_cluster = clusters[i]
            center = k_means_classifier.find_central_pixel(groupings[i])
            new_cluster = Cluster(center, groupings[i])
            clusters[i] = new_cluster
            dist = max(find_euclidean_distance(old_cluster.center, new_cluster.center), dist)

        if dist < 10:
            break
    clusters.sort(key=lambda cluster: len(cluster.pixels), reverse=True)
    rgb_values = []
    for c in clusters:
        rgb_values.append(map(int, c.center.coordinates))
    return list(rgb_values)

# Represents a single pixel
# Each pixel has corresponding rgb values as coordinates
class Pixel:
    def __init__(self, coordinates):
        self.coordinates = coordinates

# Represents a cluster of pixels
# Each cluster contains non-central/central pixels
class Cluster:
    def __init__(self, center, pixels):
        self.center = center
        self.pixels = pixels

# Test
colors = find_rep_colors('pup.jpg', 5)
print(colors)


