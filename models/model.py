# PDI/models/model.py
import cv2
from PIL import Image, ImageTk
import numpy as np

# Importa as classes de processamento que criámos
from models.color_model import ColorModel
from models.histogram_model import HistogramModel
from models.threshold_model import ThresholdModel

# Model agora herda todas as funções de processamento
class Model(ColorModel, HistogramModel, ThresholdModel):
    
    def __init__(self):
        self.image = None
        self.original = None

    def load_image(self, path):
        self.image = cv2.imread(path)
        self.original = self.image.copy()
        # Retorna a imagem original para ser exibida nos dois painéis
        return self.to_tk_image(self.original) 

    def save_image(self, path):
        # Salva a imagem 'self.image' (a processada)
        if self.image is not None:
            cv2.imwrite(path, self.image)

    def reset_image(self):
        # Restaura a imagem de trabalho para a original
        if self.original is not None:
            self.image = self.original.copy()
            return self.to_tk_image(self.image)
        return None

    # ========== Conversão de Imagem (Utils) ==========
    
    def to_tk_image(self, cv_image):
        """Converte uma imagem OpenCV BGR para formato Tkinter."""
        try:
            rgb = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(rgb)
            return ImageTk.PhotoImage(img)
        except Exception as e:
            print(f"Erro ao converter imagem para TK: {e}")
            return None

    # ========== Operações de PDI ==========
    
    # NOTA: Os métodos convert_to_gray() e equalize_histogram()
    # são herdados automaticamente de color_model.py e histogram_model.py
    # Removemos as versões duplicadas que estavam aqui.