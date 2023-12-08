import numpy as np
from fuzzywuzzy import fuzz,process
import os
def filter_terpene_profiler(data):
  filter = ~data['Sample Type'].isin(['Archived', 'NaN'])
  return data[filter]


def stitch_data(data_df, 
                feature_data_df,
                data_name_col, 
                feature_data_name_col, 
                feature_data_features_start):
  data = data_df.to_numpy()
  feature_data = feature_data_df.to_numpy()

  names = np.append(
    data_df.columns.to_numpy(), 
    feature_data_df.columns[feature_data_features_start:].to_numpy()
  )

  data_new_cols_start = data.shape[1] 
  zero_matrix = np.zeros(
    (data.shape[0],
    feature_data[:,feature_data_features_start:].shape[1])
    )
  data = np.column_stack((data, zero_matrix))

  i = 0
  match_count = 0
  mismatch_count = 0

  strain_names = feature_data[:,feature_data_name_col]
  strain_names_dict = {idx: el for idx, el in enumerate(strain_names)}
  match_filter = np.array([], dtype=int)
  for strain in data[:,data_name_col]:
    #print(strain)
    match = process.extractOne(strain,strain_names_dict,scorer=fuzz.token_sort_ratio)
    #print(match)
    if len(match) < 1 or match[1] < 100:
      mismatch_count += 1
      #print('mismatch:', i, match_count,mismatch_count, strain, match)
    else:
      match_count += 1
      # print('match:',i, match_count, mismatch_count, strain, match)
      data[i, data_new_cols_start:] = feature_data[match[2], feature_data_features_start:]
      match_filter = np.append(match_filter, i)
    if mismatch_count > feature_data.shape[0]:
      break
    i += 1

  data_matched = data[match_filter]
  return data_matched, data_new_cols_start, names
