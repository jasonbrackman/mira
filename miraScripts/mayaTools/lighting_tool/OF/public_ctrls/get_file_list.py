import os


def get_file_list(file_dir, ext):
    if isinstance(ext, list):
        if os.path.isdir(file_dir):
            file_list = []
            for root, dirs, files in os.walk(file_dir):
                for f in files:
                    if 'swatches' not in f:
                        if os.path.splitext(f)[-1] in ext:
                            file_list.append(os.path.join(root, f))
        else:
            if os.path.splitext(file_dir)[-1] in ext:
                file_list = file_dir
        if file_list:
            return file_list
    else:
        raise TypeError('The second argument(ext) must be a type of list')