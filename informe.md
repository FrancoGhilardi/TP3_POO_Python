# Informe — TP Integrador Unidad 3 (POO: Java → Python)

## 1. Los 8 java-ismos que encontré

| #   | Java-ismo                                             | Dónde                                    | Qué inversión lo explica                              | Qué se veía mal                                                                                                          |
| --- | ----------------------------------------------------- | ---------------------------------------- | ----------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------ |
| 1   | Getters sin ninguna lógica (`getNombre`, `getColor`)  | `Figura`                                 | Encapsulamiento por convención                        | No validan ni transforman nada, solo devuelven el atributo — en Python no hace falta ese paso extra                      |
| 2   | Atributo de clase mutable (`catalogo`)                | `Poligono`                               | Declaración → runtime / estado compartido sin querer  | Todas las instancias terminaban compartiendo la misma lista de clase                                                     |
| 3   | Argumento por defecto mutable (`lados=[]`)            | `Poligono.__init__`                      | La trampa clásica de Python                           | Los defaults se evalúan una sola vez, así que dos objetos sin argumento explícito terminaban compartiendo la misma lista |
| 4   | Nunca se llama a `super().__init__()`                 | `Poligono.__init__`                      | Herencia → duck typing / disciplina de inicialización | Se reasignaban los atributos a mano en vez de dejar que la cadena de constructores hiciera su trabajo                    |
| 5   | Falta de copia defensiva                              | `Poligono.__init__` y el getter de lados | Copia defensiva                                       | Se guardaba/devolvía la lista original, sin copiar — mutarla desde afuera rompía el objeto por dentro                    |
| 6   | El type hint miente (`-> int` pero devuelve `str`)    | `Poligono.area`                          | Declaración → runtime                                 | Python no chequea tipos en tiempo de ejecución, así que esto pasaba sin ningún error                                     |
| 7   | Constructor "sobrecargado" con `*args` + `isinstance` | `Triangulo`, `Cuadrado`                  | Compilador → acuerdo                                  | Es un intento de imitar el overloading de Java, que en Python no existe — se resuelve con parámetros por defecto         |
| 8   | Un flag que nunca se usa (`_construida`)              | `Figura.__init__`                        | Ceremonia de inicialización de más                    | Se asigna pero nadie lo lee nunca; encima en `Poligono` ni siquiera llega a ejecutarse porque falla el punto 4           |

El bucle manual de `perimetro()` lo limpié también (quedó un `sum()` con generator), pero no lo cuento como uno de los 8 porque es más una cuestión de estilo que un problema de diseño. Y el caso de `Lado` (que sí tenía getter/setter con validación real) no lo cuento como error: ese es el único getter/setter que tenía sentido dejar, y lo pasé a `@property`.

## 2. Tabla de equivalencias Java ↔ Python

| Elemento en Java                                                   | Cómo quedó en Python                                   | ¿Se tradujo tal cual o cambié el enfoque? | Por qué                                                                                                  |
| ------------------------------------------------------------------ | ------------------------------------------------------ | ----------------------------------------- | -------------------------------------------------------------------------------------------------------- |
| Getter/setter sin lógica                                           | Atributo directo, o `@property` solo si hay validación | Cambié el enfoque                         | En Python no hace falta esa ceremonia si no hay nada que validar                                         |
| Constructor sobrecargado con `isinstance`                          | Un solo `__init__` con parámetros por defecto          | Cambié el enfoque                         | Python tiene defaults, no hace falta simular overloading                                                 |
| Campo estático compartido (`catalogo`)                             | Lo saqué; ese rol ya lo cumple `Taller`                | Cambié el enfoque                         | Tener dos lugares registrando lo mismo iba a terminar en lío                                             |
| Subclase solo para poder tiparla como el resto (`PoligonoRegular`) | Una función, `es_regular(poligono)`                    | Cambié el enfoque                         | Ser regular es algo que un polígono ya construido puede calcular, no hace falta un tipo aparte           |
| Clase abstracta con método abstracto                               | `ABC` + `@abstractmethod`                              | Prácticamente igual                       | Python tiene el mismo mecanismo, solo cambia la sintaxis                                                 |
| Interfaz para una clase que no puedo tocar                         | `typing.Protocol` (`Exportable`)                       | Cambié el enfoque                         | En Java tendría que hacer que la clase implemente la interfaz; en Python alcanza con que tenga el método |
| Composición (el dueño arma sus propias partes)                     | Lista propia, copiada en el constructor                | Prácticamente igual                       | Es el mismo concepto, solo que la copia hay que hacerla a mano                                           |
| Objeto de valor simple e inmutable                                 | `@dataclass(frozen=True)` (`Etiqueta`)                 | Cambié el enfoque                         | Una línea reemplaza toda una clase con campos finales y getters                                          |

