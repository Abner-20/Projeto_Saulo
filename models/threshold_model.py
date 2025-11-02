# PDI/models/threshold_model.py

import cv2
import numpy as np

class ThresholdModel:
    """
    Contém os métodos de processamento para limiarização (thresholding).
    """

    def apply_global_threshold(self, base_image, threshold_value):
        """
        Aplica um limiar global (binário) a uma imagem base.
        Esta é uma operação NÃO-DESTRUTIVA (para uso com slider).
        
        :param base_image: A imagem BGR (OpenCV) a ser processada.
        :param threshold_value: O valor (0-255) a ser usado como limiar.
        :return: Imagem binarizada (OpenCV BGR) ou None.
        """
        if base_image is None:
            return None
        
        try:
            val = int(threshold_value)
            
            # 1. Converter a imagem base para tons de cinza
            gray = cv2.cvtColor(base_image, cv2.COLOR_BGR2GRAY)
            
            # 2. Aplicar o limiar (Threshold)
            ret, binary_image = cv2.threshold(gray, val, 255, cv2.THRESH_BINARY)
            
            # 3. Converter de volta para BGR e retornar
            return cv2.cvtColor(binary_image, cv2.COLOR_GRAY2BGR)
            
        except Exception as e:
            print(f"Erro ao aplicar limiar global: {e}")
            return None

    def apply_otsu_threshold(self):
        """
        Aplica a limiarização de Otsu.
        Esta é uma operação DESTRUTIVA (atualiza self.image).
        """
        if self.image is None:
            return None
        
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        ret, binary_image = cv2.threshold(
            gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
        )
        
        self.image = cv2.cvtColor(binary_image, cv2.COLOR_GRAY2BGR)
        return self.to_tk_image(self.image)

    def apply_adaptive_threshold(self):
        """
        Aplica a limiarização adaptativa (Gaussiana).
        Esta é uma operação DESTRUTIVA (atualiza self.image).
        """
        if self.image is None:
            return None
            
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        
        binary_image = cv2.adaptiveThreshold(
            gray,
            255,  # Valor máximo
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,  # Método
            cv2.THRESH_BINARY,  # Tipo
            11,  # Tamanho do bloco (ímpar)
            2    # Constante C
        )
        
        self.image = cv2.cvtColor(binary_image, cv2.COLOR_GRAY2BGR)
        return self.to_tk_image(self.image)
        
    def apply_multi_level_threshold(self, K):
        """
        Aplica limiarização multissegmentada (Quantização).
        Reduz a imagem para K tons de cinza.
        Esta é uma operação DESTRUTIVA (atualiza self.image).
        
        :param K: O número de tons (ex: 2, 4, 8, 16).
        """
        if self.image is None:
            return None
            
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)

        # Criar uma Tabela de Consulta (LUT) para mapear os K níveis
        lut = np.zeros(256, dtype=np.uint8)
        
        # O número de níveis de saída é K-1 (ex: 4 tons = 0, 85, 170, 255)
        levels = K - 1 
        
        # Evitar divisão por zero se K=1
        if levels == 0: 
            levels = 1 
            
        step = 256.0 / K # O tamanho de cada "segmento" de entrada

        for i in range(256):
            # 1. Descobrir a qual segmento 'i' pertence (ex: 0, 1, 2, 3...)
            segment = np.floor(i / step)
            
            # 2. Mapear esse segmento para o valor de saída
            val = (segment / levels) * 255
            
            # 3. Arredondar e salvar na LUT
            lut[i] = np.round(val)
            
        # Aplicar a LUT à imagem em tons de cinza
        quantized_gray = cv2.LUT(gray, lut)
        
        # Converter de volta para BGR e salvar o estado
        self.image = cv2.cvtColor(quantized_gray, cv2.COLOR_GRAY2BGR)
        return self.to_tk_image(self.image)