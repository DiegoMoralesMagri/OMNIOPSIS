# **OMNIOPSIS**  
### *L’espace total de toutes les représentations visuelles finies*

> **OMNIOPSIS** désigne l’ensemble complet de toutes les formes visuelles et symboliques finies pouvant être encodées sous forme d’images numériques.  
> C’est un espace mathématique, un cadre conceptuel et un horizon artistique.

---

## 🌌 Présentation générale

**OMNIOPSIS** repose sur une idée simple mais vertigineuse :

> **Toute représentation visuelle finie correspond à un nombre naturel unique.**

Cela inclut :

- les photographies  
- les peintures  
- les diagrammes  
- les cartes  
- les partitions musicales  
- les notations mathématiques  
- les textes écrits  
- les plans architecturaux  
- tous les systèmes symboliques visuels  

Si cela peut être rendu visuellement, cela appartient à **l’Omniopsis**.

Le cadre établit une bijection explicite :



\[
F : \mathbb{N} \longrightarrow \text{Omniopsis}
\]



en interprétant chaque nombre naturel comme :

- une largeur \(w\)  
- une hauteur \(h\)  
- un entier \(k\) représentant les pixels  

puis en développant \(k\) en base 256 pour obtenir les valeurs RGB.

---

## 🔑 Concepts clés

### **Énumération totale**
Chaque image finie possible — à n’importe quelle résolution — apparaît exactement une fois.

### **Inclusion symbolique**
Tous les systèmes symboliques visuellement encodables sont des sous‑ensembles de l’Omniopsis.

### **Minimalité mathématique**
L’énumération est explicite, bijective et calculable en temps polynomial.

### **Profondeur philosophique**
OMNIOPSIS reformule des questions fondamentales :

- qu’est‑ce qu’une représentation  
- qu’est‑ce que percevoir  
- qu’est‑ce que créer  
- comment les formes visuelles émergent‑elles  
- quel est le lien entre nombre, image et sens  

---

## 📄 Article académique

Le cadre mathématique complet est présenté dans :

**OMNIOPSIS — A Mathematical Framework for the Enumeration of All Finite Visual Representations**  
*Diego Morales Magri, 2026*

📄 **[Lire l’article complet](paper/OMNIOPSIS_Academic_Paper.pdf)**

### Citation

```bibtex
@article{moralesmagri2026omniopsis,
  title={OMNIOPSIS --- A Mathematical Framework for the Enumeration of All Finite Visual Representations},
  author={Morales Magri, Diego},
  journal={Unpublished manuscript},
  year={2026},
  month={January}
}
```

---

## 🧭 Structure du dépôt

```
omniopsis/
│
├── paper/
│   ├── OMNIOPSIS_Academic_Paper.pdf
│   └── README.md
│
├── manifesto/
│   ├── Omniopsis_Manifesto.md
│   └── Manifesto_Short_Version.md
│
├── philosophy/
│   ├── philosophical_vision.md
│   ├── implications_for_knowledge.md
│   └── implications_for_art.md
│
├── gallery-kit/
│   ├── exhibition_proposal.md
│   ├── wall_texts.md
│   ├── artwork_descriptions.md
│   └── installation_concepts.md
│
├── press-kit/
│   ├── press_release.md
│   ├── concept_summary.md
│   ├── bio_Diego_Morales_Magri.md
│   └── FAQ.md
│
├── examples/
│   ├── enumeration_examples.md
│   └── small_resolution_samples/
│
└── README.md
```

---

## 🔢 Le cœur mathématique (version simplifiée)

OMNIOPSIS repose sur une fonction minimale :

1. **Décomposer** chaque entier \(n\) en un triplet \((w, h, k)\)  
2. **Interpréter** \(k\) comme un nombre en base 256  
3. **Développer** \(k\) en valeurs RGB :  
   \((r_0, g_0, b_0, r_1, g_1, b_1, \ldots)\)

Pour une résolution fixe :



\[
I_{w,h}(k) = (k)_{256} \in \{0, \ldots, 255\}^{3wh}
\]



où \(k\) varie de \(0\) à \(256^{3wh} - 1\).

### Points remarquables dans l’Omniopsis

- \(I(0)\) : l’image entièrement noire  
- \(I(1)\) : noir + premier pixel rouge = 1  
- \(I(256^3 - 1)\) : premier pixel blanc  
- \(I(256^{3wh} - 1)\) : l’image entièrement blanche  

Entre ces extrêmes se trouvent :

- toutes les photos jamais prises  
- toutes les peintures jamais créées  
- tous les plans, schémas, partitions  
- tous les cadres de tous les films  
- toutes les images encore inimaginées  

---

## 🌐 Implications

### **Pour l’informatique**
- énumération canonique des données visuelles  
- base pour mesurer la complexité des images  
- nouvelles perspectives en théorie algorithmique de l’information  

### **Pour la philosophie**
- chaque image concevable correspond à un entier  
- l’espace des images devient un objet structuré et parcourable  
- questionne la perception, le sens, la représentation  

### **Pour l’art**
- la formule devient une œuvre conceptuelle  
- analogue visuel de la *Bibliothèque de Babel*  
- pont entre art instructionnel et esthétique numérique  

---

## 🤝 Contribuer

Les contributions sont les bienvenues :

- réflexions philosophiques  
- interprétations artistiques  
- implémentations techniques  
- ressources pédagogiques  
- traductions  

Ouvre une *issue* pour discuter d’une contribution importante.

---

## 👤 Auteur

**Diego Morales Magri**  
Chercheur indépendant & artiste conceptuel  
Théoricien de la représentation

---

## 🗝️ Mots‑clés

Omniopsis, représentation, énumération, systèmes symboliques, esthétique numérique, art conceptuel, philosophie de l’information, espace total des images, art mathématique

---

## ✨ Pensée finale

> *Si chaque image est un nombre, alors voir devient un acte de sélection.*  
> *OMNIOPSIS est l’espace d’où émergent toutes les visions.*
