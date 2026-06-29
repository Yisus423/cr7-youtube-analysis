## Decisión de Arquitectura

Se migró de **Polars** a **Pandas** por compatibilidad nativa con las librerías de visualización y dashboards sugeridas por el profesor ([[Data Analisis (CR7)]]).

**Commits asociados:**
- `chore(dependencies): install Pandas`
- `refactor(dependencies): replace Polars with Pandas for ecosystem compatibility`

---

## Estructura del Proyecto

Se adoptó una arquitectura modular con separación de responsabilidades:

```
src/
├── preprocessing.py          # Limpieza y feature engineering
└── analysis/
    ├── shorts_vs_longs.py    # Hipótesis 1
    ├── hype_decay.py         # Hipótesis 2 (pendiente)
    └── sweet_spot.py         # Hipótesis 3 (pendiente)
tests/
├── test_preprocessing.py
└── test_analysis.py
```

**Commit:** `refactor(structure): establish modular project architecture for data analysis`

---

## Hipótesis 1: Shorts vs. Longs

Basado en el diagrama del canvas ([[diagram.canvas]]).

### Pregunta

¿Tienen los videos largos (`long`) un ratio de engagement significativamente mayor que los Shorts?

### Lógica

$$\text{Engagement Rate} = \frac{\text{likeCount} + \text{commentCount}}{\text{viewCount}}$$

### Preprocesamiento (`src/preprocessing.py`)

- Se reemplazan nulos en `likeCount` y `commentCount` con `0`.
- Se convierten `viewCount == 0` a `pd.NA` para evitar división por cero.
- El resultado `NaN` se rellena con `0.0`.

**Commit:** `feat(preprocessing): implement engagement rate calculation`

### Análisis (`src/analysis/shorts_vs_longs.py`)

Se agrupa por `video_type` usando **Named Aggregation** y se calculan:

| Métrica           | Columna origen      | Significado                         |
| ----------------- | ------------------- | ----------------------------------- |
| `mean_engagement` | `engagement_rate`   | Promedio del ratio de interacción   |
| `median_engagement`| `engagement_rate`  | Mediana (resistente a outliers)     |
| `std_engagement`  | `engagement_rate`   | Desviación estándar (consistencia)  |
| `mean_views`      | `viewCount`         | Promedio de vistas por tipo         |
| `video_count`     | `video_type`        | Cantidad de videos en cada grupo    |

### Tests Unitarios

Se utiliza **`pytest`** con **`pytest.approx`** para comparaciones de punto flotante.

**Casos probados:**
- Video con valores normales → engagement rate esperado.
- Video con `likeCount = None` → debe tratarse como `0`.
- Video con `viewCount = 0` → engagement rate debe ser `0.0` (sin división por cero).
- Agrupación correcta: 2 grupos (`short` y `long`).
- Promedio de engagement por grupo con tolerancia de floats.

**Commit:** `test(hypothesis-1): add unit tests for engagement rate and shorts-vs-longs analysis`

---

## Próximos Pasos

Pendientes de definir en el [[Project-Kanban]]:
- Hipótesis 2: El Desgaste del Hype
- Hipótesis 3: El Punto Óptimo de Duración
- Aplicación Streamlit (`app.py`)
