# TODO
- Topology Accept Genome Refactor
- [ ] Refactor Signal
    - [X] Manhattan Distance
    - [ ] Jitter
    - [ ] Signal Needs a Genome
- [ ] Bit compression
    - [X] FOV -> UP DOWN LEFT RIGHT ? ABOVE BELOW ? - cardinal directions truth table
    - [ ] Unique POS
- Node Max Min
- lookup method
- Response affordance (max time allowed... must answer before ready)
- [X] Individual
Genetic Algorithm Enhancements
    - genome.to_list?
    - Genome.to_binary

BioSim Revisions
    - Change nucleotide to True/False
    - Leverage Codons as sequences of Nucleotides

- Dynamic Species customization
    - FieldOfView definable for a species
    - Position arity
    - Nucleotide low, high
    - topology num_actions for Decisions arity
    - Structural? Haplotypes?

- Lacunar Theory
    - Non archimedean assignments


- Computer Vision
    - [X] profile
- Individual Fitness
- Train Test Valid Split
- Genetic algorithm solver
    - GA Transfer Learning
    - Stasis Oblivious Fitness
    - Signal Propagation Compression // Stasis Limits
    - Initial Pop for Diversity
        Sigma (x - 4^i) worst case -> FT@3 = 64 => 64 << init pop
- Multi channel topologies 
    - RGB
- RL Env
- LLM Datasets

# Done
- stasis - action witnesses
- lut -> state -> action
- energy evaluation (stasis claim)
    - Species
    - [X] LUT Generation with >minimum decidable nodes
- Genome Refactor
    - [X] Species Chromosomes
    - [X] Individual Chromosomes
    - [X] Haplotype
    - [X] Allele -> Strip Gene metadata (e.g. high, low)
    - [X] Chromosome accept Species Structure
    - [X] Genome accepts Species; genes themselves are fixed cardinality