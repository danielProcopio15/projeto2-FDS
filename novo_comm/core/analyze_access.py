import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from django.db import connection

# Exemplo: análise exploratória dos acessos aos temas
# Supondo que existe uma tabela ThemeAccess com campos: user_id, category, count

def fetch_theme_access():
    query = """
        SELECT user_id, category, count
        FROM core_themeaccess
    """
    with connection.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()
    df = pd.DataFrame(rows, columns=['user_id', 'category', 'count'])
    return df

def plot_top_categories(df):
    top = df.groupby('category')['count'].sum().sort_values(ascending=False)
    plt.figure(figsize=(8,4))
    sns.barplot(x=top.index, y=top.values)
    plt.title('Categorias mais acessadas')
    plt.ylabel('Total de acessos')
    plt.xlabel('Categoria')
    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    df = fetch_theme_access()
    print(df.head())
    plot_top_categories(df)
