# OpenCog in Pure Maude: Architecture Design

## 1. Introduction

This document outlines the architectural design for implementing the OpenCog cognitive framework within pure Maude rewriting logic. OpenCog is a comprehensive artificial general intelligence (AGI) architecture that integrates various cognitive components around a central hypergraph database known as the AtomSpace [1]. Maude, a high-performance reflective language based on rewriting logic, is uniquely suited for this task because its core abstraction—the rewriting of algebraic terms—maps naturally to hypergraph transformations [2].

## 2. Core Concepts Mapping

The translation of OpenCog's C++ and Scheme implementations into Maude involves mapping several fundamental concepts into their rewriting logic equivalents.

### 2.1 The AtomSpace as an Algebraic Sort
In OpenCog, knowledge is represented as a hypergraph where vertices are `Node`s and hyperedges are `Link`s. Both are subtypes of `Atom` [3]. In Maude, this is modeled using algebraic sorts:
- `Atom` is the top-level sort.
- `Node` and `Link` are subsorts of `Atom`.
- The `AtomSpace` itself is modeled as a multiset (or "soup") of `Atom`s, constructed using an associative-commutative (AC) operator, typically denoted by empty syntax (juxtaposition).

### 2.2 Truth Values and Attention Values
OpenCog uses a sophisticated probabilistic logic system where every `Atom` is annotated with a `TruthValue` (typically representing strength and confidence) and an `AttentionValue` (representing Short-Term and Long-Term Importance, or STI and LTI) [4].
In Maude, these are modeled as parameterized constructors attached to atoms:
- `tv(Strength, Confidence)`
- `av(STI, LTI)`
An evaluated atom in the AtomSpace thus takes the form: `atom(Name, tv(S, C), av(STI, LTI))`.

## 3. Module Hierarchy

The implementation is structured into a hierarchy of Maude functional modules (`fmod`), system modules (`mod`), and object-oriented modules (`omod`).

| Module Name | Type | Description |
|-------------|------|-------------|
| `TRUTH-VALUE` | `fmod` | Defines the algebraic operations for probabilistic strength and confidence. |
| `ATTENTION-VALUE` | `fmod` | Defines the integer arithmetic for Short-Term and Long-Term Importance. |
| `ATOM-TYPES` | `fmod` | Declares the complete OpenCog type hierarchy (over 180 types) using Maude subsorts. |
| `ATOM-SPACE` | `fmod` | Defines the hypergraph structure, nodes, links, and the multiset union operator. |
| `PLN-RULES` | `mod` | Implements Probabilistic Logic Networks (PLN) inference rules as conditional rewrite rules. |
| `ECAN` | `omod` | Models Economic Attention Allocation using Maude's object-oriented configuration. |
| `MOSES` | `mod` | Implements Meta-Optimizing Semantic Evolutionary Search using Maude's strategy language. |
| `URE` | `mod` | The Unified Rule Engine, leveraging Maude's meta-level reflection for forward/backward chaining. |

## 4. Probabilistic Logic Networks (PLN)

PLN provides the reasoning engine for OpenCog, handling deduction, induction, abduction, and revision [5]. In Maude, PLN inference steps are implemented as rewrite rules that transform patterns in the AtomSpace while calculating new truth values based on the PLN formulas.

For example, a deduction rule combining `InheritanceLink(A, B)` and `InheritanceLink(B, C)` to produce `InheritanceLink(A, C)` is expressed as a conditional rewrite rule that only fires when the confidence of the resulting deduction exceeds a certain threshold.

## 5. Economic Attention Allocation (ECAN)

ECAN manages the computational resources of the system by allocating attention (STI and LTI) to atoms based on their usefulness [6]. Because ECAN involves stateful updates to atoms (spreading activation), it is best modeled using Maude's object-oriented extensions (`omod`).

Atoms are treated as objects with `sti` and `lti` attributes. Hebbian links facilitate the flow of STI between atoms, modeled as asynchronous message passing within a Maude `Configuration`.

## 6. Meta-Level Reflection and the URE

The Unified Rule Engine (URE) in OpenCog orchestrates the application of rules (like those in PLN) using forward and backward chaining. Maude's reflective capabilities—specifically the `META-LEVEL` module—allow us to treat Maude terms and rules as data [7]. The URE is implemented as a meta-interpreter that controls the application of base-level PLN rewrite rules, guiding the search space efficiently.

## References

[1] OpenCog Foundation. "OpenCog: Building better minds together." https://opencog.org/
[2] Meseguer, J. "Twenty Years of Rewriting Logic." Computer Science Laboratory, SRI International.
[3] OpenCog Wiki. "Atom types." https://wiki.opencog.org/w/Atom_types
[4] OpenCog Wiki. "TruthValue." https://wiki.opencog.org/w/TruthValue
[5] Goertzel, B. et al. "Probabilistic Logic Networks: A Comprehensive Framework for Uncertain Inference."
[6] OpenCog Wiki. "Economic Attention Allocation." https://wiki.opencog.org/w/Economic_Attention_Allocation
[7] Clavel, M. et al. "Reflection, metalevel computation, and strategies in Maude."
