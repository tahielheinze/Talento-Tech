# Importar el módulo Colorama.
from colorama import Fore, Style, Back

# Importar el módulo SQLite3.
import sqlite3

#! ----- FUNCIONES -----

# Crear la base de datos.
def iniciar_db():
    try:
        # Conectar la base de datos.
        conexion = sqlite3.connect('inventario.db')
        cursor = conexion.cursor()
        
        # Crear la tabla con las columnas y el tipo de dato que se ingresa.
        cursor.execute('''
            create table productos (
                ID Integer Primary Key Autoincrement,
                Nombre Text Not Null,
                Descripcion Text,
                Cantidad Integer Not Null,
                Precio Real Not Null,
                Categoria Text
            )
        ''')

        # Confirmar los cambios realizados y cerrar la conexión.
        conexion.commit()
        conexion.close()
        print(f" {Fore.GREEN}Base de Datos Inicializada correctamente.{Style.RESET_ALL}")
        
    except sqlite3.Error as e:
        print(f"{Fore.RED}ERROR al inicializar la Base de Datos: {e}{Style.RESET_ALL}")


# Conectarse a la base de datos.
def conectar_db():
    # Retorna una conexion con la base de datos.
    try:
        return sqlite3.connect('inventario.db')
    except sqlite3.Error as e:
        print(f"{Fore.RED}ERROR al conectar a la base de datos: {e}{Style.RESET_ALL}")
        return None


# Insertar productos de ejemplo.
def insertar_productos_principales():
    conexion = conectar_db()
    if conexion:
        cursor = conexion.cursor()
        # Verificar si ya existen productos.
        cursor.execute("SELECT COUNT(*) FROM Productos")
        cantidad = cursor.fetchone()[0]
        
        # Agregar productos si no existe alguno.
        if cantidad == 0:
            productos_principales = [
                ("Manzana", "Fruta fresca y jugosa", 50, 100.0, "Fruta"),
                ("Pera", "Pera dulce de temporada", 30, 200.0, "Fruta"),
                ("Naranja", "Naranja cítrica", 40, 300.0, "Fruta"),
                ("Uva", "Uva morada", 25, 400.0, "Fruta"),
                ("Banana", "Banana amarilla", 60, 500.0, "Fruta")
            ]
            
            cursor.executemany('''
                INSERT INTO Productos (nombre, descripcion, cantidad, precio, categoria)
                VALUES (?,?,?,?,?)
            ''', productos_principales)
            
            conexion.commit()
            print("Productos de ejemplo agregados.")
            
            conexion.close()


# Mostrar el menu al ejecutar el programa.
def mostrar_menu():
    print("┌────────────────────────────────────────────────────────────────┐")
    print("│                      GESTIÓN DE PRODUCTOS                      │")
    print("│────────────────────────────────────────────────────────────────│")
    print("│ 1. Agregar Productos.                                          │")
    print("│ 2. Visualizar Lista de Productos.                              │")
    print("│ 3. Actualizar Producto por ID.                                 │")
    print("│ 4. Eliminar Producto por ID.                                   │")
    print("│ 5. Buscar Producto por ID.                                     │")
    print("│ 6. Reporte de Stock Bajo.                                      │")
    print("│ 7. Salir del programa.                                         │")
    print("└────────────────────────────────────────────────────────────────┘")


# Valida que el nombre no se encuentre en la DB.
def validar_nombre_producto():
    while True:
        nombre = str(input("Ingrese el nombre del producto: ")).strip()
        if nombre == "":
            print(f"{Fore.RED}El nombre del producto no puede estar vacío.{Style.RESET_ALL}")
            continue
        
        # Veerificar que no este duplicado en la DB.
        conexion = conectar_db()
        if conexion:
            cursor = conexion.cursor()
            cursor.execute("SELECT COUNT(*) FROM productos WHERE LOWER(nombre) = LOWER(?)", (nombre,))
            existe = cursor.fetchone()[0] > 0
            conexion.close()
            
            if existe:
                print(f"El producto {nombre} ya se encuentra agregado.")
                continue
        return nombre.capitalize() #Regresa el nombre ya validado en formato Capitalize.

