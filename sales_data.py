import pandas as pd

df= pd.read_csv(Amazon Sale Report.csv")
df= df.drop_duplicates()
'''print(df.info)
print(df.head)
print(df.tail)'''

df.columns
df['Courier Status'] = df['Courier Status'].fillna('Unknown')

df['Amount'] = pd.to_numeric(df['Amount'], errors='coerce')
df['Amount'] = df['Amount'].fillna(df['Amount'].mean())

df['currency'] = df['currency'].fillna('INR')

cols_to_fill = ['fulfilled-by', 'ship-city', 'ship-state', 'ship-postal-code', 'ship-country']
df[cols_to_fill] = df[cols_to_fill].fillna('unknown')


df = df.drop(['promotion-ids', 'Unnamed: 22'], axis=1)
print(df.columns.tolist())


print(df.isnull().sum())
df.to_csv(sales_cleaned.csv", index=False)
