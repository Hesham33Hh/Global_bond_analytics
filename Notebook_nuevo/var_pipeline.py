
"""
VAR pipeline for country-by-country analysis of Inflation vs 10Y Yield (2010–2024).
Author: Hesham + ChatGPT
Dependencies: pandas, numpy, statsmodels, matplotlib
"""

import warnings
warnings.filterwarnings("ignore")

from dataclasses import dataclass
from typing import Tuple, Optional, Dict, Any, List

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from statsmodels.tsa.api import VAR
from statsmodels.tsa.stattools import adfuller
from statsmodels.stats.diagnostic import acorr_ljungbox
from statsmodels.stats.stattools import jarque_bera
from statsmodels.stats.stattools import durbin_watson


@dataclass
class VARConfig:
    maxlags: int = 2              # Annual data: keep small (1–2)
    ic: str = "aic"               # Use AIC for lag selection
    deterministic: str = "ct"     # "n","c","ct","ctt" (const/trend)
    diff_to_stationary: bool = True  # Difference series if non-stationary (ADF p>=0.05)
    irf_horizon: int = 8
    fcst_steps: int = 4


def adf_report(series: pd.Series, name: str) -> Dict[str, Any]:
    series = series.dropna()
    res = adfuller(series, autolag="AIC")
    return {
        "variable": name,
        "adf_stat": res[0],
        "p_value": res[1],
        "lags_used": res[2],
        "nobs": res[3]
    }


def ensure_datetime_index(df: pd.DataFrame, year_col: str = "Year") -> pd.DataFrame:
    df = df.copy()
    if year_col in df.columns:
        # Create a PeriodIndex for yearly data for stability
        df["Date"] = pd.to_datetime(df[year_col].astype(int), format="%Y")
    elif "Date" in df.columns:
        df["Date"] = pd.to_datetime(df["Date"])
    else:
        raise ValueError("Provide a 'Year' or 'Date' column.")
    df = df.set_index("Date").sort_index()
    return df


def difference_if_needed(df_xy: pd.DataFrame, config: VARConfig) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """
    Check ADF for each variable; if p>=0.05 and config.diff_to_stationary True, difference once.
    Returns transformed df and a dict with metadata.
    """
    meta = {"differenced": False, "adf_before": [], "adf_after": []}
    adf_b = [adf_report(df_xy[c], c) for c in df_xy.columns]
    meta["adf_before"] = adf_b
    if config.diff_to_stationary and any(x["p_value"] >= 0.05 for x in adf_b):
        df_xy_diff = df_xy.diff().dropna()
        meta["differenced"] = True
        adf_a = [adf_report(df_xy_diff[c], c) for c in df_xy_diff.columns]
        meta["adf_after"] = adf_a
        return df_xy_diff, meta
    return df_xy, meta


def select_lags(df_xy: pd.DataFrame, config: VARConfig) -> int:
    model = VAR(df_xy)
    # statsmodels' select_order can be unstable with very few observations;
    # we fall back to config.maxlags if selection fails.
    try:
        sel = model.select_order(maxlags=config.maxlags)
        chosen = getattr(sel, config.ic)
        if np.isnan(chosen) or chosen < 1:
            return min(config.maxlags, 1)
        return int(chosen)
    except Exception:
        return min(config.maxlags, 1)


@dataclass
class VARResultsPack:
    model_fit: Any
    used_lags: int
    transformed: bool
    transform_meta: Dict[str, Any]
    diagnostics: Dict[str, Any]
    variables: List[str]


