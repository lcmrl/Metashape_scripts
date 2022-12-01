import os
import numpy as np
from pathlib import Path
import subprocess

SENSOR_SIZE = 211.9985 #212.005 # [mm]
CC_API_path = Path(r"C:\Users\Luscias\Desktop\3DOM\Github_3DOM\COLMAP_scripts\AlignCC_for_windows")
imgs_dir = Path(r"F:\PhD\bakula\IMGS_REGULAR_SCANNER")
prj_file = Path(r"G:\Shared drives\3DOM Research\PhD Luca\workflow\publications\2022\TIME_Polonia\INPUT_DATA\REGULAR_SCANNER\prj_regular_kopia.prj")

# Creating a database with all prj informations
img_list = os.listdir(imgs_dir)
img_list = ["$PHOTO_NUM : {}".format(elem[:-4]) for elem in img_list]
database = {}
current_image = None
with open(prj_file, 'r') as inpho_prj:
    lines = inpho_prj.readlines()
    for l, line in enumerate(lines):
        line = line.strip()
        
        for photo in img_list:
            if photo in line:
                print(line)
                #print("line: ", l)
                _, _, img_name = photo.split(None, 2)
                current_image = img_name
        
        if "$PIXEL_SIZE" in line and current_image != None:
            _, _, pix_size = line.split()
            print(pix_size)
        
        if "$FIDUCIALS" in line and current_image != None:
            fiducials = []
            for line2 in lines[l+1:]:
                if line2 == "  $END_POINTS\n":
                    break
                line2 = line2.strip()
                fid_id, fid_x, fid_y = line2.split()
                fiducials.append((fid_id, fid_x, fid_y))
                #print(fid_id, fid_x, fid_y)

        if "$PHOTO_POINTS" in line and current_image != None:
            projections = []
            for line2 in lines[l+1:]:
                if line2 == "  $END_POINTS\n":
                    break
                line2 = line2.strip()
                prj_id, prj_x, prj_y, _ = line2.split(None, 3)
                projections.append((prj_id, prj_x, prj_y))
                #print(prj_id, prj_x, prj_y)
                
            database[current_image] = {"pix_size" : pix_size,
                                        "fiducials" : fiducials,
                                        "projections" : projections}
            
        if line.strip() == "$END":
            current_image = None

#print(database)


# 
observation4metashape = open(r"observation4metashape.txt", 'w')
for img_dict in database:
    with open("./temp_inpho.txt", 'w') as inpho, open("./temp_meta.txt", 'w') as meta:
        fid_0 = database[img_dict]['fiducials'][0]
        fid_1 = database[img_dict]['fiducials'][1]
        fid_2 = database[img_dict]['fiducials'][2]
        fid_3 = database[img_dict]['fiducials'][3]

        #dist_pixel1 = np.sqrt((float(fid_1[1])-float(fid_0[1]))**2+(float(fid_1[2])-float(fid_0[2]))**2)
        #dist_pixel2 = np.sqrt((float(fid_2[1])-float(fid_1[1]))**2+(float(fid_2[2])-float(fid_1[2]))**2)
        #dist_pixel3 = np.sqrt((float(fid_3[1])-float(fid_2[1]))**2+(float(fid_3[2])-float(fid_2[2]))**2)
        #dist_pixel4 = np.sqrt((float(fid_0[1])-float(fid_3[1]))**2+(float(fid_0[2])-float(fid_3[2]))**2)
        #dist_pixel = (dist_pixel1+ dist_pixel2 + dist_pixel3 + dist_pixel4) / 4
        #print("dist pixel", dist_pixel1, dist_pixel2, dist_pixel3, dist_pixel4)
        #print(dist_pixel)
        #dist_pixel = SENSOR_SIZE / float(database[img_dict]['pix_size'])
        #print(dist_pixel)

        #inpho.write("{},{},{}\n".format(1, +dist_pixel/2, -dist_pixel/2))
        #inpho.write("{},{},{}\n".format(2, -dist_pixel/2, -dist_pixel/2))
        #inpho.write("{},{},{}\n".format(3, -dist_pixel/2, +dist_pixel/2))
        #inpho.write("{},{},{}".format(4, +dist_pixel/2, +dist_pixel/2))

        PIXEL_SIZE = float(database[img_dict]['pix_size']) #0.014083

        inpho.write("{},{},{}\n".format(1, 106.002 / PIXEL_SIZE, -106.002 / PIXEL_SIZE))
        inpho.write("{},{},{}\n".format(2, -106.003 / PIXEL_SIZE, -106.017 / PIXEL_SIZE))
        inpho.write("{},{},{}\n".format(3, -106.01 / PIXEL_SIZE, 105.985 / PIXEL_SIZE))
        inpho.write("{},{},{}".format(4, 105.982 / PIXEL_SIZE, 105.995 / PIXEL_SIZE))
        
        meta.write("{},{},{}\n".format(fid_0[0], fid_0[1], fid_0[2]))
        meta.write("{},{},{}\n".format(fid_1[0], fid_1[1], fid_1[2]))
        meta.write("{},{},{}\n".format(fid_2[0], fid_2[1], fid_2[2]))
        meta.write("{},{},{}\n".format(fid_3[0], fid_3[1], fid_3[2]))

    # Align the two clouds (cloud from COLMAP to ground_truth)
    output_file = open("outs.txt", "w")
    subprocess.run(["{}/Align.exe".format(CC_API_path), "temp_inpho.txt", "temp_meta.txt", ">", "out.txt"], stdout=output_file)
    output_file.close()
    
    # Upload the just created transformation matrix
    output_file = open("outs.txt", "r")
    lines = output_file.readlines()
    lines = lines[3:]
    output_file.close()
    
    output_file = open("outs.txt", "w")
    for line in lines:
        output_file.write(line)
    output_file.close()
    
    q_matrix = np.loadtxt("outs.txt", dtype='float', delimiter=" ")
    #print(q_matrix)
    
    # Prepare observations
    proj = database[img_dict]['projections']
    p_size = float(database[img_dict]['pix_size'])
    for p in proj:
        prj_id, prj_x, prj_y = p
        #print(prj_id, prj_x, prj_y)
        im_proj = np.array([[float(prj_x)/p_size],
                            [float(prj_y)/p_size],
                            [0],
                            [1]])
        im_proj_roto_tran = q_matrix @ im_proj
        observation4metashape.write("{},{},{},{}\n".format(prj_id, img_dict, im_proj_roto_tran[0,0], im_proj_roto_tran[1,0]))

observation4metashape.close()