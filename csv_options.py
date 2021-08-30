
def csv_task(file, mode, text=""):
    if mode == "r":
        with open(file, mode) as f:
            return f.readlines()
    else:
        with open(file, mode) as f:
            f.write(text)