# Validar nombre al actualizarlo
def validar_nombre_actualizado():
    while True:
        nombre = str(input(f"El producto {nombre} ya se encuentra agregado."))
        if nombre == "":
            print(f"{Fore.RED}El nombre del producto no puede estar vacío.{Style.RESET_ALL}")
            continue
        return nombre.capitalize()


# Valida la descripción del producto.
def validar_descripcion():
    descripcion = str(input("Ingrese una descripción del producto: ")).strip()
    return descripcion if descripcion else "Sin descripción"


# Valida que la cantidad ingresada del producto sea un número entero positivo.
def validar_cantidad():
    while True:
        try:
            cantidad = int(input("Ingrese una cantidad del producto: "))
            if cantidad <= 0:
                print("La cantidad del producto debe ser un número entero positivo.")
                continue
            return cantidad
        except ValueError:
            print(f"{Fore.RED}El valor ingresado no es valido, ingrese un número entero positivo.{Style.RESET_ALL}")


#Validar la categoria del producto.
def validar_categoria():
    while True:
        categoria = input("Ingrese a la categoría que pertenece el producto: ").strip()
        if categoria == "":
            print("La categoría del producto no puede estar vacía.")
            continue
        return categoria.capitalize() #Regresa la categoria ya validada en formato Capitalize.


#Validar el precio, sin centavos, y que sea un digito.
def validar_precio():
    while True:
        try: #Bloque Try para que el programa corra esta parte del código más probable a dar error.
            precio = int(input("Ingrese un precio al producto: $"))
            if precio <= 0:
                print("El precio del producto debe ser mayor que 0 (cero)")
                continue
            return precio
        except ValueError:
            print(f"{Fore.RED}El valor ingresado no es admitido, ingrese un número valido.{Style.RESET_ALL}")

# Validar ID del producto.
def validar_id_producto():
    while True:
        try:
            id_producto = int(input("Ingrese el ID del producto: "))
            if id_producto <= 0:
                print(f"{Fore.RED}El ID debe ser un número entero positivo.{Style.RESET_ALL}")
                continue
            return id_producto
        except ValueError:
            print(f"{Fore.RED}El valor ingresado no es valido, ingrese un número entero positivo.{Style.RESET_ALL}")


# Verificar si el ID del producto ya existe.
def existe_producto_con_ID(id_producto):
    conexion = conectar_db()
    if conexion:
        cursor = conexion.cursor()
        cursor.execute("SELECT COUNT(*) FROM Productos WHERE id =?", (id_producto,))
        existe = cursor.fetchone()[0] > 0
        conexion.close()
        return existe
    return False

#Agregar productos a la lista.
def agregar_producto():
    print(f"{Fore.MAGENTA}┌────────────────────────────────────────────────────────────────┐{Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}│                     AGREGAR NUEVO PRODUCTO                     │{Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}└────────────────────────────────────────────────────────────────┘{Style.RESET_ALL}")
    
    #Validar los ingresos de datos llamando a las funciones.
    nombre = validar_nombre_producto()
    descripcion = validar_descripcion()
    cantidad = validar_cantidad()
    precio = validar_precio()
    categoria = validar_categoria()
    
    # Insertar los datos ya validados en la base de datos.
    conexion = conectar_db()
    if conexion:
        try:
            cursor = conexion.cursor()
            cursor.execute('''
                INSERT INTO Productos (nombre, descripcion, cantidad, precio, categoria)
                VALUES (?, ?, ?, ?, ?)
            ''', (nombre, descripcion, cantidad, precio, categoria))
            
            conexion.commit()
    
            #Mensaje de agregado exitoso.
            print("┌────────────────────────────────────────────────────────────────┐")
            print(f"{Fore.GREEN}│                 PRODUCTO AGREGADO EXITOSAMENTE                 │{Style.RESET_ALL}")
            print("│────────────────────────────────────────────────────────────────│")
            print(f"│ Producto: {nombre}")
            print(f"│ Descripción: {descripcion}")
            print(f"│ Cantidad: {cantidad}")
            print(f"│ Precio: ${precio}")
            print(f"│ Categoría: {categoria}")
            print("└────────────────────────────────────────────────────────────────┘")
            
        except sqlite3.Error as e:
            print(f"{Fore.RED}ERROR al agregar el producto: {e}{Style.RESET_ALL}")
        finally:
            conexion.close()


