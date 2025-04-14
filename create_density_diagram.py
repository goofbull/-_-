import plotly.express as px
import pandas as pd
import matplotlib.pyplot as plt

dataset = pd.read_csv('./csv/words_frequency.csv')

fig = px.density_contour(dataset, x="word", y="frequency", title="Density of Unique Words Frequency")
fig.show()

