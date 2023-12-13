import tkinter as tk
from tkinter import filedialog, scrolledtext, Menu
from PIL import Image, ImageTk
from file_manager import FileManager
from ocr_processor import OCRProcessor


class OCRApp:
    def __init__(self, root):
        self.root = root
        self.root.title("OCR App")

        self.file_manager = FileManager()
        self.ocr_processor = OCRProcessor()

        # Configuração da interface
        self.create_widgets()
        self.create_menu()

        self.cpf_label = tk.Label(self.root, text="CPF:")
        self.cpf_label.pack(pady=5)
        self.cpf_entry = tk.Entry(self.root, state=tk.DISABLED, selectbackground="yellow")
        self.cpf_entry.pack(pady=5)

        self.rg_label = tk.Label(self.root, text="RG:")
        self.rg_label.pack(pady=5)
        self.rg_entry = tk.Entry(self.root, state=tk.DISABLED, selectbackground="yellow")
        self.rg_entry.pack(pady=5)

        self.dob_label = tk.Label(self.root, text="Data de Nascimento:")
        self.dob_label.pack(pady=5)
        self.dob_entry = tk.Entry(self.root, state=tk.DISABLED, selectbackground="yellow")
        self.dob_entry.pack(pady=5)

        self.doc_label = tk.Label(self.root, text="Documento de Identidade:")
        self.doc_label.pack(pady=5)
        self.doc_entry = tk.Entry(self.root, state=tk.DISABLED, selectbackground="yellow")
        self.doc_entry.pack(pady=5)

        self.validity_label = tk.Label(self.root, text="Validade:")
        self.validity_label.pack(pady=5)
        self.validity_entry = tk.Entry(self.root, state=tk.DISABLED, selectbackground="yellow")
        self.validity_entry.pack(pady=5)
        
        # Adiciona campo para mostrar o Nome Completo
        self.full_name_label = tk.Label(self.root, text="NOME E SOBRENOME")
        self.full_name_label.pack(pady=5)
        self.full_name_entry = tk.Entry(self.root, state=tk.DISABLED, selectbackground="yellow")
        self.full_name_entry.pack(pady=5)

        # Maximiza a janela ao iniciar
        self.root.state('zoomed')

    def create_widgets(self):
        # Adiciona uma barra de rolagem vertical
        self.scrollbar_y = tk.Scrollbar(self.root, orient=tk.VERTICAL)
        self.scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)

        # Adiciona uma barra de rolagem horizontal
        self.scrollbar_x = tk.Scrollbar(self.root, orient=tk.HORIZONTAL)
        self.scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)

        # Adiciona um widget Canvas para conter a imagem
        self.canvas = tk.Canvas(self.root, bg="white", yscrollcommand=self.scrollbar_y.set, xscrollcommand=self.scrollbar_x.set, scrollregion=(0, 0, 800, 800))
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Configura as barras de rolagem para controlar o Canvas
        self.scrollbar_y.config(command=self.canvas.yview)
        self.scrollbar_x.config(command=self.canvas.xview)

        # Botão para carregar a imagem ou PDF
        self.load_button = tk.Button(self.root, text="Carregar Imagem ou PDF", command=self.load_file)
        self.load_button.pack(pady=10)

        # Botão para executar OCR
        self.ocr_button = tk.Button(self.root, text="Executar OCR", command=self.perform_ocr)
        self.ocr_button.pack(pady=10)

        # Caixa de texto rolável para exibir o resultado do OCR
        self.text_display = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, width=80, height=20)
        self.text_display.pack(pady=10)  # Aumentei o height para 20

        # Botão para escolher o local de salvamento
        self.save_button = tk.Button(self.root, text="Escolher Local de Salvamento", command=self.choose_save_location)
        self.save_button.pack(pady=10)

        # Botão para limpar o texto
        self.clear_button = tk.Button(self.root, text="Limpar Texto", command=self.clear_text)
        self.clear_button.pack(pady=10)

    def create_menu(self):
        # Adiciona uma barra de menu à janela
        menubar = Menu(self.root)
        self.root.config(menu=menubar)

        # Adiciona uma opção no menu para carregar imagens processadas
        processed_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Imagens Processadas", menu=processed_menu)
        processed_menu.add_command(label="Carregar Imagem Processada", command=self.load_processed_image)

    def load_file(self):
        # Abre a caixa de diálogo para escolher uma imagem ou PDF
        file_path = filedialog.askopenfilename(filetypes=[("Imagens e PDFs", "*.png;*.jpg;*.jpeg;*.bmp;*.gif;*.pdf")])

        if file_path:
            # Se o arquivo for PDF, converte as páginas para imagens
            if file_path.lower().endswith(".pdf"):
                self.images = self.file_manager.load_pdf(file_path)
                self.display_image(self.images[0])  # Exibe a primeira imagem

            # Se o arquivo for uma imagem diretamente
            elif file_path.lower().endswith((".png", ".jpg", ".jpeg", ".bmp", ".gif")):
                self.image = self.file_manager.load_image(file_path)
                self.display_image(self.image)

            # Salva o caminho do arquivo para uso posterior
            self.file_path = file_path

    def load_processed_image(self):
        # Abre a caixa de diálogo para escolher uma imagem processada
        file_path = filedialog.askopenfilename(filetypes=[("Imagens", "*.png")])

        if file_path:
            # Carrega a imagem processada
            processed_image = self.file_manager.load_image(file_path)
            self.display_image(processed_image)

    def perform_ocr(self):
        if hasattr(self, 'file_path'):
            if self.file_path.lower().endswith(".pdf"):
                for img in self.images:
                    self.ocr_processor.process_image(img)
                self.display_text(self.ocr_processor.extracted_text)

            elif self.file_path.lower().endswith((".png", ".jpg", ".jpeg", ".bmp", ".gif")):
                self.ocr_processor.process_image(self.image)
                self.display_text(self.ocr_processor.extracted_text)

            # Acessa todas as informações extraídas da carteira de motorista
            all_info = self.ocr_processor.get_extracted_information()
            self.display_all_info(all_info)
            

            # Atualiza o campo com o Nome Completo
            self.full_name_entry.config(state=tk.NORMAL)
            self.full_name_entry.delete(0, tk.END)
            self.full_name_entry.insert(tk.END, all_info.get("NOME E SOBRENOME", ""))
            self.full_name_entry.config(state=tk.DISABLED)

            # Atualiza os campos com as informações específicas
            self.cpf_entry.config(state=tk.NORMAL)
            self.cpf_entry.delete(0, tk.END)
            self.cpf_entry.insert(tk.END, all_info.get("CPF", ""))
            self.cpf_entry.config(state=tk.DISABLED)

            self.rg_entry.config(state=tk.NORMAL)
            self.rg_entry.delete(0, tk.END)
            self.rg_entry.insert(tk.END, all_info.get("RG", ""))
            self.rg_entry.config(state=tk.DISABLED)

            self.dob_entry.config(state=tk.NORMAL)
            self.dob_entry.delete(0, tk.END)
            self.dob_entry.insert(tk.END, all_info.get("Data de Nascimento", ""))
            self.dob_entry.config(state=tk.DISABLED)

            self.doc_entry.config(state=tk.NORMAL)
            self.doc_entry.delete(0, tk.END)
            self.doc_entry.insert(tk.END, all_info.get("Documento de Identidade", ""))
            self.doc_entry.config(state=tk.DISABLED)

            self.validity_entry.config(state=tk.NORMAL)
            self.validity_entry.delete(0, tk.END)
            self.validity_entry.insert(tk.END, all_info.get("Validade", ""))
            self.validity_entry.config(state=tk.DISABLED)

    def display_image(self, img):
        # Converte a imagem para o formato compatível com Tkinter
        tk_image = ImageTk.PhotoImage(img)

        # Adiciona a imagem ao Canvas
        self.canvas.create_image(0, 0, anchor=tk.NW, image=tk_image)

        # Atualiza a região de rolagem do Canvas
        self.canvas.config(scrollregion=self.canvas.bbox(tk.ALL))

        # Mantém uma referência para evitar a coleta de lixo
        self.canvas.image = tk_image

    def display_text(self, text):
        # Exibe o texto extraído na caixa de texto
        self.text_display.delete(1.0, tk.END)  # Limpa o conteúdo anterior
        self.text_display.insert(tk.END, text)

    def display_specific_info(self, specific_info):
        # Exibe as informações específicas na caixa de texto correspondente
        self.text_display.insert(tk.END, f"Informações Específicas:\n{specific_info}\n\n")

    def display_all_info(self, all_info):
        # Exibe todas as informações na caixa de texto correspondente
        self.text_display.insert(tk.END, f"Todas as Informações:\n{all_info}\n\n")

    def choose_save_location(self):
        # Abre a caixa de diálogo para escolher o local de salvamento
        self.output_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Arquivos de Texto", "*.txt")])

        if not self.output_path:
            return

        # Salva a imagem processada
        for i, img in enumerate(self.ocr_processor.processed_images):
            save_path = f"{self.output_path}_processed_image_{i + 1}.png"
            self.file_manager.save_image(img, save_path)

        # Salva o texto extraído no local escolhido
        try:
            self.file_manager.save_text(self.ocr_processor.extracted_text, self.output_path)
            print(f"Texto e imagens salvas com sucesso em {self.output_path}")
        except Exception as e:
            print(f"Erro ao salvar o texto: {e}")

    def clear_text(self):
        # Limpa o conteúdo da caixa de texto
        self.text_display.delete(1.0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = OCRApp(root)
    root.mainloop()
