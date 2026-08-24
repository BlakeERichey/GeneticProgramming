# TODO
- alleles / dynamic topology construction
    - Species
    - [X] LUT Generation with >minimum decidable nodes
- Genome Refactor
    - Species Chromosomes
    - Individual Chromosomes
    - Haplotype
    - Allele -> Strip Gene metadata (e.g. high, low)
    - Chromosome accept Species Structure
    - Genome accepts Species; genes themselves are fixed cardinality
- Topology Acceptance Refactor
- Individual

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
    - [ ] Refactor Signal
        - [ ] Manhattan Distance
    - [ ] Bit compression
        - [ ] FOV -> UP DOWN LEFT RIGHT ? ABOVE BELOW ? - cardinal directions truth table
        - [ ] Unique POS
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