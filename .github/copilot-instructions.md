# OMNIOPSIS AI Agent Instructions

## Project Overview

OMNIOPSIS is a **mathematical, philosophical, and artistic framework** that establishes a bijection between natural numbers and all finite visual representations. This is NOT a software development project—it's a conceptual framework presented through academic writing, manifestos, exhibition proposals, and philosophical texts.

**Core thesis**: Every possible finite image (photograph, painting, diagram, text, musical score) corresponds to exactly one natural number via the enumeration function `F(n) = (k(n))₂₅₆`.

## Repository Structure

- `paper/` — Academic paper (LaTeX) with rigorous mathematical formulation
- `manifesto/` — Philosophical and artistic manifestos explaining the vision
- `philosophy/` — Deep philosophical implications (creativity, meaning, ontology)
- `press-kit/` — Public-facing materials (FAQ, concept summary, press release, bio)
- `gallery-kit/` — Exhibition proposals and art installation concepts
- `examples/` — Concrete enumeration examples and small resolution samples
- `README.md` / `README_FR.md` — Bilingual entry points

## Writing Conventions

### Mathematical Notation
- Use LaTeX for all formulas in markdown: `$F(n) = (k(n))_{256}$`
- Block equations use `$$` delimiters
- Maintain consistency with paper notation:
  - `$\mathbb{N}$` for natural numbers
  - `$\mathcal{I}$` for the set of all images
  - `$w \times h$` for image dimensions
  - `$(k)_{256}$` for base-256 expansion

### Terminology Standards
- **OMNIOPSIS** (all caps) refers to the total framework/project
- **Omniopsis** (capital O) or **the Omniopsis** refers to the mathematical space itself
- Always write "finite visual representations" not "finite images" in formal contexts
- The enumeration function is `F : ℕ → 𝓘` or `F(n) = (k(n))₂₅₆`

### Bilingual Content
- Main README files exist in both English (`README.md`) and French (`README_FR.md`)
- Keep them synchronized in content structure and section ordering
- French content uses formal/academic register ("l'Omniopsis", "représentations visuelles")

### Tone Guidelines
- **Academic paper** (`paper/`): Rigorous, formal, mathematical proofs, theorem-proof structure
- **Manifesto** (`manifesto/`): Bold, declarative, philosophical, poetic but precise
- **Philosophy** (`philosophy/`): Exploratory, questioning, bridging concrete and abstract
- **Press kit** (`press-kit/`): Accessible, clear, FAQ-friendly, bridges technical and general audience
- **Gallery kit** (`gallery-kit/`): Experiential, visual, installation-focused, art world conventions

## Key Concepts to Maintain

### Mathematical Core
- Bijectivity: Every number ↔ exactly one image
- Exhaustiveness: No images are missing from the enumeration
- Polynomial time: O(wh) complexity in both directions
- Base-256 interpretation: Each digit in base 256 is a color component (0-255)

### Philosophical Threads
1. **Creativity as discovery**: Artists select/discover coordinates rather than create ex nihilo
2. **Signal in noise**: Meaningful images are astronomically rare in the total space
3. **Platonism for images**: Images exist mathematically before being rendered
4. **Context creates meaning**: The Omniopsis contains visual substrate; meaning emerges from intention and interpretation

### Connections to Reference
- **Borges' Library of Babel**: Visual counterpart—finite at each resolution, countably infinite overall
- **Sol LeWitt / Conceptual Art**: Specification vs. execution; formula as artwork
- **Mathematical Platonism**: Do images exist independently of physical instantiation?

## Development Workflows

### Compiling the Academic Paper
```bash
cd paper
pdflatex OMNIOPSIS_Academic_Paper.tex
pdflatex OMNIOPSIS_Academic_Paper.tex  # Run twice for references
```
Note: The terminal history shows `pdflatex OMNIOSIS_Academic_Paper.tex` (typo) ran successfully—the actual filename has no typo.

### Version Control
- The repository uses Git (`.git/` present, `.gitignore` exists)
- Commit messages should reference which conceptual layer is being updated (e.g., "Clarify philosophical implications in manifesto")

## Common Tasks

### Extending the Framework
When adding new content:
1. Determine the audience layer (academic/manifesto/press/gallery)
2. Match the existing tone and notation conventions
3. Cross-reference related concepts across documents
4. Maintain consistency with the core mathematical formulation in `paper/OMNIOPSIS_Academic_Paper.tex`

### Updating Documentation
- Update both `README.md` and `README_FR.md` in parallel
- Ensure FAQ answers are accessible to non-technical audiences
- Use concrete examples from `examples/enumeration_examples.md` when explaining abstract concepts
- LaTeX formulas should render correctly as markdown math

### Creating New Sections
- Check existing structure in related documents first
- Philosophy documents: Balance rigor with accessibility
- Gallery proposals: Think experientially (what does a visitor see/feel?)
- Press materials: Start accessible, layer in complexity

## Critical Context

This project bridges three domains:
1. **Mathematics**: Rigorous enumeration theory, bijections, base-256 representations
2. **Philosophy**: Ontology of images, creativity, meaning, Platonism, representation theory
3. **Art**: Conceptual art, installation proposals, aesthetic implications

When editing any document, maintain awareness of how it connects to all three domains. The power of OMNIOPSIS lies in this integration—it's simultaneously a mathematical theorem, a philosophical provocation, and an artwork.
