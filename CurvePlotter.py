import os
import pandas
import matplotlib, matplotlib.pyplot as pyplot
matplotlib.use('qt5agg')
import psutil
from datetime import datetime
import numpy
import sys


#USE THE BOLLOW PROMPT IN CMD TO RUN FROM TERMINAL (windows + R, type "cmd", copy prompt below, right click cmd prompt)
r'''


for /f "delims=" %a in ('powershell -Command "(Get-ChildItem -Path . -Recurse -Filter CurveFinder.py).DirectoryName"')^
  do (cd %a & if exist %a\CurveFinder.py^
              (echo Running Python script: %a\CurveFinder.py^
              & python CurveFinder.py \^
              & if errorlevel 1 (echo Error Occurred while running CurveFinder.py))
              
              
'''

#code is used to copy data from log drive, seperate outliers, and plot outliers

#date range we are interested in diverging data from using colormap (keep in format month-day-year or MM-DD-YYY)
divergence_date_of_interest_range = ['09-01-2021','12-23-2021']

#start folder of local drive
home_dir = "C:\\"
#name of folder with log data
folder_to_find = "DailyLogs"

#function to locate directory with logs
def finding_logs(home_dir, folder_to_find):
    for rootdir, subdirs, files in os.walk(home_dir):
        if (folder_to_find in subdirs):
            path_to_logs = os.path.join(rootdir, folder_to_find)
            return path_to_logs
    return 0

#function to detect removable drives if logs cannot be found on C: drive
def get_removable_drives():
    drives = []
    partitions = psutil.disk_partitions(all=True)
    for partition in partitions:
        if 'removable' in partition.opts:
            drives.append(partition.mountpoint)
    return drives

#trying to find log path
log_dir = finding_logs(home_dir, folder_to_find)

#checks for removable drives if no log folder is found, then scans each to find logs
if not log_dir:
    removable_drives = get_removable_drives()
    if removable_drives:
        for drives in range(len(removable_drives)):
            log_dir = finding_logs(removable_drives[drives], folder_to_find)
            if log_dir:
                break
    else:
        print(f"No log folder named {folder_to_find} found")

#set log file directory as working directory for file access
os.chdir(log_dir)

#log_files is  alist containing names of each log file
log_files = os.listdir()

#counter for ...
dotdotdot_counter = 0

#colormap for graph
divergence_cmap = pyplot.get_cmap('seismic')

#setting background color for plot
#
matplotlib.style.use('ggplot')

def graph_setup(log_data, filename, column_names, dotdotdot_counter, final_sorted_logs_dict_6, norm, mode):
    #if (int(filename[10:14]) < 2022):
    #print(filename)
    for key in final_sorted_logs_dict_6:
        for file, index in key:
            if filename == file:
                color_num = final_sorted_logs_dict_6[key]
    x_val = column_names[0]
    y_val = column_names[1]
    pyplot.rcParams["figure.figsize"] = [10, 10]
    pyplot.rcParams["figure.autolayout"] = True
    pyplot.title(f"Plot of: {filename}")
    #fig.colorbar(matplotlib.cm.ScalarMappable(cmap = divergence_cmap), ax=ax, orientation = 'vertical', label = 'time from battery repair')
    # pyplot.set_cmap(divergence_cmap)
    # pyplot.colorbar(label="color intensity")
    #pyplot.figure()

    #plot_divergence_cmap = divergence_cmap(numpy.linspace(1, 0, 256))a

    pyplot.plot(log_data[x_val], log_data[y_val], c = divergence_cmap(norm(1/color_num)), marker="o", markersize = 0.5)

    if len(column_names) == 3:
        if column_names.index("BMS - System Current") == 2:
            pyplot.ylabel("Power")
            pyplot.xlabel(column_names[0])
        elif column_names.index("BMS - System Current") == 1:
            pyplot.xlabel("Power")
            pyplot.ylabel(column_names[2])
    else:
        pyplot.xlabel(column_names[0])  # Label for x-axis
        pyplot.ylabel(column_names[1])  # Label for y-axis

    pyplot.gca().invert_xaxis()  # showing x = 0 as being highest SOC
    pyplot.xticks(fontsize = 12)
    #pyplot.xlim(0,100)
    pyplot.yticks(fontsize = 12)
    #pyplot.ylim(0,300)
    #pyplot.show()

    dotdotdot_counter += 1

    if (mode == "in"):
        pyplot.show()

    return dotdotdot_counter


