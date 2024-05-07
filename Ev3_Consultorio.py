import datetime
import re
import csv
import sys
import sqlite3
import pandas as pd
from openpyxl import Workbook

# Estructura de datos --------------------------------------------------------------------------------------------------------------

# Pacientes (lista de tuplas de cada paciente)
# [(id_paciente, primer_apellido, segundo_apellido, nombre, fecha_nacimiento, sexo)]

# Citas (lista de tuplas de cada cita)
# [(id_cita, id_paciente, fecha_cita, turno_cita, hora_llegada, peso_kg, estatura_cm, presion_arterial, diagnostico, edad)]

# Cita sin realizar
# (id_cita, id_paciente, fecha_cita, turno_cita, NA, NA, NA, NA, NA, NA)

# ----------------------------------------------------------------------------------------------------------------------------------

fecha_actual = datetime.datetime.today()

menu_principal = {
    'A':'Registro de pacientes',
    'B':'Citas', 
    'C':'Consultas y reportes',
    'X':'Salir del sistema'
}


def elegir_opcion(prompt='Elige la opción deseada',
                  opciones='ABCD'):
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

# REGISTRO DE PACIENTES
def registro_pacientes():
  while True:
    # Primer apellido
    primer_apellido = input('Ingresa el primer apellido\n').title().strip()
    if primer_apellido == '*':
      return
    # 1
    if not primer_apellido: # si es que está vacío
      print("\nOpción no se puede omitir. Inténtelo de nuevo. [*]: Cancelar operación")
      continue
    # 2
    if not primer_apellido.replace(' ', '').isalpha(): # comprueba que todo sea texto
      print('\nError. Solo se aceptan caracteres alfabéticos. Intente de nuevo. [*]: Cancelar operación')
      continue
    
    while True:
      # Segundo apellido
      segundo_apellido = input('Ingresa el segundo apellido\n').title().strip()
      if segundo_apellido == '*':
        return
      # 1
      if not segundo_apellido:
        segundo_apellido = 'NA'
        break
      # 2
      if not segundo_apellido.replace(' ', '').isalpha():
        print('\nError. Solo se aceptan caracteres alfabéticos. Intente de nuevo. [*]: Cancelar operación')
        continue
      break
      
    while True:
      # Nombre
      nombre = input('Ingresa el nombre\n').title().strip()
      if nombre == '*':
        return
      # 1
      if not nombre:
        print("\nOpción no se puede omitir. Inténtelo de nuevo. [*]: Cancelar operación")
        continue
      # 2
      if not nombre.replace(' ', '').isalpha():
        print('\nError. Solo se aceptan caracteres alfabéticos. Intente de nuevo. [*]: Cancelar operación')
        continue
      break
    
    while True:
      # Fecha de nacimiento
      _fecha_nacimiento = input('Ingresa la fecha de nacimiento (mm/dd/aaaa)\n').strip()
      if _fecha_nacimiento == '*':
        return
      #1
      if not _fecha_nacimiento:
        print("\nOpción no se puede omitir. Inténtelo de nuevo. [*]: Cancelar operación")
        continue
      # 2
      try:
        fecha_nacimiento = datetime.datetime.strptime(_fecha_nacimiento, '%m/%d/%Y')
      except Exception:
        print('\nFecha inválida. Intenta de nuevo. [*]: Cancelar operación')
        continue
      # 3
      if fecha_nacimiento >= fecha_actual:
        print('\nLa fecha de nacimiento no puede ser superior o igual a la fecha actual. [*]: Cancelar operación')
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
        print('\nSolo ingresar caracteres alfabéticos. Intenta de nuevo. [*]: Cancelar operación')
        continue
      # 2
      if sexo not in ['H', 'M']:
        print('\nOpción inválida. Intenta de nuevo. [*]: Cancelar operación')
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
          segundo_apellido TEXT NOT NULL, \
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
    op_citas_crear_realizar_cancelar = mostrar_menu({ 'A':'Programación de citas', 
                                                      'B':'Realización de citas programadas', 
                                                      'C':'Cancelación de citas', 
                                                      'X':'Volver al menú anterior'})
    # PROGRAMACIÓN DE CITAS
    if op_citas_crear_realizar_cancelar == 'A':
      crear_cita()
    if op_citas_crear_realizar_cancelar == 'B':
      # if not citas:
      #   print('\nDebe haber al menos una cita creada para poder realizarla.')
      #   continue
      realizar_citas()
    if op_citas_crear_realizar_cancelar == 'C':
      # if not citas:
      #   print('\nDebe haber al menos una cita creada para poder cancelarla.')
      #   continue
      cancelar_cita_menu()
    # SALIDA
    if op_citas_crear_realizar_cancelar == 'X':
      break


