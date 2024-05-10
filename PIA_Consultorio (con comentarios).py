import datetime
import re
import csv
import sys
import sqlite3
import pandas as pd
from tabulate import tabulate
from datetime import datetime as dd

# Estructura de datos --------------------------------------------------------------------------------------------------------------

# Pacientes (lista de tuplas de cada paciente)
# [(id_paciente, primer_apellido, segundo_apellido, nombre, fecha_nacimiento, sexo)]

# Citas (lista de tuplas de cada cita)
# [(id_cita, id_paciente, fecha_cita, turno_cita, hora_llegada, peso_kg, estatura_cm, presion_arterial, diagnostico)]

# Cita sin realizar
# (id_cita, id_paciente, fecha_cita, turno_cita, NA, NA, NA, NA, NA, NA)

# ----------------------------------------------------------------------------------------------------------------------------------

fecha_actual = datetime.datetime.today()

menu_principal = {
    '1':'Registro de pacientes',
    '2':'Citas', 
    '3':'Consultas y reportes',
    'X':'Salir del sistema'
}

def exportar(nombre, datos):
  op_export = mostrar_menu({'1':'Excel', '2':'CSV', 'X':'No exportar'}, '¿Deseas exportar la información mostrada a un archivo de Excel o CSV?')
  if op_export == '1':
    datos.to_excel(f'{nombre}.xlsx', index=False)
  elif op_export == '1':
    datos.to_csv(f'{nombre}.csv', index=False)

def elegir_opcion(prompt='Elige la opción deseada',
                  opciones='123SNX'):
  while True:
    opcion = input(prompt).upper()
    if not opcion:
      print('No se puede omitir opción. Intenta de nuevo.')
      continue
  
    if not bool(re.match(f'^[{opciones}]$', opcion)):
      print('Opción inválida. Intenta de nuevo.')
      continue
    break
  return opcion

def mostrar_menu(opciones:dict,
                  titulo:str='',
                  instruccion:str='Elige una opción\n'):
  print(titulo)
  opciones_disponibles = ''
  
  for key, value in opciones.items():
    print(f'[{key}] {value}')
    opciones_disponibles += str(key)
  op = elegir_opcion(instruccion, opciones_disponibles).upper()
    
  return op

def validar_nombre(prompt, 
                    omision = False):
  while True: 
    nombre = input(prompt).title().strip()
    if nombre == '*':
        return nombre

    elif not nombre and omision == True:
        nombre = ''
        break 

    elif not nombre: # si es que está vacío
      print("\nEste campo no se puede omitir. Inténtelo de nuevo o utilice [*]: Cancelar operación")
      continue 

    elif not nombre.replace(' ', '').isalpha(): # comprueba que todo sea texto
      print('\nSolo se aceptan caracteres alfabéticos. Inténtelo de nuevo o utilice [*]: Cancelar operación')
      continue

    else: 
      return nombre

def registro_pacientes():
  while True:
    # Primer apellido
    primer_apellido = validar_nombre('Ingresa el primer apellido \n')
    if primer_apellido == '*':
      return 
    segundo_apellido = validar_nombre('Ingresa el segundo apellido \n', True)
    if segundo_apellido == '*':
      return
    nombre = validar_nombre('Ingresa el nombre \n') 
    if nombre == '*':
      return
    
    while True:
      # Fecha de nacimiento
      _fecha_nacimiento = input('Ingresa la fecha de nacimiento (mm/dd/aaaa)\n').strip()
      if _fecha_nacimiento == '*':
        return
      #1
      if not _fecha_nacimiento:
        print("\nLa fecha de nacimiento no se puede omitir. Inténtelo de nuevo o utilice [*]: Cancelar operación")
        continue
      # 2
      try:
        fecha_nacimiento = datetime.datetime.strptime(_fecha_nacimiento, '%m/%d/%Y')
      except Exception:
        print('\nFecha inválida, revise que se esté utilizando el formato adecuado. Inténtelo de nuevo o utilice [*]: Cancelar operación')
        continue
      # 3
      if fecha_nacimiento >= fecha_actual.replace(hour=0, minute=0, second=0, microsecond=0):
        print('\nLa fecha de nacimiento no puede ser superior o igual a la fecha actual. Inténtelo de nuevo o utilice [*]: Cancelar operación')
        continue
      break
    
    while True:
      # Sexo
      sexo = input('Ingresa el sexo \n[H] Hombre \n[M] Mujer\n').upper().strip()
      if sexo == '*':
        return
        
      if not sexo:
        op = elegir_opcion('Si se omite el sexo se guardará como "(N)o contestó". ¿Deseas intentarlo de nuevo? S/N\n', 'SN')
        if op == 'S':
          continue
        elif op == 'N':
          sexo = 'N'
          break
      # 1
      if not sexo.isalpha():
        print('\nSolo ingresar caracteres alfabéticos. Inténtelo de nuevo o utilice [*]: Cancelar operación')
        continue
      # 2
      if sexo not in ['H', 'M']:
        print('\nOpción inválida, sólo se aceptan los caracteres H o M. Inténtelo de nuevo o utilice [*]: Cancelar operación')
        continue
      break
    
    paciente = (primer_apellido, segundo_apellido, nombre, fecha_nacimiento, sexo)  # REVISAR TIPO FECHA DATO
    
    # Ingreso de datos a base de datos
    try:
      with sqlite3.connect('Consultorio.db') as conn:
        cursor = conn.cursor()
          
        # Creación de tabla Pacientes
        cursor.execute('CREATE TABLE IF NOT EXISTS Pacientes (\
          id_paciente INTEGER PRIMARY KEY, \
          primer_apellido TEXT NOT NULL, \
          segundo_apellido TEXT, \
          nombre TEXT NOT NULL, \
          fecha_nacimiento TIMESTAMP NOT NULL, \
          sexo TEXT NOT NULL);')
        # Ingreso de datos
        cursor.execute('INSERT INTO Pacientes (primer_apellido, segundo_apellido, nombre, fecha_nacimiento, sexo) \
                        VALUES(?,?,?,?,?)', paciente)
        print(f'La clave asignada al paciente fue {cursor.lastrowid}')
    except sqlite3.Error as e:
      print(e)
    except:
        print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
    finally:
        if (conn):
            conn.close()    
    break

def citas_crear_realizar_cancelar_menu():
  while True:
    op_citas_crear_realizar_cancelar = mostrar_menu({ '1':'Programación de citas', 
                                                      '2':'Realización de citas programadas', 
                                                      '3':'Cancelación de citas', 
                                                      'X':'Volver al menú anterior'})
    
    try:
      with sqlite3.connect('Consultorio.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Citas')
        citas = cursor.fetchall()
    except sqlite3.Error as e:
      print(e)
    except:
        print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
    finally:
        if (conn):
            conn.close()
    
    
    # PROGRAMACIÓN DE CITAS
    if op_citas_crear_realizar_cancelar == '1':
      crear_cita()
    if op_citas_crear_realizar_cancelar == '2':
      if not citas:
        print('\nDebe haber al menos una cita programada para poder realizarla.')
        continue
      realizar_citas()
    if op_citas_crear_realizar_cancelar == '3':
      if not citas:
        print('\nDebe haber al menos una cita creada para poder cancelarla.')
        continue
      cancelar_cita_menu()
    # SALIDA
    if op_citas_crear_realizar_cancelar == 'X':
      break

