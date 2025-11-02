# PDI/models/utils.py

import cv2
import numpy as np

def calculate_histogram(bgr_image):
    """
    Calcula o histograma para uma imagem (em tons de cinza).
    Esta função é um utilitário que pode ser chamado por qualquer
    componente que precise dos dados do histograma (como o histogram_canvas).
    
    :param bgr_image: Imagem no formato BGR (OpenCV)
    :return: O histograma calculado (array NumPy) ou None
    """
    if bgr_image is None:
        return None
    
    try:
        # Converte para tons de cinza para calcular o histograma
        gray = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2GRAY)
        
        # cv2.calcHist([images], [channels], mask, [histSize], ranges)
        hist = cv2.calcHist(
            [gray],       # Imagem (em uma lista)
            [0],          # Canais (canal 0 de 'gray')
            None,         # Máscara (nenhuma)
            [256],        # Tamanho do Histograma (256 bins)
            [0, 256]      # Intervalo (0 a 255)
        )
        
        # Normaliza o histograma (opcional, mas bom para exibição)
        cv2.normalize(hist, hist, 0, 255, cv2.NORM_MINMAX)
        
        return hist
        
    except Exception as e:
        log_info(f"Erro ao calcular histograma: {e}")
        return None

def log_info(message):
    """
    Função auxiliar para logging de depuração no console.
    Isto é separado do log de ações visível ao usuário no ControlPanel.
    
    :param message: A mensagem a ser impressa.
    """
    print(f"[PDI-Studio-Log] {message}")