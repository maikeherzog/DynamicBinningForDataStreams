import kagglehub
import os
import pandas as pd



def load_london(max_users=None, start_date=None, end_date=None, drop_zeros=True):
    path = kagglehub.dataset_download("zoya77/london-smartgrid-household-energy-usage-dataset")
    print("Path", path)
    df = pd.read_csv(
        os.path.join(path, "energy_consumption_dataset_london.csv"),
        usecols=["User_ID", "Date", "Actual_Energy_kWh"],
        parse_dates=["Date"],
    )
    df = df.dropna()

    # Nullwerte werden entfernt. Kann man über drop_zeros auch ausschalten. 
    if drop_zeros:
        df = df[df["Actual_Energy_kWh"] > 0]

    if max_users is not None:
        users = sorted(df["User_ID"].unique())[:max_users]
        df = df[df["User_ID"].isin(users)]
    if start_date is not None:
        df = df[df["Date"] >= start_date]
    if end_date is not None:
        df = df[df["Date"] <= end_date]

    df["time"] = (df["Date"] - df["Date"].min()).dt.days + 1
    df = df.sort_values(["time", "User_ID"])

    return [(int(t), int(u), float(v)) for t, u, v in df[["time", "User_ID", "Actual_Energy_kWh"]].itertuples(index=False)]


if __name__ == "__main__":
    data = load_london()
    times = [t for t, _, _ in data]
    values = [v for _, _, v in data]
    zeros = sum(1 for _, _, v in data if v == 0)
    print(f"Nullwerte: {zeros} ({zeros / len(data):.1%})")
    print("Anzahl Tupel:", len(data))
    print("Haushalte:", len({u for _, u, _ in data}))
    print("Tage:", min(times), "bis", max(times))
    print("Werte:", min(values), "bis", max(values))
    print("Erste Tupel:", data[:5])