def crear_cita():
  # Clave del paciente
  while True:
    try:
      with sqlite3.connect('Consultorio.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT id_paciente, primer_apellido, segundo_apellido, nombre \
                        FROM Pacientes \
                        ORDER BY primer_apellido, segundo_apellido, nombre ASC')
        pacientes = cursor.fetchall() # Retorna None si está vacío
    except sqlite3.Error as e:
      print(e)
    except:
        print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
    finally:
        if (conn):
            conn.close()

    datos_paciente = []

    for clave_paciente, primer_apellido, segundo_apellido, nombre in pacientes: 
      clave_paciente = int(clave_paciente)
      primer_apellido = str(primer_apellido)
      segundo_apellido = str(segundo_apellido)
      if segundo_apellido == 'None':
        segundo_apellido = " "
      nombre = str(nombre)

      datos_paciente.append([clave_paciente, primer_apellido, segundo_apellido, nombre])

    if pacientes:
      encabezados = ['Clave paciente', 'Primer Apellido', 'Segundo Apellido', 'Nombre']
      print(tabulate(datos_paciente, headers=encabezados, tablefmt='rounded_grid', rowalign='center'))
    _clave_paciente = input('Ingresa la clave del paciente\n').strip()
    if _clave_paciente.upper() == '*':
      break
    # 1
    if not _clave_paciente:  
      print("\nLa clave no se puede omitir. Inténtelo de nuevo o utilice [*]: Cancelar operación")
      continue
    # 2
    try:
      clave_paciente = int(_clave_paciente)
    except Exception:
      print("\nLa clave solo puede contener datos numéricos enteros. Inténtelo de nuevo o utilice [*]: Cancelar operación")
      continue
    # 3.1
    try:
      with sqlite3.connect('Consultorio.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT id_paciente FROM Pacientes WHERE id_paciente = ?', (clave_paciente,))
        id_paciente_encontrado = cursor.fetchone() # Retorna None si está vacío
    except sqlite3.Error as e:
      print(e)
    except:
        print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
    finally:
        if (conn):
            conn.close()
    # 3.2
    if id_paciente_encontrado == None:
      print('\nError. El paciente no está registrado en el sistema. Inténtelo de nuevo o utilice [*]: Cancelar operación')
      continue
    
    # Fecha de la cita
    while True:  
      fecha_actual_mas_60 = fecha_actual + datetime.timedelta(days=60)
      fecha_distante = datetime.datetime.strftime(fecha_actual_mas_60, '%m/%d/%Y')
      print(f'Fecha más distante para agendar una cita: {fecha_distante}')

      _fecha_cita = input('Ingresa la fecha de la cita (mm/dd/yyyy)\n').strip()
      if _fecha_cita.upper() == '*':
        return
      # 1
      if not _fecha_cita:
        print("\nLa fecha no se puede omitir. Inténtelo de nuevo o utilice [*]: Cancelar operación")
        continue
      # 2
      try:
        fecha_cita = datetime.datetime.strptime(_fecha_cita, '%m/%d/%Y')
      except Exception:
        print('\nFecha inválida. Inténtelo de nuevo o utilice [*]: Cancelar operación')
        continue
      # 3
      if fecha_cita < fecha_actual:
        print('\nLa fecha ingresada debe ser posterior a la fecha actual. Inténtelo de nuevo o utilice [*]: Cancelar operación')
        continue
      # 4
      
      if fecha_cita > fecha_actual_mas_60:
        print('\nLa fecha ingresada no debe ser mayor o igual a 60 días posteriores a la fecha actual. Inténtelo de nuevo o utilice [*]: Cancelar operación')
        print(f'Fecha más distante para agendar una cita: {fecha_distante}')
        continue
      # 5 No puede caer en domingo
      if fecha_cita.weekday() == 6:
        op_reagendar = elegir_opcion('La cita no se puede agendar en domingo. ¿Deseas agendarla para el sábado anterior inmediato? S/N\n', 'SN')
        if op_reagendar == 'S':
          fecha_cita = fecha_cita - datetime.timedelta(days=1)
          _fecha_cita = datetime.datetime.strftime(fecha_cita, '%m/%d/%Y')
          print(f'La cita será agendada para el sábado {_fecha_cita}\n')
          break
        elif op_reagendar == 'N':
          print('\nDebes agendar la cita en otra fecha. Inténtelo de nuevo o utilice [*]: Cancelar operación')
          continue    
      break
    
    # Turno de la cita
    while True:
      print('\nTurnos disponibles')
      menu_turno_cita = {'1':'Mañana', '2':'Mediodía', '3':'Tarde'}
      [print(f'[{num}] {turno}') for num, turno in menu_turno_cita.items()]
      _turno_cita = input('Ingresa el turno de la cita\n').strip()
      if _turno_cita == '*':
        return
      # 1
      if not _turno_cita:
        print("\nEl turno no se puede omitir. Inténtelo de nuevo o utilice [*]: Cancelar operación")
        continue
      # 2
      try:
        turno_cita = int(_turno_cita)
      except Exception:
        print("\nEl turno solo puede contener datos numéricos enteros. Inténtelo de nuevo o utilice [*]: Cancelar operación")
        continue

      if turno_cita == 1:
        _turno_cita = 'Mañana'
      elif turno_cita == 2:
        _turno_cita = 'Mediodía'
      elif turno_cita == 3:
        _turno_cita = 'Tarde'
      else:
        print("\nEl turno solo puede ser 1: Mañana, 2: Mediodía, 3: Tarde. Inténtelo de nuevo o utilice [*]: Cancelar operación")
        continue
      break
    
    # Ingreso de datos # folio de cita: clave_paciente,...
    cita = (clave_paciente, fecha_cita, _turno_cita, 'NA', 'NA', 'NA', 'NA', 'NA')
    
    try:
      with sqlite3.connect('Consultorio.db') as conn:
        cursor = conn.cursor()
        
        cursor.execute('CREATE TABLE IF NOT EXISTS Citas (\
          id_cita INTEGER PRIMARY KEY, \
          id_paciente INTEGER NOT NULL, \
          fecha_cita TIMESTAMP NOT NULL, \
          turno_cita TEXT NOT NULL, \
          hora_llegada TEXT NOT NULL, \
          peso_kg TEXT NOT NULL, \
          estatura_cm TEXT NOT NULL, \
          presion_arterial TEXT NOT NULL, \
          diagnostico TEXT NOT NULL, \
          FOREIGN KEY(id_paciente) REFERENCES Pacientes(id_paciente));')
        
        cursor.execute('INSERT INTO Citas (id_paciente, fecha_cita, turno_cita, hora_llegada, peso_kg, estatura_cm, presion_arterial, diagnostico) \
                        VALUES(?,?,?,?,?,?,?,?)', cita)
        print(f'El folio de la cita asignada fue {cursor.lastrowid}')

    except sqlite3.Error as e:
      print(e)
    except:
        print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
    finally:
        if (conn):
            conn.close()
    break

