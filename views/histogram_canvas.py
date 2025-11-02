# PDI/views/histogram_canvas.py

import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from models.utils import calculate_histogram # Importa o utilitário

class HistogramCanvas:
    """
    Um widget Tkinter para exibir um histograma de imagem usando Matplotlib.
    """
    
    def __init__(self, root):
        """
        Inicializa o componente do canvas do histograma.
        :param root: O widget pai (normalmente um frame).
        """
        
        self.frame = tk.Frame(root, bg="#222")
        
        # Configuração da Figura Matplotlib
        self.fig = plt.figure(figsize=(4, 3), dpi=100, facecolor="#333")
        self.ax = self.fig.add_subplot(111, facecolor="#222")
        
        self.stylize_plot()

        # Incorpora a figura Matplotlib no Canvas Tkinter
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.clear_histogram() # Garante que o gráfico comece limpo

    def stylize_plot(self):
        """Aplica a estilização de cores escuras ao gráfico."""
        self.ax.set_title("Histograma Comparativo", color='white', fontsize=10)
        self.ax.set_ylabel('Frequência', color='white', fontsize=8)
        self.ax.set_xlabel('Intensidade', color='white', fontsize=8)
        
        self.ax.tick_params(axis='x', colors='white')
        self.ax.tick_params(axis='y', colors='white')
        
        for spine in self.ax.spines.values():
            spine.set_edgecolor('white')

    def plot_histogram(self, original_bgr, processed_bgr):
        """
        Calcula e desenha o histograma comparativo para a 
        imagem original e a processada.
        """
        self.ax.clear() # Limpa o gráfico anterior

        # 1. Calcular e desenhar Histograma Original
        hist_original = calculate_histogram(original_bgr)
        if hist_original is not None:
            self.ax.plot(hist_original, color='gray', label='Original')

        # 2. Calcular e desenhar Histograma Processado
        hist_processed = calculate_histogram(processed_bgr)
        if hist_processed is not None:
            self.ax.plot(hist_processed, color='cyan', label='Processado')

        # 3. Re-estilizar e desenhar
        self.stylize_plot()
        self.ax.set_xlim([0, 256]) # Define o limite do eixo X
        
        # Adiciona a legenda
        if hist_original is not None or hist_processed is not None:
            legend = self.ax.legend(facecolor='#333', labelcolor='white', fontsize=8)
            legend.get_frame().set_edgecolor('white')
        
        self.canvas.draw()

    def clear_histogram(self):
        """
        Limpa o gráfico do histograma.
        """
        self.ax.clear()
        self.stylize_plot()
        # Adiciona labels vazios para a legenda aparecer mesmo limpa
        self.ax.plot([], color='gray', label='Original')
        self.ax.plot([], color='cyan', label='Processado')
        legend = self.ax.legend(facecolor='#333', labelcolor='white', fontsize=8)
        legend.get_frame().set_edgecolor('white')
        self.canvas.draw()