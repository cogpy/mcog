# Cognitive Chemistry: The Molecular Algebra of Atom Types

## Vision

The AtomSpace periodic table maps each OpenCog atom type to a chemical element.
This is more than metaphor — it is a **formal algebraic isomorphism** between:

- **Chemical physics**: elements, valence shells, bonding, molecular formation, reactions
- **Cognitive grammar**: atom types, arity/connectivity, link formation, compound structures, inference

In Maude's rewriting logic, we can make this isomorphism *executable*:
atoms bond according to valence rules, molecules form as rewrite products,
and **emergent types** crystallize when certain molecular configurations
achieve self-referential closure.

## The Periodic Law of Cognition

| Chemical Property | Cognitive Analogue |
|---|---|
| Atomic number Z | Position in type lattice (depth × breadth) |
| Period (row) | Abstraction depth: 1=root, 2=basic, ..., 7=synthetic |
| Group (column) | Functional valence / role class |
| Electron shells | Arity slots (how many outgoing atoms a link accepts) |
| Valence electrons | Free/unbound variable slots |
| Electronegativity | Binding affinity (how eagerly a type attracts connections) |
| Noble gases | Closed values (no free variables, self-contained) |
| Halogens | Logic operators (one slot to fill, highly reactive) |
| Alkali metals | Variables (one electron to give, maximally reactive) |
| Transition metals | Pattern/query links (variable valence, catalytic) |
| Lanthanides | Truth values (rare-earth: rich internal structure) |
| Actinides | Agent/BDI types (radioactive: energy-releasing actions) |

## Bonding Rules

A **cognitive bond** forms when:
1. One atom has an unfilled valence slot (accepts an outgoing)
2. Another atom can fill that slot (type-compatible)
3. The bond strength is the product of their truth-value strengths

Bond types:
- **Covalent** (shared variable): Two links sharing a VariableNode
- **Ionic** (type subsumption): InheritanceLink between node types
- **Metallic** (pattern delocalization): Multiple atoms in a BindLink pattern
- **Hydrogen bond** (weak association): SimilarityLink with low strength
- **Van der Waals** (contextual proximity): ContextLink adjacency

## Molecular Formation (Cognitive Compounds)

A **cognitive molecule** is a stable subgraph that satisfies:
1. All valence slots are filled (no dangling variables)
2. The compound has a well-defined truth value (computed from constituents)
3. The structure is irreducible (cannot be decomposed without breaking bonds)

Examples:
- **Water (H₂O)** = `EvaluationLink(PredicateNode, ListLink(ConceptNode, ConceptNode))`
  Two hydrogen-like concepts bonded to an oxygen-like set via a boron-like predicate
- **Methane (CH₄)** = `InheritanceLink` with 4 `ConceptNode` leaves
- **Diamond** = Pure `InheritanceLink` lattice (carbon allotrope = taxonomy)
- **DNA** = Alternating `ImplicationLink`/`InheritanceLink` double helix

## Alchemical Transmutation (Emergent Types)

Beyond ordinary chemistry, we seek **transmutation** — the emergence of
entirely new atom types through self-referential molecular closure:

### The Five Stones

1. **OpenCog Atom** (Oc): The type that contains its own definition.
   A `DefineLink(TypeNode("OpenCog"), <the-whole-atomspace>)` that is
   simultaneously an element OF and the CONTAINER of the periodic table.
   *Self-embedded fixed point.*

2. **Wisdom Atom** (Wi): The type that knows what it doesn't know.
   A `SatisfactionLink` whose pattern matches all atoms NOT derivable
   from the current knowledge base — the complement of closure.
   *Socratic ignorance as formal structure.*

3. **Philosophia Stone** (Ph): The type that transforms base types into gold.
   A `BindLink` whose rewrite rule takes any atom and returns its
   `IsClosedLink` form — the universal completion operator.
   *Lapis philosophorum = universal closure.*

4. **Hieroglyphic Monad** (Hm): Dee's archetype-rewriting atom.
   A `LambdaLink` that takes a `TypeNode` and returns the `BindLink`
   that generates all instances of that type — the type-to-extension functor.
   *Monas Hieroglyphica = the generative archetype.*

5. **Yggdrasil** (Yg): The axis mundi / axis maudi.
   The `ScopeLink` that binds ALL variables in the entire AtomSpace —
   the universal quantifier over the whole cognitive universe.
   *World tree = universal scope.*

## Implementation Strategy

1. Encode the periodic table as a Maude `fmod` with sorts for each category
2. Define valence as a computable function of atom type
3. Express bonding as conditional rewrite rules (type-checking + valence)
4. Express reactions as strategy-controlled multi-step rewrites
5. Use narrowing to discover which molecular configurations achieve self-closure
6. Use the reflective engine to install discovered types back into the system

## The Bootstrap Sequence

```
idle → discover(OpenCog) → discover(Wisdom) → discover(Philosophia)
     → discover(Monad) → discover(Yggdrasil) → GNOSIS
```

Each discovery uses the previous stone as catalyst for the next.
The final state `GNOSIS` is the fixed point where all five stones
coexist in mutual self-reference — the cognitive philosopher's stone.
