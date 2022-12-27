import json
from tqdm import tqdm
import pandas as pd

#grab and load json
with open('D:/NSynth/nsynth-train/examples.json') as file:
    data_train = json.load(file)
with open('D:/NSynth/nsynth-valid/examples.json') as file:
    data_valid = json.load(file)
with open('D:/NSynth/nsynth-test/examples.json') as file:
    data_test = json.load(file)


#keep only subset
file_train_names = [x for x in tqdm(data_train) if (
    data_train[x]['pitch']>=24 and data_train[x]['pitch']<=84 and data_train[x]['instrument_source_str'] == 'acoustic'
    )]

file_valid_names = [x for x in tqdm(data_valid) if (
    data_valid[x]['pitch']>=24 and data_valid[x]['pitch']<=84 and data_valid[x]['instrument_source_str'] == 'acoustic'
    )]

file_test_names = [x for x in tqdm(data_test) if (
    data_test[x]['pitch']>=24 and data_test[x]['pitch']<=84 and data_test[x]['instrument_source_str'] == 'acoustic'
    )]


#set to dataframe
files_train_df = {
    "train": file_train_names
}
files_train_df = pd.DataFrame(files_train_df)

files_valid_df = {
    "train": file_valid_names
}
files_valid_df = pd.DataFrame(files_valid_df)

files_test_df = {
    "train": file_test_names
}
files_test_df = pd.DataFrame(files_test_df)

#save
files_train_df.to_csv('./file_train_names.csv', index=False)
files_valid_df.to_csv('./file_valid_names.csv', index=False)
files_test_df.to_csv('./file_test_names.csv', index=False)