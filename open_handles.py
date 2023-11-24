import psutil

file_list = []

def open_handles():
    for proc in psutil.process_iter():  
        try:
            open_file = proc.open_files()
            file_list.append(open_file)
        except (PermissionError, psutil.AccessDenied):
            continue

    number_of_open_files = len(file_list) 
    return number_of_open_files