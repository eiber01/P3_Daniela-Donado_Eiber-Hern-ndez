from clases import *
dic_archivos = {}
pacientes = {} 
medios = {}

def main():
    
    carpeta_imagenes = os.getcwd()
    archivo_dicom = DICOM()
    pacientes = {} 
    medios = {}  
    
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
        
        