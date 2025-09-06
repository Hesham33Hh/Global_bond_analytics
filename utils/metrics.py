from sklearn.metrics import mean_absolute_error, mean_squared_error
import numpy as np

def eval_metrics(y_true, y_pred):
    """
    Calcula métricas básicas de error.
    
    Parámetros:
    - y_true: array/list de valores reales
    - y_pred: array/list de valores predichos
    
    Devuelve:
    - dict con MAE y RMSE
    """
    mae = mean_absolute_error(y_true, y_pred)
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    return {"MAE": mae, "RMSE": rmse}
