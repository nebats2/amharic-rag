import os

def make_directory_from_path(path : str):
    try:
        os.mkdir(path)
        print(f"Directory is created successfully path = {path}")
    except Exception as ex:
        print(f"failed to create directory {path}")
        raise ex

def remove_dir_by_path(path :str):
    try:
        os.rmdir(path)
        print(f"Directory '{path}' deleted successfully.")
    except OSError as e:
        print(f"Error deleting directory '{path}': {e}")