
buffer = 5
def getBounds(sourceLat, sourceLong, destinationLat, destinationLong):
    minLat = min(sourceLat,destinationLat) - buffer
    maxLat = max(sourceLat,destinationLat) + buffer
    minLong = min(sourceLong,destinationLong) - buffer
    maxLong = max(sourceLong,destinationLong) + buffer

    return {
        "leftUpper" : [minLat,minLong],
        "leftLower" : [maxLat,minLong],
        "rightUpper" : [minLat,maxLong],
        "rightLower" : [maxLat,maxLong]
    }

def generateMatrix(source,destination) :
    boundaryDetails = getBounds(source[0],source[1],destination[0],destination[1])
    sourceLat, sourceLong = source
    destinationLat, destinationLong = destination
    print(boundaryDetails)
    
    minLat = min(sourceLat,destinationLat) - buffer
    maxLat = max(sourceLat,destinationLat) + buffer
    minLong = min(sourceLong,destinationLong) - buffer
    maxLong = max(sourceLong,destinationLong) + buffer

    matrix = []

    for i in range(minLat,maxLat+1,buffer):
        row = []
        for j in range(minLong,maxLong+1,buffer):
            row.append({'lat' : i, 'long' : j})
            # row.append((i,j))
        matrix.append(row)

    return matrix