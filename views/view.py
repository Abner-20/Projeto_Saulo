# PDI/views/view.py
import tkinter as tk
from views.menu_bar import MenuBar
from views.image_panel import ImagePanel
from views.control_panel import ControlPanel

class View:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller

        # Menu superior
        self.menu = MenuBar(self.root, controller)
        self.root.config(menu=self.menu.menubar)

        # Painéis
        self.image_panel = ImagePanel(self.root, controller) 
        self.control_panel = ControlPanel(self.root, controller) 

        # Layout
        self.control_panel.frame.pack(side="right", fill="y")
        self.image_panel.frame.pack(side="left", fill="both", expand=True)

    def display_original_image(self, image):
        self.image_panel.show_original_image(image)

    def display_processed_image(self, image):
        self.image_panel.show_processed_image(image)

    def log_action(self, text):
        self.control_panel.add_log(text)

    def update_histogram(self, original_bgr, processed_bgr):
        """
        Atualiza o gráfico do histograma com a comparação.
        (Parâmetros alterados)
        """
        self.control_panel.histogram_canvas.plot_histogram(original_bgr, processed_bgr)
        
    def update_pixel_info(self, info_text):
        """Passa a informação do pixel para o control_panel."""
        self.control_panel.update_pixel_info(info_text)