def realizar_citas():
  # Folio de la cita
  while True:
    _folio_cita = input('Ingresa el folio de la cita (Número entero)\n').strip()
    if _folio_cita.upper() == '*':
      break
    # 1
    if not _folio_cita: # Si está vacío
      print('\nEl folio de la cita no se puede omitir. Inténtelo de nuevo o utilice [*]: Cancelar operación')
      continue
    # 2
    try:
      folio_cita = int(_folio_cita)
    except Exception:
      print('\nEl folio solo puede contener datos numéricos enteros. Inténtelo de nuevo o utilice [*]: Cancelar operación')
      continue
    # 3.1
    try:
      with sqlite3.connect('Consultorio.db') as conn:
        conn.execute("PRAGMA foreign_keys=1")
        cursor = conn.cursor()
        # Obtención de cita buscada
        cursor.execute('SELECT * FROM Citas WHERE id_cita = ?', (folio_cita,))
        cita_buscada = cursor.fetchone()
        # Obtención todas las citas
        cursor.execute('SELECT * FROM Citas')
        # citas_lista = cursor.fetchall()
    except sqlite3.Error as e:
      print(e)
    except:
        print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
    finally:
        if (conn):
            conn.close()
    # 3.2
    if cita_buscada == None:
      print('\nLa cita no ha sido registrada con anterioridad. Inténtelo de nuevo o utilice [*]: Cancelar operación')
      continue
    # 4
    if cita_buscada[5] != 'NA':
      print('\nLa cita programada ya ha sido realizada. Inténtelo de nuevo o utilice [*]: Cancelar operación')
      continue
    
    # Clave del paciente
    clave_paciente = cita_buscada[1]
    
    # Hora de llegada del paciente
    hora_llegada = datetime.datetime.now().time()
    _hora_llegada = str(hora_llegada)[0:8]

    # Peso del paciente en kg
    while True:
      _peso_kg = input("Ingresa el peso del paciente\n").strip()
      if _peso_kg.upper() == '*':
        return
      # 1
      if not _peso_kg:
        print("\nEl peso no se puede omitir. Inténtelo de nuevo o utilice [*]: Cancelar operación")
        continue
      # 2
      try:
        peso_kg = float(_peso_kg)
      except Exception:
        print('\nEl peso debe ser de dato numérico. Inténtelo de nuevo o utilice [*]: Cancelar operación')
        continue
      # 3
      if peso_kg <= 0:
        print("\nEl peso no puede ser menor o igual a 0. Inténtelo de nuevo o utilice [*]: Cancelar operación")
        continue
      break
    
    # Estatura del paciente en cm
    while True:
      _estatura_cm = input("Ingresa la estatura del paciente\n").strip()
      if _estatura_cm.upper() == '*':
        return
      # 1
      if not _estatura_cm:
        print("\nLa estatura no se puede omitir. Inténtelo de nuevo o utilice [*]: Cancelar operación")
        continue
      # 2
      try:
        estatura_cm = float(_estatura_cm)
      except Exception:
        print('\nLa estatura debe ser de dato numérico. Inténtelo de nuevo o utilice [*]: Cancelar operación')
        continue
      # 3
      if estatura_cm <= 0:
        print("\nLa estatura no puede ser menor o igual a 0. Inténtelo de nuevo o utilice [*]: Cancelar operación")
        continue
      break
    
    # Presion sistólica
    while True:
      _sistolica = input('Ingresa la presión sistólica del paciente\n').strip()
      if _sistolica.upper() == '*':
        return
      # 1
      if not _sistolica:
        print("\nEl valor de presión no se puede omitir. Inténtelo de nuevo o utilice [*]: Cancelar operación")
        continue
      # 2
      try:
        sistolica = int(_sistolica)
      except Exception:
        print('\nEl valor debe ser de tipo entero. Inténtelo de nuevo o utilice [*]: Cancelar operación')
        continue
      # 3
      if sistolica <= 0:
        print('\nEl valor tiene que ser un número entero positivo. Inténtelo de nuevo o utilice [*]: Cancelar operación')
        continue
      # 4
      if len(_sistolica) > 3:
        print('\nSolo puede contener hasta 3 dígitos. Inténtelo de nuevo o utilice [*]: Cancelar operación')
        continue
      
      # Añadido de ceros a la izquierda
      _sistolica = _sistolica.rjust(3, '0')
      break
    
    # Presión diastólica
    while True:
      _diastolica = input('Ingresa la presión diastólica del paciente\n').strip()
      if _diastolica.upper() == '*':
        return
      # 1
      if not _diastolica:
        print("\nEl valor de presión no se puede omitir. Inténtelo de nuevo o utilice [*]: Cancelar operación")
        continue
      # 2
      try:
        diastolica = int(_diastolica)
      except Exception:
        print('\nEl valor debe ser de tipo entero. Inténtelo de nuevo o utilice [*]: Cancelar operación')
        continue
      # 3
      if diastolica <= 0:
        print('\nEl valor tiene que ser un número entero positivo. Inténtelo de nuevo o utilice [*]: Cancelar operación')
        continue
      # 4
      if len(_diastolica) > 3:
        print('\nSolo puede contener hasta 3 dígitos. Inténtelo de nuevo o utilice [*]: Cancelar operación')
        continue
      
      # Añadido de ceros a la izquierda
      while len(_diastolica) < 3:
        _diastolica = '0' + _diastolica
      break
      
    # Presión arterial
    presion_arterial = f'{_sistolica}/{_diastolica}'
      
    # Diagnóstico (200 caracteres máximo)
    while True:
      diagnostico = input('Diagnóstico (200 caracteres máximo)\n').title().strip()
      if diagnostico == '*':
        return
      # 1
      if not diagnostico:
        print("\nOpción no se puede omitir. Inténtelo de nuevo o utilice [*]: Cancelar operación")
        continue
      # 2
      if len(diagnostico) > 200:
        print('\nEl diagnóstico excedió los 200 caracteres. Inténtelo de nuevo o utilice [*]: Cancelar operación')
        continue
      break
    
    # 1.1
    try:
      with sqlite3.connect('Consultorio.db',
                            detect_types = sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES) as conn:
        cursor = conn.cursor()
        # Obtención datos de fechas
        # Fecha nacimiento
        cursor.execute('SELECT fecha_nacimiento FROM Pacientes WHERE id_paciente = (?);', (clave_paciente,))
        fecha_nacimiento_tupla = cursor.fetchone()
        fecha_nacimiento = fecha_nacimiento_tupla[0] 
        
        # Fecha cita
        cursor.execute('SELECT fecha_cita FROM Citas WHERE id_cita = (?);', (folio_cita,))
        fecha_cita_tupla = cursor.fetchone()
        fecha_cita = fecha_cita_tupla[0]
        
    except sqlite3.Error as e:
      print(e)
    except:
        print(cursor.description)
        print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
    finally:
        if (conn):
            conn.close()
    
    # Ingreso del registro {folio_cita: [id_paciente, hora_llegada,...., no confundirse con clave_paciente]
    cita_realizada = (_hora_llegada, peso_kg, estatura_cm, presion_arterial, diagnostico, folio_cita)
    
    # Actualización de datos a base de datos
    try:
      with sqlite3.connect('Consultorio.db') as conn:
        conn.execute("PRAGMA foreign_keys=1")
        cursor = conn.cursor()
        
        # Creación de tabla Citas
        cursor.execute('CREATE TABLE IF NOT EXISTS Citas (\
          id_cita INTEGER PRIMARY KEY, \
          id_paciente INTEGER NOT NULL, \
          fecha_cita TIMESTAMP NOT NULL, \
          turno_cita TEXT NOT NULL, \
          hora_llegada TEXT NOT NULL, \
          peso_kg REAL NOT NULL, \
          estatura_cm REAL NOT NULL, \
          presion_arterial TEXT NOT NULL, \
          diagnostico TEXT NOT NULL, \
          FOREIGN KEY(id_paciente) REFERENCES Pacientes(id_paciente));')
        # Actualización
        cursor.execute('UPDATE Citas\
                        SET hora_llegada = ?, peso_kg = ?, estatura_cm = ?, presion_arterial = ?, diagnostico = ?\
                        WHERE id_cita = ?', cita_realizada)
        print(f'La cita realizada fue la cita {folio_cita}')
    except sqlite3.Error as e:
      print(e)
    except:
        print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
    finally:
        if (conn):
            conn.close()
            
    break


