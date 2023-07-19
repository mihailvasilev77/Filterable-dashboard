import pandas as pd

if __name__ == "__main__":

    df = pd.read_excel ("Book2.xlsx")

    df.dropna(inplace=True)

    df.drop_duplicates(inplace=True)

    df.to_csv ("data.csv", index = None, header=True)