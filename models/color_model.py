# PDI/models/color_model.py

import cv2
import numpy as np 

class ColorModel:
    """
    Contém os métodos de processamento para conversão de sistemas de cores.
    Esta classe destina-se a ser herdada pela classe Model principal.
    Assume que self.image (uma imagem BGR do OpenCV) e 
    self.to_tk_image (método de conversão) existem.
    """

    def convert_to_gray(self):
        """
        Converte a imagem principal para tons de cinza.
        A imagem self.image é atualizada.
        """
        if self.image is None:
            return None
        
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        self.image = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
        
        return self.to_tk_image(self.image)

    # --- Funções de visualização HSV ---

    def convert_to_hsv_h_channel(self):
        if self.image is None:
            return None
        hsv = cv2.cvtColor(self.image, cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(hsv)
        self.image = cv2.cvtColor(h, cv2.COLOR_GRAY2BGR)
        return self.to_tk_image(self.image)

    def convert_to_hsv_s_channel(self):
        if self.image is None:
            return None
        hsv = cv2.cvtColor(self.image, cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(hsv)
        self.image = cv2.cvtColor(s, cv2.COLOR_GRAY2BGR)
        return self.to_tk_image(self.image)

    def convert_to_hsv_v_channel(self):
        if self.image is None:
            return None
        hsv = cv2.cvtColor(self.image, cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(hsv)
        self.image = cv2.cvtColor(v, cv2.COLOR_GRAY2BGR)
        return self.to_tk_image(self.image)

    # --- Funções de visualização LAB (COM CORREÇÃO) ---

    def convert_to_lab_l_channel(self):
        if self.image is None:
            return None
        lab = cv2.cvtColor(self.image, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        self.image = cv2.cvtColor(l, cv2.COLOR_GRAY2BGR)
        return self.to_tk_image(self.image)

    def convert_to_lab_a_channel(self):
        if self.image is None:
            return None
        lab = cv2.cvtColor(self.image, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        normalized_a = cv2.normalize(a, None, 0, 255, cv2.NORM_MINMAX)
        self.image = cv2.cvtColor(normalized_a, cv2.COLOR_GRAY2BGR)
        return self.to_tk_image(self.image)

    def convert_to_lab_b_channel(self):
        if self.image is None:
            return None
        lab = cv2.cvtColor(self.image, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        normalized_b = cv2.normalize(b, None, 0, 255, cv2.NORM_MINMAX)
        self.image = cv2.cvtColor(normalized_b, cv2.COLOR_GRAY2BGR)
        return self.to_tk_image(self.image)

    # --- MÉTODO CORRIGIDO: Obter dados do Pixel ---
    
    def get_pixel_color_values(self, image_bgr, x, y):
        """
        Extrai os valores BGR, HSV e LAB de um pixel (x, y) específico.
        """
        if image_bgr is None:
            return "N/A"
            
        try:
            # 1. Obter BGR (OpenCV é BGR, não RGB)
            bgr = image_bgr[y, x] # (Linha, Coluna) == (Y, X)
            b, g, r = bgr[0], bgr[1], bgr[2]
            
            # 2. Converter para HSV
            pixel_bgr = np.uint8([[bgr]])
            
            # --- CORREÇÃO AQUI ---
            hsv = cv2.cvtColor(pixel_bgr, cv2.COLOR_BGR2HSV)[0][0]
            # ---------------------
            
            h, s, v = hsv[0], hsv[1], hsv[2]
            
            # 3. Converter para LAB
            
            # --- CORREÇÃO AQUI ---
            lab = cv2.cvtColor(pixel_bgr, cv2.COLOR_BGR2LAB)[0][0]
            # ---------------------
            
            l, a, b_lab = lab[0], lab[1], lab[2]

            # 4. Formatar a String
            info = (
                f"Coord (X, Y): ({x}, {y})\n"
                f"RGB:          ({r}, {g}, {b})\n"
                f"HSV:          ({h}, {s}, {v})\n"
                f"LAB:          ({l}, {a}, {b_lab})"
            )
            return info
            
        except Exception as e:
            print(f"Erro ao obter pixel: {e}")
            return f"Erro ao ler pixel ({x}, {y})"