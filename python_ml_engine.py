import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.impute import SimpleImputer
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler

NON_FEATURES = {'city', 'date', 'datetime', 'timestamp', 'station', 'location'}

def numeric_features(df):
    candidates = [c for c in df.columns if c.lower() not in NON_FEATURES]
    numeric = df[candidates].apply(pd.to_numeric, errors='coerce').replace([np.inf, -np.inf], np.nan)
    numeric = numeric.mask(numeric < 0).dropna(axis=1, how='all')
    if numeric.shape[1] < 2:
        raise ValueError('CSV needs at least two usable numeric pollutant columns.')
    numeric = numeric.dropna(axis=0, how='all')
    if len(numeric) < 3:
        raise ValueError('CSV needs at least three rows with numeric measurements.')
    return numeric, SimpleImputer(strategy='median').fit_transform(numeric)

def cluster_data(df, clusters=3):
    clusters = int(clusters)
    if not 2 <= clusters <= 10:
        raise ValueError('Clusters must be between 2 and 10.')
    original, values = numeric_features(df)
    if len(values) <= clusters:
        raise ValueError('Number of rows must be greater than the cluster count.')
    scaled = StandardScaler().fit_transform(values)
    labels = KMeans(n_clusters=clusters, random_state=42, n_init=10).fit_predict(scaled)
    unique = np.unique(labels)
    score = float(silhouette_score(scaled, labels)) if 1 < len(unique) < len(scaled) else None
    coords = PCA(n_components=2).fit_transform(scaled)
    return {'feature_columns': list(original.columns), 'rows_analyzed': int(len(values)), 'cluster_count': clusters, 'silhouette_score': score, 'points': [{'x': round(float(coords[i,0]),5), 'y': round(float(coords[i,1]),5), 'cluster': int(labels[i])} for i in range(len(labels))], 'summary': [{'cluster': int(k), 'rows': int(np.sum(labels == k))} for k in sorted(unique)]}

def forecast_data(df, target, periods=7):
    periods = int(periods)
    if not 1 <= periods <= 30:
        raise ValueError('Forecast periods must be between 1 and 30.')
    if target not in df.columns:
        raise ValueError(f'Target column {target!r} was not found in the CSV.')
    values = pd.to_numeric(df[target], errors='coerce').replace([np.inf,-np.inf], np.nan).dropna()
    values = values[values >= 0].reset_index(drop=True)
    if len(values) < 3:
        raise ValueError('At least three valid non-negative observations are required.')
    x = np.arange(len(values), dtype=float)
    slope, intercept = np.polyfit(x, values.to_numpy(dtype=float), 1)
    predictions = np.maximum(0, slope * np.arange(len(values),len(values)+periods,dtype=float)+intercept)
    return {'target': target, 'method': 'linear trend baseline', 'validated': False, 'observations': int(len(values)), 'forecast': [{'step': i+1, 'value': round(float(v),3)} for i,v in enumerate(predictions)], 'note': 'Experimental baseline only. Validate against held-out historical observations before operational use.'}