# def graph_setup(log_data, filename):
#     pyplot.rcParams["figure.figsize"] = [10, 10]
#     pyplot.rcParams["figure.autolayout"] = True
#     pyplot.title(f"Plot of: {filename}")
#     pyplot.plot(log_data["BMS - System SOC"], log_data["BMS - System Current"], marker="o")
#     pyplot.xlabel("BMS - System SOC")  # Label for x-axis
#     pyplot.gca().invert_xaxis()  # showing x = 0 as being highest SOC
#     pyplot.ylabel("BMS - System Current")  # Label for y-axis
#     pyplot.xticks(fontsize = 12)
#     #pyplot.xlim(0,100)
#     pyplot.yticks(fontsize = 12)
#     #pyplot.ylim(0,300)
#     #pyplot.show()


#sorts file list by correct order and stores sorted file names in list: sorted_log_files
def extract_date(log_files):
    return datetime.strptime(log_files.split('_')[1].split('.')[0], "%m-%d-%Y")
sorted_log_files = sorted(log_files, key=extract_date)


#dictionary of row values for different parameters on log .csv
data_labels = {
    "power": ["BMS - System Voltage", "BMS - System Current"],
    "time": "Time (24Hr)",
    "soc": "BMS - System SOC",
    "soh": "BMS - System SOH",
    "voltage": "BMS - System Voltage",
    "current": "BMS - System Current",
    "system mode": "BMS - System Mode",
    "watchdogHB": "BMS - Watchdog HB",
    "alarm status": "BMS - Alarm Status",
    "connecting status": "BMS - Connecting Status",
    "discharge current limit": "BMS - Discharge I Limit",
    "charge current limit": "BMS - Charge I Limit",
    "racks in service": "BMS - Racks In Service",
    "protection1": "BMS - Protection 1",
    "protection2": "BMS - Protection 2",
    "protection3": "BMS - Protection 3",
    "protection4": "BMS - Protection 4",
    "alarm1": "BMS - Alarm 1",
    "alarm2": "BMS - Alarm 2",
    "alarm3": "BMS - Alarm 3",
    "alarm4": "BMS - Alarm 4",
    "di status": "BMS - DI Status",
    "max cv": "BMS - Max CV",
    "min cv": "BMS - Min CV",
    "max ct": "BMS - Max CT",
    "min ct": "BMS - Min CT",
    "dc voltage": "PCS - DC Voltage",
    "dc current": "PCS - DC Current",
    "dc power": "PCS - DC Power",
    "grid i avg": "PCS - Grid I Avg",
    "grid ia": "PCS - Grid Ia",
    "grid ib": "PCS - Grid Ib",
    "pcs - grid ic": "PCS - Grid Ic",
    "pcs - inv hs temp": "PCS - Inv HS Temp",
    "pcs - inv i avg": "PCS - Inv I Avg",
    "pcs - inv ia": "PCS - Inv Ia",
    "pcs - inv ib": "PCS - Inv Ib",
    "pcs - inv ic": "PCS - Inv Ic",
    "pcs - out v avg": "PCS - Out V Avg",
    "pcs - out vab": "PCS - Out Vab",
    "pcs - out vbc": "PCS - Out Vbc",
    "pcs - out vca": "PCS - Out Vca",
    "pcs - out frequency": "PCS - Out Frequency",
    "cs - out kva": "PCS - Out kVA",
    "pcs - out kw": "PCS - Out kW",
    "pcs - out kvar": "PCS - Out kVAR",
    "pcs - applied idcmax": "PCS - Applied IdcMax",
    "pcs - applied idcmin": "PCS - Applied IdcMin",
    "pcs - status1": "PCS - Status 1",
    "pcs - status2": "PCS - Status 2",
    "pcs - status3": "PCS - Status 3",
    "pcs - status4": "PCS - Status 4",
    "pcs - status5": "PCS - Status 5",
    "pcs - status6": "PCS - Status 6",
    "pcs - status7": "PCS - Status 9",
    "pcs - status8": "PCS - Status 10",
    "pcs - wd out": "PCS - WD Out",
    "mlc state": "MLC State",
    "mlc status1": "MLC Status1",
    "mlc status2": "MLC Status2",
    "mlc faults1": "MLC Faults1",
    "mlc faults2": "MLC Faults2",
    "mlc alarms1": "MLC Alarms1",
    "mlc alarms2": "MLC Alarms2",
    "hvac alarms1": "HVAC Alarms1",
    "hvac alarms2": "HVAC Alarms2",
    "external ambient (°c)": "External Ambient (°C)",
    "hvac a probe1(°c)": "HVAC A Probe1(°C)",
    "hvac a probe2(°c)": "HVAC A Probe2(°C)",
    "hvac b probe1(°c)": "HVAC B Probe1(°C)",
    "hvac b probe2(°c)": "HVAC B Probe2(°C)"
}

