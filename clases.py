import os
import pydicom
import numpy as np
import matplotlib.pyplot as plt
import cv2
import time


class DICOM:
    def __init__(self):
        self.almacenar = {}

    def cargar_carpeta(self, ruta):
        archivos = [os.path.join(ruta, f)
                 for f in os.listdir(ruta)
                 if f.lower().endswith('.dcm')]
        if not archivos:
            print(f"No encontré DICOMs en {ruta}")
            return None, None

        slices = [pydicom.dcmread(f) for f in archivos]  
        slices.sort(key=lambda s: int(getattr(s, 'InstanceNumber', 0)))
        
        volume = np.stack([s.pixel_array for s in slices], axis=-1)
        header = slices[0]

        self.almacenar[ruta] = {'volume': volume, 'header': header}

        self.mostrar_planos(volume)
        return volume, header
    
    def mostrar_planos(self, volume):
        x0, y0, z0 = np.array(volume.shape) // 2

        fig, axes = plt.subplots(1, 3, figsize=(15, 5))

        cortes = [
            ('Plano transversal', volume[:, :, z0]),
            ('Plano sagital',     volume[:, y0, :]),
            ('Plano coronal',     volume[x0, :, :])
        ]
        
        for ax, (titulo, slc) in zip(axes, cortes):
        
            slc_rot = np.rot90(slc)
            ax.imshow(slc_rot, cmap='gray', aspect='auto')
            ax.set_title(titulo)
            ax.axis('on')

        plt.tight_layout()
        plt.show()


class Paciente:
    def _init_(self, nombre, edad, ID, imagen_asociada):
        self.nombre = nombre
        self.edad = edad
        self.id = ID
        self.imagen = imagen_asociada

    def _str_(self):
        return f"Paciente(nombre={self.nombre}, edad={self.edad}, id={self.id})"

def translacion(imagen, dx, dy):
    h, w = imagen.shape
    M = np.float32([[1, 0, dx], [0, 1, dy]])
    trasladada = cv2.warpAffine(imagen, M, (w, h))
    return trasladada

class gestion_imagen:
    def __init__(self, ruta):
        
        self.imagen = cv2.imread(ruta, 0)
        self.ruta = ruta

    def binarizar(self, metodo, umbral=127):
            tipos = {
                'binario': cv2.THRESH_BINARY,
                'binario_invertido': cv2.THRESH_BINARY_INV,
                'truncado': cv2.THRESH_TRUNC,
                'tozero': cv2.THRESH_TOZERO,
                'tozero_invertido': cv2.THRESH_TOZERO_INV
            }        
    def transformar_morfologia(self, kernel_size):
         kernel = np.ones((kernel_size, kernel_size), np.uint8)
         self.imagen = cv2.morphologyEx(self.imagen, cv2.MORPH_OPEN, kernel)
    def modificar_forma(self, forma, texto, salida):
        color = (0, 0, 0)
        img_color = cv2.cvtColor(self.imagen, cv2.COLOR_GRAY2BGR)
        alto, ancho = self.imagen.shape
        centro_x, centro_y = ancho // 2, alto // 2

        if forma == 'circulo':
            cv2.circle(img_color, (centro_x, centro_y), 60, color, 2)
        else:
            cv2.rectangle(img_color, (centro_x-60, centro_y-30), (centro_x+60, centro_y+30), color, 2)

        cv2.rectangle(img_color, (20, alto - 50), (ancho - 20, alto - 20), (255, 255, 255), -1)

        cv2.putText(img_color, texto, (30, alto - 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
        cv2.imwrite(salida, img_color)
def listar_imagenes_png_jpg(carpeta):
    return [f for f in os.listdir(carpeta) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

                 