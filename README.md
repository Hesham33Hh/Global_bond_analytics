
# Global Bond Analytics

Este proyecto tiene como objetivo entender y predecir la dinámica entre inflación y bonos, utilizando econometría (VAR) y Machine Learning, y comparando resultados entre distintos países.

## Objetivo
Analizar y predecir la relación entre la inflación y los rendimientos de bonos a 10 años (yield 10Y) en Estados Unidos y otros países, empleando modelos econométricos y de aprendizaje automático.

## Metodología

### 1. Análisis Estados Unidos (USA)

**Carga y visualización de datos:**
- Lectura de datos de rendimientos de bonos a 10 años (USA) y datos macroeconómicos de inflación anual.
- Unificación de datos por año, obteniendo una serie histórica desde 1962 hasta 2024.
- Visualización de la evolución del yield 10Y, inflación anual (YoY) y real yield (yield – inflación).

**Análisis exploratorio:**
- Correlación simple: yield e inflación correlacionan 0.61 (relación positiva moderada).
- Regresión lineal: yield = 3.37 + 0.65 × inflación. Significativo, pero solo explica ~38% de la variación (R² = 0.38).

**Diagnósticos:**
- Residuos no completamente normales.
- Fuerte autocorrelación (Durbin-Watson = 0.23).
- Se justifica el uso de errores robustos (HAC/Newey-West).

**Modelo VAR:**
- Aplicación de modelo VAR con selección de rezagos (criterios AIC/BIC).


**Forecast y visualizaciones:**
- Proyección histórica y futura de yields e inflación.
- Funciones de impulso-respuesta (IRF): análisis de cómo un shock en inflación afecta yields y viceversa.

### 2. Análisis Multi-país

**Construcción del dataset:**
- Integración de yields de varios países (EEUU, Alemania, Japón, España, etc.).
- Incorporación de inflación anual de cada país.
- Cálculo de real yield y limpieza de valores extremos.

**KPIs y visualizaciones:**
- Correlación inflación–yield por país.
- Ranking de real yield (últimos 10 años y último año).
- Visualización de series de yields e inflación por país.
- Barras: real yield último año.
- Heatmap: correlaciones inflación–yield por país.

**Modelos de predicción:**
- Aplicación de algoritmos de Machine Learning: Ridge/Lasso, Random Forest, Gradient Boosting, XGBoost, etc.
- Feature engineering: inclusión de más países y variables macroeconómicas (PIB, empleo, exportaciones).
- Entrenamiento y validación: división train/test, cálculo de métricas (RMSE, MAE, R²).
- Comparación de modelos: evaluación de si los modelos de ML predicen mejor que el VAR.

### 3. Integración y entrega final

El proyecto integra la parte econométrica (explicación de relaciones causales) con la parte de Machine Learning (capacidad predictiva en escenarios complejos).

> Los modelos VAR ayudan a entender relaciones causales.
> Los modelos de ML permiten predecir mejor en escenarios complejos con muchos países y variables.

## Entregables
- `README.md` explicando objetivo, datos, metodología, resultados e implicaciones.
- Código limpio en Jupyter/VSCode.
- Figuras y visualizaciones clave.