# PROGRAMACIÓN DE CITAS
def crear_cita():
  # Clave del paciente
  while True:
    _clave_paciente = input('Ingresa la clave del paciente\n').strip()
    if _clave_paciente.upper() == '*':
      break
    # 1
    if not _clave_paciente:  
      print("\nOpción no se puede omitir. Inténtelo de nuevo. [*]: Cancelar operación")
      continue
    # 2
    try:
      clave_paciente = int(_clave_paciente)
    except Exception:
      print("\nLa clave solo puede contener datos numéricos enteros. Intenta de nuevo. [*]: Cancelar operación")
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
      print('\nError. El paciente no está registrado en el sistema. [*]: Cancelar operación')
      continue
    
    # Fecha de la cita
    while True:  
      _fecha_cita = input('Ingresa la fecha de la cita (mm/dd/yyyy)\n').strip()
      if _fecha_cita.upper() == '*':
        return
      # 1
      if not _fecha_cita:
        print("\nOpción no se puede omitir. Inténtelo de nuevo. [*]: Cancelar operación")
        continue
      # 2
      try:
        fecha_cita = datetime.datetime.strptime(_fecha_cita, '%m/%d/%Y')
      except Exception:
        print('\nFecha inválida. Intenta de nuevo. [*]: Cancelar operación')
        continue
      # 3
      if fecha_cita < fecha_actual:
        print('\nLa fecha ingresada debe ser posterior a la fecha actual. [*]: Cancelar operación')
        continue
      # 4
      fecha_actual_mas_60 = fecha_actual + datetime.timedelta(days=60)
      if fecha_cita > fecha_actual_mas_60:
        print('\nLa fecha ingresada no debe ser mayor o igual a 60 días posteriores a la fecha actual. [*]: Cancelar operación')
        fecha_distante = datetime.datetime.strftime(fecha_actual_mas_60, '%m/%d/%Y')
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
          print('\nDebes agendar la cita en otra fecha. [*]: Cancelar operación')
          continue    
      break
    
    # Turno de la cita
    while True:
      print('\nTurnos disponibles')
      menu_turno_cita = {'1':'Mañana', '2':'Mediodía', '3':'Tarde'}
      [print(f'[{k}] {v}') for k, v in menu_turno_cita.items()]
      _turno_cita = input('Ingresa el turno de la cita\n').strip()
      if _turno_cita == '*':
        return
      # 1
      if not _turno_cita:
        print("\nOpción no se puede omitir. Inténtelo de nuevo. [*]: Cancelar operación")
        continue
      # 2
      try:
        turno_cita = int(_turno_cita)
      except Exception:
        print("\nEl turno solo puede contener datos numéricos enteros. Intenta de nuevo. [*]: Cancelar operación")
        continue

      if turno_cita == 1:
        _turno_cita = 'Mañana'
      elif turno_cita == 2:
        _turno_cita = 'Mediodía'
      elif turno_cita == 3:
        _turno_cita = 'Tarde'
      break

    
    # Ingreso de datos # folio de cita: clave_paciente,...
    cita = (clave_paciente, fecha_cita, _turno_cita, 'NA', 'NA', 'NA', 'NA', 'NA', 'NA')
    
    # Ingreso de datos a base de datos
    try:
      with sqlite3.connect('Consultorio.db') as conn:
        cursor = conn.cursor()
        
        # Creación de tabla Citas
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
          edad TEXT NOT NULL, \
          FOREIGN KEY(id_paciente) REFERENCES Pacientes(id_paciente));')
        
        cursor.execute('INSERT INTO Citas (id_paciente, fecha_cita, turno_cita, hora_llegada, peso_kg, estatura_cm, presion_arterial, diagnostico, edad) \
                        VALUES(?,?,?,?,?,?,?,?,?)', cita)
        print(f'El folio de la cita asignada fue {cursor.lastrowid}')

    except sqlite3.Error as e:
      print(e)
    except:
        print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
    finally:
        if (conn):
            conn.close()
    break


