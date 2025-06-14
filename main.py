from clases import *
dic_archivos = {}
pacientes = {} 
medios = {}

def main():
    
    carpeta_imagenes = os.getcwd()
    archivo_dicom = DICOM()

    while True:
        print("\n=== Menú Principal ===")
        print("a) Procesar carpeta DICOM")
        print("b) Ingresar Paciente")
        print("c) Ver imágenes disponibles y seleccionar")
        print("d) Procesar imagen (binarización + morfología + forma + texto)")
        print("e) Aplicar translación")
        print("f) Salir")
        opc = input("Opción: ").lower()
        
        if opc == 'a':
            carpeta = input("Ruta carpeta DICOM: ")
            vol, hdr = archivo_dicom.cargar_carpeta(carpeta)
            if vol is not None:
                medios[carpeta] = {'type': 'DICOM', 'volume': vol, 'header': hdr}
                print(f"Carpeta DICOM procesada y guardada en medios bajo clave '{carpeta}'")
                
        elif opc == 'b':
            carpeta = input("Carpeta DICOM (procesada) para crear paciente: ")
            prueba = medios.get(carpeta)
            if not prueba or prueba['type'] != 'DICOM':
                print("Esa carpeta aún no se ha procesado en la opción 'a'.")
                continue
            
            hdr    = prueba['header']
            volumen = prueba['volume']

            de_name = hdr.get('PatientName', None)
            nombre = str(de_name) if de_name else 'Anon'

            de_id   = hdr.get('PatientID', None)
            pid     = str(de_id) if de_id else 'N/A'

            de_age  = hdr.get('PatientAge', None)
            edad    = str(de_age) if de_age else 'N/A'

            p = Paciente(nombre, edad, pid, volumen)
            pacientes[pid] = p

            medios[f"paciente_{pid}"] = prueba
            print(f"Paciente creado: {p}")
            
        elif opc == 'c':
            imagenes = listar_imagenes_png_jpg(carpeta_imagenes)

            print("\nImágenes disponibles:")
            for i, img in enumerate(imagenes):
                print(f"{i+1}. {img}")

            try:
                num = int(input("Seleccione una imagen por número: ")) - 1
                if 0 <= num < len(imagenes):
                    ruta = os.path.join(carpeta_imagenes, imagenes[num])
                    clave = input("Nombre clave para guardar esta imagen: ")
                    dic_archivos[clave] = ruta
                    print(f" Imagen '{imagenes[num]}' cargada con clave '{clave}'")
                else:
                    print(" Selección inválida")
            except ValueError:
                print(" Debe ingresar un número")
        
        elif opc == 'd':
            clave = input("Clave de la imagen cargada: ")
            if clave in dic_archivos:
                ruta = dic_archivos[clave]
                imagen_modificar = gestion_imagen(ruta)

                metodos = ['binario', 'binario_invertido', 'truncado', 'tozero', 'tozero_invertido']
                while True:
                    print("Selecciona el método:", ", ".join(metodos))
                    metodo = input("Método: ").strip().lower()
                    if metodo in metodos:
                        break
                    else:
                        print(" Método inválido. Intenta nuevamente.")

                umbral = int(input("Valor de umbral (0-255): "))
                imagen_modificar.binarizar(metodo, umbral)

                kernel = int(input("Tamaño del kernel: "))
                
                imagen_modificar.transformar_morfologia(kernel)

                forma = input("¿Forma a dibujar (circulo/cuadrado)?: ").strip().lower()

                texto = f"Imagen binarizada: {metodo}  Umbral: {umbral}  Kernel: {kernel}"

                salida = f"procesada_{clave}_{int(time.time())}.png"

                imagen_modificar.modificar_forma(forma, texto, salida)
                print(f" Imagen final guardada como: {salida}")
                dic_archivos[f"procesada_{clave}_{int(time.time())}"] = salida
            else:
                print("La clave no existe")
                
        elif opc == 'e':
            carpeta = input("Carpeta DICOM procesada: ")
            prueba = medios.get(carpeta)
            if not prueba or prueba['type'] != 'DICOM':
                print("La carpeta no se ha procesado")
                continue

            vol = prueba['volume']
            corte = vol[:, :, vol.shape[2] // 2]  
            corte_rot = np.rot90(corte)

            print("Opciones de traslación:")
            print("1) (-100, 100)")
            print("2) (-243, 15)")
            print("3) (0, 400)")
            print("4) Ingresar una opción diferente")
            opt = input("Elige una opción (1-4): ")
        
            if opt == '1':
                dx, dy = -100, 100
            elif opt == '2':
                dx, dy = -243, 15
            elif opt == '3':
                dx, dy = 0, 400
            elif opt == '4':
                dx = int(input("Valor de traslación en X: "))
                dy = int(input("Valor de traslación en Y: "))

            trasladada = translacion(corte_rot, dx, dy)

            plt.figure(figsize=(10, 5))
            plt.subplot(1, 2, 1)
            plt.imshow(corte_rot, cmap='gray')
            plt.title("Original")

            plt.subplot(1, 2, 2)
            plt.imshow(trasladada, cmap='gray')
            plt.title(f"Traslación ({dx},{dy})")
            plt.tight_layout()
            plt.show()

            nombre_imagen = f"imagen_trasladada_dx{dx}_dy{dy}.png"
            cv2.imwrite(nombre_imagen, trasladada)
            print(f"Imagen trasladada guardada como: {nombre_imagen}")
            
            
        elif opc == 'f':
            print("Gracias por usar el sistema")
            break
        
        else:
            print("Opción inválida, intente de nuevo.")


if __name__ == '__main__':
    main()
            