#Visualizar la lista de productos registrados en la base de datos.
def lista_productos():
    conexion = conectar_db()
    if conexion:
        try:
            cursor = conexion.cursor()
            cursor.execute("SELECT * FROM Productos ORDER BY id")
            productos = cursor.fetchall()
            
            if len(productos) == 0:
                print("No hay productos registrados en la base de datos.")
                return
            
            # Mostrar los campos de la tabla
            print("┌─────────────────────────────────────────────────────────────────────────────────┐")
            print("│                              PRODUCTOS REGISTRADOS                              │")
            print("│─────────────────────────────────────────────────────────────────────────────────│")
            print(f"│{"ID": <3}{"Nombre": <15}{"Descripción": <20}{"Cant": <5}{"Precio": <8}{"Categoría": <12}          │")
            print("└─────────────────────────────────────────────────────────────────────────────────┘")
            
            for producto in productos:
                id_prod, nombre, descripcion, cantidad, precio, categoria = producto
                # Si la descripción es muy larga, truncarla para acortarla.
                descrip_corta = descripcion[:17] + "... " if len(descripcion) > 20 else descripcion
                print(f" {id_prod:<3}{nombre:<15}{descrip_corta:<20}{cantidad:<5}${precio:<7}{categoria:<12}")
        except sqlite3.Error as e:
            print(f"{Fore.RED}ERROR al consultar los productos: {e}{Style.RESET_ALL}")
        finally:
            conexion.close()


