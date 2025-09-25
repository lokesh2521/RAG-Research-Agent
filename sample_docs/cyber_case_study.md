# Case Study: Migration to Post-Quantum Safe TLS (Sample)

Organization X prepared a lab migration to evaluate post-quantum key exchange for TLS. Key takeaways:
- A hybrid key-exchange combining ECDHE + a lattice-based KEM was implemented to preserve current compatibility and provide PQ assurance.
- Latency increased modestly (benchmarked at ~5-12% overhead depending on chosen PQ algorithm and implementation).
- Performance and packet size impacts should be validated for high-throughput gateways.

Recommendations:
- Start by inventorying long-lived encrypted data and prioritized services for PQ migration.
- Adopt hybrid key exchange in high-risk channels (VPN, inter-datacenter links) as a first step.
- Monitor NIST PQC standardization outcomes and vendor support timelines.
