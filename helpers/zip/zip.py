import zipfile


def get_files_in_zip_file(file_path):
    payload = zipfile.ZipFile(file_path, 'r')
    return payload.namelist()
