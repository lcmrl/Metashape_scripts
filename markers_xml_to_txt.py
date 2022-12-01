# CONVERT METASHAPE MARKERS TO TXT FILE WITH IMAGE COORDINATES
# Choose the correct version between Agisoft and Metashape
# Variables
path = "G:/3DOM/13_Imgs_aeree/dortmund/metashape/markers.txt"

# Script
file = open(path, "wt")
#chunk = PhotoScan.app.document.chunk # for Agisoft PhotoScan Pro v.1.2.0
chunk = Metashape.app.document.chunk # for Metashape
photos_total = len(chunk.cameras) #number of photos in chunk
markers_total = len(chunk.markers) #number of markers in chunk

if (markers_total):
	file.write(chunk.label + "\n")

for i in range (0, markers_total):    #processing every marker in chunk
	cur_marker = chunk.markers[i]
	cur_projections = cur_marker.projections   #list of marker projections
	marker_name = cur_marker.label
		
	for camera in cur_marker.projections.keys(): #
	#for j in range (0, len(photos_list)): 		#processing every projection of the current marker
		x, y = cur_projections[camera].coord			#x and y coordinates of the current projection in pixels
		label = camera.label
	
		file.write(marker_name + "," + label + "," + "{:.4f}".format(x) + "," + "{:.4f}".format(y) + "\n")  #writing output

file.write("#\n")
file.close()	