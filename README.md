> *Branch creada para analizar el código y hacer comentarios.*

# Global_bond_analytics
mi proyecto busca entender y predecir la dinámica inflación–bonos usando econometría (VAR) y Machine Learning, comparando resultados entre países.
Analizar y predecir la relación entre inflación y rendimientos de bonos (yield 10Y) en Estados Unidos y otros países, usando:

🔹 Lo que has hecho hasta ahora

Carga de datos y visualización inicial (USA):

Leí datos de yields (bonos 10 años USA) y datos macro (inflación anual).

Hizo un merge por año → obtuvo una serie histórica desde 1962–2024.

Visualizaste:

Evolución del yield 10Y.

Inflación anual (YoY).

Real yield (yield – inflación).

Esto permitió ver los grandes periodos (ejemplo: inflación alta en 70s, yields más bajos post-2008).

Análisis exploratorio (USA):

Correlación simple → yield e inflación correlacionan 0.61 (relación positiva moderada).

Regresión lineal → yield = 3.37 + 0.65 × inflación.
✅ Significativo, pero solo explica ~38% de la variación (R² = 0.38).

Diagnósticos:

Residuos no normales del todo.

Fuerte autocorrelación (Durbin-Watson = 0.23).

→ Justificó usar errores robustos (HAC/Newey-West).

Modelo VAR (USA):

Use un modelo VAR con selección de rezagos (criterios AIC/BIC).

Hizo forecast y gráficas:

Forecast histórico/futuro → proyección yields e inflación.

IRF (impulse-response functions) → cómo un shock en inflación afecta yields y viceversa.

 En qué punto estamos ahora

Ya se ha terminado el bloque USA completo:

Limpieza

Análisis exploratorio

Regresión robusta

VAR y funciones impulso-respuesta

Qué falta para hacer

Ahora pasamos al bloque multi-país, que es el corazón comparativo del proyecto:

Construcción del dataset multi-país:

Combinar yields de varios países (EEUU, Alemania, Japón, España, etc.).

Añadir inflación anual de cada país (macro dataset).

Calcular real_yield y limpiar valores extremos.

KPIs multi-país:

Correlación inflación–yield por país.

Ranking de real_yield (últimos 10 años y último año).

Guardar dataset final.

Visualizaciones comparativas:

Series de yields e inflación por países seleccionados.

Barras: real_yield último año.

Heatmap: correlaciones inflación–yield por país.

Modelos de predicción: usar ML para predecir la rentabilidad de bonos o la inflación.

Algoritmos: Ridge/Lasso, Random Forest, Gradient Boosting, XGBoost, etc.

Feature engineering: incluir más países, variables macro (PIB, empleo, exportaciones), y preparar los datos.

Entrenamiento y validación: dividir train/test, calcular métricas (RMSE, MAE, R²).

Comparar modelos: ver si un modelo de ML predice mejor que el VAR.

3. Integración en el proyecto final

Combinas la parte econométrica (explica la lógica y relaciones) con la parte ML (demuestra capacidad de predicción).


“Los VAR ayudan a entender relaciones causales.”

“Los modelos ML ayudan a predecir mejor en escenarios complejos con muchos países y variables.”
Entrega final:

README.md explicando objetivo, datos, metodología, resultados e implicaciones.

Código limpio en Jupyter/VSCode.

Figuras clave.

