import datetime
import re
import csv
import sys
# import threading

fecha_actual = datetime.date.today()

menu_principal = {
    'A':'Registro de pacientes',
    'B':'Citas', 
    'C':'Consultas y reportes',
    'X':'Salir del sistema'
}

################################## DATOS PRUEBA (Comentar/descomentar de quererse así) ########################################

# # clave paciente : [primer apellido, segundo apellido, nombre, nacimiento, sexo]
# pacientes = { 1: ["Patricio", "Muñiz", "Juan", "02/06/2002", 'H'], 
#               2: ["García", "Esquivel", "José", "03/21/2000", 'H']
#               }

# # folio cita : [clave paciente, fecha cita, turno cita (1,2,3)]
# citas = { 1: [1, "01/02/2024", 'Mediodía'], 
#           2: [1, "11/02/2024", 'Tarde'], 
#           3: [2, "11/03/2024", 'Mañana']
#           }

# # folio cita: [clave paciente, hora de llegada, peso kg, estatura cm, presion_arterial, diagnostico, str(edad)]
# citas_realizadas = {2: [1, "10:30:20", 70.0, 171.0, '150/200', 'Diágnostico de prueba 1. Queda algo largo ekis lolololo. Pero bueno, cómo estás, lorem ipsum.', '22'], 
#                     3: [1, "10:30:20", 70.0, 171.0, '150/200', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation', '22']
#                     }

################################################################################################################################

# pacientes = {}
# citas = {}
# citas_realizadas = {}

def elegir_opcion(prompt='Elige la opción deseada',
                  opciones='ABCD'):
  while True:
    opcion = input(prompt)
    opcion = opcion.upper()
    if not opcion:
      print('No se puede omitir opción. Intenta de nuevo.')
      continue
  
    if not bool(re.match(f'^[{opciones}]$', opcion)):
      print('Opción inválida. Intenta de nuevo.')
      continue
    break
  return opcion

def mostrar_menu( opciones:dict,
                  titulo:str=''):
  print(titulo)
  opciones_disponibles = ''
  
  for key, value in opciones.items():
    print(f'[{key}] {value}')
    opciones_disponibles += str(key)
  op = elegir_opcion('Elige una opción\n', opciones_disponibles).upper()
    
  return op

# REGISTRO DE PACIENTES
def registro_pacientes():
  flag_salir = False # Controla si salimos o no del while exterior
  while True:
    # Clave del paciente
    clave_paciente = len(pacientes) + 1
    
    # Primer apellido
    primer_apellido = input('Ingresa el primer apellido. [X]: Cancelar operación\n').title().strip()
    if primer_apellido == 'X':
      break
    # 1
    if not primer_apellido: # si es que está vacío
      print("\nOpción no se puede omitir. Inténtelo de nuevo.")
      continue
    # 2
    if not primer_apellido.replace(' ', '').isalpha(): # comprueba que todo sea texto
      print('\nError. Solo se aceptan caracteres alfabéticos. Intente de nuevo.')
      continue
    
    while True:
      # Segundo apellido
      segundo_apellido = input('Ingresa el segundo apellido. [*]: Cancelar operación\n').title().strip()
      if segundo_apellido == '*':
        flag_salir = True
        break
      # 1
      if not segundo_apellido:
        break
      # 2
      if not segundo_apellido.replace(' ', '').isalpha():
        print('\nError. Solo se aceptan caracteres alfabéticos. Intente de nuevo.')
        continue
      break
    if flag_salir:
      break
      
    while True:
      # Nombre
      nombre = input('Ingresa el nombre. [*]: Cancelar operación\n').title().strip()
      if nombre == '*':
        flag_salir = True
        break
      # 1
      if not nombre:
        print("\nOpción no se puede omitir. Inténtelo de nuevo.")
        continue
      # 2
      if not nombre.replace(' ', '').isalpha():
        print('\nError. Solo se aceptan caracteres alfabéticos. Intente de nuevo.')
        continue
      break
    if flag_salir:
      break
    
    while True:
      # Fecha de nacimiento
      _fecha_nacimiento = input('Ingresa la fecha de nacimiento (mm/dd/aaaa). [*]: Cancelar operación\n').strip()
      if _fecha_nacimiento == '*':
        flag_salir = True
        break
      #1
      if not _fecha_nacimiento:
        print("\nOpción no se puede omitir. Inténtelo de nuevo.")
        continue
      # 2
      try:
        fecha_nacimiento = datetime.datetime.strptime(_fecha_nacimiento, '%m/%d/%Y').date()
      except Exception:
        print('\nFecha inválida. Intenta de nuevo.')
        continue
      # 3
      if fecha_nacimiento >= fecha_actual:
        print('\nLa fecha de nacimiento no puede ser superior o igual a la fecha actual.')
        continue
      break
    if flag_salir:
      break
    
    while True:
      # Sexo
      sexo = input('Ingresa el sexo \n[H] Hombre \n[M] Mujer \n[*] Cancelar operación\n').upper()
      if sexo == '*':
        flag_salir = True
        break
      # 1
      if not sexo:
        op = elegir_opcion('Si se omite el sexo se guardará como "(N)o contestó". ¿Deseas intentarlo de nuevo? S/N\n', 'SN')
        if op == 'S':
          continue
        elif op == 'N':
          sexo = 'N'
          break
      # 2
      if sexo not in ['H', 'M']:
        print('\nOpción inválida. Intenta de nuevo.')
        continue
      break
    if flag_salir:
      break
    
    # Ingreso de datos
    pacientes[clave_paciente] = [primer_apellido, segundo_apellido, nombre, _fecha_nacimiento, sexo]
    
    # print(pacientes[clave_paciente])
    
    print(f'\nEl paciente {clave_paciente} ha sido registrado con éxito.')
    break

