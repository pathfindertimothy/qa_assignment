__Author__ = "Timothy"
__Email__ = "pathfindertimothy@gmail.com"
__Date__ = "20-November-2023"
__Platform__ = "Windows 11"

import psutil,datetime,time,schedule,openpyxl
from open_handles import open_handles

process_name = input("Enter process name: ")
total_duration = int(input("Enter monitorin duration in seconds: "))
sample_interval = int(input("Enter sample interval in seconds: "))
path = r".\Output_Result.xlsx"

def warning():
    cpuUsage = psutil.cpu_percent(interval=1)
    if cpuUsage > 50:
        print("CpuUsage is above 50%: ", cpuUsage)
    memUsage = psutil.virtual_memory().percent
    if memUsage > 50: 
        print("Memory usage is above 50%: ", memUsage)

def process_monitor():
    time = datetime.datetime.now().strftime("%Y%M%D -%H:%M:%S")

    # number of open handles
    number_of_open_files = open_handles()

    for p in psutil.process_iter(['name']):
        if p.info['name'] == process_name:
            cpu = p.cpu_percent(interval=1) / psutil.cpu_count()

            memory_mb = p.memory_full_info().rss / (1024*1024)
            memory = p.memory_percent()
            
            # get the file descriptor of the excelsheet
            open_file = open(path, "r")
            fd = open_file.fileno()

            file = openpyxl.load_workbook(path)
            sheet = file.active
            sheet.cell(column=1, row=sheet.max_row + 1, value=time)
            sheet.cell(column=2, row=sheet.max_row, value=process_name)
            sheet.cell(column=3, row=sheet.max_row, value=cpu)
            sheet.cell(column=4, row=sheet.max_row, value=memory_mb)
            sheet.cell(column=5, row=sheet.max_row, value=memory)
            sheet.cell(column=6, row=sheet.max_row, value=number_of_open_files)
            sheet.cell(column=7, row=sheet.max_row, value=fd)
            file.save(path)

schedule.every(1).seconds.until(datetime.timedelta(seconds=total_duration)).do(warning)
schedule.every(sample_interval).seconds.until(datetime.timedelta(seconds=total_duration)).do(process_monitor)

start_time = time.time()
while ((time.time() - start_time) < (total_duration + 1)):
    schedule.run_pending()
    time.sleep(1)