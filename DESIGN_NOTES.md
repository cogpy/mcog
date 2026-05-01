# OpenCog in Pure Maude — Design Notes

## Key Mapping: OpenCog → Maude Rewriting Logic

### AtomSpace → Maude Sorts + Equational Theory
- **Atom** = top sort, subsorts Node < Atom, Link < Atom
- **AtomSpace** = a multiset (soup) of Atoms with AC (assoc-comm) operator
- **TruthValue** = record sort with (strength, confidence) floats
- **AttentionValue** = record sort with (STI, LTI) integers
- **Values** = parameterized sorts (FloatValue, StringValue, LinkValue)

### Type Hierarchy → Maude Sort Hierarchy
- OpenCog's 180+ atom types map directly to Maude subsort declarations
- E.g., `subsort ConceptNode < Node < Atom`
- Multiple inheritance via `subsort X < Y, Z` (Maude supports this)

### Hypergraph → Maude Terms
- Nodes are ground terms: `concept("cat")`, `predicate("is-a")`
- Links are constructor terms: `inheritance(concept("cat"), concept("animal"))`
- The outgoing set of a Link = the arguments of the constructor

### PLN → Maude Rewrite Rules with TruthValue Computation
- Each PLN rule (deduction, induction, abduction, revision) = a conditional rewrite rule
- TruthValue formulas computed equationally
- Forward/backward chaining = strategy-controlled rewriting

### ECAN → Maude Object-Oriented Module
- Atoms as objects with mutable STI/LTI attributes
- Spreading activation = rewrite rules on the configuration
- Hebbian links = associative links with weight updates

### MOSES → Maude Strategy Language
- Program trees = Maude terms (combo language)
- Evolutionary operators (mutation, crossover) = rewrite rules
- Fitness evaluation = equational reduction
- Search strategy = Maude strategy language (srew)

### URE → Maude Meta-Level
- Rule base = a Maude module (reified at meta-level)
- Forward chainer = meta-level strategy applying rules
- Backward chainer = goal-directed meta-level search

### CogServer → Maude Object System (CONFIGURATION)
- MindAgents as objects sending/receiving messages
- Scheduler as rewrite rules on the configuration
- External I/O via Maude's built-in socket/process modules

## Module Hierarchy

```
OPENCOG-MAUDE
├── TRUTH-VALUE          (fmod - strength/confidence arithmetic)
├── ATTENTION-VALUE      (fmod - STI/LTI arithmetic)  
├── ATOM-TYPES           (fmod - sort hierarchy for all atom types)
├── ATOM                 (fmod - atoms with names, truth values, attention values)
├── ATOM-SPACE           (fmod - hypergraph store with query operations)
├── PLN-FORMULAS         (fmod - truth value formulas)
├── PLN-RULES            (mod  - rewrite rules for PLN inference)
├── URE                  (mod  - unified rule engine with forward/backward chaining)
├── ECAN                 (omod - economic attention allocation)
├── MOSES-COMBO          (fmod - combo program representation)
├── MOSES-EVOLVE         (mod  - evolutionary search with strategies)
├── PATTERN-MATCHER      (mod  - graph pattern matching via unification)
├── COG-SERVER           (omod - agent-based cognitive server)
└── OPENCOG              (mod  - top-level integration module)
```
