import glob
import os

def getTxtFilesFromFolder(path):
    file_paths = glob.glob(os.path.join(path, '**', '*.txt'), recursive=True)

    # Remover o ficheiro optimal.txt e capinfo.txt
    filtered_file_paths = [
        file_path for file_path in file_paths
        if os.path.basename(file_path) not in ['optimal.txt', 'capinfo.txt']
    ]

    return filtered_file_paths