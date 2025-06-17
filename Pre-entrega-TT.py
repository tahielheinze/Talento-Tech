
#! --- REQUISITOS PROYECTO ---
#* Ingreso de datos de productos.
#* Validar el ingreso de datos, categoria y precio.
#* Almacenarlos en listas.
#* Incorporar bucles while y for.
#* Visualización de productos registrados.
#* Utilizar un condicional para gestionar las opciones del menú
#* El menu debe poder elegir entre: agregar, visualizar, buscar y eliminar productos.
#* Finalizar el programa cuando se seleccione la opcion de 'Salir'

#! ----- DEFINIR FUNCIONES -----

# Mostrar el menu al ejecutar el programa.
def mostrar_menu():
    print("┌────────────────────────────────────────────────────────────────┐")
    print("│                      GESTIÓN DE PRODUCTOS                      │")
    print("│────────────────────────────────────────────────────────────────│")
    print("│ 1. Agregar Productos.                                          │")
    print("│ 2. Visualizar Lista de Productos.                              │")
    print("│ 3. Salir del programa.                                         │")
    print("└────────────────────────────────────────────────────────────────┘")


# Valida el ingreso del nombre del producto, no puede estar vacio, ni repetido.
def validar_nombre_producto(productos):
    while True:
        nombre = input("Ingrese el nombre del producto: ").strip()
        if nombre == "":
            print("El nombre del producto no puede estar vacío.")
            continue
        # Validar que el nombre no exista ya, sin importar si esta en mayúsuculas o no, mediante bucle for.
        existe = False
        for producto in productos: #Bucle for para buscar nombres duplicados.
            if producto[0].lower() == nombre.lower():
                existe = True
                break
        if existe:
            print(f"El producto '{nombre}' ya se encuentra agregado.")
            continue
        return nombre.capitalize() #Regresa el nombre una vez validado en formato Capitalize.


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
            print("El valor ingresado no es admitido, ingrese un número valido.")


#Agregar productos a la lista.
def agregar_producto(productos):
    print("┌────────────────────────────────────────────────────────────────┐")
    print("│                     AGREGAR NUEVO PRODUCTO                     │")
    print("└────────────────────────────────────────────────────────────────┘")
    #Validar los ingresos de datos llamando a las funciones.
    nombre = validar_nombre_producto(productos)
    categoria = validar_categoria()
    precio = validar_precio()
    #Almacenar los datos ya validados.
    nuevo_producto = [nombre, categoria, precio]
    productos.append(nuevo_producto)
    #Mensaje de agregado exitoso.
    print("┌────────────────────────────────────────────────────────────────┐")
    print("│                 PRODUCTO AGREGADO EXITOSAMENTE                 │")
    print("│────────────────────────────────────────────────────────────────│")
    print(f"│ Producto: {nombre}")
    print(f"│ Categoría: {categoria}")
    print(f"│ Precio: ${precio}")
    print("└────────────────────────────────────────────────────────────────┘")


#Visualizar la lista de productos registrados.
def lista_productos(productos):
    if len(productos) == 0:
        print("No hay productos registrados.")
        return
    #Imprimir mensaje de los productos ya registrados.
    print("┌────────────────────────────────────────────────────────────────┐")
    print("│                      PRODUCTOS REGISTRADOS                     │")
    print("│────────────────────────────────────────────────────────────────│")
    print(f"│{"N°": <3}{"Nombre": <20}{"Categoría": <15} {"Precio": <10}               │")
    print("└────────────────────────────────────────────────────────────────┘")
    for i in range(len(productos)):
        producto = productos[i]
        nombre, categoria, precio = producto
        print(f" {i+1:<3} {nombre:<20} {categoria:<15} ${precio:<9}")


def obtener_opcion_menu():
    """Obtiene y valida la opción del menú usando bucle while"""
    while True:
        try:
            opcion = int(input("Seleccione una opción (1-3): "))
            if opcion >= 1 and opcion <= 3:
                return opcion
            else:
                print("Opción inválida. Ingrese un número del 1 al 3.")
        except ValueError:
            print("Por favor ingrese un número válido.")


#! ----- PROGRAMA PRINCIPAL -----

def main():
    # Almacenar datos en listas - cada producto es una sublista de 3 elementos
    productos = [
        ["Manzana", "Fruta", 100],
        ["Pera", "Fruta", 200],
        ["Naranja", "Fruta", 300],
        ["Uva", "Fruta", 400],
        ["Banana", "Fruta", 500]
    ]
    
    print("Bienvenido al Sistema de Gestión de Productos")
    
    # Bucle principal del programa
    while True:
        mostrar_menu()
        opcion = obtener_opcion_menu()
        
        # Utilizar condicionales para gestionar las opciones del menú
        if opcion == 1:
            agregar_producto(productos)
        elif opcion == 2:
            lista_productos(productos)
        elif opcion == 3:
            # Finalizar el programa cuando se seleccione 'Salir'
            print("┌────────────────────────────────────────────────────────────────┐")
            print("│                    Gracias por usar el sistema                 │")
            print("│                   Productos finales registrados:               │")
            print("└────────────────────────────────────────────────────────────────┘")
            lista_productos(productos)
            print("┌────────────────────────────────────────────────────────────────┐")
            print("│                          ¡Hasta Luego!                         │")
            print("└────────────────────────────────────────────────────────────────┘")
            break


# Ejecutar el programa
if __name__ == "__main__":
    main()