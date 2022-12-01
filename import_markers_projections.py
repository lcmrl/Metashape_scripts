import PhotoScan
#import Metashape

print("Importing image projections ...")

chunk = PhotoScan.app.document.chunk
path = r"G:\Shared drives\3DOM Research\PhD Luca\workflow\publications\2022\TIME_Polonia\INPUT_DATA\REGULAR_SCANNER\inpho2metashape\REGULARobservation4metashape.txt"
file = open(path, "rt")  # input file

eof = False
line = file.readline()
if not len(line):
    eof = True

while not eof:

    sp_line = line.rsplit(",", 3)  # splitting read line by four parts
    print(sp_line)
    y = float(sp_line[3])  # y- coordinate of the current projection in pixels
    x = float(sp_line[2])  # x- coordinate of the current projection in pixels
    path = sp_line[1] + ".tif"  # camera label # sp_line[1][:-4]
    marker_name = sp_line[0]  # marker label
    print(marker_name, path, x, y)

    flag = 0
    for i in range(len(chunk.cameras)):

        if chunk.cameras[i].label == path:  # searching for the camera

            for j in range(
                    len(chunk.markers)):  # searching for the marker (comparing with all the marker labels in chunk)
                if chunk.markers[j].label == marker_name:
                    chunk.markers[j].projections[chunk.cameras[i]] = PhotoScan.Marker.Projection(
                        PhotoScan.Vector([x, y]), True)  # setting up marker projection of the correct photo)
                    flag = 1
                    break

            if not flag:
                marker = chunk.addMarker()
                marker.label = marker_name
                marker.projections[chunk.cameras[i]] = PhotoScan.Marker.Projection(PhotoScan.Vector([x, y]), True)
            break

    line = file.readline()  # reading the line from input file
    if not len(line):
        eof = True
        break  # EOF

file.close()
print("Markers import finished.\n")