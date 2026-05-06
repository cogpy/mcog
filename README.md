# OpenCog in Pure Maude (mcog)

This project implements the core systems of the **OpenCog** cognitive architecture entirely in **Pure Maude**, leveraging rewriting logic to model hypergraphs, probabilistic reasoning, attention allocation, and evolutionary program search.

## Overview

OpenCog's architecture revolves around a hypergraph database called the **AtomSpace**, where nodes and links (Atoms) represent knowledge, and cognitive processes (MindAgents) operate concurrently over this graph. 

Maude is a high-performance reflective language and system supporting both equational and rewriting logic specification and programming. It turns out that Maude's algebraic data types and multiset rewriting rules are a highly natural fit for modeling OpenCog:

1. **AtomSpace as a Multiset**: The AtomSpace is simply a multiset ("soup") of annotated atoms (Atoms paired with TruthValues and AttentionValues).
2. **MindAgents as Rewrite Rules**: Cognitive processes like PLN inference, ECAN attention spreading, and MOSES mutation are expressed directly as conditional rewrite rules over the AtomSpace multiset.
3. **Control via Strategy/Search**: Maude's built-in search and strategy languages naturally map to the Unified Rule Engine's (URE) forward and backward chaining.

## Architecture

The implementation consists of the following modules:

### 1. Core Representation
* `truth-value.maude` (`OC-TRUTH-VALUE`): Probabilistic truth values (Strength, Confidence) and their algebraic operations (And, Or, Negate, Revision).
* `attention-value.maude` (`OC-ATTENTION-VALUE`): Attention values (Short-Term Importance, Long-Term Importance, VLTI) for resource allocation.
* `atom-types.maude` (`OC-ATOM-TYPES`): The complete OpenCog Atom type hierarchy (180+ types) encoded as a Maude sort lattice.
* `atom-space.maude` (`OC-ATOM-SPACE`, `OC-ATOM-SPACE-QUERY`): The hypergraph store, modeled as an associative-commutative multiset of annotated atoms, with query and graph traversal operations.

### 2. Probabilistic Logic Networks (PLN)
* `pln.maude` (`OC-PLN-FORMULAS`, `OC-PLN-RULES`): The probabilistic reasoning engine. Implements PLN formulas (Deduction, Modus Ponens, Induction, Abduction) and the corresponding inference rules that derive new links from existing knowledge.

### 3. Economic Attention Networks (ECAN)
* `ecan.maude` (`OC-ECAN-CONFIG`, `OC-ECAN`): The attention allocation subsystem. Implements asymmetric and symmetric Hebbian importance spreading, rent collection, forgetting (garbage collection), and Hebbian learning (link weight updates based on co-activation).

### 4. Meta-Optimizing Semantic Evolutionary Search (MOSES)
* `moses.maude` (`OC-COMBO`, `OC-COMBO-EVAL`, `OC-MOSES-POPULATION`, `OC-MOSES-EVOLVE`): The program learning system. Implements the COMBO functional language (Boolean and Arithmetic expression trees), evaluation environments, populations (Demes), and evolutionary operators (mutation rules).

### 5. Orchestration
* `ure.maude` (`OC-URE-RULE-BASE`, `OC-URE-FORWARD-CHAINER`, `OC-URE-BACKWARD-CHAINER`, `OC-COG-SERVER`, `OC-PATTERN-MATCHER`, `OPENCOG`): The Unified Rule Engine (URE) for forward and backward chaining, pattern matching via substitutions, and the CogServer which rotates execution among the MindAgents.

### 6. Advanced Subsystems (Phase 2)
* `execution-engine.maude` (`OC-EXECUTION-ENGINE`): Atomese Execution Engine (Lambda calculus, beta-reduction, arithmetic eval, PutLink, CondLink, SequentialAnd).
* `pattern-matcher.maude` (`OC-GRAPH-MATCH`): Full first-order unification and graph pattern matching (BindLink, MeetLink, QueryLink, SatisfactionLink).
* `pattern-miner.maude` (`OC-PATTERN-MINER`): Frequent subgraph pattern mining with support counting and I-Surprisingness.
* `spacetime.maude` (`OC-SPACETIME`): Allen's 13 interval relations, TimeServer, temporal inference rules, and spatial bounding boxes.
* `ghost-psi.maude` (`OC-OPENPSI-ENGINE`): OpenPsi motivational system (demands, modulators, action-selection) and GHOST dialogue rules (responder, gambit, rejoinder).
* `meta-opencog.maude` (`OC-META`): Meta-level reflection for cognitive synergy (type introspection, strategy selection, self-modification, inference monitoring).

