# PDI/views/control_panel.py
import tkinter as tk
from tkinter import scrolledtext, ttk
from views.histogram_canvas import HistogramCanvas 

class ControlPanel:
    def __init__(self, root, controller):
        
        # --- Configuração do Frame Principal com Scrollbar ---
        
        self.frame = tk.Frame(root, bg="#333", width=250)
        self.frame.pack_propagate(False) 

        self.scrollbar = ttk.Scrollbar(self.frame, orient="vertical")
        self.canvas = tk.Canvas(self.frame, bg="#333", yscrollcommand=self.scrollbar.set, highlightthickness=0)
        
        self.scrollbar.config(command=self.canvas.yview)
        
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        # --- Frame Interno (Rlável) ---
        self.scrollable_frame = tk.Frame(self.canvas, bg="#333")
        
        self.frame_window_id = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        # --- Binds para a Scrollbar ---
        self.scrollable_frame.bind("<Configure>", self.on_frame_configure)
        self.canvas.bind("<Configure>", self.on_canvas_configure)
        
        # --- NOVO: Bind do Rato ---
        self._bind_mousewheel(self.canvas)
        self._bind_mousewheel(self.scrollable_frame)
        # -----------------------------
        
        # --- FIM da Configuração do Scrollbar ---
        

        # --- Início dos Widgets (Adicionados ao self.scrollable_frame) ---

        # --- Quadro de Informação do Pixel ---
        info_frame = tk.Frame(self.scrollable_frame, bg="#333", relief=tk.SUNKEN, bd=1)
        info_frame.pack(fill="x", padx=5, pady=5, anchor="n") 
        
        tk.Label(info_frame, text="Info. do Pixel (Clique na imagem)", fg="white", bg="#333").pack()
        
        self.info_text = tk.Text(
            info_frame, height=5, bg="#222", fg="white", bd=0, 
            highlightthickness=0, font=("Consolas", 9)
        )
        self.info_text.pack(fill="x", padx=2, pady=2)
        self.info_text.insert(tk.END, "Nenhum pixel selecionado.")
        self.info_text.config(state="disabled")
        self._bind_mousewheel(self.info_text) # Permite rolar mesmo sobre o texto

        # --- Botão de Reset Rápido ---
        self.reset_button = tk.Button(
            self.scrollable_frame, 
            text="Restaurar Imagem Original", 
            command=controller.apply_reset,
            bg="#555", fg="white", relief=tk.RAISED, bd=1
        )
        self.reset_button.pack(fill="x", padx=5, pady=(0, 5), anchor="n")

        # --- Histograma (Visualização Gráfica) ---
        self.histogram_canvas = HistogramCanvas(self.scrollable_frame)
        self.histogram_canvas.frame.pack(fill="x", padx=5, pady=5, anchor="n")
        self._bind_mousewheel(self.histogram_canvas.frame)
        self._bind_mousewheel(self.histogram_canvas.canvas.get_tk_widget())

        # --- Controles de Ajuste Manual ---
        controls_frame = tk.Frame(self.scrollable_frame, bg="#333")
        controls_frame.pack(fill="x", padx=5, pady=5, anchor="n")

        tk.Label(controls_frame, text="Brilho", fg="white", bg="#333").pack()
        self.brightness_slider = tk.Scale(
            controls_frame, from_=-100, to=100, orient=tk.HORIZONTAL,
            bg="#333", fg="white", troughcolor="#555",
            command=controller.on_brightness_contrast_change
        )
        self.brightness_slider.set(0)
        self.brightness_slider.pack(fill="x")
        self._bind_mousewheel(self.brightness_slider)

        tk.Label(controls_frame, text="Contraste", fg="white", bg="#333").pack()
        self.contrast_slider = tk.Scale(
            controls_frame, from_=1.0, to=3.0, orient=tk.HORIZONTAL, resolution=0.1,
            bg="#333", fg="white", troughcolor="#555",
            command=controller.on_brightness_contrast_change
        )
        self.contrast_slider.set(1.0)
        self.contrast_slider.pack(fill="x")
        self._bind_mousewheel(self.contrast_slider)
        
        tk.Label(controls_frame, text="Limiar Global (Ajustável)", fg="white", bg="#333").pack()
        self.threshold_slider = tk.Scale(
            controls_frame, 
            from_=0, to=255, orient=tk.HORIZONTAL, resolution=1,
            bg="#333", fg="white", troughcolor="#555",
            command=controller.on_global_threshold_change
        )
        self.threshold_slider.set(127)
        self.threshold_slider.pack(fill="x")
        self._bind_mousewheel(self.threshold_slider)

        # --- Histórico de Ações (Log) ---
        tk.Label(self.scrollable_frame, text="Histórico de Ações", fg="white", bg="#333").pack(pady=5, anchor="n")
        
        # O ScrolledText já tem sua própria barra de rolagem,
        # não precisamos de um bind de rato para ele.
        self.log_area = scrolledtext.ScrolledText(self.scrollable_frame, height=30, bg="#111", fg="white", state='normal')
        self.log_area.pack(padx=5, pady=5, fill="x", expand=False, anchor="n")

    # --- Funções de Callback da Scrollbar ---
    
    def on_frame_configure(self, event):
        """Atualiza a scrollregion do canvas."""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def on_canvas_configure(self, event):
        """Ajusta a largura do frame interno à largura do canvas."""
        self.canvas.itemconfig(self.frame_window_id, width=event.width)

    # --- NOVOS MÉTODOS: Binds do Rato ---
    
    def _bind_mousewheel(self, widget):
        """Aplica o bind de rolagem do rato a um widget."""
        widget.bind("<MouseWheel>", self._on_mousewheel)

    def _on_mousewheel(self, event):
        """Permite a rolagem do canvas com a roda do rato."""
        # 'event.delta' é 120 para scroll para cima, -120 para baixo (no Windows)
        # Dividimos por 120 para normalizar para -1 ou 1
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    # --- Funções de Widget ---

    def add_log(self, text):
        self.log_area.insert(tk.END, f"> {text}\n")
        self.log_area.see(tk.END) # Auto-scroll para o fim

    def reset_sliders(self):
        self.brightness_slider.set(0)
        self.contrast_slider.set(1.0)
        self.threshold_slider.set(127)
        
    def update_pixel_info(self, info_text):
        self.info_text.config(state="normal")
        self.info_text.delete(1.0, tk.END)
        self.info_text.insert(tk.END, info_text)
        self.info_text.config(state="disabled")