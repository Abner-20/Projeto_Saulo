# PDI/models/transform_model.py

import cv2

class TransformModel:
    """
    Contém os métodos de processamento para transformações geométricas.
    """

    def resize_image(self, target_w, target_h):
        """
        Redimensiona a imagem atual para uma largura e altura específicas.
        Esta operação é "destrutiva" (atualiza self.image).
        """
        if self.image is None:
            return None
            
        try:
            w = int(target_w)
            h = int(target_h)
            
            resized_cv = cv2.resize(
                self.image, 
                (w, h), 
                interpolation=cv2.INTER_AREA
            )
            
            self.image = resized_cv
            return self.to_tk_image(self.image)
            
        except Exception as e:
            print(f"Erro ao redimensionar imagem: {e}")
            return None

    # --- NOVOS MÉTODOS ADICIONADOS ---

    def rotate_90_cw(self):
        """
        Rotaciona a imagem 90 graus no sentido horário.
        Esta é uma operação DESTRUTIVA.
        """
        if self.image is None:
            return None
        
        self.image = cv2.rotate(self.image, cv2.ROTATE_90_CLOCKWISE)
        return self.to_tk_image(self.image)

    def flip_horizontal(self):
        """
        Espelha a imagem horizontalmente.
        Esta é uma operação DESTRUTIVA.
        """
        if self.image is None:
            return None
        
        # 1 = flip horizontal, 0 = vertical, -1 = ambos
        self.image = cv2.flip(self.image, 1)
        return self.to_tk_image(self.image)

    def flip_vertical(self):
        """
        Espelha a imagem verticalmente.
        Esta é uma operação DESTRUTIVA.
        """
        if self.image is None:
            return None
        
        # 0 = flip vertical
        self.image = cv2.flip(self.image, 0)
        return self.to_tk_image(self.image)