def citas_crear_realizar_cancelar():
  while True:
    op_citas_crear_realizar_cancelar = mostrar_menu({ 'A':'Programación de citas', 
                                                      'B':'Realización de citas programadas', 
                                                      'C':'Cancelación de citas', 
                                                      'X':'Volver al menú anterior'})
    # PROGRAMACIÓN DE CITAS
    if op_citas_crear_realizar_cancelar == 'A':
      crear_cita()
    if op_citas_crear_realizar_cancelar == 'B':
      realizar_citas()
    if op_citas_crear_realizar_cancelar == 'C':
      cancelar_cita()
    # SALIDA
    if op_citas_crear_realizar_cancelar == 'X':
      break


# PROGRAMACIÓN DE CITAS
def crear_cita():
  flag_salir = False # Controla si salimos o no del while exterior
  while True:
    # Folio de la cita
    folio_cita = len(citas) + 1
    
    # Clave del paciente
    _clave_paciente = input('Ingresa la clave del paciente [*]: Cancelar operación\n').strip()
    if _clave_paciente.upper() == '*':
      break
    # 1
    if not _clave_paciente:  
      print("\nOpción no se puede omitir. Inténtelo de nuevo.")
      continue
    # 2
    try:
      clave_paciente = int(_clave_paciente)
    except Exception:
      print("\nLa clave solo puede contener datos numéricos enteros. Intenta de nuevo.")
      continue
    # 3
    if clave_paciente not in pacientes:
      print('\nError. El paciente no está registrado en el sistema.')
      continue
    
    while True:  
      # Fecha de la cita
      _fecha_cita = input('Ingresa la fecha de la cita (mm/dd/yyyy) [*]: Cancelar operación\n').strip()
      if _fecha_cita.upper() == '*':
        flag_salir = True
        break
      # 1
      if not _fecha_cita:
        print("\nOpción no se puede omitir. Inténtelo de nuevo.")
        continue
      # 2
      try:
        fecha_cita = datetime.datetime.strptime(_fecha_cita, '%m/%d/%Y').date()
      except Exception:
        print('\nFecha inválida. Intenta de nuevo.')
        continue
      # 3
      if fecha_cita < fecha_actual:
        print('\nLa fecha ingresada debe ser posterior a la fecha actual.')
        continue
      # 4
      fecha_actual_mas_60 = fecha_actual + datetime.timedelta(days=60)
      if fecha_cita > fecha_actual_mas_60:
        print('\nLa fecha ingresada no debe ser mayor o igual a 60 días posteriores a la fecha actual.')
        fecha_distante = datetime.datetime.strftime(fecha_actual_mas_60, '%m/%d/%Y')
        print(f'Fecha más distante para agendar una cita: {fecha_distante}')
        continue
      # 5 No puede caer en domingo
      if fecha_cita.weekday() == 6:
        op_reagendar = elegir_opcion('La cita no se puede agendar en domingo. ¿Deseas agendarla para el sábado anterior inmediato? S/N\n', 'SN')
        if op_reagendar == 'S':
          fecha_cita = fecha_cita - datetime.timedelta(days=1)
          _fecha_cita = datetime.datetime.strftime(fecha_cita, '%m/%d/%Y')
          print(f'La cita ha sido agendada para el sábado {_fecha_cita}\n')
          break
        elif op_reagendar == 'N':
          print('\nDebes agendar la cita en otra fecha.')
          continue    
      break
    
    if flag_salir:
      break
    
    # Turno de la cita
    menu_turno_cita = {'1':'Mañana', '2':'Mediodía', '3':'Tarde', '*':'Cancelar operación'}
    turno_cita = mostrar_menu(menu_turno_cita, '\nTurno de la cita')
    if turno_cita == '*':
        break
    
    # Ingreso de datos
    citas[folio_cita] = [clave_paciente, _fecha_cita, menu_turno_cita[turno_cita]]
    
    # print(citas[folio_cita])
    
    print(f'\nLa cita {folio_cita} ha sido registrada con éxito.')
    break


