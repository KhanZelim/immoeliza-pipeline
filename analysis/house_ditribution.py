import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'ml', 'data', 'base_clean_data_with_mv.csv')

df = pd.read_csv(file_path)

def house_distribution():
    sns.set_theme(style="whitegrid", palette="muted")

    plt.figure(figsize=(10, 6))
    ax = sns.histplot(df['price'], kde=True, color='skyblue', bins=30, edgecolor='black')

    plt.grid(axis='y', linestyle='--', alpha=0.5)

    plt.xticks(ticks=range(0, 10000000, 1000000), labels=[f'${i}M' for i in range(0, 10)])

    plt.title("Distribution of House Prices", fontsize=18, fontweight='bold', pad=20, color='navy')
    plt.xlabel('Price (in Millions Euro)', fontsize=14, labelpad=10, color='darkslategray')
    plt.ylabel('Number of Houses', fontsize=14, labelpad=10, color='darkslategray')

    for line in ax.lines:
        line.set_color('blue') 
        line.set_linewidth(2)   

    sns.despine(left=True, bottom=False)

    # Check if the images folder exists, if not, create it
    images_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'images')
    if not os.path.exists(images_folder):
        os.makedirs(images_folder)

    image_path = os.path.join(images_folder, 'house_price_distribution.png')

    plt.tight_layout()
    plt.savefig(image_path)
    #plt.show()

    print(f"Plot saved to {image_path}")
    
house_distribution()
