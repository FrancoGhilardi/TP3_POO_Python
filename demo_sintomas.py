class PoligonoConDefaultMutable:
    def __init__(self, lados: "list[str]" = []) -> None:
        self._lados = lados


class PoligonoSinCopiaDefensiva:
    def __init__(self, lados: "list[int]") -> None:
        self._lados = lados

    def getLados(self) -> "list[int]":
        return self._lados


def demo_default_mutable() -> None:
    print("--- Síntoma 1: argumento por defecto mutable (java-ismo #3) ---")
    t1 = PoligonoConDefaultMutable()
    t2 = PoligonoConDefaultMutable()
    t1._lados.append("lado fantasma")
    print(f"t1._lados is t2._lados -> {t1._lados is t2._lados}")
    print(f"t2._lados quedó contaminado por t1: {t2._lados}")


def demo_alias_sin_copia() -> None:
    print("--- Síntoma 2: alias sin copia defensiva (java-ismo #5) ---")
    lados_originales = [3, 4, 5]
    poligono = PoligonoSinCopiaDefensiva(lados_originales)
    lados_externos = poligono.getLados()
    lados_externos.append(999)
    print(f"lados internos del polígono tras mutar la referencia externa: {poligono._lados}")


if __name__ == "__main__":
    demo_default_mutable()
    demo_alias_sin_copia()
