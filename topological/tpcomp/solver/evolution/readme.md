## Steps
1. Evaluate Population
    - Rank individuals against fitness heuristic
2. Construct Mating Pool
  - Each candidate decides will reproduce: YES/NO
    - Highest fitness decide first
    - Must select living, non-family member (within 3 generations), not already selected this cycle
3. Fertilization
    - Splice mating pool genomes
4. Mortality
    - Individuals over their max age die
5. Mutate
    - Mutate unborn population
        - Swap
        - Replace
        - Insertion
        - Deletion = Delete + Insert + Replacement
        - Reverse (Between locus `a` and `b`)
6. Next Generation
    - Birth fertilized population
    - Merge with remaining population
7. Repeat.


Gene Ideas:
- Fertilization period (structural?)
- Mortality limit (Structural and environmental)
- Subjective heuristics (non-structural, environmental)
- Replacement frequency (1/person = stable population excluding environmental factors)