def actualizar_producto():
    print(f"{Fore.CYAN}┌────────────────────────────────────────────────────────────────┐{Style.RESET_ALL}")
    print(f"{Fore.CYAN}│                     ACTUALIZAR PRODUCTO                        │{Style.RESET_ALL}")
    print(f"{Fore.CYAN}└────────────────────────────────────────────────────────────────┘{Style.RESET_ALL}")
    print("Productos disponibles:")
    lista_productos()
    print()
    
    # Validar ID del producto a actualizar.
    id_producto = validar_id_producto()
    
    # Verificar que el producto existe.
    if not existe_producto_con_ID(id_producto):
        print(f"{Fore.RED}No existe un producto con el ID {id_producto}.{Style.RESET_ALL}")
    
    # Mostrar datos actuales del producto.
    conexion = conectar_db()
    if conexion:
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM productos WHERE id = ?", (id_producto,))
        producto = cursor.fetchone()
        
        print(f"\nDatos actuales del producto ID {id_producto}:")
        print(f"Nombre: {producto[1]}")
        print(f"Descripción: {producto[2]}")
        print(f"Cantidad: {producto[3]}")
        print(f"Precio: ${producto[4]}")
        print(f"Categoría: {producto[5]}")
        print()
    
    # Obtener datos nuevos.
    print("Ingrese los nuevos datos (Presione Enter para mantener los valores actuales): ")
    
    # Validar datos nuevos.
    nombre = input(f"Nuevo nombre [{producto[1]}]: ").strip()
    if nombre == "":
        nombre = producto[1]
    else:
        cursor.execute("SELECT COUNT (*) FROM Productos WHERE LOWER(nombre) = LOWER(?) AND id !=  ?", (nombre, id_producto))
        existe = cursor.fetchone()[0] > 0
        if existe:
            print(f"El nombre '{nombre}' ya existe. Manteniendo nombre actual.")
            nombre = producto[1]
        else:
            nombre = nombre.capitalize()
    
    descripcion = input(f"Nueva descripción [{producto[2]}]: ").strip()
    if descripcion == "":
        descripcion = producto[2]
        
    cantidad_input = input(f"Nueva cantidad [{producto[3]}]: ").strip()
    if cantidad_input == "":
        cantidad = producto[3]
    else:
        try:
            cantidad = int(cantidad_input)
            if cantidad <= 0:
                print("Manteniendo valor actual.")
                cantidad = producto[3]
        except ValueError:
            print("Manteniendo valor actual por valor inválido.")
            cantidad = producto[3]

        precio_input = input(f"Nuevo precio [{producto[4]}]: ").strip()
        if precio_input == "":
            precio = producto[4]
        else:
            try:
                precio = float(precio_input)
                if precio <= 0:
                    print("Manteniendo precio actual por valor inválido.")
                    precio = producto[4]
            except ValueError:
                print("Manteniendo precio actual por valor inválido.")
                precio = producto[4]

        categoria = input(f"Nueva categoría [{producto[5]}]: ").strip()
        if categoria == "":
            categoria = producto[5]
        else:
            categoria = categoria.capitalize()
        
        # Actualizar en la base de datos
        try:
            cursor.execute('''
                UPDATE productos 
                SET nombre = ?, descripcion = ?, cantidad = ?, precio = ?, categoria = ?
                WHERE id = ?
            ''', (nombre, descripcion, cantidad, precio, categoria, id_producto))
            
            conexion.commit()
            
            print("┌────────────────────────────────────────────────────────────────┐")
            print(f"{Fore.GREEN}│                PRODUCTO ACTUALIZADO EXITOSAMENTE               │{Style.RESET_ALL}")
            print("│────────────────────────────────────────────────────────────────│")
            print(f"│ ID: {id_producto}")
            print(f"│ Producto: {nombre}")
            print(f"│ Descripción: {descripcion}")
            print(f"│ Cantidad: {cantidad}")
            print(f"│ Precio: ${precio}")
            print(f"│ Categoría: {categoria}")
            print("└────────────────────────────────────────────────────────────────┘")
            
        except sqlite3.Error as e:
            print(f"{Fore.RED}ERROR al actualizar el producto: {e}{Style.RESET_ALL}")
        finally:
            conexion.close()


# Eliminar producto por ID.
def eliminar_producto():
    print(f"{Fore.RED}┌────────────────────────────────────────────────────────────────┐{Style.RESET_ALL}")
    print(f"{Fore.RED}│                      ELIMINAR PRODUCTO                         │{Style.RESET_ALL}")
    print(f"{Fore.RED}└────────────────────────────────────────────────────────────────┘{Style.RESET_ALL}")
    
    # Mostrar productos disponibles para referencia
    print("Productos disponibles:")
    lista_productos()
    print()
    
    # Validar ID del producto a eliminar
    id_producto = validar_id_producto()
    
    # Verificar que el producto existe
    if not existe_producto_con_ID(id_producto):
        print(f"{Fore.RED}No existe un producto con el ID {id_producto}.{Style.RESET_ALL}")
        return
    
    # Mostrar datos del producto antes de eliminar
    conexion = conectar_db()
    if conexion:
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM productos WHERE id = ?", (id_producto,))
        producto = cursor.fetchone()
        
        print(f"\nProducto a eliminar:")
        print(f"ID: {producto[0]}")
        print(f"Nombre: {producto[1]}")
        print(f"Descripción: {producto[2]}")
        print(f"Cantidad: {producto[3]}")
        print(f"Precio: ${producto[4]}")
        print(f"Categoría: {producto[5]}")
        
        # Confirmar eliminación
        while True:
            confirmacion = input(f"\n¿Está seguro que desea eliminar este producto? (s/n): ").strip().lower()
            if confirmacion in ['s', 'si', 'sí']:
                try:
                    cursor.execute("DELETE FROM productos WHERE id = ?", (id_producto,))
                    conexion.commit()
                    print(f"{Fore.GREEN}Producto eliminado exitosamente.{Style.RESET_ALL}")
                    break
                except sqlite3.Error as e:
                    print(f"{Fore.RED}ERROR al eliminar el producto: {e}{Style.RESET_ALL}")
                    break
            elif confirmacion in ['n', 'no']:
                print("Eliminación cancelada.")
                break
            else:
                print("Respuesta inválida. Ingrese 's' para sí o 'n' para no.")
        
        conexion.close()


