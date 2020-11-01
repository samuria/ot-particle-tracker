import os

from main import app

UPLOAD_DIR = app.config["UPLOAD_DIR"]


def get_file_extension(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower()


def get_all_uploaded_files():
    files_in_directory = os.listdir(UPLOAD_DIR)
    files = []

    for index, file in enumerate(files_in_directory):
        files.append(
            {
                'id': index,
                'name': os.path.splitext(file)[0],
                'extension': os.path.splitext(file)[1][1:].upper(),
                'size': os.stat(os.path.join(UPLOAD_DIR, file)).st_size
            }
        )

    return files


def delete_file(id):
    files_in_directory = os.listdir(UPLOAD_DIR)
    os.remove(os.path.join(UPLOAD_DIR, files_in_directory[int(id)]))
