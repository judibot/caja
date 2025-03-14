import sqlite3
import os
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
    os.system('pause>nul')
    print('.- Presioná cualquier tecla para voler al menú')
    menu()
def nueva_cuenta():
    cliente = 0
    conn = conectar()
    cursor = conn.cursor()
    print('CLIENTE NRO.: ', cliente +1)
    subtotal = 0  # Inicializamos subtotal
    idProd = idProd = input('.- Ingrese el ID del producto para sumar (0 para finalizar): ')
    while idProd != "0":  
        cursor.execute("SELECT nombre, precio FROM productos WHERE id = ?", (idProd,))
        producto = cursor.fetchone()

        if producto is None:
            print("⚠ Producto no encontrado.")
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
    os.system('pause')


def menu():
    while True:
        limpiar()
        print("\n💰 SISTEMA DE CAJA REGISTRADORA")
        print("1️⃣ Agregar producto")
        print("2️⃣ Ver productos")
        print('3 Nueva cuenta')
        print("0 Salir")
        
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            nombre = input("Ingrese el nombre del producto: ")
            precio = float(input("Ingrese el precio: "))
            agregar_producto(nombre, precio)
        elif opcion == "2":
            mostrar_productos()
        elif opcion == "3":
            nueva_cuenta()
        elif opcion == "0":
            print("👋 Saliendo del programa...")
            break
        else:
            print("❌ Opción inválida, intente nuevamente.")

crear_tabla()           # se ejecuta al principio para chequear que exista la tabla
menu()