# REALIZACIÓN DE CITAS PROGRAMADASs
def realizar_citas():
  flag_salir = False # Controla si salimos o no del while exterior
  while True:
    # Folio de la cita
    _folio_cita = input('Ingresa el folio de la cita (Número entero) [*]: Cancelar operación\n').strip()
    if _folio_cita.upper() == '*':
      break
    # 1
    if not _folio_cita: # Si está vacío
      print('\nOpción no se puede omitir. Inténtelo de nuevo.')
      continue
    # 2
    try:
      folio_cita = int(_folio_cita)
    except Exception:
      print('\nEl folio solo puede contener datos numéricos enteros. Intenta de nuevo.')
      continue
    # 3
    if folio_cita not in citas:
      print('\nLa cita no ha sido registrada con anterioridad.')
      continue
    #4
    if folio_cita in citas_realizadas:
      print('\nLa cita programada ya ha sido realizada.')
      continue
    
    # Hora de llegada del paciente
    hora_llegada = datetime.datetime.now().time()
    _hora_llegada = str(hora_llegada)[0:8]

    # Peso del paciente en kg
    while True:
      _peso_kg = input("Ingresa el peso del paciente [*]: Cancelar operación\n").strip()
      if _peso_kg.upper() == '*':
        flag_salir = True
        break
      # 1
      if not _peso_kg:
        print("\nOpción no se puede omitir. Inténtelo de nuevo.")
        continue
      # 2
      try:
        peso_kg = float(_peso_kg)
      except Exception:
        print('\nEl peso debe ser de dato numérico. Intenta de nuevo.')
        continue
      # 3
      if peso_kg <= 0:
        print("\nEl peso no puede ser menor o igual a 0. Inténtelo de nuevo.")
        continue
      break
    if flag_salir:
      break
    
    # Estatura del paciente en cm
    while True:
      _estatura_cm = input("Ingresa la estatura del paciente [*]: Cancelar operación\n").strip()
      if _estatura_cm.upper() == '*':
        flag_salir = True
        break
      # 1
      if not _estatura_cm:
        print("\nOpción no se puede omitir. Inténtelo de nuevo.")
        continue
      # 2
      try:
        estatura_cm = float(_estatura_cm)
      except Exception:
        print('\nLa estatura debe ser de dato numérico. Intenta de nuevo.')
        continue
      # 3
      if estatura_cm <= 0:
        print("\nLa estatura no puede ser menor o igual a 0. Inténtelo de nuevo.")
        continue
      break
    if flag_salir:
      break
    
    # Presion sistólica
    while True:
      _sistolica = input('Ingresa la presión sistólica del paciente [*]: Cancelar operación\n').strip()
      if _sistolica.upper() == '*':
        flag_salir = True
        break
      # 1
      if not _sistolica:
        print("\nOpción no se puede omitir. Inténtelo de nuevo.")
        continue
      # 2
      try:
        sistolica = int(_sistolica)
      except Exception:
        print('\nEl valor debe ser de tipo entero. Intenta de nuevo.')
        continue
      # 3
      if sistolica <= 0:
        print('\nEl valor tiene que ser un número entero positivo. Intenta de nuevo.')
        continue
      # 4
      if len(_sistolica) > 3:
        print('\nSolo puede contener hasta 3 dígitos. Intenta de nuevo.')
        continue
      # 5 Agrega ceros a la izquierda
      _sistolica = _sistolica.rjust(3, '0')
      break
    if flag_salir:
      break
    
    # Presión diastólica
    while True:
      _diastolica = input('Ingresa la presión diastólica del paciente [*]: Cancelar operación\n').strip()
      if _diastolica.upper() == '*':
        flag_salir = True
        break
      # 1
      if not _diastolica:
        print("\nOpción no se puede omitir. Inténtelo de nuevo.")
        continue
      # 2
      try:
        diastolica = int(_diastolica)
      except Exception:
        print('\nEl valor debe ser de tipo entero. Intenta de nuevo.')
        continue
      # 3
      if diastolica <= 0:
        print('\nEl valor tiene que ser un número entero positivo. Intenta de nuevo.')
        continue
      # 4
      if len(_diastolica) > 3:
        print('\nSolo puede contener hasta 3 dígitos. Intenta de nuevo.')
        continue
      # 5 Agrega ceros a la izquierda para cumplir los 3 digitos
      while len(_diastolica) < 3:
        _diastolica = '0' + _diastolica
      break
    if flag_salir:
      break
      
    # Presión arterial
    presion_arterial = f'{_sistolica}/{_diastolica}'
    print(presion_arterial)
      
    # Diagnóstico (200 caracteres max)
    while True:
      diagnostico = input('Diagnóstico (200 caracteres máximo) [*]: Cancelar operación\n').upper()
      if diagnostico.upper() == '*':
        flag_salir = True
        break
      # 1
      if len(diagnostico) > 200:
        print('\nEl diagnóstico excedió los 200 caracteres. Intenta de nuevo.')
        continue
      break
    
    if flag_salir:
      break
    
    # Edad
    clave_paciente = citas[folio_cita][0]
    _fecha_nacimiento = pacientes[clave_paciente][3]
    fecha_nacimiento = datetime.datetime.strptime(_fecha_nacimiento, '%m/%d/%Y').date()
    _fecha_cita = citas[folio_cita][1]
    fecha_cita = datetime.datetime.strptime(_fecha_cita, '%m/%d/%Y').date()
    edad = fecha_cita.year - fecha_nacimiento.year
    
    if (fecha_nacimiento.month, fecha_nacimiento.day) > (fecha_cita.month, fecha_cita.day):
      edad = edad - 1
    
    # Ingreso del registro
    citas_realizadas[folio_cita] = [list(citas.values())[0], _hora_llegada, peso_kg, estatura_cm, presion_arterial, diagnostico, str(edad)]
    
    print(f'\nLa cita {folio_cita} se ha realizado correctamente.')

    break
  
