import os
import pandas as pd
import nfl_data_py as nfl 


print(nfl.see_pbp_cols())

prep = nfl.import_pbp_data([2023])
df = pd.DataFrame(prep) 
print(df)