def cancelar_cita_menu():
  while True:
    op_cancelar_fecha_paciente = mostrar_menu({ '1':'Búsqueda por fecha', 
                                                '2':'Búsqueda por paciente', 
                                                'X':'Volver al menú anterior'})
    # Extracción de las citas
    try:
      with sqlite3.connect('Consultorio.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Citas WHERE peso_kg = 'NA';")
        citas = cursor.fetchall()
    except sqlite3.Error as e:
      print(e)
    except:
        print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
    finally:
        if (conn):
            conn.close()

    # BÚSQUEDA POR FECHA
    if op_cancelar_fecha_paciente == '1':
      if not citas:
        print('\nDebe haber al menos una cita creada para poder cancelarla.')
        continue
      eliminar_por_fecha()
    # BÚSQUEDA POR PACIENTE
    elif op_cancelar_fecha_paciente == '2':
      if not citas:
        print('\nDebe haber al menos una cita creada para poder cancelarla.')
        continue
      cancelacion_por_paciente()
    elif op_cancelar_fecha_paciente == 'X':
      break
    
# BÚSQUEDA POR FECHA
def eliminar_por_fecha():
    while True:
      # Fecha cita
      fecha_a_buscar = input('Ingresa la fecha a buscar (mm/dd/yyyy)\n').strip()
      if fecha_a_buscar.upper() == "*":
          break
      # 1
      if not fecha_a_buscar:
          print("Opción no se puede omitir. Inténtelo de nuevo o utilice [*]: Cancelar operación")
          continue
      # 2.1
      try:
          fecha_a_buscar = datetime.datetime.strptime(fecha_a_buscar, "%m/%d/%Y")
      except Exception:
          print('\nFecha inválida. Inténtelo de nuevo o utilice [*]: Cancelar operación')
          continue
      # 2.2
      try:
        with sqlite3.connect('Consultorio.db', 
                              detect_types = sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES) as conn:
          cursor = conn.cursor()
          cursor.execute("SELECT C.id_cita, P.nombre, P.primer_apellido, P.segundo_apellido, C.turno_cita \
                          FROM Citas C \
                          INNER JOIN Pacientes P \
                          ON C.id_paciente = P.id_paciente \
                          WHERE peso_kg = 'NA' AND fecha_cita = ?;", (fecha_a_buscar,))
          citas_en_fecha = cursor.fetchall()     
      except sqlite3.Error as e:
        print(e)
      except:
          print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
      finally:
          if (conn):
              conn.close()
      # 3
      if not citas_en_fecha:
          print("\nNo hay citas pendientes para la fecha ingresada.")
          return  
      # Impresión de citas encontradas en la fecha ingresada
      print("\nCitas encontradas para la fecha", fecha_a_buscar.strftime('%m/%d/%Y') + ":")
      encabezados = ["Folio","Nombre", "Primer apellido", "Segundo apellido", "Turno"]
      print(tabulate((citas_en_fecha), headers = encabezados, tablefmt="rounded_grid", rowalign="center"))
          
      # Folio cita
      while True:
        _folio_a_eliminar = input("Ingrese el folio de la cita a eliminar o utilice [*]: Cancelar operación\n").strip()
        if _folio_a_eliminar == '*':
          return
        # 1
        if not _folio_a_eliminar:
          print("\nEl folio no se puede omitir. Inténtelo de nuevo. [*]: Cancelar operación")
          continue
        # 2
        try:
          folio_a_eliminar = int(_folio_a_eliminar)
        except Exception:
          print('\nEl folio debe ser de tipo entero. Inténtelo de nuevo o utilice [*]: Cancelar operación')
          continue
        # 3
        if folio_a_eliminar not in [id_cita for id_cita, _, _, _, _ in citas_en_fecha]:
          print("\nEl folio de cita a eliminar no existe en las citas desplegadas. Inténtelo de nuevo o utilice [*]: Cancelar operación")
          continue
        break
    
      op_confirmacion = elegir_opcion('¿En verdad deseas cancelar la cita? S/N\n', 'SN')
      if op_confirmacion == "S":  
        # Eliminación
        try:
          with sqlite3.connect('Consultorio.db') as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM Citas WHERE id_cita = ?;', (folio_a_eliminar,))
            print(f'Se ha eliminado la cita {folio_a_eliminar}')
        except sqlite3.Error as e:
          print(e)
        except:
            print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
        finally:
            if (conn):
                conn.close()
      else:
        return
      break

# BÚSQUEDA POR PACIENTE
def cancelacion_por_paciente():
      try:
        with sqlite3.connect('Consultorio.db') as conn:
          cursor = conn.cursor()
          cursor.execute("SELECT DISTINCT(P.id_paciente), P.nombre, P.primer_apellido, P.segundo_apellido \
                          FROM Citas C \
                          INNER JOIN Pacientes P \
                          ON C.id_paciente = P.id_paciente \
                          WHERE C.peso_kg = 'NA';")
          pacientes_citas_pendientes = cursor.fetchall()     
      except sqlite3.Error as e:
        print(e)
      except:
          print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
      finally:
          if (conn):
              conn.close()
              
      # Mostrar la lista de pacientes con citas pendientes
      if pacientes_citas_pendientes:
          print("Pacientes con citas pendientes:")
          encabezados = ["Clave_paciente", "Nombre", "Primer apellido", "Segundo apellido" ]
          print(tabulate((pacientes_citas_pendientes), headers = encabezados, tablefmt="rounded_grid", rowalign="center"))

      else:
          print("No hay pacientes con citas pendientes.")
          return  # Salir si no hay pacientes con citas pendientes

      while True:
        # Capturar el folio del paciente seleccionado por el usuario
        _clave_paciente = input("Ingresa la clave del paciente al cual deseas eliminar alguna cita o utilice [*]: Cancelar operación\n").strip().upper()
        if _clave_paciente == "*":
            break
        # 1
        if not _clave_paciente:
            print("\nLa clave no se puede omitir. Inténtelo de nuevo o utilice [*]: Cancelar operación")
            continue
        # 2
        try:
            clave_paciente = int(_clave_paciente)
        except Exception:
            print("\nOpción inválida. Solo se aceptan números enteros. Inténtelo de nuevo o utilice [*]: Cancelar operación")
            continue
        # 3
        if clave_paciente not in [id_paciente for id_paciente, _, _, _ in pacientes_citas_pendientes]:
            print("\nLa clave del paciente no existe en la lista de pacientes mostrada. Inténtelo de nuevo o utilice [*]: Cancelar operación")
            continue

        # 4.1
        try:
          with sqlite3.connect('Consultorio.db',
                                detect_types = sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES) as conn:
            conn.execute("PRAGMA foreign_keys=1")
            cursor = conn.cursor()
            # Obtención de todas las citas del paciente ingresado
            cursor.execute("SELECT id_cita, fecha_cita, turno_cita FROM Citas \
                            WHERE id_paciente = ? AND peso_kg = 'NA'", (clave_paciente,))
            citas_encontradas = cursor.fetchall()
        except sqlite3.Error as e:
          print(e)
        except:
            print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
        finally:
            if (conn):
                conn.close()
        # 4.2
        if not citas_encontradas:
          print('\nNo existen citas pendientes por eliminar del paciente')
          return

        for folio_cita, fecha_cita, turno in citas_encontradas:
          fecha_cita = fecha_cita.date().strftime('%m/%d/%Y')
          citas_encontradas[[folio_cita, fecha_cita, turno]]

        print('Citas encontradas: ')
        encabezados = ["Folio_cita", "Fecha_cita", "Turno"]
        print(tabulate((citas_encontradas), headers = encabezados, tablefmt="rounded_grid", rowalign="center"))   
        
        while True:
          _folio_a_eliminar = input("Ingrese el folio de la cita a eliminar\n").strip()
          if _folio_a_eliminar == '*':
            return
          # 1
          if not _folio_a_eliminar:
              print("\nEl folio no se puede omitir. Inténtelo de nuevo o utilice [*]: Cancelar operación")
              continue
          # 2
          try:
            folio_a_eliminar = int(_folio_a_eliminar)
          except Exception:
            print('\nEl valor debe ser de tipo entero. Inténtelo de nuevo o utilice [*]: Cancelar operación')
            continue
          # 3
          if folio_a_eliminar not in [id_cita for id_cita,_ ,_ in citas_encontradas]:
            print("\nEl folio a eliminar no existe en las citas desplegadas. Inténtelo de nuevo o utilice [*]: Cancelar operación")
            continue
          break
          
        op_confirmacion = elegir_opcion('¿En verdad deseas cancelar la cita? S/N\n', 'SN')
        if op_confirmacion == "S":  
          # Eliminación
          try:
            with sqlite3.connect('Consultorio.db') as conn:
              cursor = conn.cursor()
              cursor.execute('DELETE FROM Citas WHERE id_cita = ?;', (folio_a_eliminar,))
              print(f'Se ha eliminado la cita {folio_a_eliminar}')
          except sqlite3.Error as e:
            print(e)
          except:
              print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
          finally:
              if (conn):
                  conn.close()
        else:
          return
        break

# CONSULTAS Y REPORTES
def consultas_reportes():
  try:
    with sqlite3.connect('Consultorio.db') as conn:
      cursor = conn.cursor()
      cursor.execute('SELECT * FROM Pacientes')
      pacientes = cursor.fetchall()
      cursor.execute('SELECT * FROM Citas')
      citas = cursor.fetchall()
      cursor.execute("SELECT * FROM Citas WHERE peso_kg != 'NA'")
      citas_realizadas = cursor.fetchall()

  except sqlite3.Error as e:
    print(e)
  except:
      print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
  finally:
      if (conn):
          conn.close()
    
  
  while True:
    op_citas_pacientes_estadistico = mostrar_menu({ '1':'Reporte de citas', 
                                        '2':'Reporte de pacientes',
                                        '3':'Estadísticos demográficos',
                                        'X':'Volver al menú anterior'})
    # REPORTE DE CITAS
    if op_citas_pacientes_estadistico == '1':
      # 1
      if not citas:
        print('\nNo existen citas registradas en el sistema.')
        continue
      menu_periodo_paciente()
    # REPORTE DE PACIENTES
    elif op_citas_pacientes_estadistico == '2':
      # 1
      if not pacientes:
        print('\nNo hay pacientes registrados en el sistema.')
        continue
      menu_listado_busqueda_clave_apellidos()
    # ESTADÍSTICOS DEMOGRÁFICOS
    elif op_citas_pacientes_estadistico == '3':
      # 1
      if not citas_realizadas:
        print('\nNo hay citas realizadas por analizar.')
        continue
      estadisticos_demograficos()
    # SALIDA
    elif op_citas_pacientes_estadistico == 'X':
      break


def menu_periodo_paciente():
  while True:
    op_periodo_paciente = mostrar_menu({'1':'Por periodo', 
                                        '2':'Por paciente', 
                                        'X':'Volver al menú anterior'})

    # REPORTE DE CITAS POR PERIODO
    if op_periodo_paciente == '1':
      flag_salir = False
      while True:
        # Fecha inicial
        _fecha_inicial = input('Ingresa la fecha inicial (mm/dd/aaaa)\n').strip()
        if _fecha_inicial.upper() == '*':
          break
        # 1
        if not _fecha_inicial:
          print("\nLa fecha no se puede omitir. Inténtelo de nuevo o utilice [*]: Cancelar operación")
          continue
        # 2
        try:
          fecha_inicial = datetime.datetime.strptime(_fecha_inicial, '%m/%d/%Y')
        except Exception:
          print('\nFecha inválida. Inténtelo de nuevo o utilice [*]: Cancelar operación')
          continue
        
        while True:
          # Fecha final
          _fecha_final = input('Ingresa la fecha final (mm/dd/aaaa)\n').strip()
          if _fecha_final.upper() == '*':
            flag_salir = True
            break
          # 1
          if not _fecha_final:
            print("\nOpción no se puede omitir. Inténtelo de nuevo o utilice [*]: Cancelar operación")
            continue
          # 2
          try:
            fecha_final = datetime.datetime.strptime(_fecha_final, '%m/%d/%Y')
          except Exception:
            print('\nFecha inválida. Inténtelo de nuevo o utilice [*]: Cancelar operación')
            continue
          break
        if flag_salir:
          break
        
        # 1
        if fecha_final < fecha_inicial:
          print('\nError. La fecha final debe ser superior o igual a la fecha inicial. Inténtelo de nuevo o utilice [*]: Cancelar operación')
          continue
        
        fechas = (fecha_inicial, fecha_final)
        
        try:
          with sqlite3.connect('Consultorio.db',
                                detect_types = sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES) as conn:
            conn.execute("PRAGMA foreign_keys=1")
            cursor = conn.cursor()
            # peso_kg, estatura_cm 
            cursor.execute("SELECT P.id_paciente, P.primer_apellido, P.segundo_apellido, P.nombre, P.fecha_nacimiento, P.sexo, C.id_cita, C.fecha_cita, C.turno_cita, C.hora_llegada, C.peso_kg, C.estatura_cm, C.presion_arterial \
                            FROM Pacientes P \
                            INNER JOIN Citas C \
                            ON P.id_paciente = C.id_paciente \
                            WHERE fecha_cita BETWEEN ? AND ?", fechas)
            citas_encontradas = cursor.fetchall()
            df_citas_encontradas = pd.read_sql("SELECT P.id_paciente, P.primer_apellido, P.segundo_apellido, P.nombre, P.fecha_nacimiento, P.sexo, C.id_cita, C.fecha_cita, C.turno_cita, C.hora_llegada, C.peso_kg, C.estatura_cm, C.presion_arterial \
                            FROM Pacientes P \
                            INNER JOIN Citas C \
                            ON P.id_paciente = C.id_paciente \
                            WHERE fecha_cita BETWEEN ? AND ?", conn, params=fechas)
        except sqlite3.Error as e:
          print(e)
        except:
            print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
        finally:
            if (conn):
                conn.close()
                
        if not citas_encontradas:
          print('\nNo existen citas para el periodo especificado.')
          break
        
        for clave_paciente, primer_apellido, segundo_apellido, nombre, fecha_nacimiento, sexo, folio_cita, fecha_cita, turno, hora_llegada, peso_kg, estatura_cm, presion_arterial in citas_encontradas:
          fecha_nacimiento = fecha_nacimiento.date().strftime('%m/%d/%Y')
          citas_encontradas = [[clave_paciente, primer_apellido, segundo_apellido, nombre, fecha_nacimiento, sexo, folio_cita, fecha_cita, turno, hora_llegada, peso_kg, estatura_cm, presion_arterial]]

        print(f'Reporte de citas entre {_fecha_inicial} y {_fecha_final}')
        encabezados = ['Clave_paciente', '1er_Apellido', '2do_Apellido', 'Nombre', 'Fecha_nacimiento', 'Sexo', 'Folio_cita', 'Fecha_cita', 'Turno', 'Hora_llegada', 'Peso_kg', 'Estatura_cm',  'Presion_arterial']
        print(tabulate(citas_encontradas, headers = encabezados, tablefmt="rounded_grid", rowalign="center"))
        
        exportar('reporte_citas_periodo', df_citas_encontradas)
        break
      
    # REPORTE DE CITAS POR PACIENTE
    if op_periodo_paciente == '2':
      while True:
        _clave_paciente = input('Ingresa la clave del paciente\n').strip()
        if _clave_paciente.upper() == '*':
          break
        # 1
        if not _clave_paciente:  
          print("La clave no se puede omitir. Inténtelo de nuevo o utilice [*]: Cancelar operación")
          continue
        # 2
        try:
          clave_paciente = int(_clave_paciente)
        except Exception:
          print("La clave solo puede contener datos numéricos enteros. Inténtelo de nuevo o utilice [*]: Cancelar operación\n")
          continue
        # 3
        try:
          with sqlite3.connect('Consultorio.db',
                                detect_types = sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES) as conn:
            cursor = conn.cursor()
            # peso_kg, estatura_cm 
            cursor.execute("SELECT * FROM Pacientes WHERE id_paciente = ?", (clave_paciente,))
            paciente_buscado = cursor.fetchall()
            
            cursor.execute("SELECT id_cita, fecha_cita, turno_cita, hora_llegada, peso_kg, estatura_cm, presion_arterial FROM Citas WHERE id_paciente = ?", (clave_paciente,))
            citas_encontradas = cursor.fetchall()
            df_citas_encontradas = pd.read_sql("SELECT id_cita, fecha_cita, turno_cita, hora_llegada, peso_kg, estatura_cm, presion_arterial FROM Citas WHERE id_paciente = ?", conn, params=(clave_paciente,))

        except sqlite3.Error as e:
          print(e)
        except:
            print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
        finally:
            if (conn):
                conn.close()

        if not paciente_buscado:
          print('\nEl paciente no está registrado. Inténtelo de nuevo o utilice [*]: Cancelar operación')
          continue
        
        if not citas_encontradas:
          print('\nNo existen citas registradas para el paciente.')
          break

        for clave_paciente, primer_apellido, segundo_apellido, nombre, fecha_nacimiento, sexo in paciente_buscado:
          fecha_nacimiento = fecha_nacimiento.date().strftime('%m/%d/%Y')
          paciente_buscado = [[clave_paciente, primer_apellido, segundo_apellido, nombre, fecha_nacimiento, sexo]]
        
        print('Datos del paciente:')
        encabezados = ['Clave_paciente',  '1er_Apellido',  '2do_Apellido', 'Nombre', 'Fecha_nacimiento', 'Sexo']
        print(tabulate((paciente_buscado), headers= encabezados, tablefmt="rounded_grid", rowalign="center"))
        
        for folio_cita, fecha_cita, turno, hora_llegada, peso_kg, estatura_cm, presion_arterial in citas_encontradas:
          fecha_cita = fecha_cita.date().strftime('%m/%d/%Y')
          citas_encontradas = [[folio_cita, fecha_cita, turno, hora_llegada, peso_kg, estatura_cm, presion_arterial]]

        print('Citas del paciente: ')
        encabezados = ['Folio_cita', 'Fecha_cita', 'Turno', 'Hora_llegada', 'Peso_kg', 'Estatura_cm', 'Presion_arterial']
        print(tabulate((citas_encontradas), headers= encabezados, tablefmt="rounded_grid", rowalign="center"))

        # Exportación
        exportar(f'citas_', df_citas_encontradas)
        break
      
    # VOLVER AL MENÚ ANTERIOR
    if op_periodo_paciente == 'X':
      break

def menu_listado_busqueda_clave_apellidos():
  while True:
    op_listado_busqueda = mostrar_menu({'1':'Listado completo de pacientes', 
                                        '2':'Búsqueda por clave de paciente', 
                                        '3':'Búsqueda por apellidos y nombres',
                                        'X':'Volver al menú anterior'})
          
    # Obtención de pacientes
    try:
      with sqlite3.connect('Consultorio.db',
                            detect_types = sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Pacientes")
        pacientes = cursor.fetchall()  
        df_pacientes = pd.read_sql('SELECT * FROM Pacientes', conn) #Importante imprime nombre cols
    except sqlite3.Error as e:
      print(e)
    except:
        print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
    finally:
        if (conn):
            conn.close()
            
    # LISTADO COMPLETO DE PACIENTES
    if op_listado_busqueda == '1':
      # 1
      if not pacientes:
        print('\nNo hay pacientes registrados en el sistema.')
        continue
      
      for clave_paciente, primer_apellido, segundo_apellido, nombre, fecha_nacimiento, sexo in pacientes:
        fecha_nacimiento = fecha_nacimiento.date().strftime('%m/%d/%Y')
        pacientes = [[clave_paciente, primer_apellido, segundo_apellido, nombre, fecha_nacimiento, sexo]]

      print(f'Información de los pacientes registrados')
      encabezados = ['Clave_paciente', '1er_Apellido', '2do_Apellido',  'Nombre', 'Fecha_nacimiento', 'Sexo']
      print(tabulate((pacientes), headers= encabezados, tablefmt = "rounded_grid", rowalign="center"))

      # Exportación
      exportar("listado_pacientes", df_pacientes)
      

    # BÚSQUEDA POR CLAVE DE PACIENTE
    if op_listado_busqueda == '2':
      while True:
        _clave_paciente = input('Ingresa la clave del paciente a buscar\n').strip()
        if _clave_paciente.upper() == '*':
          break
        # 1
        if not _clave_paciente: # Si está vacío
          print("La clave no se puede omitir. Inténtelo de nuevo o utilice [*]: Cancelar operación")
          continue
        # 2
        try:
          clave_paciente = int(_clave_paciente)
        except Exception:
          print("La clave solo puede contener datos numéricos enteros. Inténtelo de nuevo o utilice [*]: Cancelar operación\n")
          continue
        # 3
        if clave_paciente not in [id_paciente for id_paciente, _, _, _, _, _ in pacientes]:
          print('\nEl paciente no está registrado.')
          break
        
        try:
          with sqlite3.connect('Consultorio.db',
                                detect_types = sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Pacientes WHERE id_paciente = ?", (clave_paciente,))
            paciente_buscado = cursor.fetchall()     
            df_paciente_buscado = pd.read_sql('SELECT * FROM Pacientes WHERE id_paciente = ?', conn, params=(clave_paciente,))
        except sqlite3.Error as e:
          print(e)
        except:
            print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
        finally:
            if (conn):
                conn.close()

        for clave_paciente, primer_apellido, segundo_apellido, nombre, fecha_nacimiento, sexo in paciente_buscado:
          fecha_nacimiento = fecha_nacimiento.date().strftime('%m/%d/%Y')
          paciente_buscado = [[clave_paciente, primer_apellido, segundo_apellido, nombre, fecha_nacimiento, sexo]]
        
        encabezados = ['Clave_paciente',  '1er_Apellido',  '2do_Apellido', 'Nombre', 'Fecha_nacimiento', 'Sexo']
        print(tabulate((paciente_buscado), headers= encabezados, tablefmt="rounded_grid", rowalign="center"))

        # Exportación
        exportar("busqueda_paciente_clave", df_paciente_buscado)

        # Expediente clínico ------------------------------------------------------------------------------------------------------------------------------------------------------
        op_expediente = elegir_opcion('\n¿Deseas consultar el expediente clínico del paciente? S/N\n', 'SN')
        if op_expediente == 'N':
          break
        
        try:
          with sqlite3.connect('Consultorio.db',
                                detect_types = sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id_cita, fecha_cita, turno_cita, hora_llegada, peso_kg, estatura_cm, presion_arterial, diagnostico FROM Citas WHERE id_paciente = ?", (clave_paciente,))
            expediente = cursor.fetchall()     
        except sqlite3.Error as e:
          print(e)
        except:
            print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
        finally:
            if (conn):
                conn.close()
                
        if not expediente:
          print('\nNo hay citas registradas para el paciente')
          break

        for folio_cita, fecha_cita, turno, hora_llegada, peso_kg, estatura_cm, presion_arterial, diagnostico in expediente:
          fecha_cita = fecha_cita.date().strftime('%m/%d/%Y')
          expediente = [[folio_cita, fecha_cita, turno, hora_llegada, peso_kg, estatura_cm, presion_arterial, diagnostico]]

        print('Diagnostico del paciente: ')
        encabezados = ['id_cita', 'fecha_cita', 'turno_cita', 'hora_llegada', 'peso_kg', 'estatura_cm', 'presion_arterial', 'diagnostico']
        print(tabulate((expediente), headers = encabezados, tablefmt="rounded_grid", rowalign="center"))

        break
      

    # BÚSQUEDA POR APELLIDOS Y NOMBRES
    if op_listado_busqueda == '3':
      flag_salir = False
      while True: 
        # Nombre
        nombre_u = input('Ingresa el nombre\n').title().strip()
        if nombre_u == '*':
          break
        # 1
        if not nombre_u:
          print("\nEl nombre no se puede omitir. Inténtelo de nuevo o utilice [*]: Cancelar operación")
          continue
        # 2
        if not nombre_u.replace(' ', '').isalpha():
          print('\nError. Solo se aceptan caracteres alfabéticos. Inténtelo de nuevo o utilice [*]: Cancelar operación')
          continue
        
        while True:
          # Primer apellido
          primer_apellido_u = input('Ingresa el primer apellido\n').title().strip()
          if primer_apellido_u == '*':
            flag_salir = True
            break
          # 1
          if not primer_apellido_u:
            print("\nEl apellido no se puede omitir. Inténtelo de nuevo o utilice [*]: Cancelar operación")
            continue
          # 2
          if not primer_apellido_u.replace(' ', '').isalpha():
            print('\nError. Solo se aceptan caracteres alfabéticos. Inténtelo de nuevo o utilice [*]: Cancelar operación')
            continue
          break
        if flag_salir:
          break
        
        while True:
          # Segundo apellido
          segundo_apellido_u = input('Ingresa el segundo apellido\n').title().strip()
          if segundo_apellido_u == '*':
            flag_salir = True
            break
          # 1
          if not segundo_apellido_u:
            segundo_apellido_u = 'NA'
            break
          # 2
          if not segundo_apellido_u.replace(' ', '').isalpha():
            print('\nError. Solo se aceptan caracteres alfabéticos. Inténtelo de nuevo o utilice [*]: Cancelar operación')
            continue
          break
        if flag_salir:
          break
        
        try:
          with sqlite3.connect('Consultorio.db',
                                detect_types = sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Pacientes \
                            WHERE primer_apellido = ? AND segundo_apellido = ? AND nombre = ?;", (primer_apellido_u, segundo_apellido_u, nombre_u))
            paciente_buscado = cursor.fetchall()     
            df_paciente_buscado = pd.read_sql("SELECT * FROM Pacientes WHERE primer_apellido = ? AND segundo_apellido = ? AND nombre = ?;", conn, params=(primer_apellido_u, segundo_apellido_u, nombre_u))
            
        except sqlite3.Error as e:
          print(e)
        except:
            print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
        finally:
            if (conn):
                conn.close()
                
        if not paciente_buscado:
          print('\nPaciente no encontrado.')
          break

        for clave_paciente, primer_apellido, segundo_apellido, nombre, fecha_nacimiento, sexo in paciente_buscado:
          fecha_nacimiento = fecha_nacimiento.date().strftime('%m/%d/%Y')
          paciente_buscado = [[clave_paciente, primer_apellido, segundo_apellido, nombre, fecha_nacimiento, sexo]]

        encabezados = ('Clave_paciente', '1er_Apellido', '2do_Apellido', 'Nombre', 'Fecha_nacimiento', 'Sexo')
        print(tabulate((paciente_buscado), headers = encabezados, tablefmt="rounded_grid", rowalign="center"))

        exportar("busqueda_paciente_nombre_apellidos", df_paciente_buscado)

        
        # Expediente clínico ------------------------------------------------------------------------------------------------------------------------------------------------------
        op_expediente = elegir_opcion('\n¿Deseas consultar el expediente clínico del paciente? S/N\n', 'SN')
        if op_expediente == 'N':
          break
        
        try:
          with sqlite3.connect('Consultorio.db',
                                detect_types = sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES) as conn:
            conn.execute("PRAGMA foreign_keys=1")
            cursor = conn.cursor()
            cursor.execute("SELECT id_cita, fecha_cita, turno_cita, hora_llegada, peso_kg, estatura_cm, presion_arterial, diagnostico \
                            FROM Citas \
                            WHERE id_paciente = ? AND peso_kg != 'NA'", (clave_paciente,))
            expediente = cursor.fetchall()
          print(e)
        except:
            print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
        finally:
            if (conn):
                conn.close()

        for folio_cita, fecha_cita, turno, hora_llegada, peso_kg, estatura_cm, presion_arterial, diagnostico in expediente:
          fecha_cita = fecha_cita.date().strftime('%m/%d/%Y')
          expediente = [[folio_cita, fecha_cita, turno, hora_llegada, peso_kg, estatura_cm, presion_arterial, diagnostico]]

        encabezados = ('Folio_cita', 'Fecha_cita', 'Turno', 'Hora_llegada', 'Peso_kg', 'Estatura_cm', 'Presion_arterial', 'Diagnóstico')
        print(tabulate((expediente), headers = encabezados, tablefmt="rounded_grid", rowalign="center"))

        break
      # ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # SALIR AL MENÚ ANTERIOR
    if op_listado_busqueda == 'X':
      break

def estadisticos_demograficos():
  while True:
    op_edad_sexo = mostrar_menu({ '1':'Por edad', 
                                  '2':'Por sexo',
                                  '3':'Por edad y sexo',
                                  'X':'Volver al menú anterior'})
    # POR EDAD
    if op_edad_sexo == '1':
      flag_salir = False
      # Edad inicial
      while True:
        _edad_inicial = input("Ingresa la edad inicial del rango\n").strip()
        if _edad_inicial.upper() == '*':
          break
        # 1
        if not _edad_inicial:
          print("\nLa edad no se puede omitir. Inténtelo de nuevo o utilice [*]: Cancelar operación")
          continue
        # 2
        try:
          edad_inicial = int(_edad_inicial)
        except Exception:
          print('\nLa edad debe ser de dato numérico tipo entero. Inténtelo de nuevo o utilice [*]: Cancelar operación')
          continue
        # 3
        if edad_inicial <= 0:
          print("\nLa edad no puede ser menor o igual a 0. Inténtelo de nuevo o utilice [*]: Cancelar operación")
          continue
      
        # Edad final
        while True:
          _edad_final = input("Ingresa la edad final del rango\n").strip()
          if _edad_final.upper() == '*':
            flag_salir = True
            break
          # 1
          if not _edad_final:
            print("\nOpción no se puede omitir. Inténtelo de nuevo o utilice [*]: Cancelar operación")
            continue
          # 2
          try:
            edad_final = int(_edad_final)
          except Exception:
            print('\nLa edad debe ser de dato numérico tipo entero. Inténtelo de nuevo o utilice [*]: Cancelar operación')
            continue
          # 3
          if edad_final <= 0:
            print("\nLa edad no puede ser menor o igual a 0. Inténtelo de nuevo o utilice [*]: Cancelar operación")
            continue
          break
        if flag_salir == True:
          break
        
        try:
          with sqlite3.connect('Consultorio.db',
                                detect_types = sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES) as conn:
            conn.execute("PRAGMA foreign_keys=1")
            cursor = conn.cursor()
            cursor.execute("SELECT peso_kg, estatura_cm, presion_arterial, fecha_cita, fecha_nacimiento \
                           FROM Citas INNER JOIN Pacientes \
                           ON Citas.id_paciente = Pacientes.id_Paciente \
                           WHERE peso_kg != 'NA';")
            peso_estatura_presion_fecha = cursor.fetchall()

        except sqlite3.Error as e:
          print(e)
        except:
            print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
        finally:
            if (conn):
                conn.close()

        peso_estatura_presion_fecha_lista = []

        for peso, estatura, presion_arterial, fecha_cita, fecha_nacimiento in peso_estatura_presion_fecha:
          peso = float(peso) 
          estatura = float(estatura)
          sistolica, diastolica = presion_arterial.split('/')
          sistolica = int(sistolica)
          diastolica = int(diastolica)
          fecha_cita = fecha_cita
          fecha_nacimiento = fecha_nacimiento

          edad = fecha_cita.year - fecha_nacimiento.year
          if (fecha_nacimiento.month, fecha_nacimiento.day) > (fecha_cita.month, fecha_cita.day):
            edad = edad - 1

          peso_estatura_presion_fecha_lista.append([peso, estatura, sistolica, diastolica, edad])
        
        df_peso_estatura_presion_fecha = pd.DataFrame(peso_estatura_presion_fecha_lista, columns = ['Peso', 'Estatura', 'Sistolica', 'Diastolica', 'edad'])

        filtro_edad_inicial = df_peso_estatura_presion_fecha["edad"] >= edad_inicial 
        filtro_edad_final = df_peso_estatura_presion_fecha["edad"] <= edad_final

        datos_filtrados = df_peso_estatura_presion_fecha[filtro_edad_inicial & filtro_edad_final]

        if datos_filtrados.empty:
          print('\nNo existen datos para analizar con ese rango de edad.')
          break
        
        # Análisis de datos
        peso_estatura_presion_edad_medidas = datos_filtrados[['Peso', 'Estatura', 'Sistolica', 'Diastolica']].describe().loc[['count', 'min', 'max', 'mean', '50%', 'std']]
        peso_estatura_presion_edad_medidas = peso_estatura_presion_edad_medidas.rename(index={'count': 'Conteo', 'min': 'Mínimo', 'max': 'Máximo', 'mean': 'Media', '50%': 'Mediana', 'std': 'Desviación estándar'})
        # Impresión
        print(peso_estatura_presion_edad_medidas.round(2))

        exportar('estadisticos_demograficos_edad', datos_filtrados[['Peso', 'Estatura', 'Sistolica', 'Diastolica']])
        
        break
      

    # POR SEXO
    elif op_edad_sexo == '2':
      # Sexo
      while True:
        sexo = input('Ingresa el sexo \n[H] Hombre \n[M] Mujer\n[N] No contestó\n').upper().strip()
        if sexo == '*':
          flag_salir = True
          break
        # 1
        if not sexo:
          print('\nEl sexo no se puede omitir. Inténtelo de nuevo o utilice [*]: Cancelar operación')
          continue
        # 2
        if not sexo.isalpha():
          print('\nSolo ingresar caracteres alfabéticos. Inténtelo de nuevo o utilice [*]: Cancelar operación')
          continue
        # 3
        if sexo not in ['H', 'M', 'N']:
          print('\nOpción inválida. Inténtelo de nuevo o utilice [*]: Cancelar operación')
          continue
        break

      # Impresión de peso, estatura, presion sistólica y diastólica por sexo
      try:
        with sqlite3.connect('Consultorio.db',
                            detect_types = sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES) as conn:
          conn.execute("PRAGMA foreign_keys=1")
          cursor = conn.cursor()

        if sexo == 'H':
            cursor.execute("SELECT C.peso_kg, C.estatura_cm, C.presion_arterial \
                            FROM Citas C\
                            INNER JOIN Pacientes P \
                            ON C.id_paciente = P.id_paciente \
                            WHERE peso_kg != 'NA' AND P.sexo = ?", ('H',))
            sexo = cursor.fetchall()

        elif sexo == 'M':
            cursor.execute("SELECT C.peso_kg, C.estatura_cm, C.presion_arterial \
                            FROM Citas C\
                            INNER JOIN Pacientes P \
                            ON C.id_paciente = P.id_paciente \
                            WHERE peso_kg != 'NA' AND P.sexo = ?", ('M',))
            sexo = cursor.fetchall()

        elif sexo == 'N':
            cursor.execute("SELECT C.peso_kg, C.estatura_cm, C.presion_arterial \
                            FROM Citas C\
                            INNER JOIN Pacientes P \
                            ON C.id_paciente = P.id_paciente \
                            WHERE peso_kg != 'NA' AND P.sexo = ?", ('N',))
            sexo = cursor.fetchall()

      except sqlite3.Error as e:
        print(e)
      except:
          print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
      finally:
          if (conn):
              conn.close()
      
      peso_estatura_presion_lista = []

      for peso, estatura, presion_arterial in sexo:
        peso = float(peso) 
        estatura = float(estatura)
        sistolica, diastolica = presion_arterial.split('/')
        sistolica = int(sistolica)
        diastolica = int(diastolica)
        
        peso_estatura_presion_lista.append((peso, estatura, sistolica, diastolica))
        
      # Conversión a dataframe
      df = pd.DataFrame(peso_estatura_presion_lista, columns=['Peso', 'Estatura', 'Sistolica', 'Diastolica'])
      # Análisis de datos
      peso_estatura_presion_medidas = df[['Peso', 'Estatura', 'Sistolica', 'Diastolica']].describe().loc[['count', 'min', 'max', 'mean', '50%', 'std']]
      peso_estatura_presion_medidas = peso_estatura_presion_medidas.rename(index={'count': 'Conteo', 'min': 'Mínimo', 'max': 'Máximo', 'mean': 'Media', '50%': 'Mediana', 'std': 'Desviación estándar'})
      # Impresión
      print(peso_estatura_presion_medidas.round(2))

      exportar('estadisticos_demograficos_sexo', df)
      
      
    # POR EDAD Y SEXO
    elif op_edad_sexo == '3':
      flag_salir = False
      # Edad inicial
      while True:
        _edad_inicial = input("Ingresa la edad inicial del rango\n").strip()
        if _edad_inicial.upper() == '*':
          break
        # 1
        if not _edad_inicial:
          print("\nLa edad no se puede omitir. Inténtelo de nuevo o utilice [*]: Cancelar operación")
          continue
        # 2
        try:
          edad_inicial = int(_edad_inicial)
        except Exception:
          print('\nLa edad debe ser de dato numérico tipo entero. Inténtelo de nuevo o utilice [*]: Cancelar operación')
          continue
        # 3
        if edad_inicial <= 0:
          print("\nLa edad no puede ser menor o igual a 0. Inténtelo de nuevo o utilice [*]: Cancelar operación")
          continue
        
        # Edad final
        while True:
          _edad_final = input("Ingresa la edad final del rango\n").strip()
          if _edad_final.upper() == '*':
            flag_salir = True
            break
          # 1
          if not _edad_final:
            print("\nLa edad no se puede omitir. Inténtelo de nuevo o utilice [*]: Cancelar operación")
            continue
          # 2
          try:
            edad_final = int(_edad_final)
          except Exception:
            print('\nLa edad debe ser de dato numérico tipo entero. Inténtelo de nuevo o utilice [*]: Cancelar operación')
            continue
          # 3
          if edad_final <= 0:
            print("\nLa edad no puede ser menor o igual a 0. Inténtelo de nuevo o utilice [*]: Cancelar operación")
            continue
          break
        if flag_salir == True:
          break
        
        # Sexo
        while True:
          sexo = input('Ingresa el sexo \n[H] Hombre \n[M] Mujer\n[N] No contestó\n').upper().strip()
          if sexo == '*':
            flag_salir = True
            break
          # 1
          if not sexo:
            print('\nEl sexo no se puede omitir. Inténtelo de nuevo o utilice [*]: Cancelar operación')
            continue
          # 2
          if not sexo.isalpha():
            print('\nSolo ingresar caracteres alfabéticos. Inténtelo de nuevo o utilice [*]: Cancelar operación')
            continue
          # 3
          if sexo not in ['H', 'M', 'N']:
            print('\nOpción inválida. Inténtelo de nuevo o utilice [*]: Cancelar operación')
            continue
          break
        if flag_salir == True:
          break
        
        try:
          with sqlite3.connect('Consultorio.db',
                                detect_types = sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES) as conn:
            conn.execute("PRAGMA foreign_keys=1")
            cursor = conn.cursor()
            cursor.execute("SELECT C.peso_kg, C.estatura_cm, C.presion_arterial, C.fecha_cita, P.fecha_nacimiento \
                            FROM Citas C \
                            INNER JOIN Pacientes P \
                            ON C.id_paciente = P.id_paciente \
                            AND P.sexo = ?;", (sexo))
            peso_estatura_presion_sexo = cursor.fetchall()
        except sqlite3.Error as e:
          print(e)
        except:
            print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
        finally:
            if (conn):
                conn.close()

        peso_estatura_presion_fecha_lista = []

        for peso, estatura, presion_arterial, fecha_cita, fecha_nacimiento in peso_estatura_presion_sexo:
          peso = float(peso) 
          estatura = float(estatura)
          sistolica, diastolica = presion_arterial.split('/')
          sistolica = int(sistolica)
          diastolica = int(diastolica)
          fecha_cita = fecha_cita
          fecha_nacimiento = fecha_nacimiento

          edad = fecha_cita.year - fecha_nacimiento.year
          if (fecha_nacimiento.month, fecha_nacimiento.day) > (fecha_cita.month, fecha_cita.day):
            edad = edad - 1

          peso_estatura_presion_fecha_lista.append([peso, estatura, sistolica, diastolica, edad])
        
        df_peso_estatura_presion_fecha = pd.DataFrame(peso_estatura_presion_fecha_lista, columns = ['Peso', 'Estatura', 'Sistolica', 'Diastolica', 'edad'])

        filtro_edad_inicial = df_peso_estatura_presion_fecha["edad"] >= edad_inicial 
        filtro_edad_final = df_peso_estatura_presion_fecha["edad"] <= edad_final

        datos_filtrados = df_peso_estatura_presion_fecha[filtro_edad_inicial & filtro_edad_final]
                
                
        if datos_filtrados.empty:
          print('\nNo existen datos para analizar con ese rango de edad y sexo.')
          break
        
        if sexo == 'H':
          sexo = 'Masculino'
        if sexo == 'M':
          sexo = 'Femenino'
        if sexo == 'N':
          sexo = 'Sin contestar'
        
        print(f'\nDatos demográficos para el rango de edad de {edad_inicial} a {edad_final} y sexo: {sexo}\n')
          
        # Conversión a dataframe
        df = pd.DataFrame(datos_filtrados, columns=['Peso', 'Estatura', 'Sistolica', 'Diastolica'])
        # Análisis de datos
        peso_estatura_presion_edad_sexo_medidas = datos_filtrados[['Peso', 'Estatura', 'Sistolica', 'Diastolica']].describe().loc[['count', 'min', 'max', 'mean', '50%', 'std']]
        peso_estatura_presion_edad_sexo_medidas = peso_estatura_presion_edad_sexo_medidas.rename(index={'count': 'Conteo', 'min': 'Mínimo', 'max': 'Máximo', 'mean': 'Media', '50%': 'Mediana', 'std': 'Desviación estándar'})
        # Impresión
        print(peso_estatura_presion_edad_sexo_medidas.round(2))

        exportar('estadisticos_demograficos_sexo_y_edad', datos_filtrados[['Peso', 'Estatura', 'Sistolica', 'Diastolica']])
        
        break
      
    elif op_edad_sexo == 'X':
      break


# Programa principal
while True:
  try:
    with sqlite3.connect('Consultorio.db') as conn:
      cursor = conn.cursor()
      cursor.execute('SELECT * FROM Pacientes')
      pacientes = cursor.fetchall()
  except sqlite3.Error as e:
    print(e)
    pacientes = ()
  except:
      print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
  finally:
      if (conn):
          conn.close()

  try:
    with sqlite3.connect('Consultorio.db') as conn:
      cursor = conn.cursor()
      cursor.execute('SELECT * FROM Citas')
      citas = cursor.fetchall()
  except sqlite3.Error as e:
    print(e)
    citas = ()
  except:
      print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
  finally:
      if (conn):
          conn.close()
  
  op_principal = mostrar_menu(menu_principal, '\nSistema de gestión de pacientes de un consultorio')
  match op_principal:
    case '1':
      registro_pacientes()
    case '2':
      if not pacientes:
        print('\nDebe haber al menos un paciente registrado para entrar al menú de citas.')
        continue
      citas_crear_realizar_cancelar_menu()
    case '3':
      consultas_reportes()
    case 'X':
      op_salida = elegir_opcion('¿En verdad deseas salir del sistema? S/N\n', 'SN')
      if op_salida == "S":
        print('Fin del programa.')
        break
    case _:
      print('Opción no reconocida.')