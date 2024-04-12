# run this command pip install numpy pandas matplotlib plotly


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import os
import plotly.express as px

df = pd.read_csv(
    "./Bangalore proj.csv",
    parse_dates=["Date"],
    dayfirst=True,
)

print(df.head())
print(df.info())
print(df.isnull().sum())
print(df.Date.dt.year.min(), df.Date.dt.year.max())


fig = make_subplots(
    rows=2,
    cols=2,
    subplot_titles=[
        "ABBIGERE	(in mcft)",
        "AGARA	(in mcft)",
        "AKSHAYANAGARA	(in mcft)",
        "ALLALASANDRA  (in mcft)",
    ],
)

fig.add_trace(go.Scatter(x=df.Date, y=df.ABBIGERE, name="ABBIGERE"), row=1, col=1)
fig.add_trace(go.Scatter(x=df.Date, y=df.AGARA, name="AGARA"), row=1, col=2)
fig.add_trace(
    go.Scatter(x=df.Date, y=df.AKSHAYANAGARA, name="AKSHAYANAGARA"), row=2, col=1
)
fig.add_trace(go.Scatter(x=df.Date, y=df.ALLALASANDRA, name="ALLALASANDRA"), row=2, col=2)

fig.update_layout(
    title_text="Water availability in Bangalore's four major reserviours {}-{}".format(
        df.Date.dt.year.min(), df.Date.dt.year.max()
    )
)

print(fig.show())


df_tidy = df.melt(id_vars=["Date"], var_name="Resoviour", value_name="Water_Level")
print(df_tidy.head())

px.line(
    df_tidy,
    x="Date",
    y="Water_Level",
    facet_col="Resoviour",
    facet_col_wrap=2,
    color="Resoviour",
    title="Water availability in Bangalore's four major reserviours {}-{}".format(
        df.Date.dt.year.min(), df.Date.dt.year.max()
    ),
)


fig = px.line(
    df.melt(id_vars=["Date"], var_name="Resoviour", value_name="Water_Level"),
    x="Date",
    y="Water_Level",
    color="Resoviour",
    facet_col="Resoviour",
    facet_col_wrap=1,
    height=1000,
)
fig.update_yaxes(matches=None)
print(fig.show())


df["total"] = df.drop(columns="Date").sum(axis=1)
print(df.head())

px.line(
    df,
    x="Date",
    y="total",
    title="Total water availability from all four resoviours in mcft",
)

rain_df = pd.read_csv(
    "./chennai_reservoir_rainfall.csv",
    parse_dates=["Date"],
    dayfirst=True,
)
print(rain_df.head())

print(rain_df.dtypes)

px.line(
    rain_df.melt(id_vars=["Date"], var_name="Resoviour", value_name="Rainfall"),
    x="Date",
    y="Rainfall",
    facet_col="Resoviour",
    facet_col_wrap=2,
    color="Resoviour",
)

rain_df["YearMonth"] = pd.to_datetime(
    rain_df.Date.dt.year.astype(str) + rain_df.Date.dt.month.astype(str), format="%Y%m"
)
print(rain_df.head())

print(rain_df.YearMonth.value_counts())


rain_df["total"] = rain_df.drop(columns=["Date", "YearMonth"]).sum(axis=1)
print(rain_df.head())

print(rain_df.groupby("YearMonth").total.sum().reset_index())


px.bar(
    rain_df.groupby("YearMonth").total.sum().reset_index(),
    x="YearMonth",
    y="total",
    # color='season'
)

rain_df["Year"] = pd.to_datetime(rain_df.Date.dt.year.astype(str), format="%Y")
print(rain_df.head())

monthly_rain_df = rain_df.groupby("YearMonth").total.sum().reset_index()
print(monthly_rain_df)

# Creating Season column
month_to_season = {
    1: "winter",
    2: "winter",
    3: "summer",
    4: "summer",
    5: "summer",
    6: "monsoon",
    7: "monsoon",
    8: "monsoon",
    9: "monsoon",
    10: "post-monsoon",
    11: "post-monsoon",
    12: "post-monsoon",
}

monthly_rain_df["season"] = monthly_rain_df.YearMonth.dt.month.map(month_to_season)
print(monthly_rain_df)


px.bar(
    monthly_rain_df,
    x="YearMonth",
    y="total",
    color="season",
    title="Yearly rainfall in the four major resoviour regions in mm",
)

px.bar(
    df.query("Date.dt.month== 3 and Date.dt.day== 1"),
    x="Date",
    y="total",
    title="Availability of water in total at the beginning of summer",
)
