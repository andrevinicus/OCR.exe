import pytesseract
import re

class OCRProcessor:
    pytesseract.pytesseract.tesseract_cmd = r'C:\Users\USER\AppData\Local\Tesseract-OCR\tesseract.exe'

    def __init__(self):
        self.extracted_text = ""
        self.processed_images = []
        self.cpf = ""
        self.rg = ""
        self.dob = ""

    def process_image(self, image):
        try:
            text = pytesseract.image_to_string(image, config='--dpi 300 --psm 4')
            self.extracted_text = text
            self.processed_images.append(image)
            self.extract_information()
        except Exception as e:
            print(f"Erro ao executar OCR: {e}")

    def extract_information(self):
        # Expressões regulares para identificar CPF, RG e data de nascimento
        cpf_pattern = re.compile(r'\b\d{3}\.\d{3}\.\d{3}-\d{2}\b')
        rg_pattern = re.compile(r'\b\d{1,2}\.\d{3}\.\d{3}(-\d{1}|\s\d{2})\b')
        dob_pattern = re.compile(r'\b\d{2}/\d{2}/\d{4}\b')

        # Encontrar correspondências nos padrões
        cpf_matches = cpf_pattern.findall(self.extracted_text)
        rg_matches = rg_pattern.findall(self.extracted_text)
        dob_matches = dob_pattern.findall(self.extracted_text)

        # Atribuir os valores encontrados às variáveis da classe
        self.cpf = cpf_matches[0] if cpf_matches else ""
        self.rg = rg_matches[0] if rg_matches else ""
        self.dob = dob_matches[0] if dob_matches else ""

    def get_extracted_information(self):
        return {
            "CPF": self.cpf,
            "RG": self.rg,
            "Data de Nascimento": self.dob
        }
