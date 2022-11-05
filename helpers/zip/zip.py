import zipfile
import io


def get_file(zip_path):
    return zipfile.ZipFile(zip_path, 'r')


def get_files_in_zip_file(zip_path):
    payload = get_file(zip_path)
    return payload.namelist()


def get_text_in_zip_file(zip_path, file_name):
    payload = get_file(zip_path)
    file = payload.open(file_name, 'r')
    contents = file.read().decode('utf-8')
    file.close()
    return contents
