import os
import secrets
from PIL import Image
from DeadMatter import app

def picture_save(picture_data):
    random_name = secrets.token_hex(8)
    _, p_ext = os.path.splitext(picture_data.filename)
    picture_new_name = random_name + p_ext
    picture_path = os.path.join(
        app.root_path, r'static\img\Server_pics', picture_new_name).replace("\\","/")

    output_size = (500, 500)
    i = Image.open(picture_data)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_new_name
