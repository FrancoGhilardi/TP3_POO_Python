from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Protocol, runtime_checkable


@runtime_checkable
class Exportable(Protocol):
    def exportar(self) -> str: ...


@dataclass(frozen=True)
class Etiqueta:
    texto: str


class Lado:
    def __init__(self, longitud: float, etiqueta: "Etiqueta | None" = None) -> None:
        self._longitud = longitud
        self._etiqueta = etiqueta  # asociación 0..1: Lado no crea la Etiqueta, solo referencia una ya existente

    @property
    def longitud(self) -> float:
        return self._longitud

    @longitud.setter
    def longitud(self, valor: float) -> None:
        if valor <= 0:
            raise ValueError("La longitud debe ser positiva")
        self._longitud = valor

    @property
    def etiqueta(self) -> "Etiqueta | None":
        return self._etiqueta


class Figura:
    def __init__(self, nombre: str, color: str) -> None:
        self._nombre = nombre
        self._color = color

    def area(self) -> float:
        return 0.0


class Poligono(ABC, Figura):
    def __init__(
        self,
        nombre: str,
        color: str,
        lados: "list[Lado] | None" = None,
        observaciones: "list[str] | None" = None,
    ) -> None:
        super().__init__(nombre, color)
        self._lados = list(lados) if lados is not None else []  # composición: Poligono crea/posee su lista de Lado
        self._observaciones = list(observaciones) if observaciones is not None else []
        if len(self._lados) != self.lados_esperados():
            raise ValueError(
                f"{type(self).__name__} esperaba {self.lados_esperados()} lados, recibió {len(self._lados)}"
            )

    @abstractmethod
    def lados_esperados(self) -> int:
        ...

    def perimetro(self) -> float:
        return sum(lado.longitud for lado in self._lados)

    def area(self) -> float:
        raise NotImplementedError("El área depende de la subclase concreta")

    def agregar_observacion(self, texto: str) -> None:
        self._observaciones.append(texto)

    def lados(self) -> "tuple[Lado, ...]":
        return tuple(self._lados)

    def exportar(self) -> str:
        return f"{type(self).__name__}[{self._nombre}, {len(self._lados)} lados, perímetro={self.perimetro():.2f}]"


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


class Pentagono(Poligono):
    def __init__(
        self, nombre: str = "pentágono", color: str = "negro", lados: "list[Lado] | None" = None
    ) -> None:
        super().__init__(nombre, color, lados)

    def lados_esperados(self) -> int:
        return 5


class Hexagono(Poligono):
    def __init__(
        self, nombre: str = "hexágono", color: str = "negro", lados: "list[Lado] | None" = None
    ) -> None:
        super().__init__(nombre, color, lados)

    def lados_esperados(self) -> int:
        return 6


def es_regular(poligono: "Poligono") -> bool:
    lados = poligono.lados()
    return all(lado.longitud == lados[0].longitud for lado in lados)


def exportar_todo(items: "list[Exportable]") -> "list[str]":
    return [item.exportar() for item in items]


class Taller:
    def __init__(self) -> None:
        self._poligonos: "list[Poligono]" = []

    def recibir(self, poligono: "Poligono") -> None:
        self._poligonos.append(poligono)  # agregación: recibe un objeto ya construido por otro

    def restaurar(self, poligono: "Poligono") -> None:
        self._poligonos.remove(poligono)

    def inventario(self) -> "tuple[Poligono, ...]":
        return tuple(self._poligonos)
