import os
import errno
import shutil

user_documents = os.path.join(os.path.expanduser('~\\'), 'Documents\\')


def make_new_dirs(base_dir, path):
    directory = os.path.join(base_dir, path)
    if not os.path.exists(directory):
        try:
            os.makedirs(directory)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
    return directory


def delete_this_dir(path):
    if os.path.exists(path):
        try:
            shutil.rmtree(path)
        except OSError as e:
            print("Error: %s - %s." % (e.filename, e.strerror))


def make_castle_temps():
    return make_new_dirs(user_documents, 'My Games\CastlePythonTemps')