def cancelar_cita():
  while True:
    op_cancelar_fecha_paciente = mostrar_menu({ 'A':'Búsqueda por fecha', 
                                                'B':'Búsqueda por paciente', 
                                                'X':'Volver al menú anterior'})

    # BÚSQUEDA POR FECHA
    if op_cancelar_fecha_paciente == 'A':
      eliminar_por_fecha()
    elif op_cancelar_fecha_paciente == 'B':
      eliminar_pacientes_con_citas_pendientes()
    elif op_cancelar_fecha_paciente == 'X':
      break
    
def eliminar_por_fecha():
    while True:
        fecha_a_buscar = input('Ingresa la fecha a buscar mm/dd/yyyy/. [X]: Volver al menú anterior\n').strip()
        if fecha_a_buscar.upper() == "X":
            break
        if not fecha_a_buscar:
            print("Opción no se puede omitir. Inténtelo de nuevo.")
            continue
        if not citas:
            print("No existen citas registradas todavía.")
            continue
        try:
            fecha_a_buscar = datetime.datetime.strptime(fecha_a_buscar, "%m/%d/%Y").date()
        except Exception:
            print('\nFecha inválida. Intenta de nuevo.')
            continue
        
        citas_en_fecha = []
        for id_cita, datos_cita in citas.items():
            fecha_cita = datetime.datetime.strptime(datos_cita[1], '%m/%d/%Y').date()
            if fecha_cita == fecha_a_buscar:
                if id_cita in citas_realizadas:  # Verificar si la cita ya ha sido realizada
                    continue
                folio_paciente = datos_cita[0]
                turno = datos_cita[2]
                nombre_paciente = pacientes[folio_paciente][2]
                apellido_paterno = pacientes[folio_paciente][0]
                apellido_materno = pacientes[folio_paciente][1]
                citas_en_fecha.append((id_cita, nombre_paciente, apellido_paterno, apellido_materno, turno))

        if not citas_en_fecha:
            print("No hay citas programadas para la fecha ingresada o todas las citas ya han sido realizadas.")
            continue

        print("Citas encontradas para la fecha", fecha_a_buscar.strftime('%m/%d/%Y') + ":")
        for id_cita, nombre_paciente, apellido_paterno, apellido_materno, turno in citas_en_fecha:
            print(f"ID Cita: {id_cita}, Nombre del Paciente: {nombre_paciente} {apellido_paterno} {apellido_materno}, Turno: {turno}")

        id_a_eliminar = input("Ingrese el ID de la cita que desea eliminar o presione Enter para salir: ")
        if id_a_eliminar.isdigit() and int(id_a_eliminar) in [id_cita for id_cita, _, _, _, _ in citas_en_fecha]:
            if int(id_a_eliminar) in citas_realizadas:
                print("Esta cita ya ha sido realizada y no se puede eliminar.")
            else:
                del citas[int(id_a_eliminar)]
                print(f"Se ha eliminado la cita con ID {id_a_eliminar}.")
        else:
            print("No se eliminó ninguna cita.")

def eliminar_pacientes_con_citas_pendientes():
    while True:
        pacientes_con_citas_pendientes = []

        # Obtener la lista de pacientes con citas pendientes
        for folio_paciente, datos_paciente in pacientes.items():
            tiene_cita_pendiente = False
            for id_cita, datos_cita in citas.items():
                if datos_cita[0] == folio_paciente and id_cita not in citas_realizadas:
                    tiene_cita_pendiente = True
                    break
            if tiene_cita_pendiente:
                pacientes_con_citas_pendientes.append((folio_paciente, datos_paciente))

        # Mostrar la lista de pacientes con citas pendientes
        if pacientes_con_citas_pendientes:
            print("Pacientes con citas pendientes:")
            for folio, datos_paciente in pacientes_con_citas_pendientes:
                nombre = datos_paciente[2]
                apellido_paterno = datos_paciente[0]
                apellido_materno = datos_paciente[1]
                print(f"Folio: {folio}, Nombre: {nombre}, Apellido Paterno: {apellido_paterno}, Apellido Materno: {apellido_materno}")
        else:
            print("No hay pacientes con citas pendientes.")

        # Capturar el folio del paciente seleccionado por el usuario
        opcion = input("Ingrese el folio del paciente para eliminarlo o presione 'X' para salir al menú anterior: ").strip().upper()
        
        if opcion == "X":
            print("Regresando al menú anterior...")
            break
        elif not opcion:
            print("No ha ingresado ningún folio.")
            continue

        try:
            folio_seleccionado = int(opcion)
        except ValueError:
            print("Opción inválida. Por favor, ingrese un número de folio válido o 'X' para salir al menú anterior.")
            continue

        # Verificar si el paciente seleccionado tiene una cita pendiente
        for id_cita, datos_cita in citas.items():
            if datos_cita[0] == folio_seleccionado and id_cita not in citas_realizadas:
                print("Cita del paciente seleccionado:")
                print(f"Folio: {folio_seleccionado}, Fecha: {datos_cita[1]}, Turno: {datos_cita[2]}")
                confirmacion = input("¿Está seguro de eliminar esta cita? (s/n): ").strip().lower()
                if confirmacion == "s":
                    del citas[id_cita]
                    print("Cita eliminada correctamente.")
                return

        print("El paciente seleccionado no tiene citas pendientes.")
        
        
        
