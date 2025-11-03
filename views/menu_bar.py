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
        file_menu.add_command(label="Sair", command=root.quit)
        self.menubar.add_cascade(label="Arquivo", menu=file_menu)

        # --- Menu Transformar (Atualizado) ---
        transform_menu = tk.Menu(self.menubar, tearoff=0)
        
        # Sub-menu Redimensionar
        resize_menu = tk.Menu(transform_menu, tearoff=0)
        resize_menu.add_command(label="Full HD (1920x1080)", command=controller.apply_resize_fhd)
        resize_menu.add_command(label="2K (2560x1440)", command=controller.apply_resize_2k)
        resize_menu.add_command(label="4K (3840x2160)", command=controller.apply_resize_4k)
        resize_menu.add_separator()
        resize_menu.add_command(label="Personalizada...", command=controller.apply_custom_resolution)
        transform_menu.add_cascade(label="Redimensionar", menu=resize_menu)
        
        transform_menu.add_separator()
        
        # Novas Opções de Rotação/Espelhamento
        transform_menu.add_command(label="Rotacionar 90° Horário", command=controller.apply_rotate_90)
        transform_menu.add_command(label="Espelhar Horizontalmente", command=controller.apply_flip_h)
        transform_menu.add_command(label="Espelhar Verticalmente", command=controller.apply_flip_v)
        
        self.menubar.add_cascade(label="Transformar", menu=transform_menu)

        # --- Menu Filtros (Reorganizado) ---
        filter_menu = tk.Menu(self.menubar, tearoff=0)
        
        # Filtros de Histograma
        filter_menu.add_command(
            label="Equalizar Histograma (Auto)", 
            command=controller.apply_equalization
        )
        
        filter_menu.add_separator()
        
        # Sub-menu Filtros Espaciais (NOVO)
        spatial_menu = tk.Menu(filter_menu, tearoff=0)
        spatial_menu.add_command(label="Suavizar (Blur Gaussiano)", command=controller.apply_blur)
        spatial_menu.add_command(label="Suavizar (Mediana)", command=controller.apply_median_blur)
        spatial_menu.add_separator()
        spatial_menu.add_command(label="Aumentar Nitidez (Sharpen)", command=controller.apply_sharpen)
        filter_menu.add_cascade(label="Filtros Espaciais", menu=spatial_menu)
        
        filter_menu.add_separator()

        # Sub-menu Sistemas de Cor
        color_menu = tk.Menu(filter_menu, tearoff=0)
        color_menu.add_command(label="Converter para Tons de Cinza (L)", command=controller.apply_gray)
        color_menu.add_separator()
        
        # Sub-sub-menu HSV
        hsv_menu = tk.Menu(color_menu, tearoff=0)
        hsv_menu.add_command(label="Canal H (Matiz)", command=controller.apply_hsv_h_channel)
        hsv_menu.add_command(label="Canal S (Saturação)", command=controller.apply_hsv_s_channel)
        hsv_menu.add_command(label="Canal V (Valor)", command=controller.apply_hsv_v_channel)
        color_menu.add_cascade(label="Visualizar Canais HSV", menu=hsv_menu)

        # Sub-sub-menu LAB
        lab_menu = tk.Menu(color_menu, tearoff=0)
        lab_menu.add_command(label="Canal L (Luminosidade)", command=controller.apply_lab_l_channel)
        lab_menu.add_command(label="Canal A (Normalizado)", command=controller.apply_lab_a_channel)
        lab_menu.add_command(label="Canal B (Normalizado)", command=controller.apply_lab_b_channel)
        color_menu.add_cascade(label="Visualizar Canais LAB", menu=lab_menu)
        
        filter_menu.add_cascade(label="Sistemas de Cor", menu=color_menu)
        
        filter_menu.add_separator() 
        
        # Sub-menu Limiarização
        thresh_menu = tk.Menu(filter_menu, tearoff=0)
        thresh_menu.add_command(label="Limiar de Otsu (Auto)", command=controller.apply_otsu_threshold)
        thresh_menu.add_command(label="Limiar Adaptativo (Gaussiano)", command=controller.apply_adaptive_threshold)
        
        # Sub-sub-menu Multissegmentada
        multi_menu = tk.Menu(thresh_menu, tearoff=0)
        multi_menu.add_command(label="2 Tons (Binário)", command=controller.apply_multi_2)
        multi_menu.add_command(label="4 Tons", command=controller.apply_multi_4)
        multi_menu.add_command(label="8 Tons", command=controller.apply_multi_8)
        multi_menu.add_command(label="16 Tons", command=controller.apply_multi_16)
        thresh_menu.add_cascade(label="Multissegmentada (Quantizar)", menu=multi_menu)
        
        filter_menu.add_cascade(label="Limiarização (Threshold)", menu=thresh_menu)
        
        self.menubar.add_cascade(label="Filtros", menu=filter_menu)