# pyplot.clf()
# close_choice = "none"
# close_choice = input("\n\t\tdo you want to close previous plots? (y/n): ").lower().strip()
# if close_choice in ["yes", "y", "ye"]:
#     pyplot.close('all')

#aggregate time list for continuous time axis
time = []

#enter the values that you want graphed in this list, use the key above and type exactly (case-sensitive)
formatted_labels = []
labels_per_line = 10

mode = input("\n\tAGGREGATE OR INDIVIDUAL?\n\tEnter Aggregate or Individual: ").lower().strip()
while mode not in ["aggregate", "ag", "agg", "a", "individual", "ind", "in", "i"]:
    mode = input("\n\tERROR ERROR ERROR PICK 1 OF 2: AGGREGATE OR INDIVIDUAL?\n\tEnter Aggregate or Individual: ").lower().strip()
if mode in ["aggregate", "ag", "agg", "a"]:
    mode = "ag"
elif mode in ["individual", "ind", "in", "i"]:
    mode = "in"

print("\n\tREFERENCE NAMES OF VALUES (MUST TYPE EXACTLY):\n")
for chunk in range(0, len(data_labels.keys()), labels_per_line):
    print("\n\t" + "  ||  ".join(map(str, list(data_labels.keys())[chunk : chunk + labels_per_line])) + "\n")
y_val = input(f"\n\n\t\tEnter Desired Values to Plot Graph:\n\t\t(y vs. x)\n\n\t\t\ty = ").lower().strip()
while y_val not in data_labels:
        y_val = input(f"\n\n\t\tERROR ERROR ERROR UKNOWN VALUE\n\tPlease Re-enter Value From Table:\n\t\t(y vs. x)\n\n\t\t\ty = ").lower().strip()
x_val = input(f"\n\n\t\t(y = {y_val}) vs. (x = ").lower().strip()
while x_val not in data_labels:
    x_val = input(f"\n\n\t\tERROR ERROR ERROR UKNOWN VALUE\n\tPlease Re-enter Value From Table:\n\t\t(y = {y_val}) vs. (x = ").lower().strip()
print("\n\n\t")
desired_values = [x_val, y_val]
#gets the column names corresponding to desired_values
if "power" in desired_values:
    pre_column_names  = [ data_labels[key] for key in desired_values if key != "power"]
    column_names = pre_column_names + data_labels["power"]

else:
    column_names = [data_labels[key] for key in desired_values]

#sorted_log_files6 = sorted_log_files[::-1]
#organizing logs by date starting from oldest and ascending
sorted_logs_dict = {value: index for index, value in enumerate(sorted_log_files)}
list_dict = list(sorted_logs_dict.items())
sorted_logs_dict_6 = {}
for flag in range(int(len(list_dict)/6)):
    sorted_logs_dict_6[flag+1] = list_dict[(6 * flag) : (6 * (flag + 1))]
#flipping dict to be able to index number by file name
final_sorted_logs_dict_6 = {tuple(value): key for key, value in sorted_logs_dict_6.items()}


#adding further identifiers to file name in list
for val in divergence_date_of_interest_range:
    divergence_date_of_interest_range[divergence_date_of_interest_range.index(val)] = "UTC_" + val + "_.csv"
#finding index of beginning and ending val in list to shorten range and find median value
beginning_val  = sorted_log_files.index(divergence_date_of_interest_range[0])
ending_val = sorted_log_files.index(divergence_date_of_interest_range[1])
median_list = sorted_log_files[beginning_val:ending_val+1]
#finding median in range
center_of_divergence_index = numpy.median(range(len(median_list)+1))
closest_center = numpy.floor(center_of_divergence_index)
#middle log file in divergence range
center_of_divergence = median_list[int(center_of_divergence_index)]
for key in final_sorted_logs_dict_6:
    for file, index in key:
        if center_of_divergence == file:
            center_num = final_sorted_logs_dict_6[key]

