import math
import heapq

def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Earth radius in km
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    dphi = math.radians(abs(lat2 - lat1))
    dlambda = math.radians(abs(lon2 - lon1))

    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c


def getId(i,j,cols) :
    return (cols * i + j)

def get_node_index(coordinates, node):
    sourceLat = node['lat']
    sourceLong = node['long']
    d = float('inf')
    index = (0,0)
    for i,l in enumerate(coordinates):
        for j,latLong in enumerate(l):
            lat = latLong['lat']
            long = latLong['long']
            dist = haversine(sourceLat,sourceLong,lat, long)
            if dist < d:
                d = dist
                index = (i,j)
    return index
                
def a_star(coordinates, weather, start, goal):
    directions = [ [0,1], [1,0], [0,-1], [-1,0], [1,1], [1,-1], [-1,1], [-1,-1] ]
    rows = len(coordinates)
    cols = len(coordinates[0])
    # print(f"rows : {rows}")
    # print(f"cols : {cols}")
    open_set = [(0,start)]
    came_from = {}
    g_score = [[float('inf') for j in range(cols)] for i in range(rows)]
    g_score[start[0]][start[1]] = 0
    f_score = [[float('inf') for j in range(cols)] for i in range(rows)]
    f_score[start[0]][start[1]] = haversine(coordinates[start[0]][start[1]]['lat'], coordinates[start[0]][start[1]]['long'], coordinates[goal[0]][goal[1]]['lat'], coordinates[goal[0]][goal[1]]['long'])

    while open_set:
        current = heapq.heappop(open_set)[1]
        i = current[0]
        j = current[1]

        if current == goal:
            total_path = []
            while current in came_from:
                total_path.append({"lat" : coordinates[current[0]][current[1]]['lat'], "long" : coordinates[current[0]][current[1]]['long']})
                # total_path.append(current)
                current = came_from[current]
            total_path.append({"lat" : coordinates[start[0]][start[1]]['lat'], "long" : coordinates[start[0]][start[1]]['long']})
            # total_path.append(start)
            return (f_score[goal[0]][goal[1]], total_path[::-1])
        
        for d in directions:
            x = i + d[0]
            y = j + d[1]
            # print(f"x : {x}")
            # print(f"y : {y}")

            if x >= 0 and x < rows and y >= 0 and y < cols:
                # neighbour is (x,y)
                weight = haversine(
                    coordinates[x][y]['lat'], 
                    coordinates[x][y]['long'], 
                    coordinates[i][j]['lat'], 
                    coordinates[i][j]['long']
                )
                tentative_g_score = g_score[i][j] + weight

                if tentative_g_score < g_score[x][y]:
                    came_from[(x,y)] = current
                    g_score[x][y] = tentative_g_score
                    f_score[x][y] = g_score[x][y] + haversine(coordinates[x][y]['lat'], coordinates[x][y]['long'], coordinates[goal[0]][goal[1]]['lat'], coordinates[goal[0]][goal[1]]['long'])
                    heapq.heappush(open_set, (f_score[x][y], (x,y)))

        # for neighbor in coordinates[current[0]][current[1]]:
        #     weight = weather[neighbor] * haversine(coordinates[neighbor][0],coordinates[neighbor][1],coordinates[current][0],coordinates[current][1])
        #     tentative_g_score = g_score[current] + weight

        #     if tentative_g_score < g_score[neighbor]:
        #         came_from[neighbor] = current
        #         g_score[neighbor] = tentative_g_score
        #         f_score[neighbor] = g_score[neighbor] + haversine(coordinates[neighbor][0], coordinates[neighbor][1], coordinates[goal][0], coordinates[goal][1])
        #         heapq.heappush(open_set, (f_score[neighbor], neighbor))

    return None

def get_path(coordinates, weather, source, destination):
    sourceIndex = get_node_index(coordinates,source)
    destinationIndex = get_node_index(coordinates,destination)

    path = a_star(coordinates,weather,sourceIndex,destinationIndex)

    return path