# CONSULTAS Y REPORTES
def consultas_reportes():
  while True:
    op_citas_pacientes = mostrar_menu({ 'A':'Reporte de citas', 
                                        'B':'Reporte de pacientes', 
                                        'X':'Volver al menú anterior'})
    # REPORTE DE CITAS
    if op_citas_pacientes == 'A':
      # 1
      if not citas:
        print('\nNo existen citas registradas en el sistema.')
        continue
      menu_periodo_paciente()
    if op_citas_pacientes == 'B':
      # 1
      if not pacientes:
        print('\nNo hay pacientes registrados en el sistema.')
        continue
      menu_listado_busqueda_clave_apellidos()
    # SALIDA
    if op_citas_pacientes == 'X':
      break


def menu_periodo_paciente():
  while True:
    op_periodo_paciente = mostrar_menu({'A':'Por periodo', 
                                        'B':'Por paciente', 
                                        'X':'Volver al menú anterior'})

    # REPORTE DE CITAS POR PERIODO
    if op_periodo_paciente == 'A':
      flag_salir = False
      while True:
        # Fecha inicial
        _fecha_inicial = input('Ingresa la fecha inicial (mm/dd/aaaa) [*]: Cancelar operación\n').strip()
        if _fecha_inicial.upper() == '*':
          break
        # 1
        if not _fecha_inicial:
          print("\nOpción no se puede omitir. Inténtelo de nuevo.")
          continue
        # 2
        try:
          fecha_inicial = datetime.datetime.strptime(_fecha_inicial, '%m/%d/%Y').date()
        except Exception:
          print('\nFecha inválida. Intenta de nuevo.')
          continue
        
        while True:
          # Fecha final
          _fecha_final = input('Ingresa la fecha final (mm/dd/aaaa) [*]: Cancelar operación\n').strip()
          if _fecha_final.upper() == '*':
            flag_salir = True
            break
          # 1
          if not _fecha_final:
            print("\nOpción no se puede omitir. Inténtelo de nuevo.")
            continue
          # 2
          try:
            fecha_final = datetime.datetime.strptime(_fecha_final, '%m/%d/%Y').date()
          except Exception:
            print('\nFecha inválida. Intenta de nuevo.')
            continue
          break
        if flag_salir:
          break
        
        # 1
        if fecha_final < fecha_inicial:
          print('\nError. La fecha final debe ser superior o igual a la fecha inicial.')
          continue
        
        cita_encontrada = False
        impresion_unica = True
        for i in range(1, len(citas) + 1):   # i = folio_cita
          # Extracción de datos de citas
          clave_paciente_citas, _fecha_cita, turno_cita = citas[i]
          # Extracción datos de pacientes
          primer_apellido, segundo_apellido, nombre, fecha_nacimiento, sexo = pacientes[clave_paciente_citas]
          # Conversión
          fecha_cita = datetime.datetime.strptime(_fecha_cita, '%m/%d/%Y').date()  # [2, "11/02/2024", 1]
          # Comprueba si existe primero en citas realizadas
          if i in citas_realizadas:
              
            # Extracción datos de citas realizadas
            clave_paciente_realizadas, hora_llegada, peso_kg, estatura_cm, presion_arterial, diagnostico, edad = citas_realizadas[i]
            # Acceder a datos del paciente
            if fecha_inicial <= fecha_cita <= fecha_final:  
              if impresion_unica:
                print('\n************************************************************************************************************')
                print(f'Reporte de citas entre {_fecha_inicial} y {_fecha_final}')
                print('\n************************************************************************************************************')
                print('Clave_paciente  1er_Apellido  2do_Apellido          Nombre         Fecha_nacimiento   Sexo     Folio_cita     Fecha_cita     Turno     Hora_llegada  Peso_kg   Estatura_cm  Presion_arterial  Edad ')
                impresion_unica = False              
              print(f'{clave_paciente_citas:^14} {primer_apellido:^14} {segundo_apellido:^14} {nombre:^20} {fecha_nacimiento:^16}  {sexo:^7}  {i:^15} {_fecha_cita:^13} {turno_cita:^10} {hora_llegada:^14} {peso_kg:^9} {estatura_cm:^12} {presion_arterial:^16}  {edad:^4} ')
              cita_encontrada = True
              continue
            
          if fecha_inicial <= fecha_cita <= fecha_final: # si existe en citas
            if impresion_unica:
              print('\n************************************************************************************************************')
              print(f'Reporte de citas entre {_fecha_inicial} y {_fecha_final}')
              print('\n************************************************************************************************************')
              print('Clave_paciente  1er_Apellido  2do_Apellido          Nombre         Fecha_nacimiento   Sexo     Folio_cita     Fecha_cita     Turno     Hora_llegada  Peso_kg   Estatura_cm  Presion_arterial  Edad ')
              impresion_unica = False
            print(f'{clave_paciente_citas:^14} {primer_apellido:^14} {segundo_apellido:^14} {nombre:^20} {fecha_nacimiento:^16}  {sexo:^7}  {i:^15} {_fecha_cita:^13} {turno_cita:^10} {"-":^14} {"-":^9} {"-":^12} {"-":^16}  {"-":^4} ')
            cita_encontrada = True
            
        if not cita_encontrada:
          print('\nNo existen citas para el periodo especificado.')
          break
        
        break
      
    # REPORTE DE CITAS POR PACIENTE
    if op_periodo_paciente == 'B':
      while True:
        _clave_paciente = input('Ingresa la clave del paciente [*]: Cancelar operación\n').strip()
        if _clave_paciente.upper() == '*':
          break
        # 1
        if not _clave_paciente:  
          print("Opción no se puede omitir. Inténtelo de nuevo.")
          continue
        # 2
        try:
          clave_paciente = int(_clave_paciente)
        except Exception:
          print("La clave solo puede contener datos numéricos enteros. Intenta de nuevo.\n")
          continue
        # 3
        if clave_paciente not in pacientes:
          print('\nEl paciente no está registrado.')
          continue
        
        primer_apellido, segundo_apellido, nombre, fecha_nacimiento, sexo = pacientes[clave_paciente]
        print('\n**********************************************************************************')
        print('Clave_paciente  1er_Apellido  2do_Apellido          Nombre         Fecha_nacimiento   Sexo')
        print(f'{clave_paciente:^14} {primer_apellido:^14} {segundo_apellido:^14} {nombre:^20} {fecha_nacimiento:^16}  {sexo:^7}') 
        print('\n**********************************************************************************')
        
        # Impresion de citas posibles (Vas revisando cita por cita, y si se encuentra con la cita en cita realizada, imprime solo ese registro)
        print('Folio_cita     Fecha_cita     Turno     Hora_llegada  Peso_kg   Estatura_cm  Presion_arterial  Edad ') 
        for i in range(1, len(citas) + 1):   # i = folio_cita
          # Extracción de datos
          clave_paciente_citas, fecha_cita, turno_cita = citas[i]
          # Comprueba si existe primero en citas realizadas
          if i in citas_realizadas:
            clave_paciente_realizadas, hora_llegada, peso_kg, estatura_cm, presion_arterial, diagnostico, edad = citas_realizadas[i]
            if clave_paciente == clave_paciente_realizadas: # si existe en realizadas
              print(f'{i:^11}   {fecha_cita:^13} {turno_cita:^10} {hora_llegada:^14} {peso_kg:^9} {estatura_cm:^12} {presion_arterial:^16}  {edad:^4} ')
              continue
            
          if clave_paciente == clave_paciente_citas: # si existe en citas
            print(f'{i:^11}   {fecha_cita:^13} {turno_cita:^10} {"-":^14} {"-":^9} {"-":^12} {"-":^16}  {"-":^4}')
        break
      
    # VOLVER AL MENÚ ANTERIOR
    if op_periodo_paciente == 'X':
      break