## 3. Las tres relaciones que quedaron en `figuras.py`

- **Composición** (`Poligono`—`Lado`): en `figuras.py:62`, `Poligono.__init__` arma su propia lista de `Lado`. Como nadie más se queda con una referencia a esos lados por fuera del polígono, si el polígono deja de existir, sus lados también quedan sin nada que los sostenga (lo probé con `weakref` en `main.py`).
- **Agregación** (`Taller`—`Poligono`): en `figuras.py:142`, `Taller.recibir` recibe un `Poligono` que ya fue armado en otro lado. Por eso, aunque lo saque del taller con `restaurar(...)`, el polígono sigue siendo perfectamente válido.
- **Asociación 0..1** (`Lado`—`Etiqueta`): en `figuras.py:25`, el parámetro `etiqueta` tiene default `None`. La `Etiqueta` es opcional y ninguno de los dos objetos controla el ciclo de vida del otro — `Lado` solo guarda una referencia a una que ya existe.

## 4. Por qué `PoligonoRegular` no es una clase

Armar una clase nueva solo para poder meter esos objetos en la misma lista que el resto no tenía mucho sentido en Python — para eso ya alcanza con que todos hereden de `Poligono`. Así que en vez de una clase escribí una función, `es_regular(poligono: Poligono) -> bool`, que sirve para cualquier `Triangulo`, `Cuadrado`, `Pentagono` o `Hexagono` sin tener que duplicar constructor ni validaciones.

## 5. ¿Esto lo elige el lenguaje o el dominio?

Depende de quién es dueño de la clase. A `Poligono` la escribí yo, así que ahí elijo libremente: podría haber usado una ABC sin ningún problema, y usé `Protocol` porque me servía que el mismo contrato lo cumplieran también clases que no son mías. En cambio con `PlanoCAD` (que viene de `libreria_externa.py` y no se puede tocar) no tengo margen: no puedo hacer que herede de nada mío, así que ahí `Protocol` no es un gusto, es la única forma de que cumpla el contrato sin modificarla. O sea: cuando el código es mío, elijo yo; cuando no lo es, el hecho de no poder tocarlo es lo que termina empujando hacia `Protocol`.

## 6. Qué cambió y qué quedó igual

Lo que más cambió fue toda la ceremonia que Java necesita y Python no: getters sin lógica, constructores "sobrecargados" a mano, flags para saber si algo se inicializó. Todo eso se resuelve en Python con atributos comunes, parámetros por defecto y confiando en que si el objeto se construyó, se construyó bien. También cambié la forma de compartir una propiedad entre varios objetos: en vez de armar una jerarquía de clases nueva, usé una función que la calcula sobre el objeto que ya está.

Lo que no cambió fue el modelo en sí: un `Poligono` sigue siendo una `Figura` con lados y perímetro, un `Taller` sigue juntando polígonos sin ser dueño de ellos, y un `Lado` sigue pudiendo tener una `Etiqueta` opcional. Composición, agregación y asociación son ideas de diseño que no dependen del lenguaje — lo que cambió fue cómo se escriben en código, no lo que significan.
