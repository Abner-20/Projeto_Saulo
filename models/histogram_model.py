# PDI/models/histogram_model.py

import cv2
import numpy as np

class HistogramModel:
    """
    Contém os métodos de processamento para análise e ajuste de histograma.
    """

    def equalize_histogram(self):
        """
        Aplica a equalização de histograma na imagem.
        (self.image é atualizado)
        """
        if self.image is None:
            return None
        
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        equalized = cv2.equalizeHist(gray)
        self.image = cv2.cvtColor(equalized, cv2.COLOR_GRAY2BGR)
        
        return self.to_tk_image(self.image)

    def change_brightness_contrast(self, base_image, brightness, contrast):
        """
        Aplica ajuste de brilho e contraste em uma IMAGEM BASE fornecida.
        
        Esta função é NÃO-DESTRUTIVA: ela não altera self.image ou self.original.
        Ela retorna apenas o resultado temporário do ajuste.
        
        :param base_image: A imagem (OpenCV BGR) a ser modificada.
        :param brightness: Valor de -100 a 100.
        :param contrast: Valor de 1.0 a 3.0.
        :return: A nova imagem (OpenCV BGR) com o ajuste aplicado.
        """
        if base_image is None:
            return None

        try:
            b = int(brightness)
            c = float(contrast)
            
            # Aplica a transformação: g(x) = c*f(x) + b
            # Note: Aplicamos na 'base_image' fornecida, NÃO em 'self.original'
            new_image = cv2.convertScaleAbs(base_image, alpha=c, beta=b)
            
            return new_image
            
        except Exception as e:
            print(f"Erro ao alterar brilho/contraste: {e}")
            return None