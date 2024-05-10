import datetime
import re

fecha_actual = datetime.datetime.today()

menu_principal = {
    'A':'Registro de pacientes',
    'B':'Programación de citas',
    'C':'Realización de citas programadas',
    'D':'Consultas y reportes',
    'X':'Salir del sistema\n'
}

menu_intentar_salir = {
  'A':'Volver a intentar',
  'X':'Salir al menú anterior'
}


# DATOS PRUEBA
# clave paciente : [apellido paterno, apellido materno, nombre, nacimiento]
pacientes = {1:["Patricio", "Muñiz", "Juan", "02/06/2002"], 2:["Patricio", "Muñiz", "José", "02/06/2002"]}

# folio cita : [clave paciente, fecha cita, turno cita (1,2,3)]
citas = {1: [1, "10/02/2024", 2], 2:[1, "11/02/2024", 3], 3:[2, "11/02/2024", 1]}

# folio cita: [clave paciente, hora de llegada, peso kg, estatura cm]
citas_realizadas = {2: [1, "10:30:20", 70.0, 171.0]}


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
  if titulo: 
    print(titulo)
  else:
    print('')
    
  opciones_disponibles = ''
  
  for key, value in opciones.items():
    print(f'[{key}] {value}')
    opciones_disponibles += str(key)
  op = elegir_opcion('Elige una opción\n', opciones_disponibles).upper()
    
  return op

# REGISTRO DE PACIENTES
def registro_pacientes():
  while True:
    clave_paciente = len(pacientes) + 1

    primer_apellido = input('Ingresa el primer apellido\n').title().strip()
    # 1
    if not primer_apellido: # Si es que está vacío
      print("Opción no se puede omitir. Inténtelo de nuevo.")
      continue
    # 2
    if not primer_apellido.replace(' ', '').isalpha(): # ]comprueba que todo sea texto
      print('Error. El ingreso de números no es válido. Intente de nuevo.')
      continue
    
    while True:
      segundo_apellido = input('Ingresa el segundo apellido\n').title().strip()
      # 1
      if not segundo_apellido:
        print("Opción no se puede omitir. Inténtelo de nuevo.")
        continue
      # 2
      if not segundo_apellido.replace(' ', '').isalpha():
        print('Error. El ingreso de números no es válido. Intente de nuevo.')
        continue
      break
      
    while True:
      nombre = input('Ingresa el nombre\n').title().strip()
      # 1
      if not nombre:
        print("Opción no se puede omitir. Inténtelo de nuevo.")
        continue
      # 2
      if not nombre.replace(' ', '').isalpha():
        print('Error. El ingreso de números no es válido. Intente de nuevo.')
        continue
      break
    
    while True:
      _fecha_nacimiento = input('Ingresa la fecha de nacimiento (mm/dd/aaaa)\n')
      #1
      if not _fecha_nacimiento:
        print("Opción no se puede omitir. Inténtelo de nuevo.")
        continue
      # 2
      try:
        fecha_nacimiento = datetime.datetime.strptime(_fecha_nacimiento, '%m/%d/%Y')
      except Exception:
        print('Fecha inválida. Intenta de nuevo.')
        continue
      # 3
      if fecha_nacimiento > fecha_actual:
        print('La fecha de nacimiento no debe ser superior a la fecha actual.')
        continue
      break
    
    # Ingreso de datos
    pacientes[clave_paciente] = [primer_apellido, segundo_apellido, nombre, _fecha_nacimiento]
    
    print('El paciente ha sido registrado con éxito.\n')
    print(pacientes[clave_paciente])   # ****************
    break