# Buscar producto por ID.
def buscar_producto_por_id():
    print(f"{Fore.YELLOW}┌────────────────────────────────────────────────────────────────┐{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}│                    BUSCAR PRODUCTO POR ID                      │{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}└────────────────────────────────────────────────────────────────┘{Style.RESET_ALL}")
    
    # Validar ID del producto a buscar
    id_producto = validar_id_producto()
    
    # Buscar el producto
    conexion = conectar_db()
    if conexion:
        try:
            cursor = conexion.cursor()
            cursor.execute("SELECT * FROM productos WHERE id = ?", (id_producto,))
            producto = cursor.fetchone()
            
            if producto:
                print("┌────────────────────────────────────────────────────────────────┐")
                print(f"{Fore.GREEN}│                    PRODUCTO ENCONTRADO                         │{Style.RESET_ALL}")
                print("│────────────────────────────────────────────────────────────────│")
                print(f"│ ID: {producto[0]}")
                print(f"│ Nombre: {producto[1]}")
                print(f"│ Descripción: {producto[2]}")
                print(f"│ Cantidad: {producto[3]}")
                print(f"│ Precio: ${producto[4]}")
                print(f"│ Categoría: {producto[5]}")
                print("└────────────────────────────────────────────────────────────────┘")
            else:
                print(f"{Fore.RED}No se encontró un producto con el ID {id_producto}.{Style.RESET_ALL}")
                
        except sqlite3.Error as e:
            print(f"{Fore.RED}ERROR al buscar el producto: {e}{Style.RESET_ALL}")
        finally:
            conexion.close()


