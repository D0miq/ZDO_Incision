import os.path


def get_input_files(paths):
    input_files = list()

    for path in paths:
        if os.path.isfile(path):
            input_files.append(path)
        else:
            input_files.extend(get_files_from_dir(path))

    return input_files


def get_files_from_dir(directory):
    dir_content = os.listdir(directory)
    files = list()

    for name in dir_content:
        path = os.path.join(directory, name)
        if os.path.isfile(path):
            files.append(path)

    return files
