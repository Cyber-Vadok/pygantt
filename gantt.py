import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime

# === Attività ===
attivita = [
    {"nome": "Analisi iniziale", "inizio": "2026-01-10", "fine": "2026-05-15"},
    {"nome": "Sviluppo prototipo", "inizio": "2026-05-16", "fine": "2027-01-31"},
    {"nome": "Validazione", "inizio": "2027-02-01", "fine": "2028-06-30"},
    {"nome": "Rilascio finale", "inizio": "2028-07-01", "fine": "2029-03-30"},
]

# === Preparazione dati ===
df = pd.DataFrame(attivita)
df['inizio'] = pd.to_datetime(df['inizio'])
df['fine'] = pd.to_datetime(df['fine'])
df['durata'] = df['fine'] - df['inizio']

# === Intervallo temporale ===
start = pd.Timestamp("2026-01-01")
end = pd.Timestamp("2029-12-31")

trimestri = pd.date_range(start=start, end=end, freq='3MS')  # ogni 3 mesi
anni = pd.date_range(start=start, end=end, freq='YS')        # ogni anno

# === Spaziatura e dimensioni figura ===
spaziatura = 0.4  # più basso = attività più vicine
y_pos = [i * spaziatura for i in range(len(df))]
altezza_fig = max(2, spaziatura * len(df))
fig, ax = plt.subplots(figsize=(12, altezza_fig))

# === Disegna barre con nuove posizioni Y ===
colore = 'lightblue'
bar_height = 0.2
for y, row in zip(y_pos, df.itertuples()):
    ax.barh(y, row.durata.days, left=row.inizio,
            height=bar_height, color=colore,
            edgecolor='black', linewidth=1.2)

# === Etichette asse Y ===
ax.set_yticks(y_pos)
ax.set_yticklabels(df['nome'])
ax.invert_yaxis()

# === Separatori trimestrali ===
for t in trimestri:
    ax.axvline(t, color='lightgray', linestyle='--', linewidth=0.8)

# === Etichette trimestri sotto ===
for t in trimestri:
    centro_t = t + pd.DateOffset(days=45)
    trimestre_num = (t.month - 1) // 3 + 1
    ax.text(centro_t, -0.4, f"Q{trimestre_num}", ha='center', va='center', fontsize=8)

# === Etichette anni sopra ===
for y in anni:
    centro_anno = y + pd.DateOffset(months=6)
    ax.text(centro_anno, max(y_pos) + 0.5, str(y.year),
            ha='center', va='bottom', fontsize=10, fontweight='bold')

# === Separatori anni ===
for y in anni:
    ax.axvline(y, color='black', linestyle='-', linewidth=1.2)

# === Asse X ===
ax.set_xlim(start, end)
ax.set_xticks([])
ax.set_xlabel("")

# === Titolo ===
fig.suptitle("Diagramma di Gantt con anni e trimestri (2026–2029)",
             fontsize=14, fontweight='bold')

# === Layout ===
plt.subplots_adjust(top=0.88)
plt.tight_layout()
plt.savefig("gantt.png", dpi=300, bbox_inches='tight')
print("Grafico salvato in gantt.png")