# PROGRAMACIÓN DE CITAS
def crear_cita():
  while True:
    folio_cita = len(citas) + 1

    _clave_paciente = input('Ingresa la clave del paciente\n')
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
      print('\nError. El paciente no está registrado en el sistema.')
      
      op_clave_paciente = mostrar_menu(menu_intentar_salir)
      if op_clave_paciente == "A":
        continue
      elif op_clave_paciente == "X":
        break
    
    while True:  
      _fecha_cita = input('Ingresa la fecha de la cita\n')
      # 1
      if not _fecha_cita:
        print("Opción no se puede omitir. Inténtelo de nuevo.")
        continue
      # 2
      try:
        fecha_cita = datetime.datetime.strptime(_fecha_cita, '%m/%d/%Y')
      except Exception:
        print('Fecha inválida. Intenta de nuevo.')
        continue
      # 3
      if fecha_cita < fecha_actual:
        print('La fecha ingresada debe ser posterior a la fecha actual.')
        continue
      # 4
      fecha_actual_mas_60 = fecha_actual + datetime.timedelta(days=60)
      if fecha_cita > fecha_actual_mas_60:
        print('La fecha ingresada no debe ser mayor o igual a 60 días posteriores a la fecha actual.')
        continue
      break

    turno_cita = mostrar_menu({1:'Mañana', 2:'Mediodía', 3:'Tarde'}, '\nTurno de la cita')

    citas[folio_cita] = [clave_paciente, _fecha_cita, turno_cita]

    print(f'La cita {folio_cita} ha sido registrada con éxito.')
    print(citas[folio_cita])   # *******************************

    break


# REALIZACIÓN DE CITAS PROGRAMADASs
def realizar_citas():
  while True:
    # Folio de la cita
    _folio_cita = input("Ingresa el folio de la cita (Número)\n")
    # 1
    if not _folio_cita: # Si está vacío
      print("Opción no se puede omitir. Inténtelo de nuevo.")
      continue
    # 2
    try:
      folio_cita = int(_folio_cita)
    except Exception:
      print("El folio solo puede contener datos numéricos enteros. Intenta de nuevo.\n")
      continue
    # 3
    if folio_cita not in citas:
      print('\nLa cita no ha sido registrada con anterioridad.')
      
      op_folio_cita = mostrar_menu(menu_intentar_salir)
      if op_folio_cita == "A":
        continue
      elif op_folio_cita == "X":
        break
    #4
    if folio_cita in citas_realizadas:
      print('\nLa cita programada ya ha sido realizada.')
      
      op_folio_cita = mostrar_menu(menu_intentar_salir)
      if op_folio_cita == "A":
        continue
      elif op_folio_cita == "X":
        break

    # Clave del paciente
    op_clave_paciente = "A"  # Inicialización importante más adelante
    while True:
      _clave_paciente = input("Ingresa la clave del paciente\n")
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
        
        op_clave_paciente = mostrar_menu(menu_intentar_salir)
        if op_clave_paciente == "A":
          continue
        elif op_clave_paciente == "X":
          break
      # 4 Si la clave del paciente ingresado no coincide con la clave del paciente registrado en la cita
      datos_citas = citas[folio_cita]    # [1, "10/02/2024", 2]
      if clave_paciente != datos_citas[0]:
        print('\nLa clave del paciente ingresado no coincide con la clave del paciente registrado en la cita.')
        
        op_clave_paciente = mostrar_menu(menu_intentar_salir)
        if op_clave_paciente == "A":
          continue
        elif op_clave_paciente == "X":
          break
      break

    if op_clave_paciente == "X":
      break # Retorno al menú principal ****************************************************************************
    
    
    # Hora de llegada del paciente
    hora_llegada = datetime.datetime.now().time()
    hora_llegada = str(hora_llegada)[0:8]

    # Peso del paciente en kg
    while True:
      _peso_kg = input("Ingresa el peso del paciente con 2 decimales.\n")
      # 1
      if not _peso_kg:
        print("Opción no se puede omitir. Inténtelo de nuevo.")
        continue
      # 2
      try:
        peso_kg = float(_peso_kg)
      except Exception:
        print('La estatura debe ser de dato numérico. Intenta de nuevo.')
        continue
      break
    
    # Estatura del paciente en cm
    while True:
      _estatura_cm = input("Ingresa la estatura del paciente con 2 decimales.\n")
      # 1
      if not _estatura_cm:
        print("Opción no se puede omitir. Inténtelo de nuevo.")
        continue
      # 2
      try:
        estatura_cm = float(_estatura_cm)
      except Exception:
        print('La estatura debe ser de dato numérico. Intenta de nuevo.')
        continue
      break
    
    # Ingreso del registro
    citas_realizadas[folio_cita] = [clave_paciente, hora_llegada, peso_kg, estatura_cm]
    
    print(f'''
Se ha realizado la cita correctamente
Folio de la cita: {folio_cita}
Clave del paciente: {clave_paciente}
Hora de llegada: {hora_llegada}
Peso (kg): {peso_kg}
Estatura (cm): {estatura_cm}
          ''')
    break