# REALIZACIÓN DE CITAS PROGRAMADASs
def realizar_citas():
  # Folio de la cita
  while True:
    _folio_cita = input('Ingresa el folio de la cita (Número entero)\n').strip()
    if _folio_cita.upper() == '*':
      break
    # 1
    if not _folio_cita: # Si está vacío
      print('\nOpción no se puede omitir. Inténtelo de nuevo. [*]: Cancelar operación')
      continue
    # 2
    try:
      folio_cita = int(_folio_cita)
    except Exception:
      print('\nEl folio solo puede contener datos numéricos enteros. Intenta de nuevo. [*]: Cancelar operación')
      continue
    # 3.1
    try:
      with sqlite3.connect('Consultorio.db') as conn:
        conn.execute("PRAGMA foreign_keys=1")
        cursor = conn.cursor()
        # Obtención de cita buscada
        cursor.execute('SELECT * FROM Citas WHERE id_cita = ?', (folio_cita,))
        cita_buscada = cursor.fetchone()
        print(cita_buscada)
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
      print('\nLa cita no ha sido registrada con anterioridad. [*]: Cancelar operación')
      continue
    # 4
    if cita_buscada[5] != 'NA':
      print('\nLa cita programada ya ha sido realizada. [*]: Cancelar operación')
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
        print("\nOpción no se puede omitir. Inténtelo de nuevo [*]: Cancelar operación")
        continue
      # 2
      try:
        peso_kg = float(_peso_kg)
      except Exception:
        print('\nEl peso debe ser de dato numérico. Intenta de nuevo [*]: Cancelar operación')
        continue
      # 3
      if peso_kg <= 0:
        print("\nEl peso no puede ser menor o igual a 0. Inténtelo de nuevo [*]: Cancelar operación")
        continue
      break
    
    # Estatura del paciente en cm
    while True:
      _estatura_cm = input("Ingresa la estatura del paciente\n").strip()
      if _estatura_cm.upper() == '*':
        return
      # 1
      if not _estatura_cm:
        print("\nOpción no se puede omitir. Inténtelo de nuevo. [*]: Cancelar operación")
        continue
      # 2
      try:
        estatura_cm = float(_estatura_cm)
      except Exception:
        print('\nLa estatura debe ser de dato numérico. Intenta de nuevo. [*]: Cancelar operación')
        continue
      # 3
      if estatura_cm <= 0:
        print("\nLa estatura no puede ser menor o igual a 0. Inténtelo de nuevo. [*]: Cancelar operación")
        continue
      break
    
    # Presion sistólica
    while True:
      _sistolica = input('Ingresa la presión sistólica del paciente\n').strip()
      if _sistolica.upper() == '*':
        return
      # 1
      if not _sistolica:
        print("\nOpción no se puede omitir. Inténtelo de nuevo. [*]: Cancelar operación")
        continue
      # 2
      try:
        sistolica = int(_sistolica)
      except Exception:
        print('\nEl valor debe ser de tipo entero. Intenta de nuevo. [*]: Cancelar operación')
        continue
      # 3
      if sistolica <= 0:
        print('\nEl valor tiene que ser un número entero positivo. Intenta de nuevo. [*]: Cancelar operación')
        continue
      # 4
      if len(_sistolica) > 3:
        print('\nSolo puede contener hasta 3 dígitos. Intenta de nuevo. [*]: Cancelar operación')
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
        print("\nOpción no se puede omitir. Inténtelo de nuevo. [*]: Cancelar operación")
        continue
      # 2
      try:
        diastolica = int(_diastolica)
      except Exception:
        print('\nEl valor debe ser de tipo entero. Intenta de nuevo. [*]: Cancelar operación')
        continue
      # 3
      if diastolica <= 0:
        print('\nEl valor tiene que ser un número entero positivo. Intenta de nuevo. [*]: Cancelar operación')
        continue
      # 4
      if len(_diastolica) > 3:
        print('\nSolo puede contener hasta 3 dígitos. Intenta de nuevo. [*]: Cancelar operación')
        continue
      
      # Añadido de ceros a la izquierda
      while len(_diastolica) < 3:
        _diastolica = '0' + _diastolica
      break
      
    # Presión arterial
    presion_arterial = f'{_sistolica}/{_diastolica}'
      
    # Diagnóstico (200 caracteres máximo)
    while True:
      diagnostico = input('Diagnóstico (200 caracteres máximo)\n').upper()
      if diagnostico.upper() == '*':
        return
      # 1
      if len(diagnostico) > 200:
        print('\nEl diagnóstico excedió los 200 caracteres. Intenta de nuevo. [*]: Cancelar operación')
        continue
      break
    
    # Edad (fecha_cita - fecha_nacimiento)
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
            
    # 1.2
    edad = fecha_cita.year - fecha_nacimiento.year
    
    if (fecha_nacimiento.month, fecha_nacimiento.day) > (fecha_cita.month, fecha_cita.day):
      edad = edad - 1
    
    # Ingreso del registro {folio_cita: [id_paciente, hora_llegada,...., no confundirse con clave_paciente]
    cita_realizada = (_hora_llegada, peso_kg, estatura_cm, presion_arterial, diagnostico, edad, folio_cita)
    
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
          edad INTEGER NOT NULL, \
          FOREIGN KEY(id_paciente) REFERENCES Pacientes(id_paciente));')
        # Actualización
        cursor.execute('UPDATE Citas\
                        SET hora_llegada = ?, peso_kg = ?, estatura_cm = ?, presion_arterial = ?, diagnostico = ?, edad = ? \
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
    op_cancelar_fecha_paciente = mostrar_menu({ 'A':'Búsqueda por fecha', 
                                                'B':'Búsqueda por paciente', 
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
    if op_cancelar_fecha_paciente == 'A':
      if not citas:
        print('\nDebe haber al menos una cita creada para poder cancelarla.')
        continue
      eliminar_por_fecha()
    # BÚSQUEDA POR PACIENTE
    elif op_cancelar_fecha_paciente == 'B':
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
          print("Opción no se puede omitir. Inténtelo de nuevo. [*]: Cancelar operación")
          continue
      # 2.1
      try:
          fecha_a_buscar = datetime.datetime.strptime(fecha_a_buscar, "%m/%d/%Y")
      except Exception:
          print('\nFecha inválida. Intenta de nuevo. [*]: Cancelar operación')
          continue
      # 2.2
      try:
        with sqlite3.connect('Consultorio.db') as conn:
          cursor = conn.cursor()
          cursor.execute("SELECT C.id_cita, P.nombre || ' ' || P.primer_apellido || ' ' || P.segundo_apellido, C.turno_cita \
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
          print("\nNo hay citas pendientes para la fecha ingresada. [*]: Cancelar operación")
          return
      # Impresión de citas encontradas en la fecha ingresada
      print("\nCitas encontradas para la fecha", fecha_a_buscar.strftime('%m/%d/%Y') + ":")
      print("{:^10} {:^40} {:^10}".format("Folio","Nombre_completo", "Turno"))
      for id_cita, nombre_completo, turno in citas_en_fecha:
          print("{:^10} {:^40} {:^10}".format(id_cita, nombre_completo, turno))
          
      # Folio cita
      while True:
        _folio_a_eliminar = input("Ingrese el folio de la cita a eliminar\n").strip()
        if _folio_a_eliminar == '*':
          return
        # 1
        if not _folio_a_eliminar:
          print("\nOpción no se puede omitir. Inténtelo de nuevo. [*]: Cancelar operación")
          continue
        # 2
        try:
          folio_a_eliminar = int(_folio_a_eliminar)
        except Exception:
          print('\nEl valor debe ser de tipo entero. Intenta de nuevo. [*]: Cancelar operación')
          continue
        # 3
        if folio_a_eliminar not in [id_cita for id_cita, _, _ in citas_en_fecha]:
          print("\nEl folio de cita a eliminar no existe en las citas desplegadas. [*]: Cancelar operación")
          continue
        break
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

# BÚSQUEDA POR PACIENTE
def cancelacion_por_paciente():
      try:
        with sqlite3.connect('Consultorio.db') as conn:
          cursor = conn.cursor()
          cursor.execute("SELECT P.id_paciente, P.nombre || ' ' || P.primer_apellido || ' ' || P.segundo_apellido \
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
          print("{:^16} {:^40}".format("Clave_paciente", "Nombre_completo"))
          for clave_paciente, nombre_completo in pacientes_citas_pendientes:
              print("{:^16} {:^40}".format(clave_paciente, nombre_completo))
      else:
          print("No hay pacientes con citas pendientes.")
          return  # Salir si no hay pacientes con citas pendientes

      while True:
        # Capturar el folio del paciente seleccionado por el usuario
        _clave_paciente = input("Ingresa la clave del paciente al cual deseas eliminar alguna cita\n").strip().upper()
        if _clave_paciente == "*":
            break
        # 1
        if not _clave_paciente:
            print("\nOpción no se puede omitir. [*]: Cancelar operación")
            continue
        # 2
        try:
            clave_paciente = int(_clave_paciente)
        except Exception:
            print("\nOpción inválida. Solo se aceptan números enteros. [*]: Cancelar operación")
            continue
        # 3
        if clave_paciente not in [id_paciente for id_paciente, _ in pacientes_citas_pendientes]:
            print("\nLa clave del paciente no existe en la lista de pacientes mostrada. [*]: Cancelar operación")
            continue

        # 4.1
        try:
          with sqlite3.connect('Consultorio.db') as conn:
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
        
        # 4.3
        print("{:^10} {:^20} {:^10}".format("Folio_cita", "Fecha_cita", "Turno"))
        for id_cita, fecha_cita, turno_cita in citas_encontradas:
          print("{:^10} {:^20} {:^10}".format(id_cita, str(fecha_cita), turno_cita))
          
        
        while True:
          _folio_a_eliminar = input("Ingrese el folio de la cita a eliminar\n").strip()
          if _folio_a_eliminar == '*':
            return
          # 1
          if not _folio_a_eliminar:
              print("\nOpción no se puede omitir. Inténtelo de nuevo. [*]: Cancelar operación")
              continue
          # 2
          try:
            folio_a_eliminar = int(_folio_a_eliminar)
          except Exception:
            print('\nEl valor debe ser de tipo entero. Intenta de nuevo. [*]: Cancelar operación')
            continue
          # 3
          if folio_a_eliminar not in [id_cita for id_cita,_ ,_ in citas_encontradas]:
            print("\nEl folio a eliminar no existe en las citas desplegadas. [*]: Cancelar operación")
            continue
          break
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

# CONSULTAS Y REPORTES
def consultas_reportes():
  while True:
    op_citas_pacientes_estadistico = mostrar_menu({ 'A':'Reporte de citas', 
                                        'B':'Reporte de pacientes',
                                        'C':'Estadísticos demográficos',
                                        'X':'Volver al menú anterior'})
    # REPORTE DE CITAS
    if op_citas_pacientes_estadistico == 'A':
      # 1
      # if not citas:
      #   print('\nNo existen citas registradas en el sistema.')
      #   continue
      menu_periodo_paciente()
    # REPORTE DE PACIENTES
    elif op_citas_pacientes_estadistico == 'B':
      # 1
      # if not pacientes:
      #   print('\nNo hay pacientes registrados en el sistema.')
      #   continue
      menu_listado_busqueda_clave_apellidos()
    # ESTADÍSTICOS DEMOGRÁFICOS
    elif op_citas_pacientes_estadistico == 'C':
      estadisticos_demograficos()
    # SALIDA
    elif op_citas_pacientes_estadistico == 'X':
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
        _fecha_inicial = input('Ingresa la fecha inicial (mm/dd/aaaa)\n').strip()
        if _fecha_inicial.upper() == '*':
          break
        # 1
        if not _fecha_inicial:
          print("\nOpción no se puede omitir. Inténtelo de nuevo. [*]: Cancelar operación")
          continue
        # 2
        try:
          fecha_inicial = datetime.datetime.strptime(_fecha_inicial, '%m/%d/%Y')
        except Exception:
          print('\nFecha inválida. Intenta de nuevo. [*]: Cancelar operación')
          continue
        
        while True:
          # Fecha final
          _fecha_final = input('Ingresa la fecha final (mm/dd/aaaa)\n').strip()
          if _fecha_final.upper() == '*':
            flag_salir = True
            break
          # 1
          if not _fecha_final:
            print("\nOpción no se puede omitir. Inténtelo de nuevo. [*]: Cancelar operación")
            continue
          # 2
          try:
            fecha_final = datetime.datetime.strptime(_fecha_final, '%m/%d/%Y')
          except Exception:
            print('\nFecha inválida. Intenta de nuevo. [*]: Cancelar operación')
            continue
          break
        if flag_salir:
          break
        
        # 1
        if fecha_final < fecha_inicial:
          print('\nError. La fecha final debe ser superior o igual a la fecha inicial. [*]: Cancelar operación')
          continue
        
        fechas = (fecha_inicial, fecha_final)
        
        try:
          with sqlite3.connect('Consultorio.db',
                                detect_types = sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES) as conn:
            conn.execute("PRAGMA foreign_keys=1")
            cursor = conn.cursor()
            # peso_kg, estatura_cm 
            cursor.execute("SELECT P.id_paciente, P.primer_apellido, P.segundo_apellido, P.nombre, P.fecha_nacimiento, P.sexo, C.id_cita, C.fecha_cita, C.turno_cita, C.hora_llegada, C.peso_kg, C.estatura_cm, C.presion_arterial, C.edad \
                            FROM Pacientes P \
                            INNER JOIN Citas C \
                            ON P.id_paciente = C.id_paciente \
                            WHERE fecha_cita BETWEEN ? AND ?", fechas)
            citas_encontradas = cursor.fetchall()
            df_citas_encontradas = pd.read_sql("SELECT P.id_paciente, P.primer_apellido, P.segundo_apellido, P.nombre, P.fecha_nacimiento, P.sexo, C.id_cita, C.fecha_cita, C.turno_cita, C.hora_llegada, C.peso_kg, C.estatura_cm, C.presion_arterial, C.edad \
                            FROM Pacientes P \
                            INNER JOIN Citas C \
                            ON P.id_paciente = C.id_paciente \
                            WHERE fecha_cita BETWEEN ? AND ?", fechas, conn)
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
        
        # Extracción datos de citas realizadas
        print('\n************************************************************************************************************')
        print(f'Reporte de citas entre {_fecha_inicial} y {_fecha_final}')
        print('\n************************************************************************************************************')
        print('Clave_paciente  1er_Apellido  2do_Apellido          Nombre         Fecha_nacimiento   Sexo     Folio_cita     Fecha_cita     Turno     Hora_llegada  Peso_kg   Estatura_cm  Presion_arterial  Edad ')
        for cita in citas_encontradas:
          # Acceder a datos del paciente
          clave_paciente, primer_apellido, segundo_apellido, nombre, fecha_nacimiento, sexo, id_cita, fecha_cita, turno_cita, hora_llegada, peso_kg, estatura_cm, presion_arterial, edad = cita
          # Impresion
          print(f"{clave_paciente:^14} {primer_apellido:^14} {segundo_apellido:^14} {nombre:^20} {fecha_nacimiento.date().strftime('%m/%d/%Y'):^16}  {sexo:^7}  {id_cita:^15} {fecha_cita.date().strftime('%m/%d/%Y'):^13} {turno_cita:^10} {hora_llegada:^14} {peso_kg:^9} {estatura_cm:^12} {presion_arterial:^16}  {edad:^4} ")
        print('\n************************************************************************************************************')
        
        break
      
    # REPORTE DE CITAS POR PACIENTE
    if op_periodo_paciente == 'B':
      while True:
        _clave_paciente = input('Ingresa la clave del paciente\n').strip()
        if _clave_paciente.upper() == '*':
          break
        # 1
        if not _clave_paciente:  
          print("Opción no se puede omitir. Inténtelo de nuevo. [*]: Cancelar operación")
          continue
        # 2
        try:
          clave_paciente = int(_clave_paciente)
        except Exception:
          print("La clave solo puede contener datos numéricos enteros. Intenta de nuevo. [*]: Cancelar operación\n")
          continue
        # 3
        try:
          with sqlite3.connect('Consultorio.db',
                                detect_types = sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES) as conn:
            cursor = conn.cursor()
            # peso_kg, estatura_cm 
            cursor.execute("SELECT * FROM Pacientes WHERE id_paciente = ?", (clave_paciente,))
            paciente_buscado = cursor.fetchone()
            # df_citas_encontradas = pd.read_sql("SELECT * FROM Pacientes WHERE id_paciente = ?", (clave_paciente,), conn)
            
            cursor.execute("SELECT id_cita, fecha_cita, turno_cita, hora_llegada, peso_kg, estatura_cm, presion_arterial, edad FROM Citas WHERE id_paciente = ?", (clave_paciente,))
            citas_encontradas = cursor.fetchall()

        except sqlite3.Error as e:
          print(e)
        except:
            print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
        finally:
            if (conn):
                conn.close()
        
        if not paciente_buscado:
          print('\nEl paciente no está registrado. [*]: Cancelar operación')
          continue
        
        if not citas_encontradas:
          print('\nNo existen citas registradas para el paciente.')
          break
        
        # Impresión datos del paciente
        clave_paciente, primer_apellido, segundo_apellido, nombre, fecha_nacimiento, sexo = paciente_buscado
        print('\n**********************************************************************************')
        print('Clave_paciente  1er_Apellido  2do_Apellido          Nombre         Fecha_nacimiento   Sexo')
        print(f"{clave_paciente:^14} {primer_apellido:^14} {segundo_apellido:^14} {nombre:^20} {fecha_nacimiento.date().strftime('%m/%d/%Y'):^16}  {sexo:^7}") 
        print('\n**********************************************************************************')
        
        # Impresión de citas posibles
        print('Folio_cita     Fecha_cita     Turno     Hora_llegada  Peso_kg   Estatura_cm  Presion_arterial  Edad ') 
        for cita in citas_encontradas:
          folio_cita, fecha_cita, turno_cita, hora_llegada, peso_kg, estatura_cm, presion_arterial, edad = cita
          print(f"{folio_cita:^11}   {fecha_cita.date().strftime('%m/%d/%Y'):^13} {turno_cita:^10} {hora_llegada:^14} {peso_kg:^9} {estatura_cm:^12} {presion_arterial:^16}  {edad:^4} ")
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
          
    # Obtención de pacientes
    try:
      with sqlite3.connect('Consultorio.db',
                            detect_types = sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Pacientes")
        pacientes = cursor.fetchall()  
        df = pd.read_sql('SELECT * FROM Pacientes', conn) #Importante imprime nombre cols
    except sqlite3.Error as e:
      print(e)
    except:
        print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
    finally:
        if (conn):
            conn.close()
            
    # LISTADO COMPLETO DE PACIENTES
    if op_listado_busqueda == 'A':
      # 1
      if not pacientes:
        print('\nNo hay pacientes registrados en el sistema.')
        continue
      
      # Impresion de resultados
      # print(df)
      print('\n********************************************************************************************')
      print(f'Información de los pacientes registrados')
      print('Clave_paciente  1er_Apellido  2do_Apellido          Nombre         Fecha_nacimiento   Sexo')
      for paciente in pacientes:
          clave_paciente, primer_apellido, segundo_apellido, nombre, fecha_nacimiento, sexo = paciente
          print(f"{clave_paciente:^14} {primer_apellido:^14} {segundo_apellido:^14} {nombre:^20} {fecha_nacimiento.date().strftime('%m/%d/%Y'):^16}  {sexo:^7}") 
      print('********************************************************************************************')

      # Exportación
      op_export = mostrar_menu({'A':'Excel', 'B':'CSV', 'X':'No exportar'}, '¿Deseas exportar la información mostrada a un archivo de Excel o CSV?')
      if op_export == 'A':
        df.to_excel('output.xlsx', index=False)
      elif op_export == 'B':
        df.to_csv('output.csv', index=False)
        

    # BÚSQUEDA POR CLAVE DE PACIENTE
    if op_listado_busqueda == 'B':
      while True:
        _clave_paciente = input('Ingresa la clave del paciente a buscar\n').strip()
        if _clave_paciente.upper() == '*':
          break
        # 1
        if not _clave_paciente: # Si está vacío
          print("Opción no se puede omitir. Intenta de nuevo. [*]: Cancelar operación")
          continue
        # 2
        try:
          clave_paciente = int(_clave_paciente)
        except Exception:
          print("La clave solo puede contener datos numéricos enteros. Intenta de nuevo. [*]: Cancelar operación\n")
          continue
        # 3
        if clave_paciente not in [id_paciente for id_paciente, _, _, _, _, _ in pacientes]:
          print('\nEl paciente no está registrado. [*]: Cancelar operación')
          break
        
        try:
          with sqlite3.connect('Consultorio.db',
                                detect_types = sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Pacientes WHERE id_paciente = ?", (clave_paciente,))
            paciente_buscado = cursor.fetchone()     
            df_paciente_buscado = pd.read_sql('SELECT * FROM Pacientes WHERE id_paciente = ?', (clave_paciente,), conn)
        except sqlite3.Error as e:
          print(e)
        except:
            print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
        finally:
            if (conn):
                conn.close()
        
        print('\n***************************************************************************************************************')
        print(f'Información del paciente')
        clave_paciente, primer_apellido, segundo_apellido, nombre, fecha_nacimiento, sexo = paciente_buscado
        print('Clave_paciente  1er_Apellido  2do_Apellido          Nombre         Fecha_nacimiento   Sexo')
        print(f"{clave_paciente:^14} {primer_apellido:^14} {segundo_apellido:^14} {nombre:^20} {fecha_nacimiento.date().strftime('%m/%d/%Y'):^16}  {sexo:^7}") 
        print('*****************************************************************************************************************')
        
        # Exportación
        op_export = mostrar_menu({'A':'Excel', 'B':'CSV', 'X':'No exportar'}, '¿Deseas exportar la información mostrada a un archivo de Excel o CSV?')
        if op_export == 'A':
          df_paciente_buscado.to_excel('info_paciente.xlsx', index=False)
        elif op_export == 'B':
          df_paciente_buscado.to_csv('info_paciente.csv', index=False)
        
        # Expediente clínico ------------------------------------------------------------------------------------------------------------------------------------------------------
        op_expediente = elegir_opcion('\n¿Deseas consultar el expediente clínico del paciente? S/N\n', 'SN')
        if op_expediente == 'N':
          break
        
        try:
          with sqlite3.connect('Consultorio.db',
                                detect_types = sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id_cita, fecha_cita, turno_cita, hora_llegada, peso_kg, estatura_cm, presion_arterial, diagnostico, edad FROM Citas WHERE id_paciente = ?", (clave_paciente,))
            expediente = cursor.fetchall()     
            df_citas_paciente_buscado = pd.read_sql('SELECT id_cita, fecha_cita, turno_cita, hora_llegada, peso_kg, estatura_cm, presion_arterial, diagnostico, edad FROM Citas WHERE id_paciente = ?', (clave_paciente,), conn)
        except sqlite3.Error as e:
          print(e)
        except:
            print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
        finally:
            if (conn):
                conn.close()
                
        # Impresión de las citas posibles
        print('\n******************************************************************************************************************************************')
        print('Folio_cita     Fecha_cita     Turno     Hora_llegada  Peso_kg   Estatura_cm  Presion_arterial   Edad           Diagnóstico         ') 
        for cita in expediente:
          id_cita, fecha_cita, turno_cita, hora_llegada, peso_kg, estatura_cm, presion_arterial, diagnostico, edad = cita
          # DIAGNÓSTICO Separa texto en renglones y los añade a una lista
          renglones = [diagnostico[i:i+20] for i in range(0, len(diagnostico), 20)]
          # Hace un parrafo
          parrafo = f'\n{" "*107}'.join(renglones)
          print(f"{id_cita:^11}   {fecha_cita.date().strftime('%m/%d/%Y'):^13} {turno_cita:^10} {hora_llegada:^14} {peso_kg:^9} {estatura_cm:^12} {presion_arterial:^16}   {edad:^4}       {parrafo:^22}")
        print('******************************************************************************************************************************************')
        
        
        # Exportación
        op_export = mostrar_menu({'A':'Excel', 'B':'CSV', 'X':'No exportar'}, '¿Deseas exportar la información mostrada a un archivo de Excel o CSV?')
        if op_export == 'A':
          df_citas_paciente_buscado.to_excel('info_paciente.xlsx', index=False)
        elif op_export == 'B':
          df_citas_paciente_buscado.to_csv('info_paciente.csv', index=False)
        
        break
      

    # BÚSQUEDA POR APELLIDOS Y NOMBRES
    if op_listado_busqueda == 'C':
      flag_salir = False
      while True: 
        # Nombre
        nombre_u = input('Ingresa el nombre\n').title().strip()
        if nombre_u == '*':
          break
        # 1
        if not nombre_u:
          print("\nOpción no se puede omitir. Inténtelo de nuevo. [*]: Cancelar operación")
          continue
        # 2
        if not nombre_u.replace(' ', '').isalpha():
          print('\nError. Solo se aceptan caracteres alfabéticos. Intente de nuevo. [*]: Cancelar operación')
          continue
        
        while True:
          # Primer apellido
          primer_apellido_u = input('Ingresa el primer apellido\n').title().strip()
          if primer_apellido_u == '*':
            flag_salir = True
            break
          # 1
          if not primer_apellido_u:
            print("\nOpción no se puede omitir. Inténtelo de nuevo. [*]: Cancelar operación")
            continue
          # 2
          if not primer_apellido_u.replace(' ', '').isalpha():
            print('\nError. Solo se aceptan caracteres alfabéticos. Intente de nuevo. [*]: Cancelar operación')
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
            print('\nError. Solo se aceptan caracteres alfabéticos. Intente de nuevo. [*]: Cancelar operación')
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
            paciente_buscado = cursor.fetchone()     
            df_paciente_buscado = pd.read_sql("SELECT * FROM Pacientes WHERE primer_apellido = ? AND segundo_apellido = ? AND nombre = ?;", (primer_apellido_u, segundo_apellido_u, nombre_u), conn)
            
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
        
        clave_paciente, primer_apellido, segundo_apellido, nombre, fecha_nacimiento, sexo = paciente_buscado
        print('\n**********************************************************************************')
        print(f'Información del paciente')
        print('Clave_paciente  1er_Apellido  2do_Apellido          Nombre         Fecha_nacimiento   Sexo')
        print(f"{clave_paciente:^14} {primer_apellido:^14} {segundo_apellido:^14} {nombre:^20} {fecha_nacimiento.date().strftime('%m/%d/%Y'):^16}  {sexo:^7}") 
        print('**********************************************************************************')
        
        # Expediente clínico ------------------------------------------------------------------------------------------------------------------------------------------------------
        op_expediente = elegir_opcion('\n¿Deseas consultar el expediente clínico del paciente? S/N\n', 'SN')
        if op_expediente == 'N':
          break
        
        try:
          with sqlite3.connect('Consultorio.db',
                                detect_types = sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES) as conn:
            conn.execute("PRAGMA foreign_keys=1")
            cursor = conn.cursor()
            cursor.execute("SELECT id_cita, fecha_cita, turno_cita, hora_llegada, peso_kg, estatura_cm, presion_arterial, diagnostico, edad \
                            FROM Citas \
                            WHERE id_paciente = ? AND peso_kg != 'NA'", (clave_paciente,))
            expediente = cursor.fetchall()
            df_citas_apellidos = pd.read_sql("SELECT id_cita, fecha_cita, turno_cita, hora_llegada, peso_kg, estatura_cm, presion_arterial, diagnostico, edad \
                            FROM Citas \
                            WHERE id_paciente = ? AND peso_kg != 'NA'", (clave_paciente,), conn)
        except sqlite3.Error as e:
          print(e)
        except:
            print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
        finally:
            if (conn):
                conn.close()
                
                
        print('\n******************************************************************************************************************************************')
        print('Folio_cita     Fecha_cita     Turno     Hora_llegada  Peso_kg   Estatura_cm  Presion_arterial   Edad           Diagnóstico         ') 
        for cita in expediente:
          folio_cita, fecha_cita, turno_cita, hora_llegada, peso_kg, estatura_cm, presion_arterial, diagnostico, edad = cita
          # DIAGNÓSTICO Separa texto en renglones y los añade a una lista
          renglones = [diagnostico[i:i+20] for i in range(0, len(diagnostico), 20)]
          # Hace un parrafo
          parrafo = f'\n{" "*107}'.join(renglones)
          print(f"{folio_cita:^11}   {fecha_cita.date().strftime('%m/%d/%Y'):^13} {turno_cita:^10} {hora_llegada:^14} {peso_kg:^9} {estatura_cm:^12} {presion_arterial:^16}   {edad:^4}       {parrafo:^22}")
        print('******************************************************************************************************************************************')
        
        # Exportación
        op_export = mostrar_menu({'A':'Excel', 'B':'CSV', 'X':'No exportar'}, '¿Deseas exportar la información mostrada a un archivo de Excel o CSV?')
        if op_export == 'A':
          df_citas_apellidos.to_excel('info_paciente.xlsx', index=False)
        elif op_export == 'B':
          df_citas_apellidos.to_csv('info_paciente.csv', index=False)
          
          
      # ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # SALIR AL MENÚ ANTERIOR
    if op_listado_busqueda == 'X':
      break
    
    
    
def estadisticos_demograficos():
  while True:
    op_edad_sexo = mostrar_menu({ 'A':'Por edad', 
                                  'B':'Por sexo',
                                  'C':'Por edad y sexo',
                                  'X':'Volver al menú anterior'})
    # POR EDAD
    if op_edad_sexo == 'A':
      flag_salir = False
      # Edad inicial
      while True:
        _edad_inicial = input("Ingresa la edad inicial del rango\n").strip()
        if _edad_inicial.upper() == '*':
          break
        # 1
        if not _edad_inicial:
          print("\nOpción no se puede omitir. Inténtelo de nuevo. [*]: Cancelar operación")
          continue
        # 2
        try:
          edad_inicial = int(_edad_inicial)
        except Exception:
          print('\nLa edad debe ser de dato numérico tipo entero. Intenta de nuevo. [*]: Cancelar operación')
          continue
        # 3
        if edad_inicial <= 0:
          print("\nLa edad no puede ser menor o igual a 0. Inténtelo de nuevo. [*]: Cancelar operación")
          continue
      
        # Edad final
        while True:
          _edad_final = input("Ingresa la edad final del rango\n").strip()
          if _edad_final.upper() == '*':
            flag_salir = True
            break
          # 1
          if not _edad_final:
            print("\nOpción no se puede omitir. Inténtelo de nuevo. [*]: Cancelar operación")
            continue
          # 2
          try:
            edad_final = int(_edad_final)
          except Exception:
            print('\nLa edad debe ser de dato numérico tipo entero. Intenta de nuevo. [*]: Cancelar operación')
            continue
          # 3
          if edad_final <= 0:
            print("\nLa edad no puede ser menor o igual a 0. Inténtelo de nuevo. [*]: Cancelar operación")
            continue
          break
        if flag_salir == True:
          break
        
        # Rango de edad
        edad_rango = (edad_inicial, edad_final)
        
        # Búsqueda de peso y estatura por rango de edad
        try:
          with sqlite3.connect('Consultorio.db',
                                detect_types = sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES) as conn:
            conn.execute("PRAGMA foreign_keys=1")
            cursor = conn.cursor()
            # peso_kg, estatura_cm 
            cursor.execute("SELECT peso_kg, estatura_cm, presion_arterial \
                            FROM Citas \
                            WHERE edad BETWEEN ? AND ?", (edad_rango))
            peso_estatura_presion_edad = cursor.fetchall()
            # print(peso_estatura_presion_edad)
        except sqlite3.Error as e:
          print(e)
        except:
            print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
        finally:
            if (conn):
                conn.close()
        
        if not peso_estatura_presion_edad:
          print('\nNo existen datos para analizar con ese rango de edad.')
          break
        
        print(f'\nDatos demográficos para el rango de edad de {edad_inicial} a {edad_final}\n')
        peso_estatura_presion_edad_lista = []
        for peso, estatura, presion_arterial in peso_estatura_presion_edad:
          peso = float(peso) 
          estatura = float(estatura)
          sistolica, diastolica = presion_arterial.split('/')
          sistolica = int(sistolica)
          diastolica = int(diastolica)
          
          peso_estatura_presion_edad_lista.append((peso, estatura, sistolica, diastolica))
          
        # Conversión a dataframe
        df = pd.DataFrame(peso_estatura_presion_edad_lista, columns=['Peso', 'Estatura', 'Sistolica', 'Diastolica'])
        # Análisis de datos
        peso_estatura_presion_edad_medidas = df[['Peso', 'Estatura', 'Sistolica', 'Diastolica']].describe().loc[['count', 'min', 'max', 'mean', '50%', 'std']]
        peso_estatura_presion_edad_medidas = peso_estatura_presion_edad_medidas.rename(index={'count': 'Conteo', 'min': 'Mínimo', 'max': 'Máximo', 'mean': 'Media', '50%': 'Mediana', 'std': 'Desviación estándar'})
        # Impresión
        print(peso_estatura_presion_edad_medidas.round(2))
        
        break

    # POR SEXO
    elif op_edad_sexo == 'B':
      # Sexo
      
      # Impresión de peso, estatura, presion sistólica y diastólica por sexo
      try:
        with sqlite3.connect('Consultorio.db',
                              detect_types = sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES) as conn:
          conn.execute("PRAGMA foreign_keys=1")
          cursor = conn.cursor()
          cursor.execute("SELECT C.peso_kg, C.estatura_cm, C.presion_arterial \
                          FROM Citas C\
                          INNER JOIN Pacientes P \
                          ON C.id_paciente = P.id_paciente \
                          WHERE peso_kg != 'NA' AND P.sexo = ?", ('H',))
          sexo_H = cursor.fetchall()
          
          cursor.execute("SELECT C.peso_kg, C.estatura_cm, C.presion_arterial \
                          FROM Citas C\
                          INNER JOIN Pacientes P \
                          ON C.id_paciente = P.id_paciente \
                          WHERE peso_kg != 'NA' AND P.sexo = ?", ('M',))
          sexo_M = cursor.fetchall()

          cursor.execute("SELECT C.peso_kg, C.estatura_cm, C.presion_arterial \
                          FROM Citas C\
                          INNER JOIN Pacientes P \
                          ON C.id_paciente = P.id_paciente \
                          WHERE peso_kg != 'NA' AND P.sexo = ?", ('N',))
          sexo_N = cursor.fetchall()
      except sqlite3.Error as e:
        print(e)
      except:
          print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
      finally:
          if (conn):
              conn.close()
      
      # Conversión texto a float
      # sexo_H = [(float(peso), float(estatura), presion_arterial) for peso, estatura, presion_arterial in sexo_H]
      variables_sexo_dict = {'Hombre':sexo_H, 'Mujer':sexo_M, 'No contesto':sexo_N}
      
      for sexo_nombre, datos in variables_sexo_dict.items():
        if not datos:
          break
        peso_estatura_presion_lista = []
        print(f'\n{sexo_nombre}')
        for peso, estatura, presion_arterial in datos:
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
      
      
    # POR EDAD Y SEXO
    elif op_edad_sexo == 'C':
      flag_salir = False
      # Edad inicial
      while True:
        _edad_inicial = input("Ingresa la edad inicial del rango\n").strip()
        if _edad_inicial.upper() == '*':
          break
        # 1
        if not _edad_inicial:
          print("\nOpción no se puede omitir. Inténtelo de nuevo. [*]: Cancelar operación")
          continue
        # 2
        try:
          edad_inicial = int(_edad_inicial)
        except Exception:
          print('\nLa edad debe ser de dato numérico tipo entero. Intenta de nuevo. [*]: Cancelar operación')
          continue
        # 3
        if edad_inicial <= 0:
          print("\nLa edad no puede ser menor o igual a 0. Inténtelo de nuevo. [*]: Cancelar operación")
          continue
        
        # Edad final
        while True:
          _edad_final = input("Ingresa la edad final del rango\n").strip()
          if _edad_final.upper() == '*':
            flag_salir = True
            break
          # 1
          if not _edad_final:
            print("\nOpción no se puede omitir. Inténtelo de nuevo. [*]: Cancelar operación")
            continue
          # 2
          try:
            edad_final = int(_edad_final)
          except Exception:
            print('\nLa edad debe ser de dato numérico tipo entero. Intenta de nuevo. [*]: Cancelar operación')
            continue
          # 3
          if edad_final <= 0:
            print("\nLa edad no puede ser menor o igual a 0. Inténtelo de nuevo. [*]: Cancelar operación")
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
            print('\nOpción no se puede omitir. Intenta de nuevo. [*]: Cancelar operación')
            continue
          # 2
          if not sexo.isalpha():
            print('\nSolo ingresar caracteres alfabéticos. Intenta de nuevo. [*]: Cancelar operación')
            continue
          # 3
          if sexo not in ['H', 'M', 'N']:
            print('\nOpción inválida. Intenta de nuevo. [*]: Cancelar operación')
            continue
          break
        if flag_salir == True:
          break

        # Rango de edad
        edad_sexo_tupla = (edad_inicial, edad_final, sexo)
        
        # Búsqueda de peso y estatura por sexo
        try:
          with sqlite3.connect('Consultorio.db',
                                detect_types = sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES) as conn:
            conn.execute("PRAGMA foreign_keys=1")
            cursor = conn.cursor()
            # peso_kg, estatura_cm, Pacientes 
            cursor.execute("SELECT C.peso_kg, C.estatura_cm, C.presion_arterial \
                            FROM Citas C \
                            INNER JOIN Pacientes P \
                            ON C.id_paciente = P.id_paciente \
                            WHERE C.edad BETWEEN ? AND ? \
                            AND P.sexo = ?;", (edad_sexo_tupla))
            peso_estatura_presion_edad_sexo = cursor.fetchall()
            print(peso_estatura_presion_edad_sexo)
        except sqlite3.Error as e:
          print(e)
        except:
            print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
        finally:
            if (conn):
                conn.close()
                
                
        if not peso_estatura_presion_edad_sexo:
          print('\nNo existen datos para analizar con ese rango de edad y sexo.')
          break
        
        if sexo == 'H':
          sexo = 'Masculino'
        if sexo == 'M':
          sexo = 'Femenino'
        if sexo == 'N':
          sexo = 'Sin contestar'
        
        print(f'\nDatos demográficos para el rango de edad de {edad_inicial} a {edad_final} y sexo: {sexo}\n')
        peso_estatura_presion_edad_sexo_lista = []
        for peso, estatura, presion_arterial in peso_estatura_presion_edad_sexo:
          peso = float(peso) 
          estatura = float(estatura)
          sistolica, diastolica = presion_arterial.split('/')
          sistolica = int(sistolica)
          diastolica = int(diastolica)
          
          peso_estatura_presion_edad_sexo_lista.append((peso, estatura, sistolica, diastolica))
          
        # Conversión a dataframe
        df = pd.DataFrame(peso_estatura_presion_edad_sexo_lista, columns=['Peso', 'Estatura', 'Sistolica', 'Diastolica'])
        # Análisis de datos
        peso_estatura_presion_edad_sexo_medidas = df[['Peso', 'Estatura', 'Sistolica', 'Diastolica']].describe().loc[['count', 'min', 'max', 'mean', '50%', 'std']]
        peso_estatura_presion_edad_sexo_medidas = peso_estatura_presion_edad_sexo_medidas.rename(index={'count': 'Conteo', 'min': 'Mínimo', 'max': 'Máximo', 'mean': 'Media', '50%': 'Mediana', 'std': 'Desviación estándar'})
        # Impresión
        print(peso_estatura_presion_edad_sexo_medidas.round(2))
        
        break
      
    elif op_edad_sexo == 'X':
      break



def guardar_csv(diccionario:dict, encabezados, nombre_archivo):
  with open(nombre_archivo, 'w', encoding='latin1', newline='') as archivo:
    grabador = csv.writer(archivo)
    grabador.writerow(encabezados)
    for clave, datos in diccionario.items():
        grabador.writerows([[clave] + [dato for dato in datos]])


# def leer_csv(nombre_archivo):
#     datos = {}
#     try:
#       with open(nombre_archivo, 'r', encoding='latin1', newline='') as archivo:
#         lector = csv.reader(archivo)
#         next(lector)
#         for renglon in lector:
#           # datos[renglon[0]] = [renglon[i] for i in range(1, len(renglon))]
#           datos[int(renglon[0])] = [int(renglon[1]) if renglon[1].isdigit() else dato for dato in renglon[1:]]
#     except FileNotFoundError:
#         print(f"El archivo {nombre_archivo} no se encontró, se procede a trabajar con un conjunto vacío")
#         return dict()
#     except csv.Error as fallo_csv:
#         print(f"Ocurrió un error al leer el archivo: {fallo_csv}")
#     except Exception:
#         Excepcion = sys.exc_info()
#         print(f"Ocurrió un problema del tipo: {Excepcion[0]}")
#         print(f"Mensaje del error: {Excepcion[1]}")
#     else:
#         return datos

# PROGRAMA PRINCIPAL
# Lecturas
# pacientes = leer_csv('pacientes.csv')
# if pacientes:
#   print('Datos cargados de pacientes.csv ...')

# citas = leer_csv('citas.csv')
# if citas:
#   print('Datos cargados de citas.csv ...')

# citas_realizadas = leer_csv('citas_realizadas.csv')
# if citas_realizadas:
#   print('Datos cargados de citas_realizadas.csv ...')
  
while True:
  op_principal = mostrar_menu(menu_principal, '\nSistema de gestión de pacientes de un consultorio')
  match op_principal:
    case 'A':
      registro_pacientes()
    case 'B':
      citas_crear_realizar_cancelar_menu()
      # if not pacientes:
      #   print('\nDebe haber al menos un paciente registrado para entrar al menú de citas.')
      # else:
      #   citas_crear_realizar_cancelar()
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