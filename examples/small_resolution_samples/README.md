# 🌌 Small Resolution Samples  
# 🌌 Échantillons de Petites Résolutions

*A collection of minimal images illustrating the foundations of the Omniopsis*  
*Une collection d’images minimales illustrant les fondements de l’Omniopsis*

---

# 🇬🇧 ENGLISH

## Purpose

This folder contains example images generated using the OMNIOPSIS enumeration function.  
These samples represent the **smallest building blocks** of the Omniopsis — the atoms of the universe of all possible images.

Even at minimal resolutions, the space is complete, structured, and mathematically exhaustive.  
Each file in this folder corresponds to a unique natural number.

---

## Contents

- `image_0000.png` — **n = 0** (pure black)  
- `image_0001.png` — **n = 1** (first red increment)  
- `image_0255.png` — **n = 255** (pure red)  
- `image_0256.png` — **n = 256** (first green increment)  
- `image_65536.png` — **n = 65,536** (first blue increment)  
- `image_16777215.png` — **n = 16,777,215** (pure white)  
- `gradient_2x2.png` — 2×2 grayscale gradient  
- `checkerboard_4x4.png` — 4×4 checkerboard pattern  
- `random_samples/` — folder containing random coordinates (mostly noise)

These examples illustrate how numbers map to visual appearance, from the simplest pixel to small structured patterns.

---

## Generation

Images can be generated using the Python implementation included in the main repository.

Example:

```python
from omniopsis import number_to_image, save_image

# Generate image for n = 255
img = number_to_image(n=255, w=1, h=1)
save_image(img, "image_0255.png")
```

---

## What These Samples Demonstrate

- The enumeration function is **explicit and computable**  
- Small numbers produce simple, predictable images  
- Base‑256 structure determines color progression  
- Patterns emerge from ordered sequences  
- Random numbers produce noise  
- Even tiny resolutions reveal the logic of the Omniopsis  

These images are not arbitrary — they are **coordinates** in a mathematically defined universe.

---

## Notes

More samples will be added as the implementation evolves.  
Larger resolutions will be included in separate folders.

---

# 🇫🇷 FRANÇAIS

## Objectif

Ce dossier contient des exemples d’images générées à l’aide de la fonction d’énumération OMNIOPSIS.  
Ces échantillons représentent les **plus petites briques élémentaires** de l’Omniopsis — les atomes de l’univers de toutes les images possibles.

Même aux résolutions minimales, l’espace est complet, structuré et mathématiquement exhaustif.  
Chaque fichier correspond à un nombre naturel unique.

---

## Contenu

- `image_0000.png` — **n = 0** (noir pur)  
- `image_0001.png` — **n = 1** (premier rouge)  
- `image_0255.png` — **n = 255** (rouge pur)  
- `image_0256.png` — **n = 256** (premier vert)  
- `image_65536.png` — **n = 65 536** (premier bleu)  
- `image_16777215.png` — **n = 16 777 215** (blanc pur)  
- `gradient_2x2.png` — dégradé 2×2  
- `checkerboard_4x4.png` — damier 4×4  
- `random_samples/` — dossier d’échantillons aléatoires (principalement du bruit)

Ces exemples montrent comment les nombres deviennent des images, du pixel le plus simple aux motifs élémentaires.

---

## Génération

Les images peuvent être générées via l’implémentation Python du dépôt principal.

Exemple :

```python
from omniopsis import number_to_image, save_image

# Générer l’image pour n = 255
img = number_to_image(n=255, w=1, h=1)
save_image(img, "image_0255.png")
```

---

## Ce que ces Échantillons Illustrent

- L’énumération est **explicite et calculable**  
- Les petits nombres produisent des images simples et prévisibles  
- La structure en base 256 détermine la progression des couleurs  
- Les motifs émergent de séquences ordonnées  
- Les nombres aléatoires produisent du bruit  
- Même les petites résolutions révèlent la logique de l’Omniopsis  

Ces images ne sont pas arbitraires — ce sont des **coordonnées** dans un univers mathématique.

---

## Notes

D’autres échantillons seront ajoutés au fur et à mesure du développement.  
Les résolutions plus élevées seront placées dans des dossiers séparés.

---

*OMNIOPSIS © 2026 — Diego Morales Magri*