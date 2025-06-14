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
        