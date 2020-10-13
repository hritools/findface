import threading
from functools import reduce

from PIL import Image

import faceR
from faceR.alignment import align_faces
from faceR.embedding import embed
from faceR.classification import classify

from numpy import array
import io


class RecognitionPipeline:
    def __init__(self):
        faceR.init(config='app/config.yaml')
        self.running = True
        self.to_pass = None
        self.lock = threading.Lock()
        self.pipeline = [
            align_faces,
            self.final
        ]
        self.rec_pipeline = [
            embed,
            classify
        ]
        self.pipeline = reduce(lambda x, y: y(x), self.pipeline, self.proxy_gen())
        self.rec_pipeline = reduce(lambda x, y: y(x), self.rec_pipeline, self.proxy_gen())

    def proxy_gen(self):
        while self.running:
            yield self.to_pass

    def final(self, gen):
        for frame, aligned_list in gen:
            if aligned_list.any():
                self.to_pass = frame, aligned_list
                # Simply return the first one found on the photo
                yield aligned_list[0], next(self.rec_pipeline)[0]
            else:
                yield [0, 0, frame.shape[1], frame.shape[0]], "Nobody found"

    def recognize(self, image_in):
        with self.lock:
            self.to_pass = image_in
            bbox, res = next(self.pipeline)
            return RecognitionResult(x=bbox[0], y=bbox[1], width=bbox[2] - bbox[0],
                                     height=bbox[3] - bbox[1], person_name=res)


class RecognitionResult:
    def __init__(self, *, x: int, y: int, width: int, height: int, person_name: str) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.person_name = person_name


rec = RecognitionPipeline()


def recognize(bytes) -> RecognitionResult:
    # content = image.file.read()
    # return RecognitionResult(x=3, y=3, width=13, height=13, person_name='Me')
    return rec.recognize(array(Image.open(io.BytesIO(bytes))))
