import os

REDUCTION_FACTOR = 1500/6048
REF_SYSTEM_TRANSLATION = 0.5

folder_path = r'C:\Users\Luscias\Desktop\Dottorato\PhotogrammetryCrashCourse\Materiale\Ventimiglia_1500x1000\ventimiglia_target_projections_all'

file =os.listdir(folder_path)
#print(file)

with open('rearranged.txt', 'w') as new_file:
    for item in file:
        with open('{}/{}'.format(folder_path, item),'r') as targets:
            for line in targets:
                line = line.strip()
                id, x, y, bin = line.split(" ", 3)      #id, x, y, bin = line.split(" ", 3)
                x = float(x) * REDUCTION_FACTOR + REF_SYSTEM_TRANSLATION
                y = float(y) * REDUCTION_FACTOR + REF_SYSTEM_TRANSLATION
                new_file.write("{},{},{},{}\n".format(id[0:],item[:-8],str(x),str(y)))