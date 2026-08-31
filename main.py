import gc
import weakref

from figuras import (
    Cuadrado,
    Etiqueta,
    Exportable,
    Hexagono,
    Lado,
    Pentagono,
    Poligono,
    Taller,
    Triangulo,
    es_regular,
    exportar_todo,
)
from libreria_externa import PlanoCAD


def main() -> None:
    taller = Taller()

    lado_ab = Lado(3, Etiqueta("AB"))
    lado_bc = Lado(3, Etiqueta("BC"))
    triangulo = Triangulo("Triángulo", "rojo", [lado_ab, lado_bc, Lado(3)])
    cuadrado = Cuadrado("Cuadrado", "azul", [Lado(2), Lado(2), Lado(2), Lado(2)])
    pentagono = Pentagono("Pentágono", "verde", [Lado(3) for _ in range(5)])
    hexagono = Hexagono("Hexágono", "amarillo", [Lado(2) for _ in range(6)])

    for poligono in (triangulo, cuadrado, pentagono, hexagono):
        taller.recibir(poligono)

    print("Lados etiquetados:", lado_ab.etiqueta, lado_bc.etiqueta)
    print("¿Triángulo regular?", es_regular(triangulo))
    print("¿Cuadrado regular?", es_regular(cuadrado))

    plano = PlanoCAD("PLN-001")
    items: list[Exportable] = [triangulo, cuadrado, pentagono, hexagono, plano]
    for linea in exportar_todo(items):
        print(linea)

    print("Inventario del taller:", taller.inventario())

    taller.restaurar(triangulo)
    print("El triángulo sigue siendo válido tras salir del taller:", triangulo.exportar())

    lados_taller = triangulo.lados()
    try:
        lados_taller[0] = Lado(999)  # type: ignore[index]
    except TypeError as error:
        print(f"Copia defensiva confirmada, no se puede mutar: {error}")

    try:
        Poligono("figura abstracta", "gris")  # type: ignore[abstract]
    except TypeError as error:
        print(f"Falla temprana esperada: {error}")

    lado_efimero = Lado(5)
    referencia_debil = weakref.ref(lado_efimero)
    figura_efimera = Triangulo("efímero", "gris", [lado_efimero, Lado(5), Lado(5)])
    del lado_efimero
    del figura_efimera
    gc.collect()
    print("¿El Lado sobrevive a la destrucción de su Poligono (composición)?", referencia_debil() is not None)


if __name__ == "__main__":
    main()
