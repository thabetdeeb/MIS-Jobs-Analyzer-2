import pandas as pd
import psycopg2

DATABASE_URL = "postgresql://postgresql_jztr_user:XKajGhxhz6OY25fXrROMzBAbGYHfp42s@dpg-d7tnfmosfn5c73enlgq0-a.oregon-postgres.render.com/postgresql_jztr"

conn = psycopg2.connect(DATABASE_URL)

df = pd.read_sql("SELECT * FROM opportunities;", conn)

conn.close()

df.to_excel("jobs_from_site.xlsx", index=False)

print("✅ Excel נוצר בהצלחה")
print(f"נמצאו {len(df)} רשומות")
print(df.head())
import os

df.to_excel("jobs_from_site.xlsx", index=False)

print("✅ Excel created")

os.startfile("jobs_from_site.xlsx")
import os
import subprocess

df.to_excel("jobs_from_site.xlsx", index=False)

print("✅ Excel created")

# פותח את האקסל
os.startfile("jobs_from_site.xlsx")

# פותח את הדשבורד
subprocess.Popen(
    "py -m streamlit run dashboard.py",
    shell=True
)