import os
import sys
import xyz_plot

folder = 'RobotArena/' + str(sys.argv[1]) + '/'
files = [folder + f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
save_location =  str(sys.argv[2])

xyz_plot.draw_xyz_plot(files, save=save_location, location_as_label=True)
