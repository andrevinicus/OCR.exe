# file_manager.py
from PIL import Image
import fitz  # PyMuPDF

class FileManager:
    @staticmethod
    def load_pdf(pdf_path):
        images = []
        pdf_document = fitz.open(pdf_path)

        for page_number in range(pdf_document.page_count):
            page = pdf_document[page_number]
            pix = page.get_pixmap()
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            images.append(img)

        pdf_document.close()
        return images

    @staticmethod
    def load_image(image_path):
        return Image.open(image_path)

    @staticmethod
    def save_image(image, save_path):
        image.save(save_path)

    @staticmethod
    def save_text(text, save_path):
        with open(save_path, "w", encoding="utf-8") as file:
            file.write(text)
