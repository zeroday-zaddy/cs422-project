import numpy as np

def filter_terpene_profiler(data):
  filter = ~data['Sample Type'].isin(['Archived', 'NaN'])
  return data[filter]