if (mode == "ag"):
    fig = pyplot.figure()
    norm = matplotlib.colors.TwoSlopeNorm(vmin = 0, vcenter = 1/center_num, vmax = 1.1 )
    pyplot.colorbar(matplotlib.cm.ScalarMappable(cmap=divergence_cmap, norm = norm), ax=pyplot.gca(), orientation='vertical', label='time from battery repair')
else:
    norm = matplotlib.colors.NoNorm()

#main exectuion loop
for filename in sorted_log_files:

    if (int(dotdotdot_counter) % 10 == 0) and (int(dotdotdot_counter) != 0):
        print(".", end='')
        if int(dotdotdot_counter) % 30 == 0:
            print(" ", end = '')
            if int(dotdotdot_counter) % 600 == 0:
                print("\n\t")
    elif (int(dotdotdot_counter) == 0):
        print("\t")

    error_occurred = False  # error flag

    try:
        graph_data_points = [data_labels[key] for key in desired_values]
        pandas.set_option('display.max_rows', None)

        if "power" in desired_values:
            log_data = pandas.read_csv(filename, usecols = column_names,skiprows = 0, encoding = "ISO-8859-1")
            log_data['BMS - System Voltage'] = (log_data['BMS - System Voltage']) * (log_data['BMS - System Current'])
        else:
            log_data = pandas.read_csv(filename, usecols = column_names,skiprows = 0, encoding = "ISO-8859-1")#, names = desired_values)#.to_string()

        #print(log_data
        #if (log_data["BMS - System Current"]):
        if ("time" in desired_values) and (mode == "ag"):
            new_val = log_data['Time (24Hr)'] = pandas.to_datetime(log_data['Time (24Hr)'], format='%H:%M')  # Adjust format if needed
            log_data['Time (24Hr)'] = log_data['Time (24Hr)'].apply(lambda x: x.replace(year=int(filename[10:14]), month=int(filename[4:6]), day=int(filename[7:9])))
            #log_data.extend(log_data['Time'].dt.time.tolist())
        dotdotdot_counter = graph_setup(log_data, filename, column_names, dotdotdot_counter, final_sorted_logs_dict_6, norm, mode)

    except Exception as e:
        if not error_occurred:  # prints error only once for each file
            # prints the name of the file that caused an error
            print(f"Error occurred while processing file: {filename} in directory: {os.path.abspath(filename)}")
            error_occurred = True  # sets flag to True to avoid repeated printing
        print(f"Error details: {e}")

#colors = numpy.linspace(0, 1, len(log_data["BMS - System SOC"]))
#pyplot.scatter(log_data["BMS - System SOC"], log_data["BMS - System Current"], c=colors, cmap='viridis')
print("..done")
if "soc" in desired_values:
    if "soc" == desired_values[0]:  # If "soc" is the x-axis value
        pyplot.gca().invert_xaxis()  # Invert the x-axis
    elif "soc" == desired_values[1]:  # If "soc" is the y-axis value
        pyplot.gca().invert_yaxis()  # Invert the y-axis


current_figure = pyplot.gcf()


# maybe add this as first argument in function above matplotlib.cm.ScalarMappable(cmap=divergence_cmap)
current_figure = pyplot.gcf()
pyplot.get_current_fig_manager().window.showMaximized()



if mode == "ag":
    pyplot.title("Aggregate Plot")


    #pyplot.colorbar(matplotlib.cm.ScalarMappable(cmap=divergence_cmap, norm=norm), ax=pyplot.gca(), orientation='vertical', label='time from battery repair')

    pyplot.show()

    def annot_max(log_data, ax=None):
        xmax = log_data[x_val][numpy.argmax(log_data[y_val])]
        ymax = log_data[y_val].max()
        text = "x={:.3f}, y={:.3f}".format(xmax, ymax)
        if not ax:
            ax = pyplot.gca()
        bbox_props = dict(boxstyle="square,pad=0.3", fc="w", ec="k", lw=0.72)
        arrowprops = dict(arrowstyle="->", connectionstyle = "angle,angleA=0,angleB=60")
        kw = dict(xycoords='data',textcoords="axes fraction", arrowprops=arrowprops, bbox=bbox_props, ha = "right", va = "top")
        ax.annotate(text, xy=(xmax, ymax), xytext=(0.94,0.96), **kw)

    annot_max(log_data)

    save_decision = input()

# estimate for when battery lost it's power
