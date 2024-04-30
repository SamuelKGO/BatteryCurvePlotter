

#USE THE BELLOW PROMPT IN CMD TO RUN FROM TERMINAL (windows + R, type "cmd", copy prompt below, right click cmd prompt)
r'''




for /f "delims=" %a in (
    'powershell -Command "(Get-ChildItem -Path . -Recurse -Filter CurveFinder.py).DirectoryName"'
) do (
    cd %a
    if exist %a\CurveFinder.py (
        echo Running Python script: %a\CurveFinder.py
        if errorlevel 1 (
            echo Error Occurred while running CurveFinder.py
        )
    )
)




'''


#dictionary of row values for different parameters on log .csv
data_labels = {
    "real power": ["BMS - System Voltage", "BMS - System Current"],
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
    "device power": "PCS - Out kW",
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

data_units = {
    "real power": "kW",  # Voltage, Amperage
    "time": "Military",
    "soc": "%",  # Percentage
    "soh": "%",  # Percentage
    "voltage": "V",
    "current": "A",
    "system mode": "",  # No unit
    "watchdogHB": "",  # No unit
    "alarm status": "",  # No unit
    "connecting status": "",  # No unit
    "discharge current limit": "A",
    "charge current limit": "A",
    "racks in service": "",  # No unit
    "protection1": "",  # No unit
    "protection2": "",  # No unit
    "protection3": "",  # No unit
    "protection4": "",  # No unit
    "alarm1": "",  # No unit
    "alarm2": "",  # No unit
    "alarm3": "",  # No unit
    "alarm4": "",  # No unit
    "di status": "",  # No unit
    "max cv": "",  # No unit
    "min cv": "",  # No unit
    "max ct": "",  # No unit
    "min ct": "",  # No unit
    "dc voltage": "V",
    "dc current": "A",
    "dc power": "W",  # Wattage
    "grid i avg": "A",
    "grid ia": "A",
    "grid ib": "A",
    "pcs - grid ic": "A",
    "pcs - inv hs temp": "°C",  # Celsius
    "pcs - inv i avg": "A",
    "pcs - inv ia": "A",
    "pcs - inv ib": "A",
    "pcs - inv ic": "A",
    "pcs - out v avg": "V",
    "pcs - out vab": "V",
    "pcs - out vbc": "V",
    "pcs - out vca": "V",
    "pcs - out frequency": "Hz",  # Hertz
    "cs - out kva": "kVA",  # Kilovolt-ampere
    "device power": "kW",  # Kilowatt
    "pcs - out kvar": "kVAR",  # Kilovolt-ampere reactive
    "pcs - applied idcmax": "A",
    "pcs - applied idcmin": "A",
    "pcs - status1": "",  # No unit
    "pcs - status2": "",  # No unit
    "pcs - status3": "",  # No unit
    "pcs - status4": "",  # No unit
    "pcs - status5": "",  # No unit
    "pcs - status6": "",  # No unit
    "pcs - status7": "",  # No unit
    "pcs - status8": "",  # No unit
    "pcs - wd out": "",  # No unit
    "mlc state": "",  # No unit
    "mlc status1": "",  # No unit
    "mlc status2": "",  # No unit
    "mlc faults1": "",  # No unit
    "mlc faults2": "",  # No unit
    "mlc alarms1": "",  # No unit
    "mlc alarms2": "",  # No unit
    "hvac alarms1": "",  # No unit
    "hvac alarms2": "",  # No unit
    "external ambient (°c)": "°C",  # Celsius
    "hvac a probe1(°c)": "°C",  # Celsius
    "hvac a probe2(°c)": "°C",  # Celsius
    "hvac b probe1(°c)": "°C",  # Celsius
    "hvac b probe2(°c)": "°C"  # Celsius
}

import sys
import subprocess
import os
from datetime import datetime, timedelta

unix_epoch = datetime(1970, 1, 1)

packages_used = ['pandas', 'PyQt5', 'matplotlib', 'psutil', 'numpy']

retry_flag = 0

def pip_install_packages(packages_used, retry_flag):
    for package in packages_used:
        split_import_string = package.split(".")
        import_string = split_import_string[0]
        try:
            # Attempt to import the package
            __import__(package)
        except Exception as e:
            try:
                # If the package is not found, install it
                # try:
                subprocess.check_call(['pip', 'install', '--trusted-host', 'pypi.org', '--trusted-host', 'files.pythonhosted.org', import_string])

                __import__(package)
            except Exception as i:
                subprocess.check_call(['python','-m', 'pip', 'install', '--trusted-host', 'pypi.org', '--trusted-host', 'files.pythonhosted.org','--upgrade','pip'])
                retry_flag += 1
                if retry_flag == 1:
                    pip_install_packages(packages_used, retry_flag)
                else:
                    print(f"\n\tPACKAGE {package} DOES NOT EXIST, FIX NAME IN CODE\n\tPACKAGE {package} DOES NOT EXIST, FIX NAME IN CODE\n\tPACKAGE {package} DOES NOT EXIST, FIX NAME IN CODE")
                    packages_used.remove(package)
                    pip_install_packages(packages_used, retry_flag)



# Install required packages
pip_install_packages(packages_used, retry_flag)
try:
    import pandas
    import matplotlib
    import matplotlib.pyplot as pyplot
    import psutil
    import numpy
except ImportError:
    print("\n\n\t\tDOWNLOADING NECESSARY PACKAGES....\n\n")
    # Install required packages
    pip_install_packages(packages_used, retry_flag)

matplotlib.use('qt5agg')

#code is used to copy data from log drive, seperate outliers, and plot outliers

#date range we are interested in diverging data from using colormap (keep in format month-day-year or MM-DD-YYY)
divergence_date_of_interest_range = ['09-01-2021','12-23-2021']
agregation_date_range = ['01-01-2022', 'Present']

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

def run_program():
    #counter for ...
    dotdotdot_counter = 1

    #colormap for graph
    divergence_cmap = pyplot.get_cmap('seismic')

    #setting background color for plot

    matplotlib.style.use('ggplot')

    def graph_setup(log_data, filename, column_names, dotdotdot_counter, norm, mode, sorted_logs_dict):

        for file in sorted_logs_dict:
            if filename == file:
                color_num = sorted_logs_dict[file]

        x_val = column_names[0]
        y_val = column_names[1]
        pyplot.rcParams["figure.figsize"] = [10, 10]
        pyplot.rcParams["figure.autolayout"] = True
        pyplot.title(f"Plot of: {filename}")

        #plot_divergence_cmap = divergence_cmap(numpy.linspace(1, 0, 256))a
        pyplot.plot(log_data[x_val], log_data[y_val], c = divergence_cmap(norm(color_num/len(sorted_logs_dict))), marker="o", markersize = 0.5)
        #
        # time_colorbar = pyplot.colorbar(matplotlib.cm.ScalarMappable(cmap=divergence_cmap, norm=norm), ax=pyplot.gca(), orientation='vertical', label='time from battery repair')
        # time_colorbar.set_ticks([color_line_min_days_float, color_line_max_days_float])
        dotdotdot_counter += 1

        if (mode == "in"):
            current_figure = pyplot.gcf()
            pyplot.xlabel(column_names[0] + " [" + data_units[desired_values[0]] + "] ")  # Label for x-axis
            pyplot.ylabel(column_names[1] + " [" + data_units[desired_values[1]] + "] ")  # Label for y-axis
            pyplot.get_current_fig_manager().window.showMaximized()
            pyplot.show()

        return dotdotdot_counter


    #sorts file list by correct order and stores sorted file names in list: sorted_log_files
    def extract_date(log_files):
        return datetime.strptime(log_files.split('_')[1].split('.')[0], "%m-%d-%Y")
    sorted_log_files = sorted(log_files, key=extract_date)

    #aggregate time list for continuous time axis
    time = []

    #enter the values that you want graphed in this list, use the key above and type exactly (case-sensitive)
    labels_per_line = 10

    mode = input("\n\tAGGREGATE OR INDIVIDUAL?\n\tEnter Aggregate or Individual: ").lower().strip()
    while mode not in ["aggregate", "ag", "agg", "a", "individual", "ind", "in", "i"]:
        mode = input("\n\tERROR ERROR ERROR PICK 1 OF 2: AGGREGATE OR INDIVIDUAL?\n\tEnter Aggregate or Individual: ").lower().strip()
    if mode in ["aggregate", "ag", "agg", "a"]:
        mode = "ag"
        date_range = input(f"\n\tCustom Date Range? (y/n): ")
        if date_range.lower().strip() in ["no", "n", "all"]:
            date_range = "all"
        else:
            first_date = input()
            end_date = input()
    elif mode in ["individual", "ind", "in", "i"]:
        mode = "in"
        specific_day = input("\n\tEnter Date of Interest (mm-dd-yyyy): ").strip()

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
    if "real power" in desired_values:
        if x_val == "real power":
            pre1_column_names  = data_labels["real power"]
            pre2_column_names = [data_labels[key] for key in desired_values if key != "real power"]
            column_names = pre1_column_names + pre2_column_names
        if y_val == "real power":
            pre_column_names = [data_labels[key] for key in desired_values if key != "real power"]
            column_names = pre_column_names + data_labels["real power"]

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


    for file in sorted_logs_dict:
        if center_of_divergence == file:
            center_num = sorted_logs_dict[file]

    norm = matplotlib.colors.TwoSlopeNorm(vmin = 0, vcenter = center_num / len(sorted_logs_dict), vmax = 1)

    if (mode == "ag"):
        fig = pyplot.figure()
        time_colorbar = pyplot.colorbar(matplotlib.cm.ScalarMappable(cmap=divergence_cmap, norm = norm), ax=pyplot.gca(), orientation='vertical')
        time_colorbar.set_label('Time From Battery Repair',fontsize = 20)
        time_colorbar.set_ticks([])
    else:
        divergence_cmap = pyplot.get_cmap('viridis')

    print(f"plotting {y_val} vs. {x_val}...\n")

    #main exectuion loop
    for filename in sorted_log_files:

        if mode == "in":
            filename = f"UTC_{specific_day}_.csv"
            datetimeobj = datetime.strptime(specific_day, '%m-%d-%Y')
            mindayobj = datetime.strptime(sorted_log_files[0][4:14], '%m-%d-%Y')
            while filename not in sorted_log_files:
                if (datetimeobj - mindayobj) < timedelta():
                    datetimeobj += timedelta(days=1)
                else:
                    datetimeobj -= timedelta(days=1)
                filename_date = datetime.strftime(datetimeobj, '%m-%d-%Y')
                filename = f"UTC_{filename_date}_.csv"
            pyplot.title(filename)

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
            if "real power" in desired_values:
                log_data = pandas.read_csv(filename, usecols = column_names,skiprows = 0, encoding = "ISO-8859-1")
                log_data['BMS - System Voltage'] = -(((log_data['BMS - System Voltage']) * (log_data['BMS - System Current']))/ 1000)
            else:
                log_data = pandas.read_csv(filename, usecols = column_names,skiprows = 0, encoding = "ISO-8859-1")#, names = desired_values)#.to_string()

            if ("time" in desired_values) and (mode == "ag"):
                new_val = log_data['Time (24Hr)'] = pandas.to_datetime(log_data['Time (24Hr)'], format='%H:%M')  # Adjust format if needed
                log_data['Time (24Hr)'] = log_data['Time (24Hr)'].apply(lambda x: x.replace(year=int(filename[10:14]), month=int(filename[4:6]), day=int(filename[7:9])))
            elif "time" in desired_values:
                new_val = log_data['Time (24Hr)'] = pandas.to_datetime(log_data['Time (24Hr)'], format='%H:%M')
                log_data['Time (24Hr)'] = new_val.dt.strftime('%H')

                #log_data.extend(log_data['Time'].dt.time.tolist())
            # if dotdotdot_counter == 1:
            #     color_line_min = log_data['Time (24Hr)'].apply(lambda x: x.replace(year=int(filename[10:14]), month=int(filename[4:6]), day=int(filename[7:9]))).max()

            dotdotdot_counter = graph_setup(log_data, filename, column_names, dotdotdot_counter, norm, mode, sorted_logs_dict)

        except Exception as e:
            if not error_occurred:  # prints error only once for each file
                # prints the name of the file that caused an error
                print(f"Error occurred while processing file: {filename} in directory: {os.path.abspath(filename)}")
                error_occurred = True  # sets flag to True to avoid repeated printing
            print(f"Error details: {e}")
        if mode == "in":
            break

    print("..done")
    if "soc" in desired_values:
        if "soc" == desired_values[0]:  # If "soc" is the x-axis value
            pyplot.gca().invert_xaxis()  # Invert the x-axis
        elif "soc" == desired_values[1]:  # If "soc" is the y-axis value
            pyplot.gca().invert_yaxis()  # Invert the y-axis

    # maybe add this as first argument in function above matplotlib.cm.ScalarMappable(cmap=divergence_cmap)
    current_figure = pyplot.gcf()
    pyplot.get_current_fig_manager().window.showMaximized()



    if mode == "ag":
        pyplot.title("Aggregate Plot", fontsize=30)


    if len(column_names) == 3:
        if column_names.index("BMS - System Current") == 2:
            pyplot.ylabel(f"Calculated Power Out [{data_units['real power']}]", fontsize=20)
            pyplot.xlabel(column_names[0] + " [" + data_units[desired_values[0]] + "] ", fontsize=20)

        elif column_names.index("BMS - System Current") == 1:
            pyplot.xlabel(f"Calculated Power Out [{data_units['real power']}] ", fontsize=20)
            pyplot.ylabel(column_names[2] + " [" + data_units[desired_values[2]] + "] ", fontsize=20)

    else:
        pyplot.xlabel(column_names[0] + " [" + data_units[desired_values[0]] + "] ", fontsize=20)  # Label for x-axis
        pyplot.ylabel(column_names[1] + " [" + data_units[desired_values[1]] + "] ", fontsize=20)  # Label for y-axis

    # Set the locator
    locator = matplotlib.dates.MonthLocator()  # every month

    #pyplot.gca().xaxis.set_major_locator(matplotlib.dates)
    pyplot.gca().xaxis.set_minor_locator(matplotlib.dates.MonthLocator())
    pyplot.locator_params(axis='y', nbins=50)
    pyplot.xticks(fontsize=12)
    pyplot.yticks(fontsize=12)

    #
    # color_line_max = log_data['Time (24Hr)'].apply(lambda x: x.replace(year=int(filename[10:14]), month=int(filename[4:6]), day=int(filename[7:9]))).max()
    # color_line_max_days_float = abs((color_line_max - unix_epoch).days)
    #
    #
    # color_line_min_days_float = abs((color_line_min - unix_epoch).days)
    # color_line_max_days_float = abs((color_line_max - unix_epoch).days)
    #
    # time_colorbar = pyplot.colorbar(matplotlib.cm.ScalarMappable(cmap=divergence_cmap, norm=norm), ax=pyplot.gca(),orientation='vertical', label='time from battery repair')
    # time_colorbar.set_ticks([color_line_min_days_float, color_line_max_days_float])

    # try:
    #     time_colorbar.set_ticklabels([color_line_min.strftime('%Y-%m-%d'), color_line_max.strftime('%Y-%m-%d')])
    # except ValueError as e:
    #     print("Error converting timestamps to strings:", e)


    if mode == "ag":
        pyplot.show()

        #save_decision = input()

    # estimate for when battery lost it's power

run_program()

decision = input("plot again? (y/n): ")

if decision == "y":
    run_program()
else:
    sys.exit()
