# PDI/models/spatial_filter_model.py

import cv2
import numpy as np

class SpatialFilterModel:
    """
    Contém os métodos de processamento para filtros espaciais,
    como Blur (suavização) e Sharpen (nitidez).
    Destina-se a ser herdada pela classe Model principal.
    """

    def apply_blur(self):
        """
        Aplica um filtro de suavização Gaussiano.
        Esta é uma operação DESTRUTIVA (atualiza self.image).
        """
        if self.image is None:
            return None
        
        # (5, 5) é o tamanho do kernel, 0 é o desvio padrão (calcula auto)
        self.image = cv2.GaussianBlur(self.image, (5, 5), 0)
        return self.to_tk_image(self.image)

    def apply_median_blur(self):
        """
        Aplica um filtro de suavização de Mediana (bom para ruído "sal e pimenta").
        Esta é uma operação DESTRUTIVA.
        """
        if self.image is None:
            return None
        
        # O 'ksize' (tamanho do kernel) deve ser um ímpar > 1
        self.image = cv2.medianBlur(self.image, 5)
        return self.to_tk_image(self.image)

    def apply_sharpen(self):
        """
        Aplica um filtro de nitidez (Sharpen).
        Esta é uma operação DESTRUTIVA.
        """
        if self.image is None:
            return None
            
        # Kernel de nitidez padrão (Laplaciano)
        kernel = np.array([
            [0, -1, 0],
            [-1, 5, -1],
            [0, -1, 0]
        ])
        
        # Aplica o kernel à imagem
        self.image = cv2.filter2D(self.image, -1, kernel)
        return self.to_tk_image(self.image)