import matplotlib.pyplot as plt
import numpy as np
import random
from shapely.geometry import Point, Polygon

# class definition to obtain random point within a set of point obtained from:
# https://stackoverflow.com/questions/58415606/create-random-points-within-a-polygon-within-a-class
class Agent():
    def __init__(self, bounds):
        self.polygon = Polygon(bounds)

    def add_random_point(self):
        xmin, ymin, xmax, ymax = self.polygon.bounds
        while True:
            x = random.uniform(xmin, xmax)
            y = random.uniform(ymin, ymax)

            if Point(x, y).within(self.polygon):
                return x, y
                break


times = 10000


def unexpected_plots():
    """
    Question 1: Unexpected Plots.

    Write a python function that will plot the points that come from the following
    procedure:

    Create a regular hexagon
    Pick a random point, P, inside the hexagon.
    Make a triangle, T, by randomly connecting P to two adjacent vertices of the
    hexagon.
    Compute the centroid of T. This becomes your new random point, P.  Save it,
    make a new random triangle as above, compute the new centroid etc…
    Repeat this process 10,000 times.
    Make a scatter plot of all your 10,000 random points. What emerges?

    ANSWER: a snowflake pattern!
    """
    # Definiting the vertices of a regular hexagon
    r = 1  # radius of regular hexagon
    h = 0  # y coordinate of center of regular hexagon
    v1 = [r, h]
    v2 = [r/2, h + np.sqrt(3)*(r/2)]
    v3 = [-r/2, h + np.sqrt(3)*(r/2)]
    v4 = [-r, h]
    v5 = [-r/2, h - np.sqrt(3)*(r/2)]
    v6 = [r/2, h - np.sqrt(3)*(r/2)]

    # Array of coordinates forming regular hexagon
    hex_coords = np.array([v1, v2, v3, v4, v5, v6])
    # Repeating first point to connect scatter points when plotting
    hex_coords_plot = np.array([v1, v2, v3, v4, v5, v6, v1])

    # Initialising empty lists for storing boundaries and random points
    boundaries = []
    random_points_x = []
    random_points_y = []

    for i in range(0, times, 1):
        # If loop only activates in first instance
        if i == 0:
            # Getting the boundaries of the regular hexagon
            obj = Agent(hex_coords)
            # Getting coordinates of random point P within regular hexagon
            P_x, P_y = obj.add_random_point()

            # Updating random_points x and y lista with coordinates of point P
            random_points_x.append(P_x)
            random_points_y.append(P_y)

            # Putting P coordinates in an array
            nPoint = np.array([P_x, P_y])
            # print('nPoint', nPoint)

        # Else loop after intial random P obtained in first iteration
        else:
            # Getting the boundaries of the previous shape
            obj = Agent(boundaries[-1])

            # Getting the latest point/centroid from previous iteration

            nPoint_x = random_points_x[-1]
            nPoint_y = random_points_y[-1]
            nPoint = np.array([nPoint_x, nPoint_y])
            # print('nPoint', nPoint)

        # Randomly picking two adjacent vertices of regular hexagon
        pick_2_vertices = hex_coords[np.random.choice(hex_coords.shape[0], 2, replace=False), :]

        # Coordinates of new triangle formed
        tri_coords = np.vstack((pick_2_vertices, nPoint))

        # Updating boundaries list with the coordinates of tehe latest triangle
        boundaries.append(tri_coords)

        # Finding the centroid of latest triangle
        T_centroid_x = sum(tri_coords[:, 0]) / 3
        T_centroid_y = sum(tri_coords[:, 1]) / 3

        # Updating random_points x and y lista with coordinates of centroid
        random_points_x.append(T_centroid_x)
        random_points_y.append(T_centroid_y)

    # print('Boundaries: ', boundaries)
    # print('Random points x: ', random_points_x)
    # print('Random points y: ', random_points_y)

    # Plotting the results of the random/centroid points obtained
    fig, ax = plt.subplots(1)
    plt.title('Unexpected plot')
    # Plotting the boundaries of the regular hexagon
    plt.plot(hex_coords_plot[:, 0], hex_coords_plot[:, 1], '-ok')
    # Plotting the random points/centroids obtained
    plt.scatter(random_points_x, random_points_y, marker='$T_c$', s=20, c='b', alpha=0.5)
    # Plotting the initial random point
    plt.scatter(P_x, P_y, marker='$P$', s=40, c='r')
    plt.show()
    print('Ho Ho Ho!')
    return random_points_x, random_points_y, boundaries


random_points_x, random_points_y, boundaries = unexpected_plots()
