import pandas as pd

if __name__ == "__main__":
    dir = input("Please enter the files directory:")
    sheet = input("Please enter the sheet you wish to convert:")

    df = pd.read_excel(dir, sheet_name=int(sheet))

    df.dropna(inplace=True)

    df.drop_duplicates(inplace=True)

    df.to_csv("data.csv", index = None, header=True)