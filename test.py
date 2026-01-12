import re
import csv
import os
import webbrowser
import tkinter as tk
from tkinter import filedialog, messagebox
from collections import Counter


def extraire_donnees_brutes(chemin_source):
    dossier = os.path.dirname(chemin_source)

    chemin_csv = os.path.join(dossier, "donnees_extraites.csv")
    chemin_html = os.path.join(dossier, "tableau_bord_reseau.html")

    # Regex tcpdump IP classique
    pattern = re.compile(
        r'^(\d{2}:\d{2}:\d{2}\.\d{6}) IP ([\w\.-]+) > ([\w\.-]+)\.([\w\.-]+): Flags \[([\w\.]+)\].*length (\d+)'
    )

    evenements = []
    sources = Counter()
    destinations = Counter()
    services = Counter()
    flags = Counter()

    try:
        with open(chemin_source, "r", encoding="utf-8") as f:
            for ligne in f:
                match = pattern.match(ligne)
                if match:
                    t, src, dst, svc, flg, size = match.groups()
                    dest_complete = f"{dst}.{svc}"

                    evenements.append([t, src, dest_complete, flg, size])

                    sources[src] += 1
                    destinations[dest_complete] += 1
                    services[svc] += 1
                    flags[flg] += 1

        # --- CSV ---
        with open(chemin_csv, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.writer(f, delimiter=";")
            writer.writerow([
                "Horodatage",
                "Source",
                "Destination_Service",
                "Flags",
                "Octets"
            ])
            writer.writerows(evenements)

        # --- HTML ---
        def table_html(titre, headers, data):
            rows = "".join(
                f"<tr><td>{k}</td><td>{v}</td></tr>" for k, v in data
            )
            return f"""
<h2>{titre}</h2>
<table>
<tr>{"".join(f"<th>{h}</th>" for h in headers)}</tr>
{rows}
</table>
"""

        html = f"""<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<title>Tableau de bord réseau</title>
<style>
body {{
    font-family: Arial, sans-serif;
    margin: 40px;
}}
table {{
    border-collapse: collapse;
    width: 100%;
    margin-bottom: 30px;
}}
th, td {{
    border: 1px solid #ccc;
    padding: 6px 10px;
    text-align: left;
}}
th {{
    background-color: #f0f0f0;
}}
h1 {{
    border-bottom: 3px solid #444;
}}
h2 {{
    border-bottom: 2px solid #aaa;
    margin-top: 40px;
}}
</style>
</head>
<body>

<h1>Tableau de bord – Extraction réseau</h1>
<p><strong>Fichier analysé :</strong> {os.path.basename(chemin_source)}</p>

{table_html("Sources actives", ["Source", "Paquets"], sources.most_common())}
{table_html("Destinations / Services", ["Destination", "Paquets"], destinations.most_common())}
{table_html("Ports / Services", ["Service", "Occurrences"], services.most_common())}
{table_html("Flags TCP", ["Flag", "Occurrences"], flags.most_common())}

</body>
</html>
"""

        with open(chemin_html, "w", encoding="utf-8") as f:
            f.write(html)

        webbrowser.open(f"file://{chemin_html}")

        messagebox.showinfo(
            "Extraction terminée",
            "CSV et tableau HTML générés.\nLe navigateur a été ouvert automatiquement."
        )

    except Exception as e:
        messagebox.showerror("Erreur", str(e))


# --- Interface graphique ---
def ouvrir_fichier():
    chemin = filedialog.askopenfilename(
        title="Choisir un fichier dump réseau",
        filetypes=[("Fichiers texte", "*.txt"), ("Tous les fichiers", "*.*")]
    )
    if chemin:
        extraire_donnees_brutes(chemin)


root = tk.Tk()
root.title("Extracteur réseau – HTML natif")
root.geometry("360x160")

tk.Button(
    root,
    text="Choisir le fichier dump",
    command=ouvrir_fichier,
    width=30,
    height=2
).pack(expand=True)

root.mainloop()
