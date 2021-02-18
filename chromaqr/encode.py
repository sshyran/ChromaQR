from PIL import Image
from qrcode import QRCode, constants
from enum import Enum
import math

# Error correction: LOW, MEDIUM, HIGH or MAX.
ErrorCorrection = Enum("ErrorCorrection", "LOW MED HIGH MAX")

"""
Base encoder for QR codes.
Initialised by defining the error correction level.
"""
class Encoder:
    def __init__(self, error_correction = ErrorCorrection.MED):
        self.error_correction = error_correction

    def encode(self, data: bytearray) -> Image:
        codes = []
        section_length = math.ceil(len(data) / 3)
        split_data = [
            data[0 : section_length],
            data[section_length : section_length * 2],
            data[section_length * 2 :]
        ]

        error_correction_map = {
            ErrorCorrection.LOW: constants.ERROR_CORRECT_L,
            ErrorCorrection.MED: constants.ERROR_CORRECT_M,
            ErrorCorrection.HIGH: constants.ERROR_CORRECT_Q,
            ErrorCorrection.MAX: constants.ERROR_CORRECT_H
        }

        for i in range(3):
            qr_code = QRCode(error_correction = error_correction_map[self.error_correction])
            qr_code.add_data(split_data[i], optimize=0)
            qr_code.make()
            qr_code_image = qr_code.make_image(fill_color="black", back_color="white")
            codes.append(qr_code_image.convert("L"))

        return Image.merge("RGB", codes)