import math
import heapq
import random

class Node :
    def __init__(self, idx, lat, lon) :
        self.idx = idx
        self.lat = lat
        self.lon = lon

coordinates = [
    [60.9716,17.5946],
    [60.9716,27.5946],
    [60.9716,37.5946],
    [60.9716,47.5946],
    [60.9716,57.5946],
    [60.9716,67.5946],
    [60.9716,77.5946],
    [60.9716,87.5946],
    [60.9716,97.5946],
    [60.9716,107.5946],
    [40.9716,17.5946],
    [40.9716,27.5946],
    [40.9716,37.5946],
    [40.9716,47.5946],
    [40.9716,57.5946],
    [40.9716,67.5946],
    [40.9716,77.5946],
    [40.9716,87.5946],
    [40.9716,97.5946],
    [40.9716,107.5946],
    [20.9716,17.5946],
    [20.9716,27.5946],
    [20.9716,37.5946],
    [20.9716,47.5946],
    [20.9716,57.5946],
    [20.9716,67.5946],
    [20.9716,77.5946],
    [20.9716,87.5946],
    [20.9716,97.5946],
    [20.9716,107.5946],
]

adj = []
n = 3
m = 10
for i in range(n*m):
    adj.append([])

weather = [1,2,2,1,2,3,2,3,3,1,2,3,1,3,3,2,1,1,2,3,2,3,3,3,2,3,3,2,3,3]

directions = [ [0,1], [1,0], [0,-1], [-1,0], [1,1], [1,-1], [-1,1], [-1,-1] ]

def getId(a,b) :
    return (m * a + b)

for i in range(n) :
    for j in range(m) :
        id = getId(i,j)
        for d in directions:
            x = i + d[0]
            y = j + d[1]
            if x >= 0 and x < 3 and y >= 0 and y < 10:
                xyid = getId(x,y)
                adj[id].append(xyid)

# print graph
# for i in range(n*m) :
#     print(str(i) + str(adj[i]))


def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Earth radius in km
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    dphi = math.radians(abs(lat2 - lat1))
    dlambda = math.radians(abs(lon2 - lon1))

    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

# def calculate_weight(node1, node2, parameters):
#     # Extract the relevant parameters for weight calculation
#     weather_factor = parameters.get('weather', 1.0)
#     fuel_cost_factor = parameters.get('fuel_cost', 1.0)
#     emergency_factor = parameters.get('emergency', 1.0)
#     distance = haversine(node1['lat'], node1['lon'], node2['lat'], node2['lon'])

#     # Combine factors into a single weight
#     weight = distance * weather_factor * fuel_cost_factor * emergency_factor
#     return weight

def a_star(start, goal):
    open_set = [(0,0)]
    came_from = {}
    g_score = [float('inf') for i in range(n*m)]
    g_score[start] = 0
    f_score = [float('inf') for i in range(n*m)]
    f_score[start] = haversine(coordinates[start][0], coordinates[start][1], coordinates[goal][0], coordinates[goal][1])

    while open_set:
        current = heapq.heappop(open_set)[1]

        if current == goal:
            total_path = []
            while current in came_from:
                total_path.append(current)
                current = came_from[current]
            total_path.append(start)
            return total_path[::-1]

        for neighbor in adj[current]:
            weight = weather[neighbor] * haversine(coordinates[neighbor][0],coordinates[neighbor][1],coordinates[current][0],coordinates[current][1])
            tentative_g_score = g_score[current] + weight

            if tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = g_score[neighbor] + haversine(coordinates[neighbor][0], coordinates[neighbor][1], coordinates[goal][0], coordinates[goal][1])
                heapq.heappush(open_set, (f_score[neighbor], neighbor))

    return None

# Example graph
graph = {
    'JFK': {'lat': 40.6413, 'lon': -73.7781, 'neighbors': ['LAX', 'CDG']},
    'LAX': {'lat': 33.9416, 'lon': -118.4085, 'neighbors': ['JFK', 'NRT']},
    'CDG': {'lat': 49.0097, 'lon': 2.5479, 'neighbors': ['JFK', 'NRT']},
    'NRT': {'lat': 35.7720, 'lon': 140.3929, 'neighbors': ['LAX', 'CDG']}
}

# Parameters for weight calculation
parameters = {
    'weather': 1.2,  # example weather factor
    'fuel_cost': 1.5,  # example fuel cost factor
    'emergency': 1.0  # example emergency factor
}

# Example usage
start = 0
goal = 12
optimal_path = a_star(start, goal)

if optimal_path is not None:
    print(f"The optimal path from {start} to {goal} is:")
    for airport in optimal_path:
        print(airport)
else:
    print(f"No path found from {start} to {goal}")


