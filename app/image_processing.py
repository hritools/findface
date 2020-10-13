import base64
import os
from io import BytesIO
from uuid import uuid4

import PIL
from django.core.files.uploadedfile import UploadedFile, InMemoryUploadedFile

from findface.settings import MEDIA_ROOT, MEDIA_URL
from .face_recognition import recognize, RecognitionResult

MAX_HEIGHT = 600


class Image:
    def __init__(self, recog_result: RecognitionResult):
        self.person_name = recog_result.person_name
        self.face_x = recog_result.x
        self.face_y = recog_result.y
        self.face_width = recog_result.width
        self.face_height = recog_result.height
        self.width = self.face_width
        self.height = self.face_height
        self.url = None


def process_image(uploaded_file: UploadedFile) -> Image:
    file_name, bytes_im = save_image(uploaded_file)
    recog_result = recognize(bytes_im)
    image = Image(recog_result)
    if image.height > MAX_HEIGHT:
        ratio = MAX_HEIGHT / image.height
        image.height = MAX_HEIGHT
        image.width = int(image.width * ratio)

    image.url = MEDIA_URL + file_name
    return image


def process_base64(b64: str) -> Image:
    decode_image = base64.b64decode(b64)
    img = PIL.Image.open(BytesIO(decode_image)).convert('RGB')
    img_bytes_io = BytesIO()
    img.save(img_bytes_io, format='PNG')
    img_bytes = img_bytes_io.getvalue()
    file = InMemoryUploadedFile(
        BytesIO(img_bytes),
        None,
        'photo.png',
        'image',
        len(img_bytes),
        None,
    )
    file.image = img
    img.close()
    return process_image(file)


def save_image(uploaded_file: UploadedFile) -> (str, bytes):
    content = uploaded_file.file.read()
    ext = uploaded_file.image.format
    file_name = f'{uuid4().hex}.{ext}'
    with open(os.path.join(MEDIA_ROOT, file_name), 'wb') as f:
        f.write(content)
    return file_name, content
