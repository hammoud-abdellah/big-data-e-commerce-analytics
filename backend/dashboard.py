#HAMMOUD Abdellah
import os
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Fonction pour charger et combiner les fichiers de logs dans un DataFrame
def load_logs_data(output_dir, start_date, end_date):
    all_data = []
    
    # Parcourir les fichiers du répertoire output
    for file_name in os.listdir(output_dir):
        if file_name.endswith(".txt"):
            # Extraire l'heure du nom de fichier (format: 2023051012.txt)
            file_hour = file_name.split('.')[0]
            file_datetime = datetime.strptime(file_hour, "%Y%m%d%H")
            
            # Vérifier si la date du fichier est dans la plage spécifiée
            if start_date <= file_datetime <= end_date:
                file_path = os.path.join(output_dir, file_name)
                df = pd.read_csv(file_path, sep="|", header=None, names=["timestamp", "product", "total_price"])
                df["timestamp"] = pd.to_datetime(df["timestamp"], format="%Y/%m/%d %H")
                all_data.append(df)
    
    # Combiner toutes les données dans un seul DataFrame
    if all_data:
        combined_df = pd.concat(all_data, ignore_index=True)
        return combined_df
    else:
        print("Aucune donnée trouvée pour la plage de dates spécifiée.")
        return pd.DataFrame()

# Fonction pour afficher le Dashboard
def display_dashboard(df):
    # Si le DataFrame est vide, ne rien afficher
    if df.empty:
        print("Pas de données à afficher.")
        return
    
    # Agrégation des données : somme des prix par produit
    product_sales = df.groupby('product')['total_price'].sum().sort_values(ascending=False)
    
    # Affichage des statistiques
    print("Top 5 des produits avec les ventes les plus élevées :")
    print(product_sales.head())
    
    # Visualisation des ventes par produit
    product_sales.plot(kind='bar', figsize=(10, 6), color='skyblue')
    plt.title("Ventes par produit")
    plt.xlabel("Produit")
    plt.ylabel("Total des ventes (en monnaie)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
    
    # Visualisation des ventes par heure (total des ventes par heure)
    hourly_sales = df.groupby('timestamp')['total_price'].sum()
    hourly_sales.plot(kind='line', figsize=(10, 6), color='green')
    plt.title("Ventes par heure")
    plt.xlabel("Heure")
    plt.ylabel("Total des ventes (en monnaie)")
    plt.tight_layout()
    plt.show()

# Entrée des dates de début et de fin
start_date_str = input("Entrez la date de début (YYYY-MM-DD) : ")
end_date_str = input("Entrez la date de fin (YYYY-MM-DD) : ")

# Conversion des chaînes de caractères en objets datetime
start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
end_date = datetime.strptime(end_date_str, "%Y-%m-%d")

# Répertoire contenant les fichiers de sortie
output_dir = "D:/Cours et Labs/Big Data/e-commerce/backend/output"

# Charger et filtrer les données
df = load_logs_data(output_dir, start_date, end_date)

# Afficher le Dashboard
display_dashboard(df)
