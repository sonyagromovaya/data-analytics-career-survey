"""Reproducible exploratory analysis of a SYNTHETIC survey dataset."""
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent
DATA = ROOT / 'data' / 'synthetic_survey_responses.csv'
CHARTS = ROOT / 'charts'
CHARTS.mkdir(exist_ok=True)

df = pd.read_csv(DATA, keep_default_na=False)
assert df.shape[1] == 16, 'Expected timestamp plus 15 question columns'

status = df.iloc[:, 1]
motivation = df.iloc[:, 6]
hours = pd.to_numeric(df.iloc[:, 8], errors='coerce')
obstacle = df.iloc[:, 12]

print(f'Synthetic responses: {len(df)}')
print(f'Average planned study hours/week: {hours.mean():.2f}')
print('\nMotivation counts:\n', motivation.value_counts().to_string())
print('\nMean study hours by professional status:\n',
      pd.DataFrame({'status':status,'hours':hours}).groupby('status')['hours'].agg(['count','mean']).round(2).to_string())
print('\nObstacle counts:\n', obstacle.value_counts().to_string())

fig, ax = plt.subplots(figsize=(10, 5))
motivation.value_counts().sort_values().plot.barh(ax=ax)
ax.set(title='Primary motivations (synthetic responses, n=25)', xlabel='Responses', ylabel='')
fig.tight_layout()
fig.savefig(CHARTS / 'motivations.png', dpi=160)
plt.close(fig)

fig, ax = plt.subplots(figsize=(10, 5))
(pd.DataFrame({'status':status,'hours':hours}).groupby('status')['hours'].mean()
 .sort_values().plot.barh(ax=ax))
ax.set(title='Average weekly study availability by status (synthetic)', xlabel='Hours per week', ylabel='')
fig.tight_layout()
fig.savefig(CHARTS / 'study_hours_by_status.png', dpi=160)
plt.close(fig)

fig, ax = plt.subplots(figsize=(10, 5))
obstacle.value_counts().sort_values().plot.barh(ax=ax)
ax.set(title='Main learning obstacles (synthetic responses, n=25)', xlabel='Responses', ylabel='')
fig.tight_layout()
fig.savefig(CHARTS / 'obstacles.png', dpi=160)
plt.close(fig)
