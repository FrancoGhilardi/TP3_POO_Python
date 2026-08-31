# Modelo final — `figuras.py`

```mermaid
classDiagram
    class Exportable {
        <<Protocol>>
        +exportar() str
    }
    class Figura {
        #_nombre str
        #_color str
        +area() float
    }
    class Poligono {
        <<abstract>>
        #_lados list~Lado~
        #_observaciones list~str~
        +lados_esperados()* int
        +perimetro() float
        +lados() tuple~Lado~
        +exportar() str
        +agregar_observacion(texto)
    }
    class Lado {
        #_longitud float
        #_etiqueta Etiqueta
        +longitud float
        +etiqueta Etiqueta
    }
    class Etiqueta {
        <<frozen dataclass>>
        +texto str
    }
    class Taller {
        #_poligonos list~Poligono~
        +recibir(poligono)
        +restaurar(poligono)
        +inventario() tuple~Poligono~
    }
    class Triangulo {
        +lados_esperados() int
    }
    class Cuadrado {
        +lados_esperados() int
    }
    class Pentagono {
        +lados_esperados() int
    }
    class Hexagono {
        +lados_esperados() int
    }
    class PlanoCAD {
        <<librería externa>>
        +exportar() str
    }

    Figura <|-- Poligono
    Poligono <|-- Triangulo
    Poligono <|-- Cuadrado
    Poligono <|-- Pentagono
    Poligono <|-- Hexagono
    Poligono "1" *-- "3..*" Lado
    Lado "1" --> "0..1" Etiqueta
    Taller "1" o-- "0..*" Poligono
    Poligono ..|> Exportable
    PlanoCAD ..|> Exportable
```

**Cómo leer las relaciones:**

- `Figura <|-- Poligono`: herencia normal. `Poligono` es abstracta (`lados_esperados()` es `@abstractmethod`), así que no se puede instanciar directo.
- `Poligono *-- Lado`: composición. `Poligono.__init__` arma su propia lista de `Lado` (`figuras.py:62`), no la recibe ya armada de afuera para después compartirla.
- `Lado --> Etiqueta` (0..1): asociación. En `figuras.py:25` la `Etiqueta` es un parámetro opcional (default `None`) — ninguno de los dos objetos controla el ciclo de vida del otro.
- `Taller o-- Poligono` (0..\*): agregación. `Taller.recibir` (`figuras.py:142`) recibe polígonos que ya existían antes; si los saco del taller, siguen siendo válidos.
- `Poligono ..|> Exportable`, `PlanoCAD ..|> Exportable`: acá no hay herencia, es cumplimiento por forma (`Protocol`) — por eso `PlanoCAD` cumple el contrato sin heredar de nada mío.