def menu_listado_busqueda_clave_apellidos():
  while True:
    op_listado_busqueda = mostrar_menu({'A':'Listado completo de pacientes', 
                                        'B':'Búsqueda por clave de paciente', 
                                        'C':'Búsqueda por apellidos y nombres',
                                        'X':'Volver al menú anterior'})
          
    # LISTADO COMPLETO DE PACIENTES
    if op_listado_busqueda == 'A':
      # 1
      if not pacientes:
        print('\nNo hay pacientes registrados en el sistema.')
        continue
      
      print('\n********************************************************************************************')
      print(f'Información de los pacientes registrados')
      print('Clave_paciente  1er_Apellido  2do_Apellido          Nombre         Fecha_nacimiento   Sexo')
      for clave_paciente, datos in pacientes.items():
          primer_apellido, segundo_apellido, nombre, fecha_nacimiento, sexo = datos
          print(f'{clave_paciente:^14} {primer_apellido:^14} {segundo_apellido:^14} {nombre:^20} {fecha_nacimiento:^16}  {sexo:^7}') 
      print('********************************************************************************************')

    # BÚSQUEDA POR CLAVE DE PACIENTE
    if op_listado_busqueda == 'B':
      while True:
        _clave_paciente = input('Ingresa la clave del paciente a buscar [*]: Cancelar operación\n').strip()
        if _clave_paciente.upper() == '*':
          break
        # 1
        if not _clave_paciente: # Si está vacío
          print("Opción no se puede omitir. Intenta de nuevo.")
          continue
        # 2
        try:
          clave_paciente = int(_clave_paciente)
        except Exception:
          print("La clave solo puede contener datos numéricos enteros. Intenta de nuevo.\n")
          continue
        # 3
        if clave_paciente not in pacientes:
          print('\nEl paciente no está registrado.')
          break
        
        print('\n***************************************************************************************************************')
        print(f'Información del paciente')
        primer_apellido, segundo_apellido, nombre, fecha_nacimiento, sexo = pacientes[clave_paciente]
        print('Clave_paciente  1er_Apellido  2do_Apellido          Nombre         Fecha_nacimiento   Sexo')
        print(f'{clave_paciente:^14} {primer_apellido:^14} {segundo_apellido:^14} {nombre:^20} {fecha_nacimiento:^16}  {sexo:^7}') 
        print('*****************************************************************************************************************')
        
        # Expediente clínico ------------------------------------------------------------------------------------------------------------------------------------------------------
        op_expediente = elegir_opcion('\n¿Deseas consultar el expediente clínico del paciente? S/N\n', 'SN')
        if op_expediente == 'N':
          break
        
        print('\n******************************************************************************************************************************************')
        print('Folio_cita     Fecha_cita     Turno     Hora_llegada  Peso_kg   Estatura_cm  Presion_arterial   Edad           Diagnóstico         ') 
        # Impresion de citas posibles (Vas revisando cita por cita, y si se encuentra con la cita en cita realizada, imprime solo ese registro)
        for i in range(1, len(citas) + 1):   # i = folio_cita
          # Extracción de datos
          clave_paciente_citas, fecha_cita, turno_cita = citas[i]
          # Comprueba si existe primero en citas realizadas
          if i in citas_realizadas:
            clave_paciente_realizadas, hora_llegada, peso_kg, estatura_cm, presion_arterial, diagnostico, edad = citas_realizadas[i]
            # DIAGNÓSTICO Separa texto en renglones y los añade a una lista
            renglones = [diagnostico[i:i+20] for i in range(0, len(diagnostico), 20)]
            # Hace un parrafo
            parrafo = f'\n{" "*107}'.join(renglones)
            if clave_paciente == clave_paciente_realizadas: # Si la clave ingresada está en citas realizadas
              print(f'{i:^11}   {fecha_cita:^13} {turno_cita:^10} {hora_llegada:^14} {peso_kg:^9} {estatura_cm:^12} {presion_arterial:^16}   {edad:^4}       {parrafo:^22}')
              continue
            
          if clave_paciente == clave_paciente_citas: # Si la clave ingresada está en citas
            print(f'{i:^11}   {fecha_cita:^13} {turno_cita:^10} {"-":^14} {"-":^9} {"-":^12} {"-":^16}   {"-":^4}')
        print('******************************************************************************************************************************************')
    
        break # break para salir de búsqueda por clave
      # ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
      
    # BÚSQUEDA POR APELLIDOS Y NOMBRES
    if op_listado_busqueda == 'C':
      flag_salir = False
      while True: 
        # Nombre
        nombre_u = input('Ingresa el nombre [*]: Cancelar operación\n').title().strip()
        if nombre_u == '*':
          break
        # 1
        if not nombre_u:
          print("\nOpción no se puede omitir. Inténtelo de nuevo.")
          continue
        # 2
        if not nombre_u.replace(' ', '').isalpha():
          print('\nError. Solo se aceptan caracteres alfabéticos. Intente de nuevo.')
          continue
        
        while True:
          # Primer apellido
          primer_apellido_u = input('Ingresa el primer apellido [*]: Cancelar operación\n').title().strip()
          if primer_apellido_u == '*':
            flag_salir = True
            break
          # 1
          if not primer_apellido_u:
            print("\nOpción no se puede omitir. Inténtelo de nuevo.")
            continue
          # 2
          if not primer_apellido_u.replace(' ', '').isalpha():
            print('\nError. Solo se aceptan caracteres alfabéticos. Intente de nuevo.')
            continue
          break
        if flag_salir:
          break
        
        while True:
          # Segundo apellido
          segundo_apellido_u = input('Ingresa el segundo apellido [*]: Cancelar operación\n').title().strip()
          if segundo_apellido_u == '*':
            flag_salir = True
            break
          # 1
          if not segundo_apellido_u:
            break
          # 2
          if not segundo_apellido_u.replace(' ', '').isalpha():
            print('\nError. Solo se aceptan caracteres alfabéticos. Intente de nuevo.')
            continue
          break
        if flag_salir:
          break
        
        encontrado = False
        for clave_paciente, datos in pacientes.items():
            primer_apellido, segundo_apellido, nombre, fecha_nacimiento, sexo = datos
            if primer_apellido_u == primer_apellido and segundo_apellido_u == segundo_apellido and nombre_u == nombre:
              print('\n**********************************************************************************')
              print(f'Información del paciente')
              print('Clave_paciente  1er_Apellido  2do_Apellido          Nombre         Fecha_nacimiento   Sexo')
              print(f'{clave_paciente:^14} {primer_apellido:^14} {segundo_apellido:^14} {nombre:^20} {fecha_nacimiento:^16}  {sexo:^7}') 
              print('**********************************************************************************')
              encontrado = True
              break
        if not encontrado:
          print('\nPaciente no encontrado.')
          break
        
        # Expediente clínico ------------------------------------------------------------------------------------------------------------------------------------------------------
        op_expediente = elegir_opcion('\n¿Deseas consultar el expediente clínico del paciente? S/N\n', 'SN')
        if op_expediente == 'N':
          break
        
        print('\n******************************************************************************************************************************************')
        print('Folio_cita     Fecha_cita     Turno     Hora_llegada  Peso_kg   Estatura_cm  Presion_arterial   Edad           Diagnóstico         ') 
        # Impresion de citas posibles (Vas recorriendo cita por cita, y si se encuentra con la cita en cita realizada, imprime solo ese registro)
        for i in range(1, len(citas) + 1):   # i = folio_cita
          # Extracción de datos
          clave_paciente_citas, fecha_cita, turno_cita = citas[i]
          # Comprueba si existe primero en citas realizadas
          if i in citas_realizadas:
            clave_paciente_realizadas, hora_llegada, peso_kg, estatura_cm, presion_arterial, diagnostico, edad = citas_realizadas[i]
            # DIAGNÓSTICO Separa texto en renglones y los añade a una lista
            renglones = [diagnostico[i:i+20] for i in range(0, len(diagnostico), 20)]
            # Hace un parrafo
            parrafo = f'\n{" "*107}'.join(renglones)
            if clave_paciente == clave_paciente_realizadas: # Si la clave ingresada está en citas realizadas
              print(f'{i:^11}   {fecha_cita:^13} {turno_cita:^10} {hora_llegada:^14} {peso_kg:^9} {estatura_cm:^12} {presion_arterial:^16}   {edad:^4}       {parrafo:^22}')
              continue
            
          if clave_paciente == clave_paciente_citas: # Si la clave ingresada está en citas
            print(f'{i:^11}   {fecha_cita:^13} {turno_cita:^10} {"-":^14} {"-":^9} {"-":^12} {"-":^16}   {"-":^4}')
        print('******************************************************************************************************************************************')

        break # break para salir de búsqueda por nombres y apellidos
      
      # ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # SALIR AL MENÚ ANTERIOR
    if op_listado_busqueda == 'X':
      break

