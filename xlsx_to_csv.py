import pandas as pd

if __name__ == "__main__":

    df = pd.read_excel ("Raw_data.xlsx")

    df.dropna(inplace=True)

    df.drop_duplicates(inplace=True)

    df.to_csv ("raw_data.csv", index = None, header=True)

    m = pd.DataFrame(pd.read_csv("raw_data.csv"))