# Reporte de productos bajos en stock.
def reporte_stock_bajo():
    print(f"{Fore.MAGENTA}┌────────────────────────────────────────────────────────────────┐{Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}│                    REPORTE DE STOCK BAJO                       │{Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}└────────────────────────────────────────────────────────────────┘{Style.RESET_ALL}")
    
    # Solicitar el límite de cantidad
    while True:
        try:
            limite = int(input("Ingrese el límite de cantidad para el reporte: "))
            if limite < 0:
                print("El límite debe ser un número positivo o cero.")
                continue
            break
        except ValueError:
            print("Por favor ingrese un número válido.")
    
    # Consultar productos con stock bajo
    conexion = conectar_db()
    if conexion:
        try:
            cursor = conexion.cursor()
            cursor.execute("SELECT * FROM productos WHERE cantidad <= ? ORDER BY cantidad ASC", (limite,))
            productos = cursor.fetchall()
            
            if productos:
                print(f"\n{Fore.YELLOW}Productos con cantidad igual o inferior a {limite}:{Style.RESET_ALL}")
                print("┌─────────────────────────────────────────────────────────────────────────────────┐")
                print("│                              PRODUCTOS CON STOCK BAJO                           │")
                print("│─────────────────────────────────────────────────────────────────────────────────│")
                print(f"│{"ID": <3}{"Nombre": <15}{"Descripción": <20}{"Cant": <5}{"Precio": <8}{"Categoría": <12}          │")
                print("└─────────────────────────────────────────────────────────────────────────────────┘")
                
                for producto in productos:
                    id_prod, nombre, descripcion, cantidad, precio, categoria = producto
                    descrip_corta = descripcion[:17] + "..." if len(descripcion) > 20 else descripcion
                    # Resaltar productos con cantidad crítica (0-5)
                    if cantidad <= 5:
                        print(f"{Fore.RED} {id_prod:<3}{nombre:<15}{descrip_corta:<20}{cantidad:<5}${precio:<7}{categoria:<12}{Style.RESET_ALL}")
                    else:
                        print(f"{Fore.YELLOW} {id_prod:<3}{nombre:<15}{descrip_corta:<20}{cantidad:<5}${precio:<7}{categoria:<12}{Style.RESET_ALL}")
                
                print(f"\n{Fore.GREEN}Total de productos con stock bajo: {len(productos)}{Style.RESET_ALL}")
                
                # Mostrar estadísticas adicionales
                cantidad_critica = len([p for p in productos if p[3] <= 5])
                if cantidad_critica > 0:
                    print(f"{Fore.RED}Productos con cantidad crítica (≤5): {cantidad_critica}{Style.RESET_ALL}")
                
            else:
                print(f"{Fore.GREEN}No hay productos con cantidad igual o inferior a {limite}.{Style.RESET_ALL}")
                
        except sqlite3.Error as e:
            print(f"{Fore.RED}ERROR al generar el reporte: {e}{Style.RESET_ALL}")
        finally:
            conexion.close()


def obtener_opcion_menu():
    """Obtiene y valida la opción del menú usando bucle while"""
    while True:
        try:
            opcion = int(input("Seleccione una opción (1-7): "))
            if opcion >= 1 and opcion <= 7:
                return opcion
            else:
                print(f"{Fore.RED}Opción inválida. Ingrese un número del 1 al 7.{Style.RESET_ALL}")
        except ValueError:
            print(f"{Fore.RED}Por favor ingrese un número válido.{Style.RESET_ALL}")


#! ----- PROGRAMA PRINCIPAL -----

def main():
    # Iniciar la base de datos.
    iniciar_db()
    # Insertar los productos de ejemplos si la tabla esta vacia.
    insertar_productos_principales()
    
    print(f"{Fore.CYAN}Bienvenido al Sistema de Gestión de Productos")
    
    # Bucle principal del programa
    while True:
        mostrar_menu()
        opcion = obtener_opcion_menu()
        
        if opcion == 1:
            agregar_producto()
        elif opcion == 2:
            lista_productos()
        elif opcion == 3:
            actualizar_producto()
        elif opcion == 4:
            eliminar_producto()
        elif opcion == 5:
            buscar_producto_por_id()
        elif opcion == 6:
            reporte_stock_bajo()
        elif opcion == 7:
            #Finalizar el programa cuando selecciona la opcion 8.
            print(f"{Fore.MAGENTA}┌────────────────────────────────────────────────────────────────┐{Style.RESET_ALL}")
            print(f"{Fore.MAGENTA}│                    Gracias por usar el sistema                 │{Style.RESET_ALL}")
            print(f"{Fore.MAGENTA}│                   Productos finales registrados:               │{Style.RESET_ALL}")
            print(f"{Fore.MAGENTA}└────────────────────────────────────────────────────────────────┘{Style.RESET_ALL}")
            lista_productos()  # Sin parámetro
            print(f"{Fore.MAGENTA}┌────────────────────────────────────────────────────────────────┐{Style.RESET_ALL}")
            print(f"{Fore.MAGENTA}│                          ¡Hasta Luego!                         │{Style.RESET_ALL}")
            print(f"{Fore.MAGENTA}└────────────────────────────────────────────────────────────────┘{Style.RESET_ALL}")
            break



# Ejecutar el programa
if __name__ == "__main__":
    main()