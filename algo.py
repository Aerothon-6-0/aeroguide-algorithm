import math
import heapq
from risk import get_risk_details

hour = 14 #assuming hour to be constant now, later will update it to take off timing

weatherCodeStatus = {
    "0": "Clear sky",
    "1": "Mainly clear",
    "2": "Partly cloudy",
    "3": "Heavily cloudy (overcast)",
    "45": "Fog",
    "48": "Depositing rime fog",
    "51": "Light drizzle",
    "53": "Moderate drizzle",
    "55": "Dense drizzle",
    "56": "Freezing drizzle light",
    "57": "Freezing drizzle dense",
    "61": "Slight rain",
    "63": "Moderate rain",
    "65": "Heavy rain",
    "66": "Freezing rain light",
    "67": "Freezing rain heavy",
    "71": "Slight snow fall",
    "73": "Moderate snow fall",
    "75": "Heavy snow fall",
    "77": "Snow grains",
    "80": "Slight rain showers",
    "81": "Moderate rain showers",
    "82": "Violent rain showers",
    "85": "Slight snow showers",
    "86": "Heavy snow showers",
    "95": "Slight or moderate thunderstorm",
    "96": "Thunderstorm with slight hail",
    "99": "Thunderstorm with heavy hail"
}


def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Earth radius in km
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    dphi = math.radians(abs(lat2 - lat1))
    dlambda = math.radians(abs(lon2 - lon1))

    a = (math.sin(dphi / 2) ** 2) + math.cos(phi1) * math.cos(phi2) * (math.sin(dlambda / 2) ** 2)
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



def get_weather_factor(weather_details):
    # rain snowfall cloud_cover weather_code wind_speed
    max_rain = 4
    max_wcode = 100
    min_req_visibility = 100
    max_wind_speed = 500

    rainFactor = weather_details['rain'] / max_rain
    wcodeFactor = weather_details['weatherCode'] / max_wcode
    visibilityFactor = 0.8 if weather_details['visibility'] < min_req_visibility else 0
    windSpeedFactor = weather_details['windSpeed180m'] / max_wind_speed

    return 1 + rainFactor + wcodeFactor + visibilityFactor + windSpeedFactor

path_labels = []

def a_star(coordinates, start, goal):
    directions = [ [0,1], [1,0], [0,-1], [-1,0], [1,1], [1,-1], [-1,1], [-1,-1] ]
    rows = len(coordinates)
    cols = len(coordinates[0])
    open_set = [(0,start)]
    came_from = {}
    g_score = [[float('inf') for j in range(cols)] for i in range(rows)]
    g_score[start[0]][start[1]] = 0
    f_score = [[float('inf') for j in range(cols)] for i in range(rows)]
    f_score[start[0]][start[1]] = 0
    # total_distance = haversine(coordinates[start[0]][start[1]]['lat'], coordinates[start[0]][start[1]]['long'], coordinates[goal[0]][goal[1]]['lat'], coordinates[goal[0]][goal[1]]['long'])

    while open_set:
        current = heapq.heappop(open_set)[1]
        i = current[0]
        j = current[1]

        if current == goal:
            total_path = []
            while current in came_from:
                weather_code = str(coordinates[current[0]][current[1]]['formattedHourlyData'][hour]['weatherCode'])
                total_path.append({
                        # "x,y" : current,
                        "lat" : coordinates[current[0]][current[1]]['lat'], 
                        "long" : coordinates[current[0]][current[1]]['long'],
                        "status" : weatherCodeStatus[weather_code] if weather_code in weatherCodeStatus else "Not defined"
                    })
                path_labels.append((weatherCodeStatus[weather_code] if weather_code in weatherCodeStatus else ""))
                # total_path.append(current)
                current = came_from[current]
            start_weather_code = str(coordinates[start[0]][start[1]]['formattedHourlyData'][hour]['weatherCode'])
            total_path.append({
                # "x,y" : start,
                "lat" : coordinates[start[0]][start[1]]['lat'], 
                "long" : coordinates[start[0]][start[1]]['long'],
                "status" : weatherCodeStatus[start_weather_code] if start_weather_code in weatherCodeStatus else "Not defined"
                })
            path_labels.append(weatherCodeStatus[start_weather_code] if start_weather_code in weatherCodeStatus else "")
            # total_path.append(start)
            return (total_path[::-1])
        
        for d in directions:
            x = i + d[0]
            y = j + d[1]

            if x >= 0 and x < rows and y >= 0 and y < len(coordinates[x]):
                # current is (i,j)
                # neighbour is (x,y)
                # print(f"x={x} y={y}")
                weather_factor = get_weather_factor(coordinates[x][y]['formattedHourlyData'][hour])
                distance = haversine(
                    coordinates[x][y]['lat'], 
                    coordinates[x][y]['long'], 
                    coordinates[i][j]['lat'], 
                    coordinates[i][j]['long']
                )

                weight = distance * weather_factor

                tentative_g_score = g_score[i][j] + weight

                if tentative_g_score < g_score[x][y]:
                    came_from[(x,y)] = current
                    g_score[x][y] = tentative_g_score
                    f_score[x][y] = f_score[i][j] + haversine(coordinates[x][y]['lat'], coordinates[x][y]['long'], coordinates[i][j]['lat'], coordinates[i][j]['long'])
                    heapq.heappush(open_set, (g_score[x][y], (x,y)))

    return None

def get_path(coordinates, source, destination):
    print(f"rows = {len(coordinates)}")
    for i,l in enumerate(coordinates):
        # print(f"row {i+1} size = {len(l)}")
        print(f"row {i+1}",end=" ")
        for j,ll in enumerate(l):
            print(f"({ll['lat']},{ll['long']})",end=' ')
        print()


    
    total_distance = haversine(source['lat'], source['long'], destination['lat'], destination['long'])
    sourceIndex = get_node_index(coordinates,source)
    destinationIndex = get_node_index(coordinates,destination)

    path = a_star(coordinates,sourceIndex,destinationIndex)
    risk_details = get_risk_details(path_labels)
    return [total_distance, path, risk_details[0], risk_details[1]]