# CONSULTAS Y REPORTES
def consultas_reportes():
  while True:
    op_citas_pacientes = mostrar_menu({ 'A':'Reporte de citas', 
                                        'B':'Reporte de pacientes', 
                                        'X':'Salir al menú anterior'})
    # REPORTE DE CITAS
    if op_citas_pacientes == 'A':
      menu_periodo_paciente()
    # REPORTES DE PACIENTES
    if op_citas_pacientes == 'B':
      menu_listado_busqueda_clave_apellidos()
    # SALIDA
    if op_citas_pacientes == 'X':
      break


def menu_periodo_paciente():
  while True:
    op_periodo_paciente = mostrar_menu({'A':'Por periodo', 
                                        'B':'Por paciente', 
                                        'X':'Salir al menú anterior'})

    # REPORTE DE CITAS POR PERIODO
    if op_periodo_paciente == 'A':
      while True:
        citas_filtro = {} # Inicialización 

        _fecha_inicial = input('Ingresa la fecha inicial (mm/dd/aaaa)\n')
        # 1
        if not _fecha_inicial:
          print("Opción no se puede omitir. Inténtelo de nuevo.")
          continue
        # 2
        try:
          fecha_inicial = datetime.datetime.strptime(_fecha_inicial, '%m/%d/%Y')
        except Exception:
          print('Fecha inválida. Intenta de nuevo.')
          continue
        
        while True:
          _fecha_final = input('Ingresa la fecha final (mm/dd/aaaa)\n')
          # 1
          if not _fecha_final:
            print("Opción no se puede omitir. Inténtelo de nuevo.")
            continue
          # 2
          try:
            fecha_final = datetime.datetime.strptime(_fecha_final, '%m/%d/%Y')
          except Exception:
            print('Fecha inválida. Intenta de nuevo.')
            continue
          break
        
        if fecha_final < fecha_inicial:  # ******
          print('Error. La fecha final debe ser superior o igual a la fecha inicial.')
          continue
        
        # Conversion string to date de las fechas que están en citas
        for folio, cita in citas.items():
          fecha_cita = datetime.datetime.strptime(cita[1], '%m/%d/%Y')  # [2, "11/02/2024", 1]
          # Filtro
          if fecha_inicial <= fecha_cita <= fecha_final:
            citas_filtro[folio] = cita   # Podría no ser necesario el diccionario de citas filtradas
        # 1
        if not citas_filtro:
          print('Sin citas en ese periodo.')
          op_clave_paciente = mostrar_menu(menu_intentar_salir)
          if op_clave_paciente == "A":
            continue
          elif op_clave_paciente == "X":
            break
        
        print('\n****************************************************')
        print(f'Reporte de citas entre {_fecha_inicial} y {_fecha_final}')
        print('Folio_cita  Clave_paciente   Fecha_cita   Turno')
        for folio, cita in citas_filtro.items():
          clave_paciente, fecha_cita, turno = cita
          print(f'{folio:^11} {clave_paciente:^15} {fecha_cita:^13} {turno:^5}')
        print('****************************************************')

        break

    # REPORTE DE CITAS POR PACIENTE
    if op_periodo_paciente == 'B':
      while True:
        _clave_paciente = input('Ingresa la clave del paciente.\n')
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
          
          op_clave_paciente = mostrar_menu(menu_intentar_salir)
          if op_clave_paciente == "A":
            continue
          elif op_clave_paciente == "X":
            break
                  
        # Impresion de citas posibles
        print('Folio_cita  Clave_paciente  Nombre  1er_Apellido  2do_Apellido  Nacimiento  Hora_llegada  Peso_kg  Estatura_cm') 
        # i = folio
        for i in range(1, len(citas) + 1):
          if i in citas_realizadas:
            clave_paciente_realizadas, hora_llegada, peso_kg, estatura_cm = citas_realizadas[i]
            if clave_paciente == clave_paciente_realizadas: # get para que no muestre error
              print(f'{i}, {clave_paciente_realizadas}, citas_realizadas[i]')
              continue
          
          if clave_paciente == citas.get(i)[0]: # get para que no muestre error
            print(i, citas[i])
        break
      
      # **********************
    
    # SALIDA AL MENÚ ANTERIOR
    if op_periodo_paciente == 'X':
      break


