# PDI/controllers/controller.py
from tkinter import Tk, filedialog, messagebox, simpledialog 
from models.model import Model
from views.view import View

class Controller:
    def __init__(self):
        self.root = Tk()
        self.root.title("PDI Studio - Sistema Interativo de Processamento de Imagens")
        self.root.geometry("1600x900")
        self.model = Model()
        self.view = View(self.root, controller=self)
        self.is_slider_active = False 
        self.is_threshold_slider_active = False

    def run(self):
        self.root.mainloop()

    # --- Funções Auxiliares ---
    
    def reset_all_sliders(self):
        """Reseta todos os sliders de ajuste."""
        self.view.control_panel.reset_sliders()

    def _apply_filter(self, model_function, log_message):
        """
        Função auxiliar genérica para aplicar filtros destrutivos.
        :param model_function: A função do modelo a ser chamada (ex: self.model.convert_to_gray)
        :param log_message: A mensagem para exibir no log.
        """
        if self.model.image is None:
            messagebox.showwarning("Aviso", "Nenhuma imagem carregada.")
            return

        result_tk = model_function() 
        
        if result_tk:
            self.view.display_processed_image(result_tk)
            self.view.log_action(log_message)
            self.view.update_histogram(self.model.original, self.model.image)
            self.reset_all_sliders()
        else:
            messagebox.showerror("Erro", f"Falha ao aplicar filtro: {log_message}")

    # ========== Métodos de Arquivo ==========

    def open_image(self):
        path = filedialog.askopenfilename(
            title="Selecione uma imagem",
            filetypes=[("Arquivos de imagem", "*.png;*.jpg;*.jpeg;*.bmp")]
        )
        if path:
            image_tk = self.model.load_image(path)
            if image_tk:
                self.view.display_original_image(image_tk)
                self.view.display_processed_image(image_tk)
                self.view.log_action(f"Imagem carregada: {path}")
                self.view.update_histogram(self.model.original, self.model.original) 
                self.reset_all_sliders()
            else:
                messagebox.showerror("Erro", "Falha ao carregar a imagem.")

    def save_image(self):
        if self.model.image is None:
            messagebox.showwarning("Aviso", "Nenhuma imagem carregada.")
            return
        path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG", "*.png"), ("JPEG", ".jpg"), ("BMP", ".bmp")]
        )
        if path:
            self.model.save_image(path)
            self.view.log_action(f"Imagem salva em: {path}")

    def apply_reset(self):
        result_tk = self.model.reset_image()
        if result_tk:
            self.view.display_processed_image(result_tk)
            self.view.log_action("Imagem restaurada ao original.")
            self.view.update_histogram(self.model.original, self.model.original) 
            self.reset_all_sliders()
        else:
            messagebox.showwarning("Aviso", "Nenhuma imagem carregada.")

    # ========== Métodos de Ajuste (Sliders) ==========

    def on_brightness_contrast_change(self, *args):
        if self.model.image is None: return 
        if not self.is_slider_active:
            self.view.log_action("Ajustando brilho/contraste...")
            self.is_slider_active = True
        
        brightness = self.view.control_panel.brightness_slider.get()
        contrast = self.view.control_panel.contrast_slider.get()
        
        temp_image_cv = self.model.change_brightness_contrast(
            self.model.image, brightness, contrast
        )
        
        if temp_image_cv is not None:
            result_tk = self.model.to_tk_image(temp_image_cv)
            if result_tk:
                self.view.display_processed_image(result_tk)
                self.view.update_histogram(self.model.original, temp_image_cv) 

        self.root.after(1000, self.reset_slider_flag)

    def reset_slider_flag(self):
        self.is_slider_active = False

    # ========== Métodos de Filtro (Histograma/Cor) ==========
    
    def apply_gray(self):
        self._apply_filter(self.model.convert_to_gray, "Tons de cinza aplicado.")

    def apply_equalization(self):
        self._apply_filter(self.model.equalize_histogram, "Equalização de histograma aplicada.")

    # --- Métodos de Sistema de Cor ---
    def apply_hsv_h_channel(self):
        self._apply_filter(self.model.convert_to_hsv_h_channel, "Canal H (Matiz) - HSV aplicado.")

    def apply_hsv_s_channel(self):
        self._apply_filter(self.model.convert_to_hsv_s_channel, "Canal S (Saturação) - HSV aplicado.")

    def apply_hsv_v_channel(self):
        self._apply_filter(self.model.convert_to_hsv_v_channel, "Canal V (Valor) - HSV aplicado.")

    def apply_lab_l_channel(self):
        self._apply_filter(self.model.convert_to_lab_l_channel, "Canal L (Luminosidade) - LAB aplicado.")

    def apply_lab_a_channel(self):
        self._apply_filter(self.model.convert_to_lab_a_channel, "Canal A (Normalizado) - LAB aplicado.")

    def apply_lab_b_channel(self):
        self._apply_filter(self.model.convert_to_lab_b_channel, "Canal B (Normalizado) - LAB aplicado.")
            
    # --- Métodos de Limiarização (Threshold) ---

    def on_global_threshold_change(self, *args):
        if self.model.image is None: return 
        
        if not self.is_threshold_slider_active:
            self.view.log_action("Ajustando Limiar Global...")
            self.is_threshold_slider_active = True
        
        threshold_value = self.view.control_panel.threshold_slider.get()
        
        temp_image_cv = self.model.apply_global_threshold(self.model.image, threshold_value)
        
        if temp_image_cv is not None:
            result_tk = self.model.to_tk_image(temp_image_cv)
            if result_tk:
                self.view.display_processed_image(result_tk)
                self.view.update_histogram(self.model.original, temp_image_cv) 

        self.root.after(1000, self.reset_threshold_flag)

    def reset_threshold_flag(self):
        self.is_threshold_slider_active = False

    def apply_otsu_threshold(self):
        self._apply_filter(self.model.apply_otsu_threshold, "Limiarização de Otsu aplicada.")

    def apply_adaptive_threshold(self):
        self._apply_filter(self.model.apply_adaptive_threshold, "Limiarização Adaptativa aplicada.")

    def apply_multi_2(self): self._apply_multi_level(2)
    def apply_multi_4(self): self._apply_multi_level(4)
    def apply_multi_8(self): self._apply_multi_level(8)
    def apply_multi_16(self): self._apply_multi_level(16)
        
    def _apply_multi_level(self, K):
        # Este não pode usar o _apply_filter por causa do argumento K
        if self.model.image is None:
            messagebox.showwarning("Aviso", "Nenhuma imagem carregada.")
            return
            
        result_tk = self.model.apply_multi_level_threshold(K) 
        if result_tk:
            self.view.display_processed_image(result_tk)
            self.view.log_action(f"Limiar Multissegmentado ({K} Tons) aplicado.")
            self.view.update_histogram(self.model.original, self.model.image)
            self.reset_all_sliders()
        else:
            messagebox.showerror("Erro", f"Falha ao aplicar filtro de {K} tons.")

    # --- NOVOS MÉTODOS: Filtros Espaciais ---
    
    def apply_blur(self):
        self._apply_filter(self.model.apply_blur, "Suavização (Blur Gaussiano) aplicada.")
        
    def apply_median_blur(self):
        self._apply_filter(self.model.apply_median_blur, "Suavização (Mediana) aplicada.")
        
    def apply_sharpen(self):
        self._apply_filter(self.model.apply_sharpen, "Aumento de Nitidez (Sharpen) aplicado.")

    # --- Resposta ao Clique no Pixel ---
    
    def on_pixel_selected(self, panel_name, x, y):
        image_to_sample = None
        if panel_name == 'original':
            image_to_sample = self.model.original
        else:
            image_to_sample = self.model.image
            
        if image_to_sample is None:
            self.view.update_pixel_info("Nenhuma imagem carregada.")
            return

        info_string = self.model.get_pixel_color_values(image_to_sample, x, y)
        self.view.update_pixel_info(info_string)
        self.view.log_action(f"Pixel ({x},{y}) no painel '{panel_name}' analisado.")

    # --- NOVOS MÉTODOS: Transformações ---

    def apply_resize_fhd(self):
        self._apply_resize(1920, 1080, "Full HD (1920x1080)")

    def apply_resize_2k(self):
        self._apply_resize(2560, 1440, "2K (2560x1440)")

    def apply_resize_4k(self):
        self._apply_resize(3840, 2160, "4K (3840x2160)")

    def apply_custom_resolution(self):
        if self.model.image is None:
            messagebox.showwarning("Aviso", "Nenhuma imagem carregada.")
            return
            
        result = simpledialog.askstring(
            "Resolução Personalizada", 
            "Insira a resolução (ex: 800x600):",
            parent=self.root
        )
        if result:
            try:
                if 'x' not in result.lower():
                    raise ValueError("Formato inválido. Use 'LarguraxAltura'.")
                width_str, height_str = result.lower().split('x')
                width = int(width_str)
                height = int(height_str)
                if width <= 0 or height <= 0:
                    raise ValueError("Dimensões devem ser positivas.")
                self._apply_resize(width, height, f"Personalizada ({width}x{height})")
            except Exception as e:
                messagebox.showerror("Erro de Entrada", f"Falha ao processar resolução: {e}")

    def _apply_resize(self, w, h, log_message):
        # Este também não usa o _apply_filter por causa dos argumentos
        if self.model.image is None:
            messagebox.showwarning("Aviso", "Nenhuma imagem carregada.")
            return
            
        result_tk = self.model.resize_image(w, h)
        if result_tk:
            self.view.display_processed_image(result_tk)
            self.view.log_action(f"Resolução alterada para: {log_message}.")
            self.view.update_histogram(self.model.original, self.model.image)
            self.reset_all_sliders()
        else:
            messagebox.showerror("Erro", "Falha ao redimensionar.")

    def apply_rotate_90(self):
        self._apply_filter(self.model.rotate_90_cw, "Rotação 90° (Horário) aplicada.")
        
    def apply_flip_h(self):
        self._apply_filter(self.model.flip_horizontal, "Espelhamento Horizontal aplicado.")
        
    def apply_flip_v(self):
        self._apply_filter(self.model.flip_vertical, "Espelhamento Vertical aplicado.")