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