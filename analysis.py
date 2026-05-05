import pandas as pd
import matplotlib.pyplot as plt

links = {
    "2008": "https://raw.githubusercontent.com/your-repo/fuel_2008.csv",
    "2018": "https://raw.githubusercontent.com/your-repo/fuel_2018.csv"
}

dataframes = {}

for year, link in links.items():
    dataframes[year] = pd.read_csv(link)

def explore_data(df, year):
    print(f"\n--- Analysis for {year} ---")
    print("Shape:", df.shape)
    print("Duplicate Rows:", df.duplicated().sum())
    print("\nData Types:\n", df.dtypes)
    print("\nMissing Values:\n", df.isnull().sum())
    print("\nUnique Values Count:\n", df.nunique())
    if 'fuelType' in df.columns:
        print("\nFuel Type Counts:\n", df['fuelType'].value_counts())

for year, df in dataframes.items():
    explore_data(df, year)

def clean_data(df):
    df = df.drop_duplicates()
    df = df.dropna()
    if 'comb08' in df.columns:
        df['comb08'] = pd.to_numeric(df['comb08'], errors='coerce')
    return df

for year in dataframes:
    dataframes[year] = clean_data(dataframes[year])

for year, df in dataframes.items():
    if 'VClass' in df.columns:
        mpg = df.groupby('VClass')['comb08'].mean()
        print(f"\nAverage MPG by Vehicle Class ({year}):\n", mpg)

years = []
avg_mpg = []

for year, df in dataframes.items():
    if 'comb08' in df.columns:
        years.append(year)
        avg_mpg.append(df['comb08'].mean())

plt.figure()
plt.bar(years, avg_mpg)
plt.xlabel("Year")
plt.ylabel("MPG")
plt.title("Average MPG Comparison")
plt.show()

latest_year = list(dataframes.keys())[-1]
df_latest = dataframes[latest_year]

if 'fuelType' in df_latest.columns:
    plt.figure()
    df_latest['fuelType'].value_counts().plot(kind='bar')
    plt.xlabel("Fuel Type")
    plt.ylabel("Count")
    plt.title(f"Fuel Type Distribution - {latest_year}")
    plt.show()

if 'displ' in df_latest.columns:
    plt.figure()
    plt.scatter(df_latest['displ'], df_latest['comb08'])
    plt.xlabel("Engine Size")
    plt.ylabel("MPG")
    plt.title(f"Engine Size vs MPG ({latest_year})")
    plt.show()

for year, df in dataframes.items():
    if 'smartWay' in df.columns:
        count = len(df[df['smartWay'] == 'Yes'])
        print(f"SmartWay Vehicles ({year}):", count)

print("\nAnalysis Completed Successfully!")