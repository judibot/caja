import sqlite3
import os
import time


'''
                                        CAJA 2.0
    En esta version, se encuentra la funcion "cerrar caja", donde se puede hacer un recuento local de lo que
    se recaudó en el dia de la fecha.
    Es importante entender que la caja es local, por lo tanto una vez cerrado el programa, se perderan los datos 

'''

cuentas = []*2                              
cajaFinal = 0.0 
cliente = 0

def limpiar():
    os.system('cls')

def conectar():
    return sqlite3.connect("productos.db")

def crear_tabla():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS productos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        precio REAL NOT NULL)
    """)
    conn.commit()
    conn.close()

def agregar_producto(nombre, precio):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO productos (nombre, precio) VALUES (?, ?)", (nombre, precio))
    conn.commit()
    conn.close()
    print('.- Producto ',nombre, ' agregado correctamente.')

def mostrar_productos():
    limpiar()
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM productos")
    productos = cursor.fetchall()
    conn.close()

    if not productos:
        print("⚠ No hay productos en la base de datos.")
        return

    print("\n📜 Lista de productos:")
    for i in productos:
        print(f"ID: {i[0]}")
        print(f"Nombre: {i[1]}")
        print(f"Precio: ${i[2]:.2f}")
        print("-" * 20)  # Separador entre productos
    print('.- Presioná cualquier tecla para voler al menú')
    os.system('pause>nul') 
    menu()

def nueva_cuenta():
    global cliente
    global cuentas
    cliente += 1
    conn = conectar()
    cursor = conn.cursor()
    print('CLIENTE NRO.: ', cliente)             ## Contamos cliente #
    subtotal = 0                                    ## Inicializamos subtotal
    idProd = input('.- Ingrese el ID del producto para sumar (0 para finalizar): ')
    while idProd != "0":  
        cursor.execute("SELECT nombre, precio FROM productos WHERE id = ?", (idProd,))
        producto = cursor.fetchone()

        if producto is None:
            print("⚠ Producto no encontrado.")
            idProd = input('.- Ingrese el ID del producto para sumar (0 para finalizar) ')
        else:
            nombreProd, precioProd = producto  # Extraemos nombre y precio
            precioProd = float(precioProd)  # Convertimos el precio a número
            
            print(f'nombre: {nombreProd}')
            print(f'precio: ${precioProd:.2f}')

            subtotal += precioProd  # Sumamos al subtotal

            print('-----')
            print(f'Subtotal: ${subtotal:.2f}')

            idProd = input('.- Ingrese el ID del producto para sumar (0 para finalizar): ')

    limpiar()
    print(f'TOTAL: ${subtotal:.2f}')   
    print(f' !--- Desea guardar la cuenta: Cliente nro: {cliente} , Total: ${subtotal} --- ?  ')
    op = input('S/N: ').lower()
    if op == 's':
        limpiar()
        cuentas.append([cliente, subtotal])
        print('--- CUENTA GUARDADA ---')
        time.sleep(4)
    elif op == 'n':
        limpiar()
        cliente -= 1
        print('X--- CUENTA ANULADA ---X') 
        time.sleep(4)

def cerrar_caja():
    global cuentas
    global cajaFinal
    limpiar()
    cajaFinal = 0.0
    for cuenta in cuentas:
        total += cuenta[1]
    print(f'Vallor total de la caja: ${total}')   
    print('Presiona cualquier tecla para volver al menu')
    os.system('pause>nul')

def menu():
    while True:
        limpiar()
        print("\n💰 SISTEMA DE CAJA REGISTRADORA")
        print(" 1- Agregar producto")
        print(" 2- Ver productos")
        print(' 3- Nueva cuenta')
        print(' 4- Cerrar caja')
        print(" 0- Salir")
        
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            nombre = input("Ingrese el nombre del producto: ")
            precio = float(input("Ingrese el precio: "))
            agregar_producto(nombre, precio)
        elif opcion == "2":
            mostrar_productos()
        elif opcion == "3":
            nueva_cuenta()
        elif opcion == "4":
            cerrar_caja()
        elif opcion == "0":
            print("👋 Saliendo del programa...")
            break
        else:
            print("❌ Opción inválida, intente nuevamente.")

crear_tabla()           # se ejecuta al principio para chequear que exista la tabla
menu()