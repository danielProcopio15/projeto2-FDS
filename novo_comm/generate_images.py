#!/usr/bin/env python
import os
import shutil

# Configurações das categorias
CATEGORY_CONFIG = {
    'economia': {
        'emoji': '💰',
        'color1': '#e74c3c',
        'color2': '#c0392b',
        'subtitle': 'Economia e Negócios'
    },
    'esportes': {
        'emoji': '🏈',
        'color1': '#27ae60',
        'color2': '#229954',
        'subtitle': 'Esportes e Competições'
    },
    'cultura': {
        'emoji': '🎭',
        'color1': '#9b59b6',
        'color2': '#8e44ad',
        'subtitle': 'Arte e Cultura'
    },
    'ciencia': {
        'emoji': '🔬',
        'color1': '#3498db',
        'color2': '#2980b9',
        'subtitle': 'Ciência e Tecnologia'
    },
    'jc360': {
        'emoji': '🎓',
        'color1': '#f39c12',
        'color2': '#e67e22',
        'subtitle': 'Educação e Comunidade'
    },
    'gerais': {
        'emoji': '📰',
        'color1': '#34495e',
        'color2': '#2c3e50',
        'subtitle': 'Notícias Gerais'
    }
}

# Template SVG
SVG_TEMPLATE = """<svg width="800" height="450" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="bgGradient" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:{color1};stop-opacity:1" />
      <stop offset="100%" style="stop-color:{color2};stop-opacity:1" />
    </linearGradient>
  </defs>
  <rect width="100%" height="100%" fill="url(#bgGradient)"/>
  <text x="50%" y="40%" text-anchor="middle" fill="white" font-family="Arial, sans-serif" font-size="36" font-weight="bold">{emoji} {category_upper}</text>
  <text x="50%" y="55%" text-anchor="middle" fill="rgba(255,255,255,0.95)" font-family="Arial, sans-serif" font-size="20">Jornal do Commercio</text>
  <text x="50%" y="70%" text-anchor="middle" fill="rgba(255,255,255,0.8)" font-family="Arial, sans-serif" font-size="18">{subtitle}</text>
  <text x="50%" y="85%" text-anchor="middle" fill="rgba(255,255,255,0.6)" font-family="Arial, sans-serif" font-size="14">{image_name}</text>
</svg>"""

def create_category_images():
    base_path = "core/static/core/css/images"
    
    for category, config in CATEGORY_CONFIG.items():
        category_path = os.path.join(base_path, category)
        
        if not os.path.exists(category_path):
            print(f"❌ Diretório não encontrado: {category_path}")
            continue
            
        print(f"🎨 Processando categoria: {category.upper()}")
        
        # Listar arquivos existentes
        files = os.listdir(category_path)
        
        for file in files:
            file_path = os.path.join(category_path, file)
            
            # Remover extensão para usar como nome da imagem
            image_name = os.path.splitext(file)[0].replace('-', ' ').title()
            
            # Gerar SVG
            svg_content = SVG_TEMPLATE.format(
                color1=config['color1'],
                color2=config['color2'],
                emoji=config['emoji'],
                category_upper=category.upper(),
                subtitle=config['subtitle'],
                image_name=image_name
            )
            
            # Escrever arquivo SVG (mantém extensão .jpg para compatibilidade)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(svg_content)
                
            print(f"  ✅ {file} -> {image_name}")
    
    print("\n🎯 Processo concluído!")
    print("📝 Todas as imagens foram convertidas para SVG com visual do JC")

if __name__ == "__main__":
    create_category_images()