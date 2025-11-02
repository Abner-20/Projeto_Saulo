# PDI/views/menu_bar.py
import tkinter as tk

class MenuBar:
    def __init__(self, root, controller):
        self.controller = controller
        self.menubar = tk.Menu(root)

        # --- Menu Arquivo ---
        file_menu = tk.Menu(self.menubar, tearoff=0)
        file_menu.add_command(label="Abrir", command=controller.open_image)
        file_menu.add_command(label="Salvar como...", command=controller.save_image)
        file_menu.add_separator()
        file_menu.add_command(label="Restaurar Original", command=controller.apply_reset)
        file_menu.add_separator()
        file_menu.add_command(label="Sair", command=root.quit)
        self.menubar.add_cascade(label="Arquivo", menu=file_menu)

        # --- Menu Filtros (Consolidado) ---
        filter_menu = tk.Menu(self.menubar, tearoff=0)
        
        # Filtros Principais
        filter_menu.add_command(
            label="Converter para Tons de Cinza (L)", 
            command=controller.apply_gray
        )
        filter_menu.add_command(
            label="Equalizar Histograma (Auto)", 
            command=controller.apply_equalization
        )
        
        filter_menu.add_separator()

        # Sub-menu HSV
        hsv_menu = tk.Menu(filter_menu, tearoff=0)
        hsv_menu.add_command(label="Canal H (Matiz)", command=controller.apply_hsv_h_channel)
        hsv_menu.add_command(label="Canal S (Saturação)", command=controller.apply_hsv_s_channel)
        hsv_menu.add_command(label="Canal V (Valor)", command=controller.apply_hsv_v_channel)
        filter_menu.add_cascade(label="Visualizar Canais HSV", menu=hsv_menu)

        # Sub-menu LAB
        lab_menu = tk.Menu(filter_menu, tearoff=0)
        lab_menu.add_command(label="Canal L (Luminosidade)", command=controller.apply_lab_l_channel)
        lab_menu.add_command(label="Canal A (Normalizado)", command=controller.apply_lab_a_channel)
        lab_menu.add_command(label="Canal B (Normalizado)", command=controller.apply_lab_b_channel)
        filter_menu.add_cascade(label="Visualizar Canais LAB", menu=lab_menu)
        
        filter_menu.add_separator() # Separador
        
        # --- NOVO: Sub-menu Limiarização ---
        thresh_menu = tk.Menu(filter_menu, tearoff=0)
        
        thresh_menu.add_command(
            label="Limiar de Otsu (Auto)", 
            command=controller.apply_otsu_threshold
        )
        thresh_menu.add_command(
            label="Limiar Adaptativo (Gaussiano)", 
            command=controller.apply_adaptive_threshold
        )
        
        # Sub-sub-menu Multissegmentada
        multi_menu = tk.Menu(thresh_menu, tearoff=0)
        multi_menu.add_command(label="2 Tons (Binário)", command=controller.apply_multi_2)
        multi_menu.add_command(label="4 Tons", command=controller.apply_multi_4)
        multi_menu.add_command(label="8 Tons", command=controller.apply_multi_8)
        multi_menu.add_command(label="16 Tons", command=controller.apply_multi_16)
        
        thresh_menu.add_cascade(label="Multissegmentada (Quantizar)", menu=multi_menu)
        
        # Adiciona o menu Limiarização ao menu Filtros
        filter_menu.add_cascade(label="Limiarização (Threshold)", menu=thresh_menu)
        
        # -----------------------------------
        
        # Adiciona o menu Filtros à barra principal
        self.menubar.add_cascade(label="Filtros", menu=filter_menu)