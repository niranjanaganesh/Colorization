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
        self.min_diff = 10

    def fit(self, pixels):
        clusters = [Cluster(center=p, pixels=[p]) for p in random.sample(pixels, self.num_clusters)]

        while True:

            plists = self.assign_points(clusters, pixels)
            diff = 0

            for i in range(self.num_clusters):
                if not plists[i]:
                    continue
                old = clusters[i]
                center = self.find_center(plists[i])
                new = Cluster(center, plists[i])
                clusters[i] = new
                diff = max(diff, find_euclidean_distance(old.center, new.center))

            if diff < self.min_diff:
                break

        return clusters

    def assign_points(self, clusters, pixels):
        plists = [[] for i in range(self.num_clusters)]

        for p in pixels:
            smallest_distance = float('inf')

            for i in range(self.num_clusters):
                distance = find_euclidean_distance(p, clusters[i].center)
                if distance < smallest_distance:
                    smallest_distance = distance
                    index = i

            plists[index].append(p)

        return plists

    def find_center(self, pixels):
        n_dim = len(pixels[0].coordinates)
        vals = [0.0 for i in range(n_dim)]
        for p in pixels:
            for i in range(n_dim):
                vals[i] += p.coordinates[i]
        coords = [(v / len(pixels)) for v in vals]
        return Pixel(coords)

# Finds euclidean distance between non-central points and central point
# Euclidean distance between points x and y = Sqrt(Sum for i = 1 to n of (yi - xi)^2)
def find_euclidean_distance(x, y):
    n_dim = len(x.coordinates)
    #return np.sqrt(sum([(p.coordinates[i] - q.coordinates[i]) ** 2 for i in range(n_dim)]))
    for i in range(n_dim):
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

# Don't need
def rgb_to_hex(rgb):
    return '#%s' % ''.join(('%02x' % p for p in rgb))

# Finds n representative colors given filename
def find_rep_colors(filename, n_colors=5):
    pixels = extract_pixels(1, filename)
    clusters = Classifier(num_clusters=n_colors).fit(pixels)
    clusters.sort(key=lambda c: len(c.pixels), reverse=True)
    rgb_values = [map(int, c.center.coordinates) for c in clusters]
    #return list(map(rgb_to_hex, rgb_values))
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

colors = find_rep_colors('pup.jpg', n_colors=5)
print(colors)


