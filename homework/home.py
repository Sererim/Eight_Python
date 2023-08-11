from os import walk, stat
from json import dumps as json_dumps
from csv import DictWriter as csv_writer
from pickle import dump

__save_file_name = ("save.json", "save.csv", "save.pickle")


def convert_bytes(num: int) -> str:
    """
    Function that converts bytes to mb, gb and etc.
    """
    for x in ["bytes", "KB", "MB", "GB"]:
        if num < 1024.0:
            return f"{num * 10} {x}"
        else:
            num /= 1024.0


def is_a_file(path: str) -> bool:
    try:
        with open(path, 'r') as f:
            return True
    except PermissionError:
        return False
    

def walk_dir(directory: str) -> dict:
    list_of_files = []
    data = {}
    temp = []
    path_to = ""
    file_name = ""
    for dirpath, dirnames, dirfile in walk(directory):
        for file in dirfile:
            list_of_files.append(f"{dirpath}\\{file}")
        for dir in dirnames:
            list_of_files.append(f"{dirpath}\\{dir}")
    
    for i, file in enumerate(list_of_files):
        temp = file.split("\\")
        file_name = temp[-1]
        temp = temp[:-1]
        
        for j in temp:
            path_to += j + "/"
            
        if is_a_file(file):                    
            data[i] = {
                "File name": file_name,
                "Path to": path_to,
                "Size": convert_bytes(stat(file).st_size)
            }
        else:
            
            data[i] = {
                "Directory name": file_name,
                "Parent directories": path_to,
                "Size": convert_bytes(stat(file).st_size)                
            }
        
        temp = []
        file_name, path_to = "", ""
            
    return data
        
    
def save_to_json(data: dict, file_name: str = __save_file_name[0]) -> None:
    save = json_dumps(data, indent=2, separators=(',', ':'))
    with open(file_name, "+w") as f:
        f.write(save)
    

def save_to_csv(data: dict, file_name: str = __save_file_name[1]) -> None:
    csv_data = {}
    with open(file_name, "w+") as f:
        writer = csv_writer(f, fieldnames=["id", "File name", "Path to", "Size", "Parent directories", "Directory name"], restval="Other", delimiter="|")
        writer.writeheader()
        
        for k, v in data.items():
            csv_data["id"] = k
            for x,y in v.items():
                csv_data[x] = y
            writer.writerow(csv_data)


def save_to_pickle(data: dict, file_name: str = __save_file_name[2]) -> None:
    with open(file_name, '+wb') as f:
        dump(data, f)
        


if __name__ == "__main__":
    # print(covert_bytes(100000))
    # print(is_a_file("test/Fvzjyqgcwbepmkdaixhs0.png"))
    # print(convert_bytes(stat("test").st_size))
    d = walk_dir("test")
    # save_to_json(d)
    # save_to_csv(d)
    save_to_pickle(d)