# Quantum Computing — Primer

## What is quantum computing?
Quantum computing uses quantum bits (qubits) which can exist in superposition and be entangled. This enables certain algorithms (for example, Shor's algorithm and Grover's algorithm) to solve particular problems much faster than classical algorithms.

## Relevance to cryptography
- Shor's algorithm can factor large integers in polynomial time on a sufficiently large quantum computer, threatening RSA-style public-key cryptography.
- Grover's algorithm can speed up brute-force search and weaken symmetric key strength roughly by a square-root factor (e.g., AES-256 security becomes similar to AES-128 against Grover's).

## Mitigation directions
- Research and adopt post-quantum cryptography (PQC) schemes (lattice-based, code-based, multivariate, hash-based).
- Use hybrid key-exchange (classical + PQC) during transition.
- Shorten key lifetimes and use forward secrecy where possible.

(This is a short sample document for demo purposes.)