def guardar_csv(diccionario:dict, encabezados, nombre_archivo):
  with open(nombre_archivo, 'w', encoding='latin1', newline='') as archivo:
    grabador = csv.writer(archivo)
    grabador.writerow(encabezados)
    for clave, datos in diccionario.items():
        grabador.writerows([[clave] + [dato for dato in datos]])


def leer_csv(nombre_archivo):
    datos = {}
    try:
      with open(nombre_archivo, 'r', encoding='latin1', newline='') as archivo:
        lector = csv.reader(archivo)
        next(lector)
        for renglon in lector:
          # datos[renglon[0]] = [renglon[i] for i in range(1, len(renglon))]
          datos[int(renglon[0])] = [int(renglon[1]) if renglon[1].isdigit() else dato for dato in renglon[1:]]
    except FileNotFoundError:
        print(f"El archivo {nombre_archivo} no se encontró, se procede a trabajar con un conjunto vacío")
        return dict()
    except csv.Error as fallo_csv:
        print(f"Ocurrió un error al leer el archivo: {fallo_csv}")
    except Exception:
        Excepcion = sys.exc_info()
        print(f"Ocurrió un problema del tipo: {Excepcion[0]}")
        print(f"Mensaje del error: {Excepcion[1]}")
    else:
        return datos

