import psutil

def open_handles():
    for proc in psutil.process_iter():  
        try:
            open_files = proc.open_files()
        except (PermissionError, psutil.AccessDenied):
            continue

    number_of_open_files = len(open_files) 
    return number_of_open_files