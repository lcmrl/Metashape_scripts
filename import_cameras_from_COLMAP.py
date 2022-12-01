'''
Input:
camera_poses.txt:   file prepared rearranging the images.txt file of COLMAP
                    format: camera_label x y z qx qy qz qw
'''
import Metashape
import os
import sys
import numpy as np

print("Importing camera poses...")

chunk = Metashape.app.document.chunk



with open(r"C:\Users\Luscias\Desktop\buttare\PlasticBottle\sparse3\images.txt", "r") as lines:
    lines = lines.readlines()[4:]
    shape=(int((len(lines)-4)/2),10)
    print("shape", shape)
    EO = np.array(["IMAGE_ID", "QW", "QX", "QY", "QZ", "TX", "TY", "TZ", "CAMERA_ID", "NAME"])
    for c,line in enumerate(lines):
        if c%2 == 0:
            row = int(c/2)
            print(line)
            line = line.strip()
            IMAGE_ID, QW, QX, QY, QZ, TX, TY, TZ, CAMERA_ID, NAME = line.split(" ", 9)
            #Eplus = np.array([IMAGE_ID, QW, QX, QY, QZ, TX, TY, TZ, CAMERA_ID, NAME])
            Eplus = np.array([IMAGE_ID, QW, QX, QY, QZ, TX, TY, TZ, CAMERA_ID, NAME[:-4]])
            EO = np.vstack((EO, Eplus))
            


#camera_poses = Metashape.app.getOpenFileName("camera_poses.txt","*.txt")
#open(camera_poses, 'r')
#camera_poses = open(r"E:\3DOM\13_Imgs_aeree\dortmund\RootSIFT_jpg_imgs\BA4pix\dense_metashape\camera_poses.txt", "r")
#EO = np.loadtxt(camera_poses, skiprows=1, dtype={'names': ['timestamp','X0', 'Y0', 'Z0', 'qx', 'qy', 'qz', 'qw'],
#                                                  'formats': ['<f8', '<f8',  '<f8',  '<f8',  '<f8',  '<f8',  '<f8',  '<f8']})
#camera_poses = r"E:\3DOM\13_Imgs_aeree\dortmund\RootSIFT_jpg_imgs\BA4pix\dense_metashape\camera_poses.txt"
#EO = np.loadtxt(camera_poses, delimiter=' ', dtype="str")



# Camera center scale factor
sf = 1.0

i=0
for j, camera in enumerate(chunk.cameras):
    for n,item in enumerate(EO[:,9]):
        #print(camera.label, item)
        if item==camera.label and j<100000:
            i=n
            print("i=n")
            #try:        
            qvec = np.array([float(EO[i][1]), float(EO[i][2]), float(EO[i][3]), float(EO[i][4])])
            #T = np.array([[float(EO[i][5]) * sf, float(EO[i][6]) * sf, float(EO[i][7]) * sf, 1]])
            T = np.array([[float(EO[i][5]) * sf, float(EO[i][6]) * sf, float(EO[i][7]) * sf]])
            print("j,q,T")
            print(j)
            #print(q)
            print(T)
                       

            M = np.array([[1 - 2 * qvec[2]**2 - 2 * qvec[3]**2, 
                    2 * qvec[1] * qvec[2] - 2 * qvec[0] * qvec[3], 
                    2 * qvec[3] * qvec[1] + 2 * qvec[0] * qvec[2]],
            
                    [2 * qvec[1] * qvec[2] + 2 * qvec[0] * qvec[3],
                    1 - 2 * qvec[1]**2 - 2 * qvec[3]**2,
                    2 * qvec[2] * qvec[3] - 2 * qvec[0] * qvec[1]],
            
                    [2 * qvec[3] * qvec[1] - 2 * qvec[0] * qvec[2],
                    2 * qvec[2] * qvec[3] + 2 * qvec[0] * qvec[1],
                    1 - 2 * qvec[1]**2 - 2 * qvec[2]**2]])

            #M = np.array([[ q[0]**2+q[1]**2-q[2]**2-q[3]**2,        2*(q[1]*q[2]+q[3]*q[0]),                2*(q[1]*q[3]-q[2]*q[0])],
            #            [   2*(q[1]*q[2]-q[3]*q[0]),                q[0]**2-q[1]**2+q[2]**2-q[3]**2,        2*(q[2]*q[3]+q[1]*q[0])],
            #            [   2*(q[1]*q[3]+q[2]*q[0]),                2*(q[2]*q[3]-q[1]*q[0]),                q[0]**2-q[1]**2-q[2]**2+q[3]**2]])

            M = M.transpose()
            T = T.transpose()
            T = np.dot(-M,T)
            T = np.array([[T[0], T[1], T[2], 1]])
            #M = M.transpose()
            
            #M4x4_left = np.concatenate((M.T.dot(R1),np.zeros([1,3])),0)
            M4x4_left = np.concatenate((M,np.zeros([1,3])),0)
            M4x4_left = np.concatenate((M4x4_left,T.T),1)
            LEFT_CAM_MATRIX = Metashape.Matrix ([[M4x4_left[0][0], M4x4_left[0][1], M4x4_left[0][2], M4x4_left[0][3]],
                                                [M4x4_left[1][0], M4x4_left[1][1], M4x4_left[1][2], M4x4_left[1][3]],
                                                [M4x4_left[2][0], M4x4_left[2][1], M4x4_left[2][2], M4x4_left[2][3]], 
                                                [M4x4_left[3][0], M4x4_left[3][1], M4x4_left[3][2], M4x4_left[3][3]]])



            chunk.cameras[j].transform = LEFT_CAM_MATRIX
            chunk.cameras[j].reference.location=(chunk.cameras[j].transform.translation())
            #chunk.cameras[j].reference.location_accuracy = Metashape.Vector((2, 2, 2))
            #chunk.cameras[j+1].reference.location=(chunk.cameras[j+1].transform.translation())
            #chunk.cameras[j+1].reference.location_accuracy = Metashape.Vector((2, 2, 2))            
            #chunk.cameras[j].reference.rotation = Metashape.Utils.mat2ypr(chunk.cameras[j].transform.rotation())            
            #chunk.cameras[j].reference.rotation_accuracy = Metashape.Vector((5, 5, 5))
            #chunk.cameras[j+1].reference.rotation = Metashape.Utils.mat2ypr(chunk.cameras[j+1].transform.rotation())            
            #chunk.cameras[j+1].reference.rotation_accuracy = Metashape.Vector((5, 5, 5))           
            #scalebar = chunk.addScalebar(chunk.cameras[j],chunk.cameras[j+1])
            #scalebar.label = chunk.cameras[j].label + '_' + chunk.cameras[j+1].label
            #scalebar.reference.distance = baseline
            #print(i)
            #except:
            #    print("Error for:"+camera.label)
            

#print(EO)