def fit_var_for_country(df: pd.DataFrame,
                        country: str,
                        y_col: str = "yield_10y",
                        pi_col: str = "inflation_yoy",
                        year_col: str = "Year",
                        config: VARConfig = VARConfig()) -> VARResultsPack:
    """
    df must have columns: ['Country', year_col, y_col, pi_col] for multiple countries,
    or just [year_col, y_col, pi_col] for a single country.
    """
    cols_needed = {y_col, pi_col}
    if "Country" in df.columns:
        dfc = df[df["Country"] == country].copy()
    else:
        dfc = df.copy()

    if not cols_needed.issubset(dfc.columns):
        raise ValueError(f"Missing columns: {cols_needed - set(dfc.columns)}")

    dfc = ensure_datetime_index(dfc, year_col=year_col)
    df_xy = dfc[[y_col, pi_col]].dropna()

    # Transform to stationarity if needed
    df_xy_t, meta = difference_if_needed(df_xy, config)

    # Lag selection
    used_lags = select_lags(df_xy_t, config)

    # Fit VAR
    var_model = VAR(df_xy_t)
    fit = var_model.fit(used_lags, trend=config.deterministic)

    # Diagnostics
    resid = fit.resid
    # Serial correlation (Ljung-Box) up to lag=used_lags
    lbx = {}
    for col in resid.columns:
        lb = acorr_ljungbox(resid[col], lags=[min(used_lags, 2)], return_df=True)
        lbx[col] = {
            "lb_stat": float(lb["lb_stat"].iloc[-1]),
            "lb_pvalue": float(lb["lb_pvalue"].iloc[-1])
        }
    # Normality (Jarque-Bera)
    jb_stats = {col: jarque_bera(resid[col]) for col in resid.columns}
    jb = {
        col: {"jb_stat": v[0], "p_value": float(v[1])} for col, v in jb_stats.items()
    }
    # Durbin-Watson
    dw = {col: float(durbin_watson(resid[col])) for col in resid.columns}
    # Stability (roots inside unit circle)
    roots = np.abs(fit.roots)
    stable = bool(np.all(roots < 1.0))

    diagnostics = {
        "ljung_box": lbx,
        "jarque_bera": jb,
        "durbin_watson": dw,
        "stable_roots_all_less_than_one": stable,
        "roots_modulus_max": float(np.max(roots)) if len(roots) else np.nan,
        "nobs": int(fit.nobs)
    }

    return VARResultsPack(
        model_fit=fit,
        used_lags=used_lags,
        transformed=meta["differenced"],
        transform_meta=meta,
        diagnostics=diagnostics,
        variables=list(df_xy_t.columns)
    )



def plot_irf(results: VARResultsPack, horizon: Optional[int] = None) -> None:
    if horizon is None:
        horizon = 8
    irf = results.model_fit.irf(horizon)
    names = results.variables
    # For each response and each impulse, draw a simple one-line chart (no subplots)
    for i_resp, resp in enumerate(names):
        for i_imp, imp in enumerate(names):
            arr = irf.irfs[:, i_resp, i_imp]
            x = np.arange(arr.shape[0])
            plt.figure()
            plt.plot(x, arr)
            plt.title(f"IRF: response {resp} to shock in {imp}")
            plt.xlabel("Horizon")
            plt.ylabel("Response")
            plt.show()


def forecast_levels(results: VARResultsPack, last_levels: pd.Series, steps: int = 4) -> pd.DataFrame:
    """
    If the model was fit on differences, cumulate to return level forecasts.
    last_levels: last observed *level* values for variables.
    Returns a DataFrame with forecasted levels.
    """
    y0 = results.model_fit.endog[-results.model_fit.k_ar:]
    f = results.model_fit.forecast(y=y0, steps=steps)
    fcst = pd.DataFrame(f, columns=results.variables)

    if results.transformed:
        # Cumulate differences
        levels = [last_levels.values]
        for i in range(steps):
            next_level = levels[-1] + fcst.iloc[i].values
            levels.append(next_level)
        levels = np.vstack(levels[1:])
        out = pd.DataFrame(levels, columns=results.variables)
    else:
        out = fcst

    out.index.name = "step"
    return out


def quick_var_country_report(df: pd.DataFrame, country: str, y_col="yield_10y", pi_col="inflation_yoy",
                             year_col="Year", config: VARConfig = VARConfig()) -> Dict[str, Any]:
    pack = fit_var_for_country(df, country, y_col, pi_col, year_col, config)
    # Print diagnostics
    print(f"Country: {country}")
    print(f"Used lags: {pack.used_lags}")
    print(f"Differenced to stationary: {pack.transformed}")
    print("ADF before:")
    for r in pack.transform_meta["adf_before"]:
        print(r)
    if pack.transformed:
        print("ADF after:")
        for r in pack.transform_meta["adf_after"]:
            print(r)
    print("Diagnostics:", pack.diagnostics)

    # IRFs
    plot_irf(pack, horizon=config.irf_horizon)

    # Forecast to levels
    # Get last observed levels from original data
    if "Country" in df.columns:
        dfl = df[df["Country"] == country].copy()
    else:
        dfl = df.copy()
    dfl = ensure_datetime_index(dfl, year_col=year_col)
    last_levels = dfl[[y_col, pi_col]].dropna().iloc[-1]

    fcst_levels = forecast_levels(pack, last_levels=last_levels, steps=config.fcst_steps)
    print("Forecasted levels (next steps):")
    print(fcst_levels)

    # Simple plots for forecasts (one plot per variable)
    for col in fcst_levels.columns:
        plt.figure()
        plt.plot(fcst_levels.index, fcst_levels[col])
        plt.title(f"Forecast (levels): {col}")
        plt.xlabel("Step")
        plt.ylabel(col)
        plt.show()

    return {
        "country": country,
        "used_lags": pack.used_lags,
        "transformed": pack.transformed,
        "diagnostics": pack.diagnostics,
        "forecast_levels": fcst_levels
    }
