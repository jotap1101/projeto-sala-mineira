import hashlib
import os

def generate_image_path(instance, filename):
    hash_object = hashlib.sha256(filename.encode())
    hash_filename = hash_object.hexdigest()
    extension = os.path.splitext(filename)[1]

    return f'candidate/photos/{hash_filename}{extension}'