class Figura:
    def __init__(self, nombre: str, color: str) -> None:
        self._nombre = nombre
        self._color = color

    def area(self) -> float:
        return 0.0


class Lado:
    def __init__(self, longitud: float) -> None:
        self._longitud = longitud

    @property
    def longitud(self) -> float:
        return self._longitud

    @longitud.setter
    def longitud(self, valor: float) -> None:
        if valor <= 0:
            raise ValueError("La longitud debe ser positiva")
        self._longitud = valor


class Poligono(Figura):
    def __init__(
        self,
        nombre: str,
        color: str,
        lados: "list[Lado] | None" = None,
        observaciones: "list[str] | None" = None,
    ) -> None:
        super().__init__(nombre, color)
        self._lados = list(lados) if lados is not None else []
        self._observaciones = list(observaciones) if observaciones is not None else []

    def lados_esperados(self) -> int:
        return 0

    def perimetro(self) -> float:
        return sum(lado.longitud for lado in self._lados)

    def area(self) -> float:
        raise NotImplementedError("El área depende de la subclase concreta")

    def agregar_observacion(self, texto: str) -> None:
        self._observaciones.append(texto)

    def getLados(self) -> "tuple[Lado, ...]":
        return tuple(self._lados)


class Triangulo(Poligono):
    def __init__(
        self, nombre: str = "triángulo", color: str = "negro", lados: "list[Lado] | None" = None
    ) -> None:
        super().__init__(nombre, color, lados)

    def lados_esperados(self) -> int:
        return 3


class Cuadrado(Poligono):
    def __init__(
        self, nombre: str = "cuadrado", color: str = "negro", lados: "list[Lado] | None" = None
    ) -> None:
        super().__init__(nombre, color, lados)

    def lados_esperados(self) -> int:
        return 4


if __name__ == "__main__":
    activo = True
    if activo:
        t = Triangulo("Triángulo", "rojo", [Lado(3), Lado(4), Lado(5)])
        c = Cuadrado("Cuadrado", "azul", [Lado(2), Lado(2), Lado(2), Lado(2)])
        print(f"Perímetro del triángulo: {t.perimetro()}")
        print(f"Perímetro del cuadrado: {c.perimetro()}")
        t.agregar_observacion("revisar el vértice A")
        print(f"Nombre: {t._nombre}")
