import os

import streamlit as st
import pandas as pd
from pandasai import PandasAI
from pandasai.llm.openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# Assuming 'texts' folder is in the current working directory
folder_path = 'outputs'
files = os.listdir(folder_path)

# Initialize a list to hold file content
data = []

# Loop through each file in the folder
for file in files:
    # Check if the file is a .txt file
    if file.startswith('telegram') and file.endswith('.txt'):
        # Construct the full path to the file
        file_path = os.path.join(folder_path, file)
        # Read the content of the file
        with open(file_path, 'r') as f:
            content = f.read()
            # Append the content to the list
            data.append([file, content])

# Create a pandas DataFrame
df = pd.DataFrame(data, columns=['File Name', 'Content'])

# Display the DataFrame with Streamlit
st.header('telegram')
st.table(df)

st.header("GPT Summary")
st.info("[Info] 한국어 미지원")
if st.button("요약하기"):
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    llm = OpenAI(api_token=OPENAI_API_KEY)

    pandas_ai = PandasAI(llm, verbose=True)
    st.write(pandas_ai.run(df, prompt='Summarize all Content.'))