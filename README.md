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

## License

AGPL-3.0 (following OpenCog).
