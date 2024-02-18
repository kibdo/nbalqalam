import os
import secrets
from nbalqalam import app
def save_post_image(image, location=os.path.join(app.root_path, 'static/images/post-images')):
    random_hex = secrets.token_hex(8)
    _, ext = os.path.splitext(image.filename)
    new_filename = f'{random_hex}{ext}'
    picture_path = os.path.join(location, new_filename)
    image.save(picture_path)
    return new_filename