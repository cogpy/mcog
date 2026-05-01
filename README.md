# OpenCog in Pure Maude

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

## Usage

You need Maude 3.5+ installed to run the system.

To run the integration test suite, which verifies all modules:

```bash
maude test-opencog.maude
```

The test suite performs 45 equational reductions and 3 state-space searches, verifying:
- Truth value and attention value arithmetic
- AtomSpace multiset operations
- PLN formula calculation and rule firing
- COMBO program simplification and evaluation
- ECAN parameter configuration
- URE forward chaining derivations

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

## Example: URE Forward Chaining

The Unified Rule Engine manages inference step-by-step. A Forward Chaining state is represented as `fcState(AtomSpace, RuleBase, MaxIterations, CurrentIteration, SourceAtom)`.

```maude
search [1] in OC-URE-FORWARD-CHAINER :
  fcState(
    [concept("cat"), stv(1.0, 0.9), defaultAV]
    [concept("animal"), stv(1.0, 0.9), defaultAV]
    [concept("living-thing"), stv(1.0, 0.9), defaultAV]
    [inheritance(concept("cat"), concept("animal")), stv(0.9, 0.8), defaultAV]
    [inheritance(concept("animal"), concept("living-thing")), stv(0.85, 0.7), defaultAV],
    urRule("deduction", 1.0, "pln-deduction"),
    10,
    0,
    concept("cat"))
=>+ FC:FCState .
```

This applies the rule base to the AtomSpace, incrementing the iteration counter, and returning the updated `fcState` containing the newly derived knowledge.