### 7. AGI-Native Maude Capabilities (Phase 7)
* `reflective-engine.maude` (`OC-REFLECTIVE-INFERENCE`): Gödel Machine layer — rules-as-data with effectiveness tracking, adaptive pruning, and Maude `META-LEVEL` introspection.
* `model-check-cog.maude` (`OC-COG-CHECK`): LTL model-checking of cognitive safety and liveness properties over the AtomSpace as a Kripke structure.
* `narrowing-abduce.maude` (`OC-NARROW-KB`): Complete symbolic abduction via Maude narrowing — given a goal, find all explanatory initial states.
* `parameterized-cog.maude` (`BIO-PLN`, `SOCIAL-PLN`, `PHYS-PLN`): Algebraic transfer learning via parameterized PLN modules instantiated over Biology, Social, and Physics domains.
* `cognitive-cycle.maude` (`OC-COGNITIVE-CYCLE`): Strategy-controlled cognitive heartbeat — composable `smod` strategies for perceive, attend, reason, act, learn cycles.
* `autogenesis.maude` (`OC-AUTOGENESIS`): Emergent goal generation — the system introspects its own drives/metrics and generates new goals via seven autogenesis rules, with safety verification.

### 8. Cognitive Chemistry (Phase 8)
* `cognitive-chemistry.maude` (`OC-ELEMENTS`, `OC-MOLECULES`, `OC-REACTIONS`, `OC-FIVE-STONES`, `OC-BOOTSTRAP`): The Periodic Table of Cognition — atom types mapped to chemical elements with valence/bonding rules; molecular formation via reactions; alchemical transmutation of five emergent types (OpenCog, Wisdom, Philosophia, Monad, Yggdrasil) culminating in GNOSIS; bootstrap loop installing discovered types at runtime.

## Usage

You need Maude 3.0+ installed to run the system.

To run the Phase 1 core integration test suite (48 assertions):

```bash
maude test-opencog.maude
```

To run the Phase 2 advanced subsystem test suite (56 assertions):

```bash
maude test-new-modules.maude
```

Both test suites perform equational reductions and state-space searches, verifying everything from truth value arithmetic to URE forward chaining derivations and full lambda beta-reduction.

## Example: PLN Inference

In Maude, PLN inference rules are applied using the `search` command to find paths through the state space. For example, to perform a deduction:

```maude
search [1] in OC-PLN-RULES :
  [concept("cat"), stv(1.0, 0.9), defaultAV]
  [concept("animal"), stv(1.0, 0.9), defaultAV]
  [concept("living-thing"), stv(1.0, 0.9), defaultAV]
  [inheritance(concept("cat"), concept("animal")), stv(0.9, 0.8), defaultAV]
  [inheritance(concept("animal"), concept("living-thing")), stv(0.85, 0.7), defaultAV]
=>+ AS:AtomSpace
such that
  hasAtom(AS:AtomSpace, inheritance(concept("cat"), concept("living-thing"))) == true .
```

This searches for a state where the `inheritance(cat, living-thing)` link has been derived, successfully returning the AtomSpace containing the new link with its calculated truth value `stv(1.0, 0.6996)`.

## Example: OpenPsi Action Selection

The OpenPsi engine tracks demands (e.g., "energy") and selects actions based on urgency and context. As "energy" urgency increases over time, the system will eventually fire the highest-weight `PsiRule` that satisfies the demand (e.g., eating when hungry):

```maude
crl [psi-fire-rule] :
    psiState(
      [Ctx, TV, AV] AS,
      psiDemand(DN, DU, DT) ;; DS,
      MS,
      psiRule("r", Ctx, Act, DN, RW) ;; PRS,
      GRS, Topic, N)
  =>
    psiState(
      [Ctx, TV, AV] [Act, stv(1.0, 0.9), AV] AS,
      psiDemand(DN, clamp01(DU - 0.1), DT) ;; DS,
      MS,
      psiRule("r", Ctx, Act, DN, RW) ;; PRS,
      GRS, Topic, N + 1)
  if DU > 0.3 /\ tvStrength(TV) > 0.5 .
```

## Testing