def menu_listado_busqueda_clave_apellidos():
  while True:
    op_listado_busqueda = mostrar_menu({'A':'Listado completo de pacientes', 
                                        'B':'Búsqueda por clave de paciente', 
                                        'C':'Búsqueda por apellidos y nombres',
                                        'X':'Salir al menú anterior'})
          
    # LISTADO COMPLETO DE PACIENTES
    if op_listado_busqueda == 'A':
      print('\n**********************************************************************************')
      print(f'Información de los pacientes registrados')
      print('Clave_paciente  1er_Apellido  2do_Apellido          Nombre         Fecha_nacimiento')
      for clave_paciente, datos in pacientes.items():
          primer_apellido, segundo_apellido, nombre, fecha_nacimiento = datos
          print(f'{clave_paciente:^14} {primer_apellido:^14} {segundo_apellido:^14} {nombre:^20} {fecha_nacimiento:^16}') 
      print('**********************************************************************************')

    # BÚSQUEDA POR CLAVE DE PACIENTE
    if op_listado_busqueda == 'B':
      while True:
        _clave_paciente = input('Ingresa la clave del paciente a buscar\n')
        # 1
        if not _clave_paciente: # Si está vacío
          print("Opción no se puede omitir. Inténtelo de nuevo.")
          continue
        # 2
        try:
          clave_paciente = int(_clave_paciente)
        except Exception:
          print("El folio solo puede contener datos numéricos enteros. Intenta de nuevo.\n")
          continue
        # 3
        if clave_paciente not in pacientes:
          print('\nEl paciente no está registrado.')
          
          op_clave_paciente = mostrar_menu(menu_intentar_salir)
          if op_clave_paciente == "A":
            continue
          elif op_clave_paciente == "X":
            break
        print('\n**********************************************************************************')
        print(f'Información del paciente')
        primer_apellido, segundo_apellido, nombre, fecha_nacimiento = pacientes[clave_paciente]
        print('Clave_paciente  1er_Apellido  2do_Apellido          Nombre         Fecha_nacimiento')
        print(f'{clave_paciente:^14} {primer_apellido:^14} {segundo_apellido:^14} {nombre:^20} {fecha_nacimiento:^16}') 
        print('**********************************************************************************')
        break
      
    # BÚSQUEDA POR APELLIDOS Y NOMBRES
    if op_listado_busqueda == 'C':
      while True: 
        # VALIDACIoNES
        nombre_u = input('Ingresa el nombre\n').title().strip()
        primer_apellido_u = input('Ingresa el apellido paterno\n').title().strip()
        segundo_apellido_u = input('Ingresa el apellido materno\n').title().strip()
        
        for clave_paciente, datos in pacientes.items():
            primer_apellido, segundo_apellido, nombre, fecha_nacimiento = datos
            if primer_apellido_u == primer_apellido and segundo_apellido_u == segundo_apellido and nombre_u == nombre:
              print('\n**********************************************************************************')
              print(f'Información del paciente')
              print('Clave_paciente  1er_Apellido  2do_Apellido          Nombre         Fecha_nacimiento')
              print(f'{clave_paciente:^14} {primer_apellido:^14} {segundo_apellido:^14} {nombre:^20} {fecha_nacimiento:^16}') 
              print('**********************************************************************************')
              break
        else:
          print('Paciente no encontrado.\n')
        break
        
    if op_listado_busqueda == 'X':
      break

# PROGRAMA PRINCIPAL
while True:
  print("\nSistema de gestión de pacientes de un consultorio")
  [print(f'[{key}] {value}') for key, value in menu_principal.items()] # Impresión opciones de menú
  
  op_principal = input("Ingresa la opción deseada\n").upper()
  match op_principal:
    case 'A':
      registro_pacientes()
    case 'B':
      crear_cita()
    case 'C':
      realizar_citas()
    case 'D':
      consultas_reportes()
    case 'X':
      print('¿En verdad deseas salir del sistema?')
      op_salida = mostrar_menu({'A':'Continuar con el sistema', 'X':'Salir'})
      if op_salida == "A":
        continue
      if op_salida == "X":  
        print('Fin del programa.')
        break
    case _:
      print('Opción no reconocida.')
      continue
