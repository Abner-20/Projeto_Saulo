# PDI/views/image_panel.py
import tkinter as tk
from tkinter import Label

class ImagePanel:
    def __init__(self, root, controller):
        """Atualizado para receber o controller."""
        self.controller = controller
        self.frame = tk.Frame(root, bg="#222")
        
        # Frame para a imagem Original
        original_frame = tk.Frame(self.frame, bg="#222", relief=tk.SUNKEN, bd=1)
        original_frame.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        
        Label(original_frame, text="Original", bg="#222", fg="white").pack(pady=2)
        self.original_label = Label(original_frame, bg="#222")
        self.original_label.pack(fill="both", expand=True)
        # BIND DO CLIQUE
        self.original_label.bind("<Button-1>", lambda event: self.on_image_click(event, 'original'))

        # Frame para a imagem Processada
        processed_frame = tk.Frame(self.frame, bg="#222", relief=tk.SUNKEN, bd=1)
        processed_frame.pack(side="right", fill="both", expand=True, padx=5, pady=5)

        Label(processed_frame, text="Processada", bg="#222", fg="white").pack(pady=2)
        self.processed_label = Label(processed_frame, bg="#222")
        self.processed_label.pack(fill="both", expand=True)
        # BIND DO CLIQUE
        self.processed_label.bind("<Button-1>", lambda event: self.on_image_click(event, 'processed'))

    def show_original_image(self, image):
        """Atualiza o painel da imagem original."""
        self.original_label.config(image=image)
        self.original_label.image = image  # mantém referência

    def show_processed_image(self, image):
        """Atualiza o painel da imagem processada."""
        self.processed_label.config(image=image)
        self.processed_label.image = image  # mantém referência
        
    def on_image_click(self, event, panel_name):
        """
        Lida com o clique na imagem para encontrar o pixel (x, y).
        """
        # A imagem está centrada no Label. Precisamos de calcular o offset.
        label = event.widget
        if not hasattr(label, 'image') or label.image is None:
            return # Nenhuma imagem carregada

        img_w = label.image.width()
        img_h = label.image.height()
        label_w = label.winfo_width()
        label_h = label.winfo_height()

        # Calcular o offset (espaço vazio) à volta da imagem
        offset_x = (label_w - img_w) // 2
        offset_y = (label_h - img_h) // 2
        
        # Coordenadas do clique relativas à imagem
        image_x = event.x - offset_x
        image_y = event.y - offset_y
        
        # Verificar se o clique foi dentro da imagem (e não no padding)
        if 0 <= image_x < img_w and 0 <= image_y < img_h:
            # Envia as coordenadas (x, y) e qual painel foi clicado
            self.controller.on_pixel_selected(panel_name, image_x, image_y)