# PROGRAMA PRINCIPAL
# Lecturas
pacientes = leer_csv('pacientes.csv')
if pacientes:
  print('Datos cargados de pacientes.csv ...')

citas = leer_csv('citas.csv')
if citas:
  # threading.Timer(3.0, lambda: print('Datos cargados de citas.csv ...')).start()
  print('Datos cargados de citas.csv ...')

citas_realizadas = leer_csv('citas_realizadas.csv')
if citas_realizadas:
  # threading.Timer(3.0, lambda: print('Datos cargados de citas_realizadas.csv ...')).start()
  print('Datos cargados de citas_realizadas.csv ...')
  
while True:
  op_principal = mostrar_menu(menu_principal, '\nSistema de gestión de pacientes de un consultorio')
  match op_principal:
    case 'A':
      registro_pacientes()
    case 'B':
      citas_crear_realizar_cancelar()
    case 'C':
      consultas_reportes()
    case 'X':
      op_salida = elegir_opcion('¿En verdad deseas salir del sistema? S/N\n', 'SN')
      if op_salida == "S":  
        # Guardados (diccionario, encabezados, nombre_archivo)
        if pacientes:
          guardar_csv(pacientes, ('Clave_paciente', 'Primer_apellido', 'Segundo_apellido', 'Nombre', 'Nacimiento', 'Sexo'), 'pacientes.csv')
        if citas:
          guardar_csv(citas, ('Folio_cita', 'Clave_paciente', 'Fecha_cita', 'Turno'), 'citas.csv')
        if citas_realizadas:
          guardar_csv(citas_realizadas, ('Folio_cita', 'Clave_paciente', 'Hora_llegada', 'Peso (kg)', 'Estatura (cm)', 'Presion_arterial', 'Diagnostico', 'Edad'), 'citas_realizadas.csv')
        
        print('Fin del programa.')
        break
    case _:
      print('Opción no reconocida.')