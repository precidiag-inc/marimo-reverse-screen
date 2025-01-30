import marimo

__generated_with = "0.10.17"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import pandas as pd
    import numpy as np
    import os
    import networkx as nx
    import plotly.express as px

    from itertools import product
    directory = 'data/raw/'
    return directory, mo, np, nx, os, pd, product, px


@app.cell
def _(List, pd):
    def start_pipeline(df: pd.DataFrame) -> pd.DataFrame:
        return df.copy()

    def dropna(df: pd.DataFrame) -> pd.DataFrame: 
        return df.loc[~df.isna().any(axis = 1)]

    def select_columns(df: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
        return df.loc[:, columns]

    def rename_columns(df: pd.DataFrame, column_names: List[str]) -> pd.DataFrame:
        df.columns = column_names
        return df

    def lower(df:pd.DataFrame) -> pd.DataFrame:
        return df.map(lambda v: v.lower())
    return dropna, lower, rename_columns, select_columns, start_pipeline


@app.cell
def _(pd):
    final_results = pd.read_csv('drug_protein_disease_taxa.csv')
    return (final_results,)


@app.cell
def _(final_results, mo):
    protein_col = mo.ui.multiselect(
        final_results['protein'].unique(),
        label = 'Protein',
    )
    protein_col
    return (protein_col,)


@app.cell
def _(final_results, mo):
    drug_col = mo.ui.multiselect(
        final_results['drug'].unique(),
        label = 'Drug',
    )
    drug_col
    return (drug_col,)


@app.cell
def _(final_results, mo):
    dis_col = mo.ui.multiselect(
        final_results['disease'].unique(),
        label = 'Disease',
    )
    dis_col
    return (dis_col,)


@app.cell
def _(final_results, mo):
    genera_col = mo.ui.multiselect(
        final_results['genera'].unique(),
        label = 'Genera',
    )
    genera_col
    return (genera_col,)


@app.cell
def _(dis_col, drug_col, final_results, genera_col, pd, protein_col):
    protein_mask = final_results['protein'].isin(protein_col.value) if len(protein_col.value) > 0 else ~final_results['protein'].isna()
    drug_mask = final_results['drug'].isin(drug_col.value) if len(drug_col.value) > 0 else ~final_results['drug'].isna()
    dis_mask = final_results['disease'].isin(dis_col.value) if len(dis_col.value) > 0 else ~final_results['disease'].isna()
    genera_mask = final_results['genera'].isin(genera_col.value) if len(genera_col.value) > 0 else ~final_results['genera'].isna()

    mask = pd.concat([protein_mask, drug_mask, dis_mask, genera_mask], axis = 1).all(axis = 1)
    return dis_mask, drug_mask, genera_mask, mask, protein_mask


@app.cell
def _(final_results, mask):
    retrieved = {
        'drug': final_results.loc[mask, 'drug'].unique().shape[0],
        'protein': final_results.loc[mask, 'protein'].unique().shape[0],
        'disease': final_results.loc[mask, 'disease'].unique().shape[0],
        'genera': final_results.loc[mask, 'genera'].unique().shape[0]
    }

    path = [n for n, _ in sorted(retrieved.items(), key = lambda v: v[1])]
    return path, retrieved


@app.cell
def _():
    # taxa
    # filter by microbial proteins
    return


@app.cell
def _():
    # slider for promiscuity
    return


@app.cell
def _(final_results, mask, mo, path, px):
    if mask.sum() > 200:# ==results.shape[0]:
        print('Cannot process so much data. Please update your selection.')
        mofig = ''
    else:
        mofig = mo.ui.plotly(
            px.sunburst(
                final_results.loc[mask],
                path =  path
            )
        )
    mofig
    return (mofig,)


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
