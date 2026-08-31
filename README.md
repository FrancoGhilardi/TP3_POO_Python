# TP Integrador Unidad 3 — POO (Java → Python)

## Archivos

| Archivo                 | Qué tiene                                                                                                                                                                                                                    |
| ----------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `parte1_diagnostico.py` | El dominio original, ya corregido. Corre de punta a punta sin tirar ningún error.                                                                                                                                            |
| `demo_sintomas.py`      | Reconstruye 2 de los java-ismos tal como estaban antes de arreglarlos, para poder ver el síntoma en la consola.                                                                                                              |
| `figuras.py`            | El módulo con todo el dominio: `Figura`, `Poligono` (abstracta), `Triangulo`, `Cuadrado`, `Pentagono`, `Hexagono`, `Lado`, `Etiqueta`, `Taller`, el `Protocol` `Exportable`, y las funciones `es_regular` y `exportar_todo`. |
| `libreria_externa.py`   | La clase `PlanoCAD`, que viene de afuera y no se toca.                                                                                                                                                                       |
| `main.py`               | Un ejemplo integrador: armo un taller con 4 polígonos, etiqueto lados, exporto todo junto con un `PlanoCAD`, y muestro que la composición y la agregación se comportan como corresponde.                                     |
| `informe.md`            | El informe con los java-ismos, las equivalencias Java/Python, las relaciones y el resto de las respuestas.                                                                                                                   |
| `uml/modelo_final.md`   | El diagrama de clases (Mermaid) de cómo quedó el código.                                                                                                                                                                     |

## Cómo correrlo

```
python parte1_diagnostico.py
python demo_sintomas.py
python main.py
```

## Chequeo de tipos

```
python -m mypy --strict figuras.py main.py libreria_externa.py parte1_diagnostico.py demo_sintomas.py
```
