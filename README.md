# **OMNIOPSIS**  
### *The total space of all finite visual representations*

> **OMNIOPSIS** is the name we give to the complete set of all finite visual and symbolic forms that can be encoded as digital images.  
> It is a mathematical space, a conceptual framework, and an artistic horizon.

---

## 🌌 Overview

**OMNIOPSIS** is built on a simple but powerful idea:

> **Every finite visual representation corresponds to a unique natural number.**

This includes:

- photographs  
- paintings  
- diagrams  
- maps  
- musical scores  
- mathematical notation  
- written text  
- architectural plans  
- symbolic systems of every kind  

If it can be rendered visually, it belongs to the **Omniopsis**.

The framework provides an explicit bijection:



\[
F : \mathbb{N} \longrightarrow \text{Omniopsis}
\]



by interpreting each natural number as:

- a width \(w\)  
- a height \(h\)  
- a pixel‑encoding integer \(k\)  

and expanding \(k\) in base 256 to obtain RGB values.

---

## 🔑 Key Concepts

### **Total Enumeration**
Every possible finite image — at any resolution — appears exactly once.

### **Symbolic Inclusion**
All symbolic systems that can be visually encoded are subsets of the Omniopsis.

### **Mathematical Minimality**
The enumeration is explicit, bijective, and computable in polynomial time.

### **Philosophical Depth**
OMNIOPSIS reframes questions about:

- representation  
- perception  
- creativity  
- knowledge  
- the ontology of images  

---

## 📄 Academic Paper

The full mathematical framework is presented in:

**OMNIOPSIS — A Mathematical Framework for the Enumeration of All Finite Visual Representations**  
*Diego Morales Magri, 2026*

📄 **[Read the full paper](paper/OMNIOPSIS_Academic_Paper.pdf)**

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

## 🧭 Repository Structure

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

## 🔢 The Mathematical Core (in simple terms)

OMNIOPSIS is grounded in a minimal function:

1. **Decompose** each natural number \(n\) into a triplet \((w, h, k)\)  
2. **Interpret** \(k\) as a number in base 256  
3. **Expand** \(k\) into RGB values:  
   \((r_0, g_0, b_0, r_1, g_1, b_1, \ldots)\)

For a fixed resolution:



\[
I_{w,h}(k) = (k)_{256} \in \{0, \ldots, 255\}^{3wh}
\]



where \(k\) ranges from \(0\) to \(256^{3wh} - 1\).

### Notable Points in the Omniopsis

- \(I(0)\): The completely black image  
- \(I(1)\): Black image with first pixel’s red component = 1  
- \(I(256^3 - 1)\): Black image with first pixel white  
- \(I(256^{3wh} - 1)\): The completely white image  

Between these extremes lie all photographs ever taken, all paintings ever created, all frames of every film, and all images yet to be conceived.

---

## 🌐 Implications

### **For Computer Science**
- Canonical enumeration of visual data  
- Foundation for measuring image complexity  
- New perspectives on algorithmic information theory  

### **For Philosophy**
- Every conceivable image corresponds to a natural number  
- The space of images becomes a structured, traversable object  
- Raises questions about perception, meaning, and representation  

### **For Art**
- The formula itself becomes a conceptual artwork  
- A visual analogue to Borges’ *Library of Babel*  
- Bridges instruction-based art and digital aesthetics  

---

## 🤝 Contributing

Contributions are welcome:

- philosophical reflections  
- artistic interpretations  
- technical implementations  
- educational materials  
- translations  

Open an issue to discuss substantial contributions.

---

## 👤 Author

**Diego Morales Magri**  
Independent Researcher & Conceptual Artist  
Theorist of Representation


---

## 🗝️ Keywords

Omniopsis, representation, enumeration, symbolic systems, digital aesthetics, conceptual art, philosophy of information, total image space, mathematical art

---

## ✨ Closing Thought

> *If every image is a number, then the act of seeing becomes an act of selection.*  
> *OMNIOPSIS is the space from which all visions emerge.*
