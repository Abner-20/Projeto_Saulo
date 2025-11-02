# PDI/controllers/controller.py
from tkinter import Tk, filedialog, messagebox
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
        self.is_threshold_slider_active = False # Flag para o novo slider

    def run(self):
        self.root.mainloop()

    # --- Função Auxiliar de Reset ---
    def reset_all_sliders(self):
        """Função auxiliar para resetar todos os sliders de ajuste."""
        self.view.control_panel.reset_sliders()

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
                self.reset_all_sliders() # Atualizado
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
            self.reset_all_sliders() # Atualizado
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

    # ========== Métodos de Filtro ==========
    
    def apply_gray(self):
        result_tk = self.model.convert_to_gray()
        if result_tk:
            self.view.display_processed_image(result_tk)
            self.view.log_action("Tons de cinza aplicado.")
            self.view.update_histogram(self.model.original, self.model.image)
            self.reset_all_sliders() # Atualizado
        else:
            messagebox.showwarning("Aviso", "Nenhuma imagem carregada.")

    def apply_equalization(self):
        result_tk = self.model.equalize_histogram()
        if result_tk:
            self.view.display_processed_image(result_tk)
            self.view.log_action("Equalização de histograma aplicada.")
            self.view.update_histogram(self.model.original, self.model.image)
            self.reset_all_sliders() # Atualizado
        else:
            messagebox.showwarning("Aviso", "Nenhuma imagem carregada.")

    # --- Métodos de Sistema de Cor ---

    def apply_hsv_h_channel(self):
        result_tk = self.model.convert_to_hsv_h_channel()
        if result_tk:
            self.view.display_processed_image(result_tk)
            self.view.log_action("Canal H (Matiz) - HSV aplicado.")
            self.view.update_histogram(self.model.original, self.model.image)
            self.reset_all_sliders() # Atualizado
        else:
            messagebox.showwarning("Aviso", "Nenhuma imagem carregada.")

    def apply_hsv_s_channel(self):
        result_tk = self.model.convert_to_hsv_s_channel()
        if result_tk:
            self.view.display_processed_image(result_tk)
            self.view.log_action("Canal S (Saturação) - HSV aplicado.")
            self.view.update_histogram(self.model.original, self.model.image)
            self.reset_all_sliders() # Atualizado
        else:
            messagebox.showwarning("Aviso", "Nenhuma imagem carregada.")

    def apply_hsv_v_channel(self):
        result_tk = self.model.convert_to_hsv_v_channel()
        if result_tk:
            self.view.display_processed_image(result_tk)
            self.view.log_action("Canal V (Valor) - HSV aplicado.")
            self.view.update_histogram(self.model.original, self.model.image)
            self.reset_all_sliders() # Atualizado
        else:
            messagebox.showwarning("Aviso", "Nenhuma imagem carregada.")

    def apply_lab_l_channel(self):
        result_tk = self.model.convert_to_lab_l_channel()
        if result_tk:
            self.view.display_processed_image(result_tk)
            self.view.log_action("Canal L (Luminosidade) - LAB aplicado.")
            self.view.update_histogram(self.model.original, self.model.image)
            self.reset_all_sliders() # Atualizado
        else:
            messagebox.showwarning("Aviso", "Nenhuma imagem carregada.")

    def apply_lab_a_channel(self):
        result_tk = self.model.convert_to_lab_a_channel()
        if result_tk:
            self.view.display_processed_image(result_tk)
            self.view.log_action("Canal A (Normalizado) - LAB aplicado.")
            self.view.update_histogram(self.model.original, self.model.image)
            self.reset_all_sliders() # Atualizado
        else:
            messagebox.showwarning("Aviso", "Nenhuma imagem carregada.")

    def apply_lab_b_channel(self):
        result_tk = self.model.convert_to_lab_b_channel()
        if result_tk:
            self.view.display_processed_image(result_tk)
            self.view.log_action("Canal B (Normalizado) - LAB aplicado.")
            self.view.update_histogram(self.model.original, self.model.image)
            self.reset_all_sliders() # Atualizado
        else:
            messagebox.showwarning("Aviso", "Nenhuma imagem carregada.")
            
    # ========== NOVOS MÉTODOS: Limiarização (Threshold) ==========

    def on_global_threshold_change(self, *args):
        """Chamado quando o slider de Limiar Global é movido."""
        if self.model.image is None: return 
        
        if not self.is_threshold_slider_active:
            self.view.log_action("Ajustando Limiar Global...")
            self.is_threshold_slider_active = True
        
        threshold_value = self.view.control_panel.threshold_slider.get()
        
        # Aplica o filtro na imagem base (self.model.image) de forma não-destrutiva
        temp_image_cv = self.model.apply_global_threshold(self.model.image, threshold_value)
        
        if temp_image_cv is not None:
            result_tk = self.model.to_tk_image(temp_image_cv)
            if result_tk:
                self.view.display_processed_image(result_tk)
                # Compara o original com o resultado temporário do slider
                self.view.update_histogram(self.model.original, temp_image_cv) 

        self.root.after(1000, self.reset_threshold_flag)

    def reset_threshold_flag(self):
        self.is_threshold_slider_active = False

    def apply_otsu_threshold(self):
        """Aplica o método Otsu (salva o estado)."""
        result_tk = self.model.apply_otsu_threshold() 
        if result_tk:
            self.view.display_processed_image(result_tk)
            self.view.log_action("Limiarização de Otsu aplicada.")
            self.view.update_histogram(self.model.original, self.model.image)
            self.reset_all_sliders() # Atualizado
        else:
            messagebox.showwarning("Aviso", "Nenhuma imagem carregada.")

    def apply_adaptive_threshold(self):
        """Aplica o método Adaptativo (salva o estado)."""
        result_tk = self.model.apply_adaptive_threshold() 
        if result_tk:
            self.view.display_processed_image(result_tk)
            self.view.log_action("Limiarização Adaptativa aplicada.")
            self.view.update_histogram(self.model.original, self.model.image)
            self.reset_all_sliders() # Atualizado
        else:
            messagebox.showwarning("Aviso", "Nenhuma imagem carregada.")

    def apply_multi_2(self):
        self._apply_multi_level(2)
        
    def apply_multi_4(self):
        self._apply_multi_level(4)
        
    def apply_multi_8(self):
        self._apply_multi_level(8)
        
    def apply_multi_16(self):
        self._apply_multi_level(16)
        
    def _apply_multi_level(self, K):
        """Função auxiliar para os filtros multissegmentados."""
        result_tk = self.model.apply_multi_level_threshold(K) 
        if result_tk:
            self.view.display_processed_image(result_tk)
            self.view.log_action(f"Limiar Multissegmentado ({K} Tons) aplicado.")
            self.view.update_histogram(self.model.original, self.model.image)
            self.reset_all_sliders() # Atualizado
        else:
            messagebox.showwarning("Aviso", "Nenhuma imagem carregada.")

    # ========== Resposta ao Clique no Pixel ==========
    
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