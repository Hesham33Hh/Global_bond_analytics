import matplotlib.pyplot as plt

def plot_real_vs_pred(df, title="Real vs Predicho", country=None, model=None, savepath=None):
    """
    Grafica valores reales vs predichos para un país/modelo.
    
    Parámetros:
    - df: DataFrame con columnas 'y_true' y 'y_pred'
    - title: título del gráfico
    - country: nombre del país (opcional)
    - model: nombre del modelo (opcional)
    - savepath: ruta para guardar PNG (opcional)
    """
    plt.figure(figsize=(9,5))
    plt.plot(df.index, df['y_true'], marker='o', label='Real')
    plt.plot(df.index, df['y_pred'], marker='x', label='Predicho')

    full_title = f"{country} – {title}" if country else title
    if model:
        full_title += f" ({model})"
    plt.title(full_title)

    plt.xlabel("Year")
    plt.ylabel("%")
    plt.legend()
    plt.grid(alpha=.3)

    if savepath:
        plt.savefig(savepath, dpi=150, bbox_inches="tight")
        print(f"[OK] Gráfico guardado en {savepath}")
    else:
        plt.show()
