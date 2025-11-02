# PDI/views/control_panel.py
import tkinter as tk
from tkinter import scrolledtext
from views.histogram_canvas import HistogramCanvas 

class ControlPanel:
    def __init__(self, root, controller):
        self.frame = tk.Frame(root, bg="#333", width=250)
        self.frame.pack_propagate(False)

        # --- Quadro de Informação do Pixel ---
        info_frame = tk.Frame(self.frame, bg="#333", relief=tk.SUNKEN, bd=1)
        info_frame.pack(fill="x", padx=5, pady=5)
        
        tk.Label(info_frame, text="Info. do Pixel (Clique na imagem)", fg="white", bg="#333").pack()
        
        self.info_text = tk.Text(
            info_frame, height=5, bg="#222", fg="white", bd=0, 
            highlightthickness=0, font=("Consolas", 9)
        )
        self.info_text.pack(fill="x", padx=2, pady=2)
        self.info_text.insert(tk.END, "Nenhum pixel selecionado.")
        self.info_text.config(state="disabled")

        # --- Histograma (Visualização Gráfica) ---
        self.histogram_canvas = HistogramCanvas(self.frame)
        self.histogram_canvas.frame.pack(fill="x", padx=5, pady=5)
        
        # --- Controles de Ajuste Manual ---
        controls_frame = tk.Frame(self.frame, bg="#333")
        controls_frame.pack(fill="x", padx=5, pady=5)

        tk.Label(controls_frame, text="Brilho", fg="white", bg="#333").pack()
        self.brightness_slider = tk.Scale(
            controls_frame, from_=-100, to=100, orient=tk.HORIZONTAL,
            bg="#333", fg="white", troughcolor="#555",
            command=controller.on_brightness_contrast_change
        )
        self.brightness_slider.set(0)
        self.brightness_slider.pack(fill="x")

        tk.Label(controls_frame, text="Contraste", fg="white", bg="#333").pack()
        self.contrast_slider = tk.Scale(
            controls_frame, from_=1.0, to=3.0, orient=tk.HORIZONTAL, resolution=0.1,
            bg="#333", fg="white", troughcolor="#555",
            command=controller.on_brightness_contrast_change
        )
        self.contrast_slider.set(1.0)
        self.contrast_slider.pack(fill="x")
        
        # --- NOVO: Slider de Limiar Global ---
        tk.Label(controls_frame, text="Limiar Global (Ajustável)", fg="white", bg="#333").pack()
        self.threshold_slider = tk.Scale(
            controls_frame, 
            from_=0, 
            to=255, 
            orient=tk.HORIZONTAL, 
            resolution=1, # Incremento de 1 em 1
            bg="#333", fg="white", troughcolor="#555",
            command=controller.on_global_threshold_change
        )
        self.threshold_slider.set(127) # Ponto inicial (meio)
        self.threshold_slider.pack(fill="x")
        # -------------------------------------

        # --- Histórico de Ações (Log) ---
        tk.Label(self.frame, text="Histórico de Ações", fg="white", bg="#333").pack(pady=5)
        self.log_area = scrolledtext.ScrolledText(self.frame, height=20, bg="#111", fg="white", state='normal')
        self.log_area.pack(padx=5, pady=5, fill="both", expand=True)

    def add_log(self, text):
        self.log_area.insert(tk.END, f"> {text}\n")
        self.log_area.see(tk.END)

    def reset_sliders(self):
        """Restaura TODOS os sliders para a posição original."""
        self.brightness_slider.set(0)
        self.contrast_slider.set(1.0)
        self.threshold_slider.set(127) # Adicionado
        
    def update_pixel_info(self, info_text):
        """Atualiza a caixa de informação do pixel."""
        self.info_text.config(state="normal")
        self.info_text.delete(1.0, tk.END)
        self.info_text.insert(tk.END, info_text)
        self.info_text.config(state="disabled")