Run the full test suite (6 test files, 400+ assertions and searches):

```bash
# Phase 1 — core integration tests
python3 .github/scripts/validate-tests.py test-opencog.maude

# Phase 2 — advanced subsystem tests
python3 .github/scripts/validate-tests.py test-new-modules.maude

# Comprehensive coverage tests (all untested modules)
python3 .github/scripts/validate-tests.py test-coverage.maude

# Algebraic property tests (Phase 6.3)
python3 .github/scripts/validate-tests.py test-properties.maude

# Phase 7 AGI-native capability tests (reflection, model-checking, narrowing, etc.)
python3 .github/scripts/validate-tests.py test-phase3.maude

# Cognitive Chemistry tests (elements, bonds, molecules, alchemy, bootstrap)
python3 .github/scripts/validate-tests.py test-chemistry.maude
```

Benchmarks can be run directly with Maude (`set show timing on` reports rewrite-step counts):

```bash
maude bench-pln.maude            # PLN deduction chains of depth 1–4
maude bench-ecan.maude           # ECAN spreading and forgetting
maude bench-pattern-miner.maude  # pattern mining at various dataset sizes
```

## New Modules (Phase 1–6 Roadmap)

### Phase 1 — Correctness Hardening
* **truth-value.maude**: Added `tvAnd`/`tvOr`/`tvRevision`/`tvNegate` for `ctv` and `itv` variants.  General `[owise]` fallbacks handle mixed-type operands by projecting to strength/confidence.
* **attention-value.maude**: Fixed non-linear `setVLTI` equation (was `V = V`; now uses distinct `V2`).
* **atom-space.maude**: Added `mergeTV` (applies PLN revision if atom already exists) and `getAtomList` (enumerates all atom keys in the space).
* **pln.maude**: Deduction rule now checks `not hasAtom(…, inheritance(A,C))` to prevent duplicate derivation.  Induction and abduction require minimum confidence ≥ 0.1.
* **ecan.maude**: Added `totalSTI`/`normalizeSTI` to the config module; new `OC-ECAN-PARAM` system module provides `ecanState`-wrapped, fully parameterised versions of every spreading, rent, forgetting, and Hebbian rule.

### Phase 2 — Missing Core Features
* **ure.maude**: Added `maxWeightRule` for weighted rule selection; BC modus-ponens decomposition rule; `emptyRB` total-weight invariant.
* **cogserver-full.maude**: New `OC-COG-SERVER-FULL` module with `CogServerFull` — adds `InferenceStrategy` and `AppRecordSet` to the server state; `csf-cycle` records per-rule attempts; `csf-switch-strategy` rotates the strategy when success rate falls below 0.2.
* **pattern-matcher.maude**: Multi-clause `BindLink` matching via `andLink` patterns; new `OC-TYPED-UNIFICATION` module for `TypedVariableLink` type-constrained unification; new `OC-GLOB-MATCH` module for `GlobNode` sequence matching.
* **moses.maude**: New `OC-MOSES-FITNESS` module adds `DataSet`/`DataPoint` types and `evalFitness : BoolExpr DataSet -> Float`; `OC-MOSES-FITNESS-EVOLVE` wires fitness evaluation into the metapopulation loop.

### Phase 3 — Advanced Cognitive Synergy
* **ghost-psi.maude**: `psi-fire-rule` now increments STI of `Ctx` and `Act` atoms (ECAN coupling); new `psi-demand-decay` homeostasis rule; new `ghost-rejoinder` and `ghost-record-topic` rules for multi-turn dialogue.
* **pattern-miner.maude**: `mine-inh-pattern` now injects a PLN `InheritanceLink` with TV derived from support fraction and I-Surprisingness; new `OC-PATTERN-GENERALISE` module provides `generalise`, `extendPattern`, and `extendMinedPattern`.

### Phase 4 — Meta-Level and Reflection
* **meta-opencog.maude**: `OC-SELF-MODIFY` now carries a `URRuleBase` in `SelfModState`; `register-type` injects a corresponding PLN deduction rule into the base; new `adapt-strategy` removes under-performing rules (success rate < 0.1 after ≥ 10 attempts); new `promote-rule` boosts well-performing rules.
* **meta-maude.maude** *(new)*: `OC-META-MAUDE` wraps Maude's built-in `META-LEVEL` (without importing `OC-ATOM-SPACE` to avoid `_,_` conflicts); exposes `doMetaReduce`, `doMetaApply`, `doMetaSearch`.  `OC-META-QUOTE` provides module qids and atom-quoting helpers.

### Phase 5 — I/O and External Integration
* **io-bridge.maude** *(new)*: `OC-SCHEME-SERIAL` serialises any `OcAtom` to Scheme S-expression or JSON strings; `OC-EXTERNAL-SYNC` provides a stub `importAtoms` hook for future REST/Python bridge integration; `OC-ROBOTICS` models sensor and actuator atoms (`sensorSonar`, `motorMove`, `speechSay`) and a `tick-decay` rule that ages short-lived atoms by −5 STI per cycle.

### Phase 7 — AGI-Native Maude Capabilities
* **reflective-engine.maude** *(new)*: `OC-REFLECT-TERMS`, `OC-META-OPS`, `OC-REFLECTIVE-INFERENCE`, `OC-DERIVABILITY-CHECK` — the Gödel Machine layer; rules reified as data with effectiveness tracking; `mostEffective`/`leastEffective` selection; `adapt-rule` pruning; Maude `META-LEVEL` introspection via `cogModuleName`.
* **model-check-cog.maude** *(new)*: `OC-COG-STATE`, `OC-COG-PREDS`, `OC-COG-TRANSITIONS`, `OC-COG-CHECK` — cognitive Kripke structure for Maude's built-in LTL model checker; propositions `noContradiction`, `budgetRespected`, `hasKnowledge`; state-space transitions for PLN inference and ECAN spreading.
* **narrowing-abduce.maude** *(new)*: `OC-NARROW-KB` — constructor-based knowledge base enabling Maude `vu-narrow`/`search` for complete symbolic abduction; deduction, modus-ponens, and similarity-to-inheritance rules over a narrowing-ready term algebra.
* **parameterized-cog.maude** *(new)*: `COGNITIVE-DOMAIN` functional theory; `PLN-CORE{D}` parameterized PLN module; `BIO-PLN`, `SOCIAL-PLN`, `PHYS-PLN` instantiations via views — algebraic transfer learning across Biology, Social, and Physics domains.
* **cognitive-cycle.maude** *(new)*: `OC-CYCLE-STATE`, `OC-COGNITIVE-CYCLE` — strategy-controlled cognitive cycle using Maude's `smod`; composable strategies `perceive`, `attend`, `reason`, `act`, `learn`, `tick`, `basicCycle`, `deliberative`, `reactive`, `drainPercepts`.
* **autogenesis.maude** *(new)*: `OC-INTROSPECTION`, `OC-GOAL-GENERATOR`, `OC-AUTOGENESIS` — emergent goal generation; seven autogenesis rules (exploration, inference-boost, attention-rebalance, drive-satisfaction, meta-learning, social, creativity); six-phase autogenesis loop (introspect → analyze → generate → verify → install → execute) with bounded-iteration safety check.

### Phase 8 — Cognitive Chemistry
* **cognitive-chemistry.maude** *(new)*: `OC-ELEMENTS`, `OC-MOLECULES`, `OC-REACTIONS`, `OC-FIVE-STONES`, `OC-BOOTSTRAP` — the Periodic Table of Cognition; 20 cognitive elements (helium through gold) with atomic number, symbol, period, group, valence, and electronegativity; covalent/ionic/metallic bond classification; molecular formation via synthesis reactions; five alchemical stones (OpenCog, Wisdom, Philosophia, Monad, Yggdrasil); bootstrap loop that installs discovered emergent types into a `TypeRegistry`.

### Phase 6 — Verification and Formal Properties
* **test-properties.maude** *(new)*: Algebraic laws — `tvAnd`/`tvOr` commutativity and associativity, `mergeTV` idempotence, ECAN rent monotonicity, forgetting termination, `normalizeSTI` budget invariant, `tvRevision` commutativity, PLN duplicate-derivation guard.
* **bench-pln.maude** *(new)*: PLN deduction benchmarks over taxonomy chains of depth 1–4.
* **bench-ecan.maude** *(new)*: ECAN benchmarks — single-hop spreading, chain spreading, symmetric equilibration, parameterised ECAN.
* **bench-pattern-miner.maude** *(new)*: Pattern miner benchmarks — small/medium datasets, mixed link types, support count accuracy, I-Surprisingness range.

## License

AGPL-3.0 (following OpenCog).
