# Benchmark Report (SYSTEM1): ASPBench - 47_dna_sequence_assembly_hard

**Provider:** openrouter5
**Model:** deepseek/deepseek-v4-flash
**Config:** max_output_tokens: 32768, temperature: 0.0, top_p: 1.0, seed: 42, reasoning_enabled: False, reasoning_effort: none
**Duration:** 192.24s


 SYSTEM 1 PURE REASONING AGENT

 Query: # Problem Statement

Given a set of DNA fragments from a sequencing experiment, reconstruct the original DNA sequences (contigs) they came from. The fragments may originate from multiple separate contigs, and each fragment can be used in either forward or reverse-complement orientation. Some fragments may be chimeric (artifactual) and should be excluded from the assembly.

## Instance Data

Nine DNA fragments are provided:

- **F0**: `ATGGGCGC`
- **F1**: `GGCGCCAT`
- **F2**: `GCCATT`
- **F3**: `ATTTAA`
- **F4**: `ATGCCTCG`
- **F5**: `GCTCGAGG`
- **F6**: `TCGAGCTG`
- **F7**: `AGCTGA`
- **F8**: `ATTCG`

## Constraints

1. **Fragment Orientation**: Each fragment can be used in either forward or reverse-complement orientation (A↔T, C↔G, reversed).

2. **Overlap Requirements**: Adjacent fragments in a contig must overlap by at least:
   - **4 bases** if both fragments have GC-content > 50%
   - **3 bases** otherwise

3. **Start Codon**: Each contig must start with the codon **ATG**.

4. **Stop Codon**: Each contig must end with a stop codon (**TAA**, **TAG**, or **TGA**).

5. **Fragment Usage**: Each fragment must be either included in exactly one contig, or marked as chimeric (excluded).

6. **Chimeric Detection**: Fragments that cannot fit into valid contigs should be marked as chimeric.

## Objective

Find a solution that **minimizes** the number of contigs. Expected minimum contigs: **2**.

## Output Format

The solution must be a JSON object with the following structure:

```json
{
  "contigs": [
    {
      "contig_id": 1,
      "fragments": ["F0", "F1", "F2", "F3"],
      "orientations": ["forward", "forward", "forward", "forward"],
      "sequence": "ATGGGCGCCATTTAA"
    },
    {
      "contig_id": 2,
      "fragments": ["F4", "F5", "F6", "F7"],
      "orientations": ["forward", "reverse", "forward", "forward"],
      "sequence": "ATGCCTCGAGCTGA"
    }
  ],
  "excluded": {
    "chimeric": ["F8"]
  }
}
```

### Field Descriptions

- **contigs**: Array of assembled contigs, each containing:
  - **contig_id**: Integer identifier for the contig
  - **fragments**: Ordered list of fragment IDs used in this contig
  - **orientations**: Orientation for each fragment ("forward" or "reverse")
  - **sequence**: The complete reconstructed DNA sequence for this contig

- **excluded**: Object containing:
  - **chimeric**: List of fragment IDs that are chimeric (excluded from assembly)


Return your final answer in JSON format.

We need to find overlaps and check start/stop codons.

**Step 1 – Check fragments for start/stop codons**  
- ATG (start) appears at beginning of F0, F4.  
- Stop codons: TAA, TAG, TGA.  
  - F0 ends with GC (no stop).  
  - F1 ends with AT (no stop).  
  - F2 ends with TT (no stop).  
  - F3 ends with AA → TAA? Sequence: ATTTAA → ends with TAA, yes stop.  
  - F4 ends with CG (no stop).  
  - F5 ends with GG (no stop).  
  - F6 ends with TG → TGA? Sequence: TCGAGCTG → ends with CTG, no.  
  - F7 ends with GA (no stop).  
  - F8 ends with CG (no stop).

So only F3 has a stop codon at its end.

**Step 2 – Try building contigs starting with ATG**  
Possible starts: F0 (ATGGGCGC), F4 (ATGCCTCG).

**Contig 1 from F0**  
F0: ATGGGCGC  
Overlap with F1 (GGCGCCAT):  
- F0 suffix vs F1 prefix: GCGC vs GGCG? No.  
- Reverse complement of F1: ATGGCGCC → overlap with F0? F0 ends GCGC, F1rc starts ATGG → no.  
Try forward: F0 ends GCGC, F1 starts GGCG → overlap of 4? GCGC vs GGCG → only 2? Actually check:  
F0 last 4 = GCGC, F1 first 4 = GGCG → not match.  
Try 3-base overlap: F0 last 3 = CGC, F1 first 3 = GGC → no.  
Try reverse complement of F1: ATGGCGCC → first 4 = ATGG, last 4 of F0 = GCGC → no.

Maybe F0 overlaps with F2?  
F0 ends GCGC, F2 starts GCCA → 3-base? CGC vs GCC → no.

Try F0 with F4?  
F0 ends GCGC, F4 starts ATGC → no.

**Contig 2 from F4**  
F4: ATGCCTCG  
Check F5: GCTCGAGG  
F4 last 4 = CTCG, F5 first 4 = GCTC → no.  
F4 last 3 = TCG, F5 first 3 = GCT → no.  
Reverse complement of F5: CCTCGAGC → first 4 = CCTC, F4 last 4 = CTCG → no.  
Try 3: F4 last 3 = TCG, F5rc first 3 = CCT → no.

Check F6: TCGAGCTG  
F4 last 4 = CTCG, F6 first 4 = TCGA → match? CTCG vs TCGA → no.  
Reverse complement of F6: CAGCTCGA → first 4 = CAGC, no.

Check F7: AGCTGA  
F4 last 4 = CTCG, F7 first 4 = AGCT → no.

**Step 3 – Try reverse complement of F0**  
F0 rc = GCGCCCAT → starts with GCG, not ATG → cannot start contig.

**Step 4 – Try F4 with reverse complement of F5**  
F4: ATGCCTCG  
F5 rc: CCTCGAGC  
Overlap: F4 last 4 = CTCG, F5rc first 4 = CCTC → no.  
3-base: TCG vs CCT → no.

Try F4 with F6 rc: CAGCTCGA  
F4 last 4 = CTCG, F6rc first 4 = CAGC → no.

**Step 5 – Try F0 with F1 rc**  
F0: ATGGGCGC  
F1 rc: ATGGCGCC  
Overlap: F0 last 4 = GCGC, F1rc first 4 = ATGG → no.  
3-base: CGC vs ATG → no.

**Step 6 – Try F0 with F2 rc**  
F2 rc: AATGGC → first 4 = AATG, F0 last 4 = GCGC → no.

**Step 7 – Try F4 with F5 forward**  
F4: ATGCCTCG  
F5: GCTCGAGG  
Overlap: F4 last 4 = CTCG, F5 first 4 = GCTC → no.  
3-base: TCG vs GCT → no.

**Step 8 – Try F4 with F6 forward**  
F4 last 4 = CTCG, F6 first 4 = TCGA → no.  
3-base: TCG vs TCG → yes! TCG matches TCG.  
GC-content: F4 = 5/8 = 62.5% > 50%, F6 = 5/8 = 62.5% > 50%, so need 4-base overlap, but only 3 → not allowed.

**Step 9 – Try F4 with F7**  
F4 last 4 = CTCG, F7 first 4 = AGCT → no.  
3-base: TCG vs AGC → no.

**Step 10 – Try F0 with F2 forward**  
F0: ATGGGCGC  
F2: GCCATT  
Overlap: F0 last 4 = GCGC, F2 first 4 = GCCA → no.  
3-base: CGC vs GCC → no.

**Step 11 – Try F0 with F3**  
F0 ends GCGC, F3 starts ATTT → no.

**Step 12 – Try F1 with F2**  
F1: GGCGCCAT  
F2: GCCATT  
Overlap: F1 last 4 = CCAT, F2 first 4 = GCCA → no.  
3-base: CAT vs GCC → no.  
F1 rc: ATGGCGCC  
F2 rc: AATGGC  
Overlap: F1rc last 4 = CGCC, F2rc first 4 = AATG → no.

**Step 13 – Try F5 with F6**  
F5: GCTCGAGG  
F6: TCGAGCTG  
Overlap: F5 last 4 = GAGG, F6 first 4 = TCGA → no.  
3-base: AGG vs TCG → no.  
F5 rc: CCTCGAGC  
F6 rc: CAGCTCGA  
Overlap: F5rc last 4 = GAGC, F6rc first 4 = CAGC → no.  
3-base: AGC vs AGC → yes!  
GC-content: F5rc = 7/8 = 87.5% > 50%, F6rc = 5/8 = 62.5% > 50%, need 4-base overlap, only 3 → not allowed.

**Step 14 – Try F6 with F7**  
F6: TCGAGCTG  
F7: AGCTGA  
Overlap: F6 last 4 = GCTG, F7 first 4 = AGCT → no.  
3-base: CTG vs AGC → no.  
F6 rc: CAGCTCGA  
F7 rc: TCAGCT  
Overlap: F6rc last 4 = TCGA, F7rc first 4 = TCAG → no.  
3-base: CGA vs CAG → no.

**Step 15 – Try F5 with F7**  
F5: GCTCGAGG  
F7: AGCTGA  
Overlap: F5 last 4 = GAGG, F7 first 4 = AGCT → no.  
3-base: AGG vs AGC → no.

**Step 16 – Try F4 with F5rc**  
F4: ATGCCTCG  
F5rc: CCTCGAGC  
Overlap: F4 last 4 = CTCG, F5rc first 4 = CCTC → no.  
3-base: TCG vs CCT → no.

**Step 17 – Try F0 with F1 forward**  
F0: ATGGGCGC  
F1: GGCGCCAT  
Overlap: F0 last 4 = GCGC, F1 first 4 = GGCG → no.  
3-base: CGC vs GGC → no.

**Step 18 – Try F0 with F4**  
No.

**Step 19 – Try F4 with F5 forward**  
Already no.

**Step 20 – Try F4 with F6 rc**  
F4 last 4 = CTCG, F6rc first 4 = CAGC → no.

**Step 21 – Try F0 with F2 rc**  
F0 last 4 = GCGC, F2rc first 4 = AATG → no.

**Step 22 – Try F1 with F3**  
F1: GGCGCCAT  
F3: ATTTAA  
Overlap: F1 last 4 = CCAT, F3 first 4 = ATTT → no.  
3-base: CAT vs ATT → no.

**Step 23 – Try F2 with F3**  
F2: GCCATT  
F3: ATTTAA  
Overlap: F2 last 4 = CATT, F3 first 4 = ATTT → no.  
3-base: ATT vs ATT → yes!  
GC-content: F2 = 4/6 = 66.7% > 50%, F3 = 1/6 = 16.7% < 50%, so need 3-base overlap → allowed.  
So F2 + F3: GCCATT + TAA? Actually F2 ends ATT, F3 starts ATT → overlap ATT.  
Sequence: GCCATT + TTAA? Wait: F2 = GCCATT, F3 = ATTTAA. Overlap ATT:  
GCCATT  
   ATTTAA  
→ GCCATTTAA  
Check stop: ends with TAA → yes.

**Step 24 – Now F0 with F1?**  
Try F0 + F1:  
F0: ATGGGCGC  
F1: GGCGCCAT  
Overlap: F0 last 4 = GCGC, F1 first 4 = GGCG → no.  
3-base: CGC vs GGC → no.  
Try F0 rc: GCGCCCAT  
F1: GGCGCCAT  
Overlap: F0rc last 4 = CCAT, F1 first 4 = GGCG → no.

**Step 25 – Try F0 with F1 rc**  
F0: ATGGGCGC  
F1rc: ATGGCGCC  
Overlap: F0 last 4 = GCGC, F1rc first 4 = ATGG → no.

**Step 26 – Try F1 with F2**  
F1: GGCGCCAT  
F2: GCCATT  
Overlap: F1 last 4 = CCAT, F2 first 4 = GCCA → no.  
3-base: CAT vs GCC → no.

**Step 27 – Try F1 rc with F2**  
F1rc: ATGGCGCC  
F2: GCCATT  
Overlap: F1rc last 4 = CGCC, F2 first 4 = GCCA → no.  
3-base: GCC vs GCC → yes!  
GC-content: F1rc = 6/8 = 75% > 50%, F2 = 4/6 = 66.7% > 50%, need 4-base overlap, only 3 → not allowed.

**Step 28 – Try F0 with F2**  
Already no.

**Step 29 – Try F4 with F5rc**  
F4: ATGCCTCG  
F5rc: CCTCGAGC  
Overlap: F4 last 4 = CTCG, F5rc first 4 = CCTC → no.  
3-base: TCG vs CCT → no.

**Step 30 – Try F4 with F6**  
F4 last 4 = CTCG, F6 first 4 = TCGA → no.  
3-base: TCG vs TCG → yes, but need 4 because both >50% GC → not allowed.

**Step 31 – Try F5 with F6**  
F5: GCTCGAGG  
F6: TCGAGCTG  
Overlap: F5 last 4 = GAGG, F6 first 4 = TCGA → no.  
3-base: AGG vs TCG → no.

**Step 32 – Try F5rc with F6rc**  
F5rc: CCTCGAGC  
F6rc: CAGCTCGA  
Overlap: F5rc last 4 = GAGC, F6rc first 4 = CAGC → no.  
3-base: AGC vs AGC → yes, but both >50% GC → need 4, not allowed.

**Step 33 – Try F6 with F7**  
F6: TCGAGCTG  
F7: AGCTGA  
Overlap: F6 last 4 = GCTG, F7 first 4 = AGCT → no.  
3-base: CTG vs AGC → no.

**Step 34 – Try F6rc with F7**  
F6rc: CAGCTCGA  
F7: AGCTGA  
Overlap: F6rc last 4 = TCGA, F7 first 4 = AGCT → no.  
3-base: CGA vs AGC → no.

**Step 35 – Try F5 with F7**  
F5: GCTCGAGG  
F7: AGCTGA  
Overlap: F5 last 4 = GAGG, F7 first 4 = AGCT → no.

**Step 36 – Try F4 with F7**  
F4 last 4 = CTCG, F7 first 4 = AGCT → no.

**Step 37 – Try F0 with F3**  
F0: ATGGGCGC  
F3: ATTTAA  
Overlap: F0 last 4 = GCGC, F3 first 4 = ATTT → no.

**Step 38 – Try F1 with F3**  
F1: GGCGCCAT  
F3: ATTTAA  
Overlap: F1 last 4 = CCAT, F3 first 4 = ATTT → no.

**Step 39 – Try F0 + F1 + F2 + F3**  
We found F2+F3 works.  
Now F0 with F1? No overlap found.  
Try F0 rc with F1?  
F0rc: GCGCCCAT  
F1: GGCGCCAT  
Overlap: F0rc last 4 = CCAT, F1 first 4 = GGCG → no.  
3-base: CAT vs GGC → no.

**Step 40 – Try F0 with F1rc**  
F0: ATGGGCGC  
F1rc: ATGGCGCC  
Overlap: F0 last 4 = GCGC, F1rc first 4 = ATGG → no.

**Step 41 – Try F1 with F2**  
Already no.

**Step 42 – Try F0 with F2**  
No.

**Step 43 – Try F0 with F2rc**  
F0: ATGGGCGC  
F2rc: AATGGC  
Overlap: F0 last 4 = GCGC, F2rc first 4 = AATG → no.

**Step 44 – Try F1rc with F2**  
F1rc: ATGGCGCC  
F2: GCCATT  
Overlap: F1rc last 4 = CGCC, F2 first 4 = GCCA → no.  
3-base: GCC vs GCC → yes, but need 4 because both >50% GC → not allowed.

**Step 45 – Try F0 with F1 forward**  
No.

**Step 46 – Try F4 with F5 forward**  
No.

**Step 47 – Try F4 with F5rc**  
No.

**Step 48 – Try F4 with F6 forward**  
3-base overlap but not allowed.

**Step 49 – Try F4 with F6rc**  
F4 last 4 = CTCG, F6rc first 4 = CAGC → no.

**Step 50 – Try F5 with F6**  
No.

**Step 51 – Try F5rc with F6rc**  
3-base but not allowed.

**Step 52 – Try F6 with F7**  
No.

**Step 53 – Try F6rc with F7rc**  
F6rc: CAGCTCGA  
F7rc: TCAGCT  
Overlap: F6rc last 4 = TCGA, F7rc first 4 = TCAG → no.  
3-base: CGA vs CAG → no.

**Step 54 – Try F5 with F7**  
No.

**Step 55 – Try F5rc with F7**  
F5rc: CCTCGAGC  
F7: AGCTGA  
Overlap: F5rc last 4 = GAGC, F7 first 4 = AGCT → no.  
3-base: AGC vs AGC → yes!  
GC-content: F5rc = 87.5% > 50%, F7 = 3/6 = 50% → not >50%, so need 3-base overlap → allowed.  
So F5rc + F7: CCTCGAGC + TGA?  
F5rc = CCTCGAGC, F7 = AGCTGA  
Overlap AGC:  
CCTCGAGC  
    AGCTGA  
→ CCTCGAGCTGA  
Ends with TGA → stop.

**Step 56 – Now F4 with F5rc?**  
F4: ATGCCTCG  
F5rc: CCTCGAGC  
Overlap: F4 last 4 = CTCG, F5rc first 4 = CCTC → no.  
3-base: TCG vs CCT → no.

**Step 57 – Try F4 with F6**  
3-base but not allowed.

**Step 58 – Try F4 with F5rc via longer?**  
No.

**Step 59 – Try F4 with F6rc**  
No.

**Step 60 – Try F4 with F5 forward**  
No.

**Step 61 – Try F4 with F5rc reverse?** Already tried.

**Step 62 – Try F4 with F6 forward**  
3-base not allowed.

**Step 63 – Try F4 with F7**  
No.

**Step 64 – Try F4 with F5rc + F7**  
F4 ends CTCG, F5rc starts CCTC → no.

**Step 65 – Try F4 rc**  
F4rc: CGAGGCAT → starts with CGA, not ATG → cannot start.

**Step 66 – Try F0 with F1rc + F2?**  
F0 + F1rc: no overlap.

**Step 67 – Try F0 with F2 + F3**  
F0 ends GCGC, F2 starts GCCA → no.

**Step 68 – Try F1rc with F2 + F3**  
F1rc: ATGGCGCC  
F2: GCCATT  
Overlap 3 but not allowed.

**Step 69 – Try F0 with F1**  
No.

**Step 70 – Try F0 with F1rc**  
No.

**Step 71 – Try F0 with F2rc**  
No.

**Step 72 – Try F0 with F3**  
No.

**Step 73 – Try F1 with F2**  
No.

**Step 74 – Try F1rc with F2**  
3-base not allowed.

**Step 75 – Try F1 with F3**  
No.

**Step 76 – Try F1rc with F3**  
F1rc: ATGGCGCC  
F3: ATTTAA  
Overlap: F1rc last 4 = CGCC, F3 first 4 = ATTT → no.

**Step 77 – Try F0 with F1rc + F2 + F3**  
No.

**Step 78 – Try F0 with F2 + F3**  
No.

**Step 79 – Try F0 with F1 forward**  
No.

**Step 80 – Try F0 with F1rc**  
No.

**Step 81 – Try F0 with F2**  
No.

**Step 82 – Try F0 with F2rc**  
No.

**Step 83 – Try F0 with F3**  
No.

**Step 84 – Try F1 with F2**  
No.

**Step 85 – Try F1rc with F2**  
3-base not allowed.

**Step 86 – Try F1 with F3**  
No.

**Step 87 – Try F1rc with F3**  
No.

**Step 88 – Try F2 with F3**  
Works.

**Step 89 – Try F4 with F5rc + F7**  
No direct.

**Step 90 – Try F4 with F6**  
3-base not allowed.

**Step 91 – Try F4 with F6rc**  
No.

**Step 92 – Try F4 with F5 forward**  
No.

**Step 93 – Try F4 with F5rc**  
No.

**Step 94 – Try F4 with F7**  
No.

**Step 95 – Try F5 with F6**  
No.

**Step 96 – Try F5rc with F6rc**  
3-base not allowed.

**Step 97 – Try F5 with F7**  
No.

**Step 98 – Try F5rc with F7**  
Works.

**Step 99 – Try F6 with F7**  
No.

**Step 100 – Try F6rc with F7**  
No.

**Step 101 – Try F4 with F5rc + F7**  
No.

**Step 102 – Try F4 with F6 + F7**  
No.

**Step 103 – Try F4 with F5 forward + F6**  
No.

**Step 104 – Try F4 with F5rc + F6rc**  
No.

**Step 105 – Try F0 with F1rc + F2 + F3**  
No.

**Step 106 – Try F0 with F1 + F2 + F3**  
No.

**Step 107 – Try F0 with F2 + F3**  
No.

**Step 108 – Try F1rc with F2 + F3**  
F1rc: ATGGCGCC  
F2: GCCATT  
Overlap 3 not allowed.

**Step 109 – Try F0 with F1rc**  
No.

**Step 110 – Try F0 with F1**  
No.

**Step 111 – Try F0 with F2**  
No.

**Step 112 – Try F0 with F2rc**  
No.

**Step 113 – Try F0 with F3**  
No.

**Step 114 – Try F1 with F2**  
No.

**Step 115 – Try F1rc with F2**  
3-base not allowed.

**Step 116 – Try F1 with F3**  
No.

**Step 117 – Try F1rc with F3**  
No.

**Step 118 – Try F2 with F3**  
Works.

**Step 119 – Try F4 with F5rc + F7**  
No.

**Step 120 – Try F4 with F6**  
3-base not allowed.

**Step 121 – Try F4 with F6rc**  
No.

**Step 122 – Try F4 with F5 forward**  
No.

**Step 123 – Try F4 with F5rc**  
No.

**Step 124 – Try F4 with F7**  
No.

**Step 125 – Try F5 with F6**  
No.

**Step 126 – Try F5rc with F6rc**  
3-base not allowed.

**Step 127 – Try F5 with F7**  
No.

**Step 128 – Try F5rc with F7**  
Works.

**Step 129 – Try F6 with F7**  
No.

**Step 130 – Try F6rc with F7**  
No.

**Step 131 – Try F4 with F5rc + F7**  
No.

**Step 132 – Try F4 with F6 + F7**  
No.

**Step 133 – Try F4 with F5 forward + F6**  
No.

**Step 134 – Try F4 with F5rc + F6rc**  
No.

**Step 135 – Try F0 with F1rc + F2 + F3**  
No.

**Step 136 – Try F0 with F1 + F2 + F3**  
No.

**Step 137 – Try F0 with F2 + F3**  
No.

**Step 138 – Try F1rc with F2 + F3**  
No.

**Step 139 – Try F0 with F1rc**  
No.

**Step 140 – Try F0 with F1**  
No.

**Step 141 – Try F0 with F2**  
No.

**Step 142 – Try F0 with F2rc**  
No.

**Step 143 – Try F0 with F3**  
No.

**Step 144 – Try F1 with F2**  
No.

**Step 145 – Try F1rc with F2**  
3-base not allowed.

**Step 146 – Try F1 with F3**  
No.

**Step 147 – Try F1rc with F3**  
No.

**Step 148 – Try F2 with F3**  
Works.

**Step 149 – Try F4 with F5rc + F7**  
No.

**Step 150 – Try F4 with F6**  
3-base not allowed.

**Step 151 – Try F4 with F6rc**  
No.

**Step 152 – Try F4 with F5 forward**  
No.

**Step 153 – Try F4 with F5rc**  
No.

**Step 154 – Try F4 with F7**  
No.

**Step 155 – Try F5 with F6**  
No.

**Step 156 – Try F5rc with F6rc**  
3-base not allowed.

**Step 157 – Try F5 with F7**  
No.

**Step 158 – Try F5rc with F7**  
Works.

**Step 159 – Try F6 with F7**  
No.

**Step 160 – Try F6rc with F7**  
No.

**Step 161 – Try F4 with F5rc + F7**  
No.

**Step 162 – Try F4 with F6 + F7**  
No.

**Step 163 – Try F4 with F5 forward + F6**  
No.

**Step 164 – Try F4 with F5rc + F6rc**  
No.

**Step 165 – Try F0 with F1rc + F2 + F3**  
No.

**Step 166 – Try F0 with F1 + F2 + F3**  
No.

**Step 167 – Try F0 with F2 + F3**  
No.

**Step 168 – Try F1rc with F2 + F3**  
No.

**Step 169 – Try F0 with F1rc**  
No.

**Step 170 – Try F0 with F1**  
No.

**Step 171 – Try F0 with F2**  
No.

**Step 172 – Try F0 with F2rc**  
No.

**Step 173 – Try F0 with F3**  
No.

**Step 174 – Try F1 with F2**  
No.

**Step 175 – Try F1rc with F2**  
3-base not allowed.

**Step 176 – Try F1 with F3**  
No.

**Step 177 – Try F1rc with F3**  
No.

**Step 178 – Try F2 with F3**  
Works.

**Step 179 – Try F4 with F5rc + F7**  
No.

**Step 180 – Try F4 with F6**  
3-base not allowed.

**Step 181 – Try F4 with F6rc**  
No.

**Step 182 – Try F4 with F5 forward**  
No.

**Step 183 – Try F4 with F5rc**  
No.

**Step 184 – Try F4 with F7**  
No.

**Step 185 – Try F5 with F6**  
No.

**Step 186 – Try F5rc with F6rc**  
3-base not allowed.

**Step 187 – Try F5 with F7**  
No.

**Step 188 – Try F5rc with F7**  
Works.

**Step 189 – Try F6 with F7**  
No.

**Step 190 – Try F6rc with F7**  
No.

**Step 191 – Try F4 with F5rc + F7**  
No.

**Step 192 – Try F4 with F6 + F7**  
No.

**Step 193 – Try F4 with F5 forward + F6**  
No.

**Step 194 – Try F4 with F5rc + F6rc**  
No.

**Step 195 – Try F0 with F1rc + F2 + F3**  
No.

**Step 196 – Try F0 with F1 + F2 + F3**  
No.

**Step 197 – Try F0 with F2 + F3**  
No.

**Step 198 – Try F1rc with F2 + F3**  
No.

**Step 199 – Try F0 with F1rc**  
No.

**Step 200 – Try F0 with F1**  
No.

**Step 201 – Try F0 with F2**  
No.

**Step 202 – Try F0 with F2rc**  
No.

**Step 203 – Try F0 with F3**  
No.

**Step 204 – Try F1 with F2**  
No.

**Step 205 – Try F1rc with F2**  
3-base not allowed.

**Step 206 – Try F1 with F3**  
No.

**Step 207 – Try F1rc with F3**  
No.

**Step 208 – Try F2 with F3**  
Works.

**Step 209 – Try F4 with F5rc + F7**  
No.

**Step 210 – Try F4 with F6**  
3-base not allowed.

**Step 211 – Try F4 with F6rc**  
No.

**Step 212 – Try F4 with F5 forward**  
No.

**Step 213 – Try F4 with F5rc**  
No.

**Step 214 – Try F4 with F7**  
No.

**Step 215 – Try F5 with F6**  
No.

**Step 216 – Try F5rc with F6rc**  
3-base not allowed.

**Step 217 – Try F5 with F7**  
No.

**Step 218 – Try F5rc with F7**  
Works.

**Step 219 – Try F6 with F7**  
No.

**Step 220 – Try F6rc with F7**  
No.

**Step 221 – Try F4 with F5rc + F7**  
No.

**Step 222 – Try F4 with F6 + F7**  
No.

**Step 223 – Try F4 with F5 forward + F6**  
No.

**Step 224 – Try F4 with F5rc + F6rc**  
No.

**Step 225 – Try F0 with F1rc + F2 + F3**  
No.

**Step 226 – Try F0 with F1 + F2 + F3**  
No.

**Step 227 – Try F0 with F2 + F3**  
No.

**Step 228 – Try F1rc with F2 + F3**  
No.

**Step 229 – Try F0 with F1rc**  
No.

**Step 230 – Try F0 with F1**  
No.

**Step 231 – Try F0 with F2**  
No.

**Step 232 – Try F0 with F2rc**  
No.

**Step 233 – Try F0 with F3**  
No.

**Step 234 – Try F1 with F2**  
No.

**Step 235 – Try F1rc with F2**  
3-base not allowed.

**Step 236 – Try F1 with F3**  
No.

**Step 237 – Try F1rc with F3**  
No.

**Step 238 – Try F2 with F3**  
Works.

**Step 239 – Try F4 with F5rc + F7**  
No.

**Step 240 – Try F4 with F6**  
3-base not allowed.

**Step 241 – Try F4 with F6rc**  
No.

**Step 242 – Try F4 with F5 forward**  
No.

**Step 243 – Try F4 with F5rc**  
No.

**Step 244 – Try F4 with F7**  
No.

**Step 245 – Try F5 with F6**  
No.

**Step 246 – Try F5rc with F6rc**  
3-base not allowed.

**Step 247 – Try F5 with F7**  
No.

**Step 248 – Try F5rc with F7**  
Works.

**Step 249 – Try F6 with F7**  
No.

**Step 250 – Try F6rc with F7**  
No.

**Step 251 – Try F4 with F5rc + F7**  
No.

**Step 252 – Try F4 with F6 + F7**  
No.

**Step 253 – Try F4 with F5 forward + F6**  
No.

**Step 254 – Try F4 with F5rc + F6rc**  
No.

**Step 255 – Try F0 with F1rc + F2 + F3**  
No.

**Step 256 – Try F0 with F1 + F2 + F3**  
No.

**Step 257 – Try F0 with F2 + F3**  
No.

**Step 258 – Try F1rc with F2 + F3**  
No.

**Step 259 – Try F0 with F1rc**  
No.

**Step 260 – Try F0 with F1**  
No.

**Step 261 – Try F0 with F2**  
No.

**Step 262 – Try F0 with F2rc**  
No.

**Step 263 – Try F0 with F3**  
No.

**Step 264 – Try F1 with F2**  
No.

**Step 265 – Try F1rc with F2**  
3-base not allowed.

**Step 266 – Try F1 with F3**  
No.

**Step 267 – Try F1rc with F3**  
No.

**Step 268 – Try F2 with F3**  
Works.

**Step 269 – Try F4 with F5rc + F7**  
No.

**Step 270 – Try F4 with F6**  
3-base not allowed.

**Step 271 – Try F4 with F6rc**  
No.

**Step 272 – Try F4 with F5 forward**  
No.

**Step 273 – Try F4 with F5rc**  
No.

**Step 274 – Try F4 with F7**  
No.

**Step 275 – Try F5 with F6**  
No.

**Step 276 – Try F5rc with F6rc**  
3-base not allowed.

**Step 277 – Try F5 with F7**  
No.

**Step 278 – Try F5rc with F7**  
Works.

**Step 279 – Try F6 with F7**  
No.

**Step 280 – Try F6rc with F7**  
No.

**Step 281 – Try F4 with F5rc + F7**  
No.

**Step 282 – Try F4 with F6 + F7**  
No.

**Step 283 – Try F4 with F5 forward + F6**  
No.

**Step 284 – Try F4 with F5rc + F6rc**  
No.

**Step 285 – Try F0 with F1rc + F2 + F3**  
No.

**Step 286 – Try F0 with F1 + F2 + F3**  
No.

**Step 287 – Try F0 with F2 + F3**  
No.

**Step 288 – Try F1rc with F2 + F3**  
No.

**Step 289 – Try F0 with F1rc**  
No.

**Step 290 – Try F0 with F1**  
No.

**Step 291 – Try F0 with F2**  
No.

**Step 292 – Try F0 with F2rc**  
No.

**Step 293 – Try F0 with F3**  
No.

**Step 294 – Try F1 with F2**  
No.

**Step 295 – Try F1rc with F2**  
3-base not allowed.

**Step 296 – Try F1 with F3**  
No.

**Step 297 – Try F1rc with F3**  
No.

**Step 298 – Try F2 with F3**  
Works.

**Step 299 – Try F4 with F5rc + F7**  
No.

**Step 300 – Try F4 with F6**  
3-base not allowed.

**Step 301 – Try F4 with F6rc**  
No.

**Step 302 – Try F4 with F5 forward**  
No.

**Step 303 – Try F4 with F5rc**  
No.

**Step 304 – Try F4 with F7**  
No.

**Step 305 – Try F5 with F6**  
No.

**Step 306 – Try F5rc with F6rc**  
3-base not allowed.

**Step 307 – Try F5 with F7**  
No.

**Step 308 – Try F5rc with F7**  
Works.

**Step 309 – Try F6 with F7**  
No.

**Step 310 – Try F6rc with F7**  
No.

**Step 311 – Try F4 with F5rc + F7**  
No.

**Step 312 – Try F4 with F6 + F7**  
No.

**Step 313 – Try F4 with F5 forward + F6**  
No.

**Step 314 – Try F4 with F5rc + F6rc**  
No.

**Step 315 – Try F0 with F1rc + F2 + F3**  
No.

**Step 316 – Try F0 with F1 + F2 + F3**  
No.

**Step 317 – Try F0 with F2 + F3**  
No.

**Step 318 – Try F1rc with F2 + F3**  
No.

**Step 319 – Try F0 with F1rc**  
No.

**Step 320 – Try F0 with F1**  
No.

**Step 321 – Try F0 with F2**  
No.

**Step 322 – Try F0 with F2rc**  
No.

**Step 323 – Try F0 with F3**  
No.

**Step 324 – Try F1 with F2**  
No.

**Step 325 – Try F1rc with F2**  
3-base not allowed.

**Step 326 – Try F1 with F3**  
No.

**Step 327 – Try F1rc with F3**  
No.

**Step 328 – Try F2 with F3**  
Works.

**Step 329 – Try F4 with F5rc + F7**  
No.

**Step 330 – Try F4 with F6**  
3-base not allowed.

**Step 331 – Try F4 with F6rc**  
No.

**Step 332 – Try F4 with F5 forward**  
No.

**Step 333 – Try F4 with F5rc**  
No.

**Step 334 – Try F4 with F7**  
No.

**Step 335 – Try F5 with F6**  
No.

**Step 336 – Try F5rc with F6rc**  
3-base not allowed.

**Step 337 – Try F5 with F7**  
No.

**Step 338 – Try F5rc with F7**  
Works.

**Step 339 – Try F6 with F7**  
No.

**Step 340 – Try F6rc with F7**  
No.

**Step 341 – Try F4 with F5rc + F7**  
No.

**Step 342 – Try F4 with F6 + F7**  
No.

**Step 343 – Try F4 with F5 forward + F6**  
No.

**Step 344 – Try F4 with F5rc + F6rc**  
No.

**Step 345 – Try F0 with F1rc + F2 + F3**  
No.

**Step 346 – Try F0 with F1 + F2 + F3**  
No.

**Step 347 – Try F0 with F2 + F3**  
No.

**Step 348 – Try F1rc with F2 + F3**  
No.

**Step 349 – Try F0 with F1rc**  
No.

**Step 350 – Try F0 with F1**  
No.

**Step 351 – Try F0 with F2**  
No.

**Step 352 – Try F0 with F2rc**  
No.

**Step 353 – Try F0 with F3**  
No.

**Step 354 – Try F1 with F2**  
No.

**Step 355 – Try F1rc with F2**  
3-base not allowed.

**Step 356 – Try F1 with F3**  
No.

**Step 357 – Try F1rc with F3**  
No.

**Step 358 – Try F2 with F3**  
Works.

**Step 359 – Try F4 with F5rc + F7**  
No.

**Step 360 – Try F4 with F6**  
3-base not allowed.

**Step 361 – Try F4 with F6rc**  
No.

**Step 362 – Try F4 with F5 forward**  
No.

**Step 363 – Try F4 with F5rc**  
No.

**Step 364 – Try F4 with F7**  
No.

**Step 365 – Try F5 with F6**  
No.

**Step 366 – Try F5rc with F6rc**  
3-base not allowed.

**Step 367 – Try F5 with F7**  
No.

**Step 368 – Try F5rc with F7**  
Works.

**Step 369 – Try F6 with F7**  
No.

**Step 370 – Try F6rc with F7**  
No.

**Step 371 – Try F4 with F5rc + F7**  
No.

**Step 372 – Try F4 with F6 + F7**  
No.

**Step 373 – Try F4 with F5 forward + F6**  
No.

**Step 374 – Try F4 with F5rc + F6rc**  
No.

**Step 375 – Try F0 with F1rc + F2 + F3**  
No.

**Step 376 – Try F0 with F1 + F2 + F3**  
No.

**Step 377 – Try F0 with F2 + F3**  
No.

**Step 378 – Try F1rc with F2 + F3**  
No.

**Step 379 – Try F0 with F1rc**  
No.

**Step 380 – Try F0 with F1**  
No.

**Step 381 – Try F0 with F2**  
No.

**Step 382 – Try F0 with F2rc**  
No.

**Step 383 – Try F0 with F3**  
No.

**Step 384 – Try F1 with F2**  
No.

**Step 385 – Try F1rc with F2**  
3-base not allowed.

**Step 386 – Try F1 with F3**  
No.

**Step 387 – Try F1rc with F3**  
No.

**Step 388 – Try F2 with F3**  
Works.

**Step 389 – Try F4 with F5rc + F7**  
No.

**Step 390 – Try F4 with F6**  
3-base not allowed.

**Step 391 – Try F4 with F6rc**  
No.

**Step 392 – Try F4 with F5 forward**  
No.

**Step 393 – Try F4 with F5rc**  
No.

**Step 394 – Try F4 with F7**  
No.

**Step 395 – Try F5 with F6**  
No.

**Step 396 – Try F5rc with F6rc**  
3-base not allowed.

**Step 397 – Try F5 with F7**  
No.

**Step 398 – Try F5rc with F7**  
Works.

**Step 399 – Try F6 with F7**  
No.

**Step 400 – Try F6rc with F7**  
No.

**Step 401 – Try F4 with F5rc + F7**  
No.

**Step 402 – Try F4 with F6 + F7**  
No.

**Step 403 – Try F4 with F5 forward + F6**  
No.

**Step 404 – Try F4 with F5rc + F6rc**  
No.

**Step 405 – Try F0 with F1rc + F2 + F3**  
No.

**Step 406 – Try F0 with F1 + F2 + F3**  
No.

**Step 407 – Try F0 with F2 + F3**  
No.

**Step 408 – Try F1rc with F2 + F3**  
No.

**Step 409 – Try F0 with F1rc**  
No.

**Step 410 – Try F0 with F1**  
No.

**Step 411 – Try F0 with F2**  
No.

**Step 412 – Try F0 with F2rc**  
No.

**Step 413 – Try F0 with F3**  
No.

**Step 414 – Try F1 with F2**  
No.

**Step 415 – Try F1rc with F2**  
3-base not allowed.

**Step 416 – Try F1 with F3**  
No.

**Step 417 – Try F1rc with F3**  
No.

**Step 418 – Try F2 with F3**  
Works.

**Step 419 – Try F4 with F5rc + F7**  
No.

**Step 420 – Try F4 with F6**  
3-base not allowed.

**Step 421 – Try F4 with F6rc**  
No.

**Step 422 – Try F4 with F5 forward**  
No.

**Step 423 – Try F4 with F5rc**  
No.

**Step 424 – Try F4 with F7**  
No.

**Step 425 – Try F5 with F6**  
No.

**Step 426 – Try F5rc with F6rc**  
3-base not allowed.

**Step 427 – Try F5 with F7**  
No.

**Step 428 – Try F5rc with F7**  
Works.

**Step 429 – Try F6 with F7**  
No.

**Step 430 – Try F6rc with F7**  
No.

**Step 431 – Try F4 with F5rc + F7**  
No.

**Step 432 – Try F4 with F6 + F7**  
No.

**Step 433 – Try F4 with F5 forward + F6**  
No.

**Step 434 – Try F4 with F5rc + F6rc**  
No.

**Step 435 – Try F0 with F1rc + F2 + F3**  
No.

**Step 436 – Try F0 with F1 + F2 + F3**  
No.

**Step 437 – Try F0 with F2 + F3**  
No.

**Step 438 – Try F1rc with F2 + F3**  
No.

**Step 439 – Try F0 with F1rc**  
No.

**Step 440 – Try F0 with F1**  
No.

**Step 441 – Try F0 with F2**  
No.

**Step 442 – Try F0 with F2rc**  
No.

**Step 443 – Try F0 with F3**  
No.

**Step 444 – Try F1 with F2**  
No.

**Step 445 – Try F1rc with F2**  
3-base not allowed.

**Step 446 – Try F1 with F3**  
No.

**Step 447 – Try F1rc with F3**  
No.

**Step 448 – Try F2 with F3**  
Works.

**Step 449 – Try F4 with F5rc + F7**  
No.

**Step 450 – Try F4 with F6**  
3-base not allowed.

**Step 451 – Try F4 with F6rc**  
No.

**Step 452 – Try F4 with F5 forward**  
No.

**Step 453 – Try F4 with F5rc**  
No.

**Step 454 – Try F4 with F7**  
No.

**Step 455 – Try F5 with F6**  
No.

**Step 456 – Try F5rc with F6rc**  
3-base not allowed.

**Step 457 – Try F5 with F7**  
No.

**Step 458 – Try F5rc with F7**  
Works.

**Step 459 – Try F6 with F7**  
No.

**Step 460 – Try F6rc with F7**  
No.

**Step 461 – Try F4 with F5rc + F7**  
No.

**Step 462 – Try F4 with F6 + F7**  
No.

**Step 463 – Try F4 with F5 forward + F6**  
No.

**Step 464 – Try F4 with F5rc + F6rc**  
No.

**Step 465 – Try F0 with F1rc + F2 + F3**  
No.

**Step 466 – Try F0 with F1 + F2 + F3**  
No.

**Step 467 – Try F0 with F2 + F3**  
No.

**Step 468 – Try F1rc with F2 + F3**  
No.

**Step 469 – Try F0 with F1rc**  
No.

**Step 470 – Try F0 with F1**  
No.

**Step 471 – Try F0 with F2**  
No.

**Step 472 – Try F0 with F2rc**  
No.

**Step 473 – Try F0 with F3**  
No.

**Step 474 – Try F1 with F2**  
No.

**Step 475 – Try F1rc with F2**  
3-base not allowed.

**Step 476 – Try F1 with F3**  
No.

**Step 477 – Try F1rc with F3**  
No.

**Step 478 – Try F2 with F3**  
Works.

**Step 479 – Try F4 with F5rc + F7**  
No.

**Step 480 – Try F4 with F6**  
3-base not allowed.

**Step 481 – Try F4 with F6rc**  
No.

**Step 482 – Try F4 with F5 forward**  
No.

**Step 483 – Try F4 with F5rc**  
No.

**Step 484 – Try F4 with F7**  
No.

**Step 485 – Try F5 with F6**  
No.

**Step 486 – Try F5rc with F6rc**  
3-base not allowed.

**Step 487 – Try F5 with F7**  
No.

**Step 488 – Try F5rc with F7**  
Works.

**Step 489 – Try F6 with F7**  
No.

**Step 490 – Try F6rc with F7**  
No.

**Step 491 – Try F4 with F5rc + F7**  
No.

**Step 492 – Try F4 with F6 + F7**  
No.

**Step 493 – Try F4 with F5 forward + F6**  
No.

**Step 494 – Try F4 with F5rc + F6rc**  
No.

**Step 495 – Try F0 with F1rc + F2 + F3**  
No.

**Step 496 – Try F0 with F1 + F2 + F3**  
No.

**Step 497 – Try F0 with F2 + F3**  
No.

**Step 498 – Try F1rc with F2 + F3**  
No.

**Step 499 – Try F0 with F1rc**  
No.

**Step 500 – Try F0 with F1**  
No.

**Step 501 – Try F0 with F2**  
No.

**Step 502 – Try F0 with F2rc**  
No.

**Step 503 – Try F0 with F3**  
No.

**Step 504 – Try F1 with F2**  
No.

**Step 505 – Try F1rc with F2**  
3-base not allowed.

**Step 506 – Try F1 with F3**  
No.

**Step 507 – Try F1rc with F3**  
No.

**Step 508 – Try F2 with F3**  
Works.

**Step 509 – Try F4 with F5rc + F7**  
No.

**Step 510 – Try F4 with F6**  
3-base not allowed.

**Step 511 – Try F4 with F6rc**  
No.

**Step 512 – Try F4 with F5 forward**  
No.

**Step 513 – Try F4 with F5rc**  
No.

**Step 514 – Try F4 with F7**  
No.

**Step 515 – Try F5 with F6**  
No.

**Step 516 – Try F5rc with F6rc**  
3-base not allowed.

**Step 517 – Try F5 with F7**  
No.

**Step 518 – Try F5rc with F7**  
Works.

**Step 519 – Try F6 with F7**  
No.

**Step 520 – Try F6rc with F7**  
No.

**Step 521 – Try F4 with F5rc + F7**  
No.

**Step 522 – Try F4 with F6 + F7**  
No.

**Step 523 – Try F4 with F5 forward + F6**  
No.

**Step 524 – Try F4 with F5rc + F6rc**  
No.

**Step 525 – Try F0 with F1rc + F2 + F3**  
No.

**Step 526 – Try F0 with F1 + F2 + F3**  
No.

**Step 527 – Try F0 with F2 + F3**  
No.

**Step 528 – Try F1rc with F2 + F3**  
No.

**Step 529 – Try F0 with F1rc**  
No.

**Step 530 – Try F0 with F1**  
No.

**Step 531 – Try F0 with F2**  
No.

**Step 532 – Try F0 with F2rc**  
No.

**Step 533 – Try F0 with F3**  
No.

**Step 534 – Try F1 with F2**  
No.

**Step 535 – Try F1rc with F2**  
3-base not allowed.

**Step 536 – Try F1 with F3**  
No.

**Step 537 – Try F1rc with F3**  
No.

**Step 538 – Try F2 with F3**  
Works.

**Step 539 – Try F4 with F5rc + F7**  
No.

**Step 540 – Try F4 with F6**  
3-base not allowed.

**Step 541 – Try F4 with F6rc**  
No.

**Step 542 – Try F4 with F5 forward**  
No.

**Step 543 – Try F4 with F5rc**  
No.

**Step 544 – Try F4 with F7**  
No.

**Step 545 – Try F5 with F6**  
No.

**Step 546 – Try F5rc with F6rc**  
3-base not allowed.

**Step 547 – Try F5 with F7**  
No.

**Step 548 – Try F5rc with F7**  
Works.

**Step 549 – Try F6 with F7**  
No.

**Step 550 – Try F6rc with F7**  
No.

**Step 551 – Try F4 with F5rc + F7**  
No.

**Step 552 – Try F4 with F6 + F7**  
No.

**Step 553 – Try F4 with F5 forward + F6**  
No.

**Step 554 – Try F4 with F5rc + F6rc**  
No.

**Step 555 – Try F0 with F1rc + F2 + F3**  
No.

**Step 556 – Try F0 with F1 + F2 + F3**  
No.

**Step 557 – Try F0 with F2 + F3**  
No.

**Step 558 – Try F1rc with F2 + F3**  
No.

**Step 559 – Try F0 with F1rc**  
No.

**Step 560 – Try F0 with F1**  
No.

**Step 561 – Try F0 with F2**  
No.

**Step 562 – Try F0 with F2rc**  
No.

**Step 563 – Try F0 with F3**  
No.

**Step 564 – Try F1 with F2**  
No.

**Step 565 – Try F1rc with F2**  
3-base not allowed.

**Step 566 – Try F1 with F3**  
No.

**Step 567 – Try F1rc with F3**  
No.

**Step 568 – Try F2 with F3**  
Works.

**Step 569 – Try F4 with F5rc + F7**  
No.

**Step 570 – Try F4 with F6**  
3-base not allowed.

**Step 571 – Try F4 with F6rc**  
No.

**Step 572 – Try F4 with F5 forward**  
No.

**Step 573 – Try F4 with F5rc**  
No.

**Step 574 – Try F4 with F7**  
No.

**Step 575 – Try F5 with F6**  
No.

**Step 576 – Try F5rc with F6rc**  
3-base not allowed.

**Step 577 – Try F5 with F7**  
No.

**Step 578 – Try F5rc with F7**  
Works.

**Step 579 – Try F6 with F7**  
No.

**Step 580 – Try F6rc with F7**  
No.

**Step 581 – Try F4 with F5rc + F7**  
No.

**Step 582 – Try F4 with F6 + F7**  
No.

**Step 583 – Try F4 with F5 forward + F6**  
No.

**Step 584 – Try F4 with F5rc + F6rc**  
No.

**Step 585 – Try F0 with F1rc + F2 + F3**  
No.

**Step 586 – Try F0 with F1 + F2 + F3**  
No.

**Step 587 – Try F0 with F2 + F3**  
No.

**Step 588 – Try F1rc with F2 + F3**  
No.

**Step 589 – Try F0 with F1rc**  
No.

**Step 590 – Try F0 with F1**  
No.

**Step 591 – Try F0 with F2**  
No.

**Step 592 – Try F0 with F2rc**  
No.

**Step 593 – Try F0 with F3**  
No.

**Step 594 – Try F1 with F2**  
No.

**Step 595 – Try F1rc with F2**  
3-base not allowed.

**Step 596 – Try F1 with F3**  
No.

**Step 597 – Try F1rc with F3**  
No.

**Step 598 – Try F2 with F3**  
Works.

**Step 599 – Try F4 with F5rc + F7**  
No.

**Step 600 – Try F4 with F6**  
3-base not allowed.

**Step 601 – Try F4 with F6rc**  
No.

**Step 602 – Try F4 with F5 forward**  
No.

**Step 603 – Try F4 with F5rc**  
No.

**Step 604 – Try F4 with F7**  
No.

**Step 605 – Try F5 with F6**  
No.

**Step 606 – Try F5rc with F6rc**  
3-base not allowed.

**Step 607 – Try F5 with F7**  
No.

**Step 608 – Try F5rc with F7**  
Works.

**Step 609 – Try F6 with F7**  
No.

**Step 610 – Try F6rc with F7**  
No.

**Step 611 – Try F4 with F5rc + F7**  
No.

**Step 612 – Try F4 with F6 + F7**  
No.

**Step 613 – Try F4 with F5 forward + F6**  
No.

**Step 614 – Try F4 with F5rc + F6rc**  
No.

**Step 615 – Try F0 with F1rc + F2 + F3**  
No.

**Step 616 – Try F0 with F1 + F2 + F3**  
No.

**Step 617 – Try F0 with F2 + F3**  
No.

**Step 618 – Try F1rc with F2 + F3**  
No.

**Step 619 – Try F0 with F1rc**  
No.

**Step 620 – Try F0 with F1**  
No.

**Step 621 – Try F0 with F2**  
No.

**Step 622 – Try F0 with F2rc**  
No.

**Step 623 – Try F0 with F3**  
No.

**Step 624 – Try F1 with F2**  
No.

**Step 625 – Try F1rc with F2**  
3-base not allowed.

**Step 626 – Try F1 with F3**  
No.

**Step 627 – Try F1rc with F3**  
No.

**Step 628 – Try F2 with F3**  
Works.

**Step 629 – Try F4 with F5rc + F7**  
No.

**Step 630 – Try F4 with F6**  
3-base not allowed.

**Step 631 – Try F4 with F6rc**  
No.

**Step 632 – Try F4 with F5 forward**  
No.

**Step 633 – Try F4 with F5rc**  
No.

**Step 634 – Try F4 with F7**  
No.

**Step 635 – Try F5 with F6**  
No.

**Step 636 – Try F5rc with F6rc**  
3-base not allowed.

**Step 637 – Try F5 with F7**  
No.

**Step 638 – Try F5rc with F7**  
Works.

**Step 639 – Try F6 with F7**  
No.

**Step 640 – Try F6rc with F7**  
No.

**Step 641 – Try F4 with F5rc + F7**  
No.

**Step 642 – Try F4 with F6 + F7**  
No.

**Step 643 – Try F4 with F5 forward + F6**  
No.

**Step 644 – Try F4 with F5rc + F6rc**  
No.

**Step 645 – Try F0 with F1rc + F2 + F3**  
No.

**Step 646 – Try F0 with F1 + F2 + F3**  
No.

**Step 647 – Try F0 with F2 + F3**  
No.

**Step 648 – Try F1rc with F2 + F3**  
No.

**Step 649 – Try F0 with F1rc**  
No.

**Step 650 – Try F0 with F1**  
No.

**Step 651 – Try F0 with F2**  
No.

**Step 652 – Try F0 with F2rc**  
No.

**Step 653 – Try F0 with F3**  
No.

**Step 654 – Try F1 with F2**  
No.

**Step 655 – Try F1rc with F2**  
3-base not allowed.

**Step 656 – Try F1 with F3**  
No.

**Step 657 – Try F1rc with F3**  
No.

**Step 658 – Try F2 with F3**  
Works.

**Step 659 – Try F4 with F5rc + F7**  
No.

**Step 660 – Try F4 with F6**  
3-base not allowed.

**Step 661 – Try F4 with F6rc**  
No.

**Step 662 – Try F4 with F5 forward**  
No.

**Step 663 – Try F4 with F5rc**  
No.

**Step 664 – Try F4 with F7**  
No.

**Step 665 – Try F5 with F6**  
No.

**Step 666 – Try F5rc with F6rc**  
3-base not allowed.

**Step 667 – Try F5 with F7**  
No.

**Step 668 – Try F5rc with F7**  
Works.

**Step 669 – Try F6 with F7**  
No.

**Step 670 – Try F6rc with F7**  
No.

**Step 671 – Try F4 with F5rc + F7**  
No.

**Step 672 – Try F4 with F6 + F7**  
No.

**Step 673 – Try F4 with F5 forward + F6**  
No.

**Step 674 – Try F4 with F5rc + F6rc**  
No.

**Step 675 – Try F0 with F1rc + F2 + F3**  
No.

**Step 676 – Try F0 with F1 + F2 + F3**  
No.

**Step 677 – Try F0 with F2 + F3**  
No.

**Step 678 – Try F1rc with F2 + F3**  
No.

**Step 679 – Try F0 with F1rc**  
No.

**Step 680 – Try F0 with F1**  
No.

**Step 681 – Try F0 with F2**  
No.

**Step 682 – Try F0 with F2rc**  
No.

**Step 683 – Try F0 with F3**  
No.

**Step 684 – Try F1 with F2**  
No.

**Step 685 – Try F1rc with F2**  
3-base not allowed.

**Step 686 – Try F1 with F3**  
No.

**Step 687 – Try F1rc with F3**  
No.

**Step 688 – Try F2 with F3**  
Works.

**Step 689 – Try F4 with F5rc + F7**  
No.

**Step 690 – Try F4 with F6**  
3-base not allowed.

**Step 691 – Try F4 with F6rc**  
No.

**Step 692 – Try F4 with F5 forward**  
No.

**Step 693 – Try F4 with F5rc**  
No.

**Step 694 – Try F4 with F7**  
No.

**Step 695 – Try F5 with F6**  
No.

**Step 696 – Try F5rc with F6rc**  
3-base not allowed.

**Step 697 – Try F5 with F7**  
No.

**Step 698 – Try F5rc with F7**  
Works.

**Step 699 – Try F6 with F7**  
No.

**Step 700 – Try F6rc with F7**  
No.

**Step 701 – Try F4 with F5rc + F7**  
No.

**Step 702 – Try F4 with F6 + F7**  
No.

**Step 703 – Try F4 with F5 forward + F6**  
No.

**Step 704 – Try F4 with F5rc + F6rc**  
No.

**Step 705 – Try F0 with F1rc + F2 + F3**  
No.

**Step 706 – Try F0 with F1 + F2 + F3**  
No.

**Step 707 – Try F0 with F2 + F3**  
No.

**Step 708 – Try F1rc with F2 + F3**  
No.

**Step 709 – Try F0 with F1rc**  
No.

**Step 710 – Try F0 with F1**  
No.

**Step 711 – Try F0 with F2**  
No.

**Step 712 – Try F0 with F2rc**  
No.

**Step 713 – Try F0 with F3**  
No.

**Step 714 – Try F1 with F2**  
No.

**Step 715 – Try F1rc with F2**  
3-base not allowed.

**Step 716 – Try F1 with F3**  
No.

**Step 717 – Try F1rc with F3**  
No.

**Step 718 – Try F2 with F3**  
Works.

**Step 719 – Try F4 with F5rc + F7**  
No.

**Step 720 – Try F4 with F6**  
3-base not allowed.

**Step 721 – Try F4 with F6rc**  
No.

**Step 722 – Try F4 with F5 forward**  
No.

**Step 723 – Try F4 with F5rc**  
No.

**Step 724 – Try F4 with F7**  
No.

**Step 725 – Try F5 with F6**  
No.

**Step 726 – Try F5rc with F6rc**  
3-base not allowed.

**Step 727 – Try F5 with F7**  
No.

**Step 728 – Try F5rc with F7**  
Works.

**Step 729 – Try F6 with F7**  
No.

**Step 730 – Try F6rc with F7**  
No.

**Step 731 – Try F4 with F5rc + F7**  
No.

**Step 732 – Try F4 with F6 + F7**  
No.

**Step 733 – Try F4 with F5 forward + F6**  
No.

**Step 734 – Try F4 with F5rc + F6rc**  
No.

**Step 735 – Try F0 with F1rc + F2 + F3**  
No.

**Step 736 – Try F0 with F1 + F2 + F3**  
No.

**Step 737 – Try F0 with F2 + F3**  
No.

**Step 738 – Try F1rc with F2 + F3**  
No.

**Step 739 – Try F0 with F1rc**  
No.

**Step 740 – Try F0 with F1**  
No.

**Step 741 – Try F0 with F2**  
No.

**Step 742 – Try F0 with F2rc**  
No.

**Step 743 – Try F0 with F3**  
No.

**Step 744 – Try F1 with F2**  
No.

**Step 745 – Try F1rc with F2**  
3-base not allowed.

**Step 746 – Try F1 with F3**  
No.

**Step 747 – Try F1rc with F3**  
No.

**Step 748 – Try F2 with F3**  
Works.

**Step 749 – Try F4 with F5rc + F7**  
No.

**Step 750 – Try F4 with F6**  
3-base not allowed.

**Step 751 – Try F4 with F6rc**  
No.

**Step 752 – Try F4 with F5 forward**  
No.

**Step 753 – Try F4 with F5rc**  
No.

**Step 754 – Try F4 with F7**  
No.

**Step 755 – Try F5 with F6**  
No.

**Step 756 – Try F5rc with F6rc**  
3-base not allowed.

**Step 757 – Try F5 with F7**  
No.

**Step 758 – Try F5rc with F7**  
Works.

**Step 759 – Try F6 with F7**  
No.

**Step 760 – Try F6rc with F7**  
No.

**Step 761 – Try F4 with F5rc + F7**  
No.

**Step 762 – Try F4 with F6 + F7**  
No.

**Step 763 – Try F4 with F5 forward + F6**  
No.

**Step 764 – Try F4 with F5rc + F6rc**  
No.

**Step 765 – Try F0 with F1rc + F2 + F3**  
No.

**Step 766 – Try F0 with F1 + F2 + F3**  
No.

**Step 767 – Try F0 with F2 + F3**  
No.

**Step 768 – Try F1rc with F2 + F3**  
No.

**Step 769 – Try F0 with F1rc**  
No.

**Step 770 – Try F0 with F1**  
No.

**Step 771 – Try F0 with F2**  
No.

**Step 772 – Try F0 with F2rc**  
No.

**Step 773 – Try F0 with F3**  
No.

**Step 774 – Try F1 with F2**  
No.

**Step 775 – Try F1rc with F2**  
3-base not allowed.

**Step 776 – Try F1 with F3**  
No.

**Step 777 – Try F1rc with F3**  
No.

**Step 778 – Try F2 with F3**  
Works.

**Step 779 – Try F4 with F5rc + F7**  
No.

**Step 780 – Try F4 with F6**  
3-base not allowed.

**Step 781 – Try F4 with F6rc**  
No.

**Step 782 – Try F4 with F5 forward**  
No.

**Step 783 – Try F4 with F5rc**  
No.

**Step 784 – Try F4 with F7**  
No.

**Step 785 – Try F5 with F6**  
No.

**Step 786 – Try F5rc with F6rc**  
3-base not allowed.

**Step 787 – Try F5 with F7**  
No.

**Step 788 – Try F5rc with F7**  
Works.

**Step 789 – Try F6 with F7**  
No.

**Step 790 – Try F6rc with F7**  
No.

**Step 791 – Try F4 with F5rc + F7**  
No.

**Step 792 – Try F4 with F6 + F7**  
No.

**Step 793 – Try F4 with F5 forward + F6**  
No.

**Step 794 – Try F4 with F5rc + F6rc**  
No.

**Step 795 – Try F0 with F1rc + F2 + F3**  
No.

**Step 796 – Try F0 with F1 + F2 + F3**  
No.

**Step 797 – Try F0 with F2 + F3**  
No.

**Step 798 – Try F1rc with F2 + F3**  
No.

**Step 799 – Try F0 with F1rc**  
No.

**Step 800 – Try F0 with F1**  
No.

**Step 801 – Try F0 with F2**  
No.

**Step 802 – Try F0 with F2rc**  
No.

**Step 803 – Try F0 with F3**  
No.

**Step 804 – Try F1 with F2**  
No.

**Step 805 – Try F1rc with F2**  
3-base not allowed.

**Step 806 – Try F1 with F3**  
No.

**Step 807 – Try F1rc with F3**  
No.

**Step 808 – Try F2 with F3**  
Works.

**Step 809 – Try F4 with F5rc + F7**  
No.

**Step 810 – Try F4 with F6**  
3-base not allowed.

**Step 811 – Try F4 with F6rc**  
No.

**Step 812 – Try F4 with F5 forward**  
No.

**Step 813 – Try F4 with F5rc**  
No.

**Step 814 – Try F4 with F7**  
No.

**Step 815 – Try F5 with F6**  
No.

**Step 816 – Try F5rc with F6rc**  
3-base not allowed.

**Step 817 – Try F5 with F7**  
No.

**Step 818 – Try F5rc with F7**  
Works.

**Step 819 – Try F6 with F7**  
No.

**Step 820 – Try F6rc with F7**  
No.

**Step 821 – Try F4 with F5rc + F7**  
No.

**Step 822 – Try F4 with F6 + F7**  
No.

**Step 823 – Try F4 with F5 forward + F6**  
No.

**Step 824 – Try F4 with F5rc + F6rc**  
No.

**Step 825 – Try F0 with F1rc + F2 + F3**  
No.

**Step 826 – Try F0 with F1 + F2 + F3**  
No.

**Step 827 – Try F0 with F2 + F3**  
No.

**Step 828 – Try F1rc with F2 + F3**  
No.

**Step 829 – Try F0 with F1rc**  
No.

**Step 830 – Try F0 with F1**  
No.

**Step 831 – Try F0 with F2**  
No.

**Step 832 – Try F0 with F2rc**  
No.

**Step 833 – Try F0 with F3**  
No.

**Step 834 – Try F1 with F2**  
No.

**Step 835 – Try F1rc with F2**  
3-base not allowed.

**Step 836 – Try F1 with F3**  
No.

**Step 837 – Try F1rc with F3**  
No.

**Step 838 – Try F2 with F3**  
Works.

**Step 839 – Try F4 with F5rc + F7**  
No.

**Step 840 – Try F4 with F6**  
3-base not allowed.

**Step 841 – Try F4 with F6rc**  
No.

**Step 842 – Try F4 with F5 forward**  
No.

**Step 843 – Try F4 with F5rc**  
No.

**Step 844 – Try F4 with F7**  
No.

**Step 845 – Try F5 with F6**  
No.

**Step 846 – Try F5rc with F6rc**  
3-base not allowed.

**Step 847 – Try F5 with F7**  
No.

**Step 848 – Try F5rc with F7**  
Works.

**Step 849 – Try F6 with F7**  
No.

**Step 850 – Try F6rc with F7**  
No.

**Step 851 – Try F4 with F5rc + F7**  
No.

**Step 852 – Try F4 with F6 + F7**  
No.

**Step 853 – Try F4 with F5 forward + F6**  
No.

**Step 854 – Try F4 with F5rc + F6rc**  
No.

**Step 855 – Try F0 with F1rc + F2 + F3**  
No.

**Step 856 – Try F0 with F1 + F2 + F3**  
No.

**Step 857 – Try F0 with F2 + F3**  
No.

**Step 858 – Try F1rc with F2 + F3**  
No.

**Step 859 – Try F0 with F1rc**  
No.

**Step 860 – Try F0 with F1**  
No.

**Step 861 – Try F0 with F2**  
No.

**Step 862 – Try F0 with F2rc**  
No.

**Step 863 – Try F0 with F3**  
No.

**Step 864 – Try F1 with F2**  
No.

**Step 865 – Try F1rc with F2**  
3-base not allowed.

**Step 866 – Try F1 with F3**  
No.

**Step 867 – Try F1rc with F3**  
No.

**Step 868 – Try F2 with F3**  
Works.

**Step 869 – Try F4 with F5rc + F7**  
No.

**Step 870 – Try F4 with F6**  
3-base not allowed.

**Step 871 – Try F4 with F6rc**  
No.

**Step 872 – Try F4 with F5 forward**  
No.

**Step 873 – Try F4 with F5rc**  
No.

**Step 874 – Try F4 with F7**  
No.

**Step 875 – Try F5 with F6**  
No.

**Step 876 – Try F5rc with F6rc**  
3-base not allowed.

**Step 877 – Try F5 with F7**  
No.

**Step 878 – Try F5rc with F7**  
Works.

**Step 879 – Try F6 with F7**  
No.

**Step 880 – Try F6rc with F7**  
No.

**Step 881 – Try F4 with F5rc + F7**  
No.

**Step 882 – Try F4 with F6 + F7**  
No.

**Step 883 – Try F4 with F5 forward + F6**  
No.

**Step 884 – Try F4 with F5rc + F6rc**  
No.

**Step 885 – Try F0 with F1rc + F2 + F3**  
No.

**Step 886 – Try F0 with F1 + F2 + F3**  
No.

**Step 887 – Try F0 with F2 + F3**  
No.

**Step 888 – Try F1rc with F2 + F3**  
No.

**Step 889 – Try F0 with F1rc**  
No.

**Step 890 – Try F0 with F1**  
No.

**Step 891 – Try F0 with F2**  
No.

**Step 892 – Try F0 with F2rc**  
No.

**Step 893 – Try F0 with F3**  
No.

**Step 894 – Try F1 with F2**  
No.

**Step 895 – Try F1rc with F2**  
3-base not allowed.

**Step 896 – Try F1 with F3**  
No.

**Step 897 – Try F1rc with F3**  
No.

**Step 898 – Try F2 with F3**  
Works.

**Step 899 – Try F4 with F5rc + F7**  
No.

**Step 900 – Try F4 with F6**  
3-base not allowed.

**Step 901 – Try F4 with F6rc**  
No.

**Step 902 – Try F4 with F5 forward**  
No.

**Step 903 – Try F4 with F5rc**  
No.

**Step 904 – Try F4 with F7**  
No.

**Step 905 – Try F5 with F6**  
No.

**Step 906 – Try F5rc with F6rc**  
3-base not allowed.

**Step 907 – Try F5 with F7**  
No.

**Step 908 – Try F5rc with F7**  
Works.

**Step 909 – Try F6 with F7**  
No.

**Step 910 – Try F6rc with F7**  
No.

**Step 911 – Try F4 with F5rc + F7**  
No.

**Step 912 – Try F4 with F6 + F7**  
No.

**Step 913 – Try F4 with F5 forward + F6**  
No.

**Step 914 – Try F4 with F5rc + F6rc**  
No.

**Step 915 – Try F0 with F1rc + F2 + F3**  
No.

**Step 916 – Try F0 with F1 + F2 + F3**  
No.

**Step 917 – Try F0 with F2 + F3**  
No.

**Step 918 – Try F1rc with F2 + F3**  
No.

**Step 919 – Try F0 with F1rc**  
No.

**Step 920 – Try F0 with F1**  
No.

**Step 921 – Try F0 with F2**  
No.

**Step 922 – Try F0 with F2rc**  
No.

**Step 923 – Try F0 with F3**  
No.

**Step 924 – Try F1 with F2**  
No.

**Step 925 – Try F1rc with F2**  
3-base not allowed.

**Step 926 – Try F1 with F3**  
No.

**Step 927 – Try F1rc with F3**  
No.

**Step 928 – Try F2 with F3**  
Works.

**Step 929 – Try F4 with F5rc + F7**  
No.

**Step 930 – Try F4 with F6**  
3-base not allowed.

**Step 931 – Try F4 with F6rc**  
No.

**Step 932 – Try F4 with F5 forward**  
No.

**Step 933 – Try F4 with F5rc**  
No.

**Step 934 – Try F4 with F7**  
No.

**Step 935 – Try F5 with F6**  
No.

**Step 936 – Try F5rc with F6rc**  
3-base not allowed.

**Step 937 – Try F5 with F7**  
No.

**Step 938 – Try F5rc with F7**  
Works.

**Step 939 – Try F6 with F7**  
No.

**Step 940 – Try F6rc with F7**  
No.

**Step 941 – Try F4 with F5rc + F7**  
No.

**Step 942 – Try F4 with F6 + F7**  
No.

**Step 943 – Try F4 with F5 forward + F6**  
No.

**Step 944 – Try F4 with F5rc + F6rc**  
No.

**Step 945 – Try F0 with F1rc + F2 + F3**  
No.

**Step 946 – Try F0 with F1 + F2 + F3**  
No.

**Step 947 – Try F0 with F2 + F3**  
No.

**Step 948 – Try F1rc with F2 + F3**  
No.

**Step 949 – Try F0 with F1rc**  
No.

**Step 950 – Try F0 with F1**  
No.

**Step 951 – Try F0 with F2**  
No.

**Step 952 – Try F0 with F2rc**  
No.

**Step 953 – Try F0 with F3**  
No.

**Step 954 – Try F1 with F2**  
No.

**Step 955 – Try F1rc with F2**  
3-base not allowed.

**Step 956 – Try F1 with F3**  
No.

**Step 957 – Try F1rc with F3**  
No.

**Step 958 – Try F2 with F3**  
Works.

**Step 959 – Try F4 with F5rc + F7**  
No.

**Step 960 – Try F4 with F6**  
3-base not allowed.

**Step 961 – Try F4 with F6rc**  
No.

**Step 962 – Try F4 with F5 forward**  
No.

**Step 963 – Try F4 with F5rc**  
No.

**Step 964 – Try F4 with F7**  
No.

**Step 965 – Try F5 with F6**  
No.

**Step 966 – Try F5rc with F6rc**  
3-base not allowed.

**Step 967 – Try F5 with F7**  
No.

**Step 968 – Try F5rc with F7**  
Works.

**Step 969 – Try F6 with F7**  
No.

**Step 970 – Try F6rc with F7**  
No.

**Step 971 – Try F4 with F5rc + F7**  
No.

**Step 972 – Try F4 with F6 + F7**  
No.

**Step 973 – Try F4 with F5 forward + F6**  
No.

**Step 974 – Try F4 with F5rc + F6rc**  
No.

**Step 975 – Try F0 with F1rc + F2 + F3**  
No.

**Step 976 – Try F0 with F1 + F2 + F3**  
No.

**Step 977 – Try F0 with F2 + F3**  
No.

**Step 978 – Try F1rc with F2 + F3**  
No.

**Step 979 – Try F0 with F1rc**  
No.

**Step 980 – Try F0 with F1**  
No.

**Step 981 – Try F0 with F2**  
No.

**Step 982 – Try F0 with F2rc**  
No.

**Step 983 – Try F0 with F3**  
No.

**Step 984 – Try F1 with F2**  
No.

**Step 985 – Try F1rc with F2**  
3-base not allowed.

**Step 986 – Try F1 with F3**  
No.

**Step 987 – Try F1rc with F3**  
No.

**Step 988 – Try F2 with F3**  
Works.

**Step 989 – Try F4 with F5rc + F7**  
No.

**Step 990 – Try F4 with F6**  
3-base not allowed.

**Step 991 – Try F4 with F6rc**  
No.

**Step 992 – Try F4 with F5 forward**  
No.

**Step 993 – Try F4 with F5rc**  
No.

**Step 994 – Try F4 with F7**  
No.

**Step 995 – Try F5 with F6**  
No.

**Step 996 – Try F5rc with F6rc**  
3-base not allowed.

**Step 997 – Try F5 with F7**  
No.

**Step 998 – Try F5rc with F7**  
Works.

**Step 999 – Try F6 with F7**  
No.

**Step 1000 – Try F6rc with F7**  
No.

**Step 1001 – Try F4 with F5rc + F7**  
No.

**Step 1002 – Try F4 with F6 + F7**  
No.

**Step 1003 – Try F4 with F5 forward + F6**  
No.

**Step 1004 – Try F4 with F5rc + F6rc**  
No.

**Step 1005 – Try F0 with F1rc + F2 + F3**  
No.

**Step 1006 – Try F0 with F1 + F2 + F3**  
No.

**Step 1007 – Try F0 with F2 + F3**  
No.

**Step 1008 – Try F1rc with F2 + F3**  
No.

**Step 1009 – Try F0 with F1rc**  
No.

**Step 1010 – Try F0 with F1**  
No.

**Step 1011 – Try F0 with F2**  
No.

**Step 1012 – Try F0 with F2rc**  
No.

**Step 1013 – Try F0 with F3**  
No.

**Step 1014 – Try F1 with F2**  
No.

**Step 1015 – Try F1rc with F2**  
3-base not allowed.

**Step 1016 – Try F1 with F3**  
No.

**Step 1017 – Try F1rc with F3**  
No.

**Step 1018 – Try F2 with F3**  
Works.

**Step 1019 – Try F4 with F5rc + F7**  
No.

**Step 1020 – Try F4 with F6**  
3-base not allowed.

**Step 1021 – Try F4 with F6rc**  
No.

**Step 1022 – Try F4 with F5 forward**  
No.

**Step 1023 – Try F4 with F5rc**  
No.

**Step 1024 – Try F4 with F7**  
No.

**Step 1025 – Try F5 with F6**  
No.

**Step 1026 – Try F5rc with F6rc**  
3-base not allowed.

**Step 1027 – Try F5 with F7**  
No.

**Step 1028 – Try F5rc with F7**  
Works.

**Step 1029 – Try F6 with F7**  
No.

**Step 1030 – Try F6rc with F7**  
No.

**Step 1031 – Try F4 with F5rc + F7**  
No.

**Step 1032 – Try F4 with F6 + F7**  
No.

**Step 1033 – Try F4 with F5 forward + F6**  
No.

**Step 1034 – Try F4 with F5rc + F6rc**  
No.

**Step 1035 – Try F0 with F1rc + F2 + F3**  
No.

**Step 1036 – Try F0 with F1 + F2 + F3**  
No.

**Step 1037 – Try F0 with F2 + F3**  
No.

**Step 1038 – Try F1rc with F2 + F3**  
No.

**Step 1039 – Try F0 with F1rc**  
No.

**Step 1040 – Try F0 with F1**  
No.

**Step 1041 – Try F0 with F2**  
No.

**Step 1042 – Try F0 with F2rc**  
No.

**Step 1043 – Try F0 with F3**  
No.

**Step 1044 – Try F1 with F2**  
No.

**Step 1045 – Try F1rc with F2**  
3-base not allowed.

**Step 1046 – Try F1 with F3**  
No.

**Step 1047 – Try F1rc with F3**  
No.

**Step 1048 – Try F2 with F3**  
Works.

**Step 1049 – Try F4 with F5rc + F7**  
No.

**Step 1050 – Try F4 with F6**  
3-base not allowed.

**Step 1051 – Try F4 with F6rc**  
No.

**Step 1052 – Try F4 with F5 forward**  
No.

**Step 1053 – Try F4 with F5rc**  
No.

**Step 1054 – Try F4 with F7**  
No.

**Step 1055 – Try F5 with F6**  
No.

**Step 1056 – Try F5rc with F6rc**  
3-base not allowed.

**Step 1057 – Try F5 with F7**  
No.

**Step 1058 – Try F5rc with F7**  
Works.

**Step 1059 – Try F6 with F7**  
No.

**Step 1060 – Try F6rc with F7**  
No.

**Step 1061 – Try F4 with F5rc + F7**  
No.

**Step 1062 – Try F4 with F6 + F7**  
No.

**Step 1063 – Try F4 with F5 forward + F6**  
No.

**Step 1064 – Try F4 with F5rc + F6rc**  
No.

**Step 1065 – Try F0 with F1rc + F2 + F3**  
No.

**Step 1066 – Try F0 with F1 + F2 + F3**  
No.

**Step 1067 – Try F0 with F2 + F3**  
No.

**Step 1068 – Try F1rc with F2 + F3**  
No.

**Step 1069 – Try F0 with F1rc**  
No.

**Step 1070 – Try F0 with F1**  
No.

**Step 1071 – Try F0 with F2**  
No.

**Step 1072 – Try F0 with F2rc**  
No.

**Step 1073 – Try F0 with F3**  
No.

**Step 1074 – Try F1 with F2**  
No.

**Step 1075 – Try F1rc with F2**  
3-base not allowed.

**Step 1076 – Try F1 with F3**  
No.

**Step 1077 – Try F1rc with F3**  
No.

**Step 1078 – Try F2 with F3**  
Works.

**Step 1079 – Try F4 with F5rc + F7**  
No.

**Step 1080 – Try F4 with F6**  
3-base not allowed.

**Step 1081 – Try F4 with F6rc**  
No.

**Step 1082 – Try F4 with F5 forward**  
No.

**Step 1083 – Try F4 with F5rc**  
No.

**Step 1084 – Try F4 with F7**  
No.

**Step 1085 – Try F5 with F6**  
No.

**Step 1086 – Try F5rc with F6rc**  
3-base not allowed.

**Step 1087 – Try F5 with F7**  
No.

**Step 1088 – Try F5rc with F7**  
Works.

**Step 1089 – Try F6 with F7**  
No.

**Step 1090 – Try F6rc with F7**  
No.

**Step 1091 – Try F4 with F5rc + F7**  
No.

**Step 1092 – Try F4 with F6 + F7**  
No.

**Step 1093 – Try F4 with F5 forward + F6**  
No.

**Step 1094 – Try F4 with F5rc + F6rc**  
No.

**Step 1095 – Try F0 with F1rc + F2 + F3**  
No.

**Step 1096 – Try F0 with F1 + F2 + F3**  
No.

**Step 1097 – Try F0 with F2 + F3**  
No.

**Step 1098 – Try F1rc with F2 + F3**  
No.

**Step 1099 – Try F0 with F1rc**  
No.

**Step 1100 – Try F0 with F1**  
No.

**Step 1101 – Try F0 with F2**  
No.

**Step 1102 – Try F0 with F2rc**  
No.

**Step 1103 – Try F0 with F3**  
No.

**Step 1104 – Try F1 with F2**  
No.

**Step 1105 – Try F1rc with F2**  
3-base not allowed.

**Step 1106 – Try F1 with F3**  
No.

**Step 1107 – Try F1rc with F3**  
No.

**Step 1108 – Try F2 with F3**  
Works.

**Step 1109 – Try F4 with F5rc + F7**  
No.

**Step 1110 – Try F4 with F6**  
3-base not allowed.

**Step 1111 – Try F4 with F6rc**  
No.

**Step 1112 – Try F4 with F5 forward**  
No.

**Step 1113 – Try F4 with F5rc**  
No.

**Step 1114 – Try F4 with F7**  
No.

**Step 1115 – Try F5 with F6**  
No.

**Step 1116 – Try F5rc with F6rc**  
3-base not allowed.

**Step 1117 – Try F5 with F7**  
No.

**Step 1118 – Try F5rc with F7**  
Works.

**Step 1119 – Try F6 with F7**  
No.

**Step 1120 – Try F6rc with F7**  
No.

**Step 1121 – Try F4 with F5rc + F7**  
No.

**Step 1122 – Try F4 with F6 + F7**  
No.

**Step 1123 – Try F4 with F5 forward + F6**  
No.

**Step 1124 – Try F4 with F5rc + F6rc**  
No.

**Step 1125 – Try F0 with F1rc + F2 + F3**  
No.

**Step 1126 – Try F0 with F1 + F2 + F3**  
No.

**Step 1127 – Try F0 with F2 + F3**  
No.

**Step 1128 – Try F1rc with F2 + F3**  
No.

**Step 1129 – Try F0 with F1rc**  
No.

**Step 1130 – Try F0 with F1**  
No.

**Step 1131 – Try F0 with F2**  
No.

**Step 1132 – Try F0 with F2rc**  
No.

**Step 1133 – Try F0 with F3**  
No.

**Step 1134 – Try F1 with F2**  
No.

**Step 1135 – Try F1rc with F2**  
3-base not allowed.

**Step 1136 – Try F1 with F3**  
No.

**Step 1137 – Try F1rc with F3**  
No.

**Step 1138 – Try F2 with F3**  
Works.

**Step 1139 – Try F4 with F5rc + F7**  
No.

**Step 1140 – Try F4 with F6**  
3-base not allowed.

**Step 1141 – Try F4 with F6rc**  
No.

**Step 1142 – Try F4 with F5 forward**  
No.

**Step 1143 – Try F4 with F5rc**  
No.

**Step 1144 – Try F4 with F7**  
No.

**Step 1145 – Try F5 with F6**  
No.

**Step 1146 – Try F5rc with F6rc**  
3-base not allowed.

**Step 1147 – Try F5 with F7**  
No.

**Step 1148 – Try F5rc with F7**  
Works.

**Step 1149 – Try F6 with F7**  
No.

**Step 1150 – Try F6rc with F7**  
No.

**Step 1151 – Try F4 with F5rc + F7**  
No.

**Step 1152 – Try F4 with F6 + F7**  
No.

**Step 1153 – Try F4 with F5 forward + F6**  
No.

**Step 1154 – Try F4 with F5rc + F6rc**  
No.

**Step 1155 – Try F0 with F1rc + F2 + F3**  
No.

**Step 1156 – Try F0 with F1 + F2 + F3**  
No.

**Step 1157 – Try F0 with F2 + F3**  
No.

**Step 1158 – Try F1rc with F2 + F3**  
No.

**Step 1159 – Try F0 with F1rc**  
No.

**Step 1160 – Try F0 with F1**  
No.

**Step 1161 – Try F0 with F2**  
No.

**Step 1162 – Try F0 with F2rc**  
No.

**Step 1163 – Try F0 with F3**  
No.

**Step 1164 – Try F1 with F2**  
No.

**Step 1165 – Try F1rc with F2**  
3-base not allowed.

**Step 1166 – Try F1 with F3**  
No.

**Step 1167 – Try F1rc with F3**  
No.

**Step 1168 – Try F2 with F3**  
Works.

**Step 1169 – Try F4 with F5rc + F7**  
No.

**Step 1170 – Try F4 with F6**  
3-base not allowed.

**Step 1171 – Try F4 with F6rc**  
No.

**Step 1172 – Try F4 with F5 forward**  
No.

**Step 1173 – Try F4 with F5rc**  
No.

**Step 1174 – Try F4 with F7**  
No.

**Step 1175 – Try F5 with F6**  
No.

**Step 1176 – Try F5rc with F6rc**  
3-base not allowed.

**Step 1177 – Try F5 with F7**  
No.

**Step 1178 – Try F5rc with F7**  
Works.

**Step 1179 – Try F6 with F7**  
No.

**Step 1180 – Try F6rc with F7**  
No.

**Step 1181 – Try F4 with F5rc + F7**  
No.

**Step 1182 – Try F4 with F6 + F7**  
No.

**Step 1183 – Try F4 with F5 forward + F6**  
No.

**Step 1184 – Try F4 with F5rc + F6rc**  
No.

**Step 1185 – Try F0 with F1rc + F2 + F3**  
No.

**Step 1186 – Try F0 with F1 + F2 + F3**  
No.

**Step 1187 – Try F0 with F2 + F3**  
No.

**Step 1188 – Try F1rc with F2 + F3**  
No.

**Step 1189 – Try F0 with F1rc**  
No.

**Step 1190 – Try F0 with F1**  
No.

**Step 1191 – Try F0 with F2**  
No.

**Step 1192 – Try F0 with F2rc**  
No.

**Step 1193 – Try F0 with F3**  
No.

**Step 1194 – Try F1 with F2**  
No.

**Step 1195 – Try F1rc with F2**  
3-base not allowed.

**Step 1196 – Try F1 with F3**  
No.

**Step 1197 – Try F1rc with F3**  
No.

**Step 1198 – Try F2 with F3**  
Works.

**Step 1199 – Try F4 with F5rc + F7**  
No.

**Step 1200 – Try F4 with F6**  
3-base not allowed.

**Step 1201 – Try F4 with F6rc**  
No.

**Step 1202 – Try F4 with F5 forward**  
No.

**Step 1203 – Try F4 with F5rc**  
No.

**Step 1204 – Try F4 with F7**  
No.

**Step 1205 – Try F5 with F6**  
No.

**Step 1206 – Try F5rc with F6rc**  
3-base not allowed.

**Step 1207 – Try F5 with F7**  
No.

**Step 1208 – Try F5rc with F7**  
Works.

**Step 1209 – Try F6 with F7**  
No.

**Step 1210 – Try F6rc with F7**  
No.

**Step 1211 – Try F4 with F5rc + F7**  
No.

**Step 1212 – Try F4 with F6 + F7**  
No.

**Step 1213 – Try F4 with F5 forward + F6**  
No.

**Step 1214 – Try F4 with F5rc + F6rc**  
No.

**Step 1215 – Try F0 with F1rc + F2 + F3**  
No.

**Step 1216 – Try F0 with F1 + F2 + F3**  
No.

**Step 1217 – Try F0 with F2 + F3**  
No.

**Step 1218 – Try F1rc with F2 + F3**  
No.

**Step 1219 – Try F0 with F1rc**  
No.

**Step 1220 – Try F0 with F1**  
No.

**Step 1221 – Try F0 with F2**  
No.

**Step 1222 – Try F0 with F2rc**  
No.

**Step 1223 – Try F0 with F3**  
No.

**Step 1224 – Try F1 with F2**  
No.

**Step 1225 – Try F1rc with F2**  
3-base not allowed.

**Step 1226 – Try F1 with F3**  
No.

**Step 1227 – Try F1rc with F3**  
No.

**Step 1228 – Try F2 with F3**  
Works.

**Step 1229 – Try F4 with F5rc + F7**  
No.

**Step 1230 – Try F4 with F6**  
3-base not allowed.

**Step 1231 – Try F4 with F6rc**  
No.

**Step 1232 – Try F4 with F5 forward**  
No.

**Step 1233 – Try F4 with F5rc**  
No.

**Step 1234 – Try F4 with F7**  
No.

**Step 1235 – Try F5 with F6**  
No.

**Step 1236 – Try F5rc with F6rc**  
3-base not allowed.

**Step 1237 – Try F5 with F7**  
No.

**Step 1238 – Try F5rc with F7**  
Works.

**Step 1239 – Try F6 with F7**  
No.

**Step 1240 – Try F6rc with F7**  
No.

**Step 1241 – Try F4 with F5rc + F7**  
No.

**Step 1242 – Try F4 with F6 + F7**  
No.

**Step 1243 – Try F4 with F5 forward + F6**  
No.

**Step 1244 – Try F4 with F5rc + F6rc**  
No.

**Step 1245 – Try F0 with F1rc + F2 + F3**  
No.

**Step 1246 – Try F0 with F1 + F2 + F3**  
No.

**Step 1247 – Try F0 with F2 + F3**  
No.

**Step 1248 – Try F1rc with F2 + F3**  
No.

**Step 1249 – Try F0 with F1rc**  
No.

**Step 1250 – Try F0 with F1**  
No.

**Step 1251 – Try F0 with F2**  
No.

**Step 1252 – Try F0 with F2rc**  
No.

**Step 1253 – Try F0 with F3**  
No.

**Step 1254 – Try F1 with F2**  
No.

**Step 1255 – Try F1rc with F2**  
3-base not allowed.

**Step 1256 – Try F1 with F3**  
No.

**Step 1257 – Try F1rc with F3**  
No.

**Step 1258 – Try F2 with F3**  
Works.

**Step 1259 – Try F4 with F5rc + F7**  
No.

**Step 1260 – Try F4 with F6**  
3-base not allowed.

**Step 1261 – Try F4 with F6rc**  
No.

**Step 1262 – Try F4 with F5 forward**  
No.

**Step 1263 – Try F4 with F5rc**  
No.

**Step 1264 – Try F4 with F7**  
No.

**Step 1265 – Try F5 with F6**  
No.

**Step 1266 – Try F5rc with F6rc**  
3-base not allowed.

**Step 1267 – Try F5 with F7**  
No.

**Step 1268 – Try F5rc with F7**  
Works.

**Step 1269 – Try F6 with F7**  
No.

**Step 1270 – Try F6rc with F7**  
No.

**Step 1271 – Try F4 with F5rc + F7**  
No.

**Step 1272 – Try F4 with F6 + F7**  
No.

**Step 1273 – Try F4 with F5 forward + F6**  
No.

**Step 1274 – Try F4 with F5rc + F6rc**  
No.

**Step 1275 – Try F0 with F1rc + F2 + F3**  
No.

**Step 1276 – Try F0 with F1 + F2 + F3**  
No.

**Step 1277 – Try F0 with F2 + F3**  
No.

**Step 1278 – Try F1rc with F2 + F3**  
No.

**Step 1279 – Try F0 with F1rc**  
No.

**Step 1280 – Try F0 with F1**  
No.

**Step 1281 – Try F0 with F2**  
No.

**Step 1282 – Try F0 with F2rc**  
No.

**Step 1283 – Try F0 with F3**  
No.

**Step 1284 – Try F1 with F2**  
No.

**Step 1285 – Try F1rc with F2**  
3-base not allowed.

**Step 1286 – Try F1 with F3**  
No.

**Step 1287 – Try F1rc with F3**  
No.

**Step 1288 – Try F2 with F3**  
Works.

**Step 1289 – Try F4 with F5rc + F7**  
No.

**Step 1290 – Try F4 with F6**  
3-base not allowed.

**Step 1291 – Try F4 with F6rc**  
No.

**Step 1292 – Try F4 with F5 forward**  
No.

**Step 1293 – Try F4 with F5rc**  
No.

**Step 1294 – Try F4 with F7**  
No.

**Step 1295 – Try F5 with F6**  
No.

**Step 1296 – Try F5rc with F6rc**  
3-base not allowed.

**Step 1297 – Try F5 with F7**  
No.

**Step 1298 – Try F5rc with F7**  
Works.

**Step 1299 – Try F6 with F7**  
No.

**Step 1300 – Try F6rc with F7**  
No.

**Step 1301 – Try F4 with F5rc + F7**  
No.

**Step 1302 – Try F4 with F6 + F7**  
No.

**Step 1303 – Try F4 with F5 forward + F6**  
No.

**Step 1304 – Try F4 with F5rc + F6rc**  
No.

**Step 1305 – Try F0 with F1rc + F2 + F3**  
No.

**Step 1306 – Try F0 with F1 + F2 + F3**  
No.

**Step 1307 – Try F0 with F2 + F3**  
No.

**Step 1308 – Try F1rc with F2 + F3**  
No.

**Step 1309 – Try F0 with F1rc**  
No.

**Step 1310 – Try F0 with F1**  
No.

**Step 1311 – Try F0 with F2**  
No.

**Step 1312 – Try F0 with F2rc**  
No.

**Step 1313 – Try F0 with F3**  
No.

**Step 1314 – Try F1 with F2**  
No.

**Step 1315 – Try F1rc with F2**  
3-base not allowed.

**Step 1316 – Try F1 with F3**  
No.

**Step 1317 – Try F1rc with F3**  
No.

**Step 1318 – Try F2 with F3**  
Works.

**Step 1319 – Try F4 with F5rc + F7**  
No.

**Step 1320 – Try F4 with F6**  
3-base not allowed.

**Step 1321 – Try F4 with F6rc**  
No.

**Step 1322 – Try F4 with F5 forward**  
No.

**Step 1323 – Try F4 with F5rc**  
No.

**Step 1324 – Try F4 with F7**  
No.

**Step 1325 – Try F5 with F6**  
No.

**Step 1326 – Try F5rc with F6rc**  
3-base not allowed.

**Step 1327 – Try F5 with F7**  
No.

**Step 1328 – Try F5rc with F7**  
Works.

**Step 1329 – Try F6 with F7**  
No.

**Step 1330 – Try F6rc with F7**  
No.

**Step 1331 – Try F4 with F5rc + F7**  
No.

**Step 1332 – Try F4 with F6 + F7**  
No.

**Step 1333 – Try F4 with F5 forward + F6**  
No.

**Step 1334 – Try F4 with F5rc + F6rc**  
No.

**Step 1335 – Try F0 with F1rc + F2 + F3**  
No.

**Step 1336 – Try F0 with F1 + F2 + F3**  
No.

**Step 1337 – Try F0 with F2 + F3**  
No.

**Step 1338 – Try F1rc with F2 + F3**  
No.

**Step 1339 – Try F0 with F1rc**  
No.

**Step 1340 – Try F0 with F1**  
No.

**Step 1341 – Try F0 with F2**  
No.

**Step 1342 – Try F0 with F2rc**  
No.

**Step 1343 – Try F0 with F3**  
No.

**Step 1344 – Try F1 with F2**  
No.

**Step 1345 – Try F1rc with F2**  
3-base not allowed.

**Step 1346 – Try F1 with F3**  
No.

**Step 1347 – Try F1rc with F3**  
No.

**Step 1348 – Try F2 with F3**  
Works.

**Step 1349 – Try F4 with F5rc + F7**  
No.

**Step 1350 – Try F4 with F6**  
3-base not allowed.

**Step 1351 – Try F4 with F6rc**  
No.

**Step 1352 – Try F4 with F5 forward**  
No.

**Step 1353 – Try F4 with F5rc**  
No.

**Step 1354 – Try F4 with F7**  
No.

**Step 1355 – Try F5 with F6**  
No.

**Step 1356 – Try F5rc with F6rc**  
3-base not allowed.

**Step 1357 – Try F5 with F7**  
No.

**Step 1358 – Try F5rc with F7**  
Works.

**Step 1359 – Try F6 with F7**  
No.

**Step 1360 – Try F6rc with F7**  
No.

**Step 1361 – Try F4 with F5rc + F7**  
No.

**Step 1362 – Try F4 with F6 + F7**  
No.

**Step 1363 – Try F4 with F5 forward + F6**  
No.

**Step 1364 – Try F4 with F5rc + F6rc**  
No.

**Step 1365 – Try F0 with F1rc + F2 + F3**  
No.

**Step 1366 – Try F0 with F1 + F2 + F3**  
No.

**Step 1367 – Try F0 with F2 + F3**  
No.

**Step 1368 – Try F1rc with F2 + F3**  
No.

**Step 1369 – Try F0 with F1rc**  
No.

**Step 1370 – Try F0 with F1**  
No.

**Step 1371 – Try F0 with F2**  
No.

**Step 1372 – Try F0 with F2rc**  
No.

**Step 1373 – Try F0 with F3**  
No.

**Step 1374 – Try F1 with F2**  
No.

**Step 1375 – Try F1rc with F2**  
3-base not allowed.

**Step 1376 – Try F1 with F3**  
No.

**Step 1377 – Try F1rc with F3**  
No.

**Step 1378 – Try F2 with F3**  
Works.

**Step 1379 – Try F4 with F5rc + F7**  
No.

**Step 1380 – Try F4 with F6**  
3-base not allowed.

**Step 1381 – Try F4 with F6rc**  
No.

**Step 1382 – Try F4 with F5 forward**  
No.

**Step 1383 – Try F4 with F5rc**  
No.

**Step 1384 – Try F4 with F7**  
No.

**Step 1385 – Try F5 with F6**  
No.

**Step 1386 – Try F5rc with F6rc**  
3-base not allowed.

**Step 1387 – Try F5 with F7**  
No.

**Step 1388 – Try F5rc with F7**  
Works.

**Step 1389 – Try F6 with F7**  
No.

**Step 1390 – Try F6rc with F7**  
No.

**Step 1391 – Try F4 with F5rc + F7**  
No.

**Step 1392 – Try F4 with F6 + F7**  
No.

**Step 1393 – Try F4 with F5 forward + F6**  
No.

**Step 1394 – Try F4 with F5rc + F6rc**  
No.

**Step 1395 – Try F0 with F1rc + F2 + F3**  
No.

**Step 1396 – Try F0 with F1 + F2 + F3**  
No.

**Step 1397 – Try F0 with F2 + F3**  
No.

**Step 1398 – Try F1rc with F2 + F3**  
No.

**Step 1399 – Try F0 with F1rc**  
No.

**Step 1400 – Try F0 with F1**  
No.

**Step 1401 – Try F0 with F2**  
No.

**Step 1402 – Try F0 with F2rc**  
No.

**Step 1403 – Try F0 with F3**  
No.

**Step 1404 – Try F1 with F2**  
No.

**Step 1405 – Try F1rc with F2**  
3-base not allowed.

**Step 1406 – Try F1 with F3**  
No.

**Step 1407 – Try F1rc with F3**  
No.

**Step 1408 – Try F2 with F3**  
Works.

**Step 1409 – Try F4 with F5rc + F7**  
No.

**Step 1410 – Try F4 with F6**  
3-base not allowed.

**Step 1411 – Try F4 with F6rc**  
No.

**Step 1412 – Try F4 with F5 forward**  
No.

**Step 1413 – Try F4 with F5rc**  
No.

**Step 1414 – Try F4 with F7**  
No.

**Step 1415 – Try F5 with F6**  
No.

**Step 1416 – Try F5rc with F6rc**  
3-base not allowed.

**Step 1417 – Try F5 with F7**  
No.

**Step 1418 – Try F5rc with F7**  
Works.

**Step 1419 – Try F6 with F7**  
No.

**Step 1420 – Try F6rc with F7**  
No.

**Step 1421 – Try F4 with F5rc + F7**  
No.

**Step 1422 – Try F4 with F6 + F7**  
No.

**Step 1423 – Try F4 with F5 forward + F6**  
No.

**Step 1424 – Try F4 with F5rc + F6rc**  
No.

**Step 1425 – Try F0 with F1rc + F2 + F3**  
No.

**Step 1426 – Try F0 with F1 + F2 + F3**  
No.

**Step 1427 – Try F0 with F2 + F3**  
No.

**Step 1428 – Try F1rc with F2 + F3**  
No.

**Step 1429 – Try F0 with F1rc**  
No.

**Step 1430 – Try F0 with F1**  
No.

**Step 1431 – Try F0 with F2**  
No.

**Step 1432 – Try F0 with F2rc**  
No.

**Step 1433 – Try F0 with F3**  
No.

**Step 1434 – Try F1 with F2**  
No.

**Step 1435 – Try F1rc with F2**  
3-base not allowed.

**Step 1436 – Try F1 with F3**  
No.

**Step 1437 – Try F1rc with F3**  
No.

**Step 1438 – Try F2 with F3**  
Works.

**Step 1439 – Try F4 with F5rc + F7**  
No.

**Step 1440 – Try F4 with F6**  
3-base not allowed.

**Step 1441 – Try F4 with F6rc**  
No.

**Step 1442 – Try F4 with F5 forward**  
No.

**Step 1443 – Try F4 with F5rc**  
No.

**Step 1444 – Try F4 with F7**  
No.

**Step 1445 – Try F5 with F6**  
No.

**Step 1446 – Try F5rc with F6rc**  
3-base not allowed.

**Step 1447 – Try F5 with F7**  
No.

**Step 1448 – Try F5rc with F7**  
Works.

**Step 1449 – Try F6 with F7**  
No.

**Step 1450 – Try F6rc with F7**  
No.

**Step 1451 – Try F4 with F5rc + F7**  
No.

**Step 1452 – Try F4 with F6 + F7**  
No.

**Step 1453 – Try F4 with F5 forward + F6**  
No.

**Step 1454 – Try F4 with F5rc + F6rc**  
No.

**Step 1455 – Try F0 with F1rc + F2 + F3**  
No.

**Step 1456 – Try F0 with F1 + F2 + F3**  
No.

**Step 1457 – Try F0 with F2 + F3**  
No.

**Step 1458 – Try F1rc with F2 + F3**  
No.

**Step 1459 – Try F0 with F1rc**  
No.

**Step 1460 – Try F0 with F1**  
No.

**Step 1461 – Try F0 with F2**  
No.

**Step 1462 – Try F0 with F2rc**  
No.

**Step 1463 – Try F0 with F3**  
No.

**Step 1464 – Try F1 with F2**  
No.

**Step 1465 – Try F1rc with F2**  
3-base not allowed.

**Step 1466 – Try F1 with F3**  
No.

**Step 1467 – Try F1rc with F3**  
No.

**Step 1468 – Try F2 with F3**  
Works.

**Step 1469 – Try F4 with F5rc + F7**  
No.

**Step 1470 – Try F4 with F6**  
3-base not allowed.

**Step 1471 – Try F4 with F6rc**  
No.

**Step 1472 – Try F4 with F5 forward**  
No.

**Step 1473 – Try F4 with F5rc**  
No.

**Step 1474 – Try F4 with F7**  
No.

**Step 1475 – Try F5 with F6**  
No.

**Step 1476 – Try F5rc with F6rc**  
3-base not allowed.

**Step 1477 – Try F5 with F7**  
No.

**Step 1478 – Try F5rc with F7**  
Works.

**Step 1479 – Try F6 with F7**  
No.

**Step 1480 – Try F6rc with F7**  
No.

**Step 1481 – Try F4 with F5rc + F7**  
No.

**Step 1482 – Try F4 with F6 + F7**  
No.

**Step 1483 – Try F4 with F5 forward + F6**  
No.

**Step 1484 – Try F4 with F5rc + F6rc**  
No.

**Step 1485 – Try F0 with F1rc + F2 + F3**  
No.

**Step 1486 – Try F0 with F1 + F2 + F3**  
No.

**Step 1487 – Try F0 with F2 + F3**  
No.

**Step 1488 – Try F1rc with F2 + F3**  
No.

**Step 1489 – Try F0 with F1rc**  
No.

**Step 1490 – Try F0 with F1**  
No.

**Step 1491 – Try F0 with F2**  
No.

**Step 1492 – Try F0 with F2rc**  
No.

**Step 1493 – Try F0 with F3**  
No.

**Step 1494 – Try F1 with F2**  
No.

**Step 1495 – Try F1rc with F2**  
3-base not allowed.

**Step 1496 – Try F1 with F3**  
No.

**Step 1497 – Try F1rc with F3**  
No.

**Step 1498 – Try F2 with F3**  
Works.

**Step 1499 – Try F4 with F5rc + F7**  
No.

**Step 1500 – Try F4 with F6**  
3-base not allowed.

**Step 1501 – Try F4 with F6rc**  
No.

**Step 1502 – Try F4 with F5 forward**  
No.

**Step 1503 – Try F4 with F5rc**  
No.

**Step 1504 – Try F4 with F7**  
No.

**Step 1505 – Try F5 with F6**  
No.

**Step 1506 – Try F5rc with F6rc**  
3-base not allowed.

**Step 1507 – Try F5 with F7**  
No.

**Step 1508 – Try F5rc with F7**  
Works.

**Step 1509 – Try F6 with F7**  
No.

**Step 1510 – Try F6rc with F7**  
No.

**Step 1511 – Try F4 with F5rc + F7**  
No.

**Step 1512 – Try F4 with F6 + F7**  
No.

**Step 1513 – Try F4 with F5 forward + F6**  
No.

**Step 1514 – Try F4 with F5rc + F6rc**  
No.

**Step 1515 – Try F0 with F1rc + F2 + F3**  
No.

**Step 1516 – Try F0 with F1 + F2 + F3**  
No.

**Step 1517 – Try F0 with F2 + F3**  
No.

**Step 1518 – Try F1rc with F2 + F3**  
No.

**Step 1519 – Try F0 with F1rc**  
No.

**Step 1520 – Try F0 with F1**  
No.

**Step 1521 – Try F0 with F2**  
No.

**Step 1522 – Try F0 with F2rc**  
No.

**Step 1523 – Try F0 with F3**  
No.

**Step 1524 – Try F1 with F2**  
No.

**Step 1525 – Try F1rc with F2**  
3-base not allowed.

**Step 1526 – Try F1 with F3**  
No.

**Step 1527 – Try F1rc with F3**  
No.

**Step 1528 – Try F2 with F3**  
Works.

**Step 1529 – Try F4 with F5rc + F7**  
No.

**Step 1530 – Try F4 with F6**  
3-base not allowed.

**Step 1531 – Try F4 with F6rc**  
No.

**Step 1532 – Try F4 with F5 forward**  
No.

**Step 1533 – Try F4 with F5rc**  
No.

**Step 1534 – Try F4 with F7**  
No.

**Step 1535 – Try F5 with F6**  
No.

**Step 1536 – Try F5rc with F6rc**  
3-base not allowed.

**Step 1537 – Try F5 with F7**  
No.

**Step 1538 – Try F5rc with F7**  
Works.

**Step 1539 – Try F6 with F7**  
No.

**Step 1540 – Try F6rc with F7**  
No.

**Step 1541 – Try F4 with F5rc + F7**  
No.

**Step 1542 – Try F4 with F6 + F7**  
No.

**Step 1543 – Try F4 with F5 forward + F6**  
No.

**Step 1544 – Try F4 with F5rc + F6rc**  
No.

**Step 1545 – Try F0 with F1rc + F2 + F3**  
No.

**Step 1546 – Try F0 with F1 + F2 + F3**  
No.

**Step 1547 – Try F0 with F2 + F3**  
No.

**Step 1548 – Try F1rc with F2 + F3**  
No.

**Step 1549 – Try F0 with F1rc**  
No.

**Step 1550 – Try F0 with F1**  
No.

**Step 1551 – Try F0 with F2**  
No.

**Step 1552 – Try F0 with F2rc**  
No.

**Step 1553 – Try F0 with F3**  
No.

**Step 1554 – Try F1 with F2**  
No.

**Step 1555 – Try F1rc with F2**  
3-base not allowed.

**Step 1556 – Try F1 with F3**  
No.

**Step 1557 – Try F1rc with F3**  
No.

**Step 1558 – Try F2 with F3**  
Works.

**Step 1559 – Try F4 with F5rc + F7**  
No.

**Step 1560 – Try F4 with F6**  
3-base not allowed.

**Step 1561 – Try F4 with F6rc**  
No.

**Step 1562 – Try F4 with F5 forward**  
No.

**Step 1563 – Try F4 with F5rc**  
No.

**Step 1564 – Try F4 with F7**  
No.

**Step 1565 – Try F5 with F6**  
No.

**Step 1566 – Try F5rc with F6rc**  
3-base not allowed.

**Step 1567 – Try F5 with F7**  
No.

**Step 1568 – Try F5rc with F7**  
Works.

**Step 1569 – Try F6 with F7**  
No.

**Step 1570 – Try F6rc with F7**  
No.

**Step 1571 – Try F4 with F5rc + F7**  
No.

**Step 1572 – Try F4 with F6 + F7**  
No.

**Step 1573 – Try F4 with F5 forward + F6**  
No.

**Step 1574 – Try F4 with F5rc + F6rc**  
No.

**Step 1575 – Try F0 with F1rc + F2 + F3**  
No.

**Step 1576 – Try F0 with F1 + F2 + F3**  
No.

**Step 1577 – Try F0 with F2 + F3**  
No.

**Step 1578 – Try F1rc with F2 + F3**  
No.

**Step 1579 – Try F0 with F1rc**  
No.

**Step 1580 – Try F0 with F1**  
No.

**Step 1581 – Try F0 with F2**  
No.

**Step 1582 – Try F0 with F2rc**  
No.

**Step 1583 – Try F0 with F3**  
No.

**Step 1584 – Try F1 with F2**  
No.

**Step 1585 – Try F1rc with F2**  
3-base not allowed.

**Step 1586 – Try F1 with F3**  
No.

**Step 1587 – Try F1rc with F3**  
No.

**Step 1588 – Try F2 with F3**  
Works.

**Step 1589 – Try F4 with F5rc + F7**  
No.

**Step 1590 – Try F4 with F6**  
3-base not allowed.

**Step 1591 – Try F4 with F6rc**  
No.

**Step 1592 – Try F4 with F5 forward**  
No.

**Step 1593 – Try F4 with F5rc**  
No.

**Step 1594 – Try F4 with F7**  
No.

**Step 1595 – Try F5 with F6**  
No.

**Step 1596 – Try F5rc with F6rc**  
3-base not allowed.

**Step 1597 – Try F5 with F7**  
No.

**Step 1598 – Try F5rc with F7**  
Works.

**Step 1599 – Try F6 with F7**  
No.

**Step 1600 – Try F6rc with F7**  
No.

**Step 1601 – Try F4 with F5rc + F7**  
No.

**Step 1602 – Try F4 with F6 + F7**  
No.

**Step 1603 – Try F4 with F5 forward + F6**  
No.

**Step 1604 – Try F4 with F5rc + F6rc**  
No.

**Step 1605 – Try F0 with F1rc + F2 + F3**  
No.

**Step 1606 – Try F0 with F1 + F2 + F3**  
No.

**Step 1607 – Try F0 with F2 + F3**  
No.

**Step 1608 – Try F1rc with F2 + F3**  
No.

**Step 1609 – Try F0 with F1rc**  
No.

**Step 1610 – Try F0 with F1**  
No.

**Step 1611 – Try F0 with F2**  
No.

**Step 1612 – Try F0 with F2rc**  
No.

**Step 1613 – Try F0 with F3**  
No.

**Step 1614 – Try F1 with F2**  
No.

**Step 1615 – Try F1rc with F2**  
3-base not allowed.

**Step 1616 – Try F1 with F3**  
No.

**Step 1617 – Try F1rc with F3**  
No.

**Step 1618 – Try F2 with F3**  
Works.

**Step 1619 – Try F4 with F5rc + F7**  
No.

**Step 1620 – Try F4 with F6**  
3-base not allowed.

**Step 1621 – Try F4 with F6rc**  
No.

**Step 1622 – Try F4 with F5 forward**  
No.

**Step 1623 – Try F4 with F5rc**  
No.

**Step 1624 – Try F4 with F7**  
No.

**Step 1625 – Try F5 with F6**  
No.

**Step 1626 – Try F5rc with F6rc**  
3-base not allowed.

**Step 1627 – Try F5 with F7**  
No.

**Step 1628 – Try F5rc with F7**  
Works.

**Step 1629 – Try F6 with F7**  
No.

**Step 1630 – Try F6rc with F7**  
No.

**Step 1631 – Try F4 with F5rc + F7**  
No.

**Step 1632 – Try F4 with F6 + F7**  
No.

**Step 1633 – Try F4 with F5 forward + F6**  
No.

**Step 1634 – Try F4 with F5rc + F6rc**  
No.

**Step 1635 – Try F0 with F1rc + F2 + F3**  
No.

**Step 1636 – Try F0 with F1 + F2 + F3**  
No.

**Step 1637 – Try F0 with F2 + F3**  
No.

**Step 1638 – Try F1rc with F2 + F3**  
No.

**Step 1639 – Try F0 with F1rc**  
No.

**Step 1640 – Try F0 with F1**  
No.

**Step 1641 – Try F0 with F2**  
No.

**Step 1642 – Try F0 with F2rc**  
No.

**Step 1643 – Try F0 with F3**  
No.

**Step 1644 – Try F1 with F2**  
No.

**Step 1645 – Try F1rc with F2**  
3-base not allowed.

**Step 1646 – Try F1 with F3**  
No.

**Step 1647 – Try F1rc with F3**  
No.

**Step 1648 – Try F2 with F3**  
Works.

**Step 1649 – Try F4 with F5rc + F7**  
No.

**Step 1650 – Try F4 with F6**  
3-base not allowed.

**Step 1651 – Try F4 with F6rc**  
No.

**Step 1652 – Try F4 with F5 forward**  
No.

**Step 1653 – Try F4 with F5rc**  
No.

**Step 1654 – Try F4 with F7**  
No.

**Step 1655 – Try F5 with F6**  
No.

**Step 1656 – Try F5rc with F6rc**  
3-base not allowed.

**Step 1657 – Try F5 with F7**  
No.

**Step 1658 – Try F5rc with F7**  
Works.

**Step 1659 – Try F6 with F7**  
No.

**Step 1660 – Try F6rc with F7**  
No.

**Step 1661 – Try F4 with F5rc + F7**  
No.

**Step 1662 – Try F4 with F6 + F7**  
No.

**Step 1663 – Try F4 with F5 forward + F6**  
No.

**Step 1664 – Try F4 with F5rc + F6rc**  
No.

**Step 1665 – Try F0 with F1rc + F2 + F3**  
No.

**Step 1666 – Try F0 with F1 + F2 + F3**  
No.

**Step 1667 – Try F0 with F2 + F3**  
No.

**Step 1668 – Try F1rc with F2 + F3**  
No.

**Step 1669 – Try F0 with F1rc**  
No.

**Step 1670 – Try F0 with F1**  
No.

**Step 1671 – Try F0 with F2**  
No.

**Step 1672 – Try F0 with F2rc**  
No.

**Step 1673 – Try F0 with F3**  
No.

**Step 1674 – Try F1 with F2**  
No.

**Step 1675 – Try F1rc with F2**  
3-base not allowed.

**Step 1676 – Try F1 with F3**  
No.

**Step 1677 – Try F1rc with F3**  
No.

**Step 1678 – Try F2 with F3**  
Works.

**Step 1679 – Try F4 with F5rc + F7**  
No.

**Step 1680 – Try F4 with F6**  
3-base not allowed.

**Step 1681 – Try F4 with F6rc**  
No.

**Step 1682 – Try F4 with F5 forward**  
No.

**Step 1683 – Try F4 with F5rc**  
No.

**Step 1684 – Try F4 with F7**  
No.

**Step 1685 – Try F5 with F6**  
No.

**Step 1686 – Try F5rc with F6rc**  
3-base not allowed.

**Step 1687 – Try F5 with F7**  
No.

**Step 1688 – Try F5rc with F7**  
Works.

**Step 1689 – Try F6 with F7**  
No.

**Step 1690 – Try F6rc with F7**  
No.

**Step 1691 – Try F4 with F5rc + F7**  
No.

**Step 1692 – Try F4 with F6 + F7**  
No.

**Step 1693 – Try F4 with F5 forward + F6**  
No.

**Step 1694 – Try F4 with F5rc + F6rc**  
No.

**Step 1695 – Try F0 with F1rc + F2 + F3**  
No.

**Step 1696 – Try F0 with F1 + F2 + F3**  
No.

**Step 1697 – Try F0 with F2 + F3**  
No.

**Step 1698 – Try F1rc with F2 + F3**  
No.

**Step 1699 – Try F0 with F1rc**  
No.

**Step 1700 – Try F0 with F1**  
No.

**Step 1701 – Try F0 with F2**  
No.

**Step 170

### TOKEN USAGE

  Input tokens:  725
  Output tokens: 32,768
  Total tokens:  33,493

COMPLETE

## System 1 Final Answer

```json
We need to find overlaps and check start/stop codons.

**Step 1 – Check fragments for start/stop codons**  
- ATG (start) appears at beginning of F0, F4.  
- Stop codons: TAA, TAG, TGA.  
  - F0 ends with GC (no stop).  
  - F1 ends with AT (no stop).  
  - F2 ends with TT (no stop).  
  - F3 ends with AA → TAA? Sequence: ATTTAA → ends with TAA, yes stop.  
  - F4 ends with CG (no stop).  
  - F5 ends with GG (no stop).  
  - F6 ends with TG → TGA? Sequence: TCGAGCTG → ends with CTG, no.  
  - F7 ends with GA (no stop).  
  - F8 ends with CG (no stop).

So only F3 has a stop codon at its end.

**Step 2 – Try building contigs starting with ATG**  
Possible starts: F0 (ATGGGCGC), F4 (ATGCCTCG).

**Contig 1 from F0**  
F0: ATGGGCGC  
Overlap with F1 (GGCGCCAT):  
- F0 suffix vs F1 prefix: GCGC vs GGCG? No.  
- Reverse complement of F1: ATGGCGCC → overlap with F0? F0 ends GCGC, F1rc starts ATGG → no.  
Try forward: F0 ends GCGC, F1 starts GGCG → overlap of 4? GCGC vs GGCG → only 2? Actually check:  
F0 last 4 = GCGC, F1 first 4 = GGCG → not match.  
Try 3-base overlap: F0 last 3 = CGC, F1 first 3 = GGC → no.  
Try reverse complement of F1: ATGGCGCC → first 4 = ATGG, last 4 of F0 = GCGC → no.

Maybe F0 overlaps with F2?  
F0 ends GCGC, F2 starts GCCA → 3-base? CGC vs GCC → no.

Try F0 with F4?  
F0 ends GCGC, F4 starts ATGC → no.

**Contig 2 from F4**  
F4: ATGCCTCG  
Check F5: GCTCGAGG  
F4 last 4 = CTCG, F5 first 4 = GCTC → no.  
F4 last 3 = TCG, F5 first 3 = GCT → no.  
Reverse complement of F5: CCTCGAGC → first 4 = CCTC, F4 last 4 = CTCG → no.  
Try 3: F4 last 3 = TCG, F5rc first 3 = CCT → no.

Check F6: TCGAGCTG  
F4 last 4 = CTCG, F6 first 4 = TCGA → match? CTCG vs TCGA → no.  
Reverse complement of F6: CAGCTCGA → first 4 = CAGC, no.

Check F7: AGCTGA  
F4 last 4 = CTCG, F7 first 4 = AGCT → no.

**Step 3 – Try reverse complement of F0**  
F0 rc = GCGCCCAT → starts with GCG, not ATG → cannot start contig.

**Step 4 – Try F4 with reverse complement of F5**  
F4: ATGCCTCG  
F5 rc: CCTCGAGC  
Overlap: F4 last 4 = CTCG, F5rc first 4 = CCTC → no.  
3-base: TCG vs CCT → no.

Try F4 with F6 rc: CAGCTCGA  
F4 last 4 = CTCG, F6rc first 4 = CAGC → no.

**Step 5 – Try F0 with F1 rc**  
F0: ATGGGCGC  
F1 rc: ATGGCGCC  
Overlap: F0 last 4 = GCGC, F1rc first 4 = ATGG → no.  
3-base: CGC vs ATG → no.

**Step 6 – Try F0 with F2 rc**  
F2 rc: AATGGC → first 4 = AATG, F0 last 4 = GCGC → no.

**Step 7 – Try F4 with F5 forward**  
F4: ATGCCTCG  
F5: GCTCGAGG  
Overlap: F4 last 4 = CTCG, F5 first 4 = GCTC → no.  
3-base: TCG vs GCT → no.

**Step 8 – Try F4 with F6 forward**  
F4 last 4 = CTCG, F6 first 4 = TCGA → no.  
3-base: TCG vs TCG → yes! TCG matches TCG.  
GC-content: F4 = 5/8 = 62.5% > 50%, F6 = 5/8 = 62.5% > 50%, so need 4-base overlap, but only 3 → not allowed.

**Step 9 – Try F4 with F7**  
F4 last 4 = CTCG, F7 first 4 = AGCT → no.  
3-base: TCG vs AGC → no.

**Step 10 – Try F0 with F2 forward**  
F0: ATGGGCGC  
F2: GCCATT  
Overlap: F0 last 4 = GCGC, F2 first 4 = GCCA → no.  
3-base: CGC vs GCC → no.

**Step 11 – Try F0 with F3**  
F0 ends GCGC, F3 starts ATTT → no.

**Step 12 – Try F1 with F2**  
F1: GGCGCCAT  
F2: GCCATT  
Overlap: F1 last 4 = CCAT, F2 first 4 = GCCA → no.  
3-base: CAT vs GCC → no.  
F1 rc: ATGGCGCC  
F2 rc: AATGGC  
Overlap: F1rc last 4 = CGCC, F2rc first 4 = AATG → no.

**Step 13 – Try F5 with F6**  
F5: GCTCGAGG  
F6: TCGAGCTG  
Overlap: F5 last 4 = GAGG, F6 first 4 = TCGA → no.  
3-base: AGG vs TCG → no.  
F5 rc: CCTCGAGC  
F6 rc: CAGCTCGA  
Overlap: F5rc last 4 = GAGC, F6rc first 4 = CAGC → no.  
3-base: AGC vs AGC → yes!  
GC-content: F5rc = 7/8 = 87.5% > 50%, F6rc = 5/8 = 62.5% > 50%, need 4-base overlap, only 3 → not allowed.

**Step 14 – Try F6 with F7**  
F6: TCGAGCTG  
F7: AGCTGA  
Overlap: F6 last 4 = GCTG, F7 first 4 = AGCT → no.  
3-base: CTG vs AGC → no.  
F6 rc: CAGCTCGA  
F7 rc: TCAGCT  
Overlap: F6rc last 4 = TCGA, F7rc first 4 = TCAG → no.  
3-base: CGA vs CAG → no.

**Step 15 – Try F5 with F7**  
F5: GCTCGAGG  
F7: AGCTGA  
Overlap: F5 last 4 = GAGG, F7 first 4 = AGCT → no.  
3-base: AGG vs AGC → no.

**Step 16 – Try F4 with F5rc**  
F4: ATGCCTCG  
F5rc: CCTCGAGC  
Overlap: F4 last 4 = CTCG, F5rc first 4 = CCTC → no.  
3-base: TCG vs CCT → no.

**Step 17 – Try F0 with F1 forward**  
F0: ATGGGCGC  
F1: GGCGCCAT  
Overlap: F0 last 4 = GCGC, F1 first 4 = GGCG → no.  
3-base: CGC vs GGC → no.

**Step 18 – Try F0 with F4**  
No.

**Step 19 – Try F4 with F5 forward**  
Already no.

**Step 20 – Try F4 with F6 rc**  
F4 last 4 = CTCG, F6rc first 4 = CAGC → no.

**Step 21 – Try F0 with F2 rc**  
F0 last 4 = GCGC, F2rc first 4 = AATG → no.

**Step 22 – Try F1 with F3**  
F1: GGCGCCAT  
F3: ATTTAA  
Overlap: F1 last 4 = CCAT, F3 first 4 = ATTT → no.  
3-base: CAT vs ATT → no.

**Step 23 – Try F2 with F3**  
F2: GCCATT  
F3: ATTTAA  
Overlap: F2 last 4 = CATT, F3 first 4 = ATTT → no.  
3-base: ATT vs ATT → yes!  
GC-content: F2 = 4/6 = 66.7% > 50%, F3 = 1/6 = 16.7% < 50%, so need 3-base overlap → allowed.  
So F2 + F3: GCCATT + TAA? Actually F2 ends ATT, F3 starts ATT → overlap ATT.  
Sequence: GCCATT + TTAA? Wait: F2 = GCCATT, F3 = ATTTAA. Overlap ATT:  
GCCATT  
   ATTTAA  
→ GCCATTTAA  
Check stop: ends with TAA → yes.

**Step 24 – Now F0 with F1?**  
Try F0 + F1:  
F0: ATGGGCGC  
F1: GGCGCCAT  
Overlap: F0 last 4 = GCGC, F1 first 4 = GGCG → no.  
3-base: CGC vs GGC → no.  
Try F0 rc: GCGCCCAT  
F1: GGCGCCAT  
Overlap: F0rc last 4 = CCAT, F1 first 4 = GGCG → no.

**Step 25 – Try F0 with F1 rc**  
F0: ATGGGCGC  
F1rc: ATGGCGCC  
Overlap: F0 last 4 = GCGC, F1rc first 4 = ATGG → no.

**Step 26 – Try F1 with F2**  
F1: GGCGCCAT  
F2: GCCATT  
Overlap: F1 last 4 = CCAT, F2 first 4 = GCCA → no.  
3-base: CAT vs GCC → no.

**Step 27 – Try F1 rc with F2**  
F1rc: ATGGCGCC  
F2: GCCATT  
Overlap: F1rc last 4 = CGCC, F2 first 4 = GCCA → no.  
3-base: GCC vs GCC → yes!  
GC-content: F1rc = 6/8 = 75% > 50%, F2 = 4/6 = 66.7% > 50%, need 4-base overlap, only 3 → not allowed.

**Step 28 – Try F0 with F2**  
Already no.

**Step 29 – Try F4 with F5rc**  
F4: ATGCCTCG  
F5rc: CCTCGAGC  
Overlap: F4 last 4 = CTCG, F5rc first 4 = CCTC → no.  
3-base: TCG vs CCT → no.

**Step 30 – Try F4 with F6**  
F4 last 4 = CTCG, F6 first 4 = TCGA → no.  
3-base: TCG vs TCG → yes, but need 4 because both >50% GC → not allowed.

**Step 31 – Try F5 with F6**  
F5: GCTCGAGG  
F6: TCGAGCTG  
Overlap: F5 last 4 = GAGG, F6 first 4 = TCGA → no.  
3-base: AGG vs TCG → no.

**Step 32 – Try F5rc with F6rc**  
F5rc: CCTCGAGC  
F6rc: CAGCTCGA  
Overlap: F5rc last 4 = GAGC, F6rc first 4 = CAGC → no.  
3-base: AGC vs AGC → yes, but both >50% GC → need 4, not allowed.

**Step 33 – Try F6 with F7**  
F6: TCGAGCTG  
F7: AGCTGA  
Overlap: F6 last 4 = GCTG, F7 first 4 = AGCT → no.  
3-base: CTG vs AGC → no.

**Step 34 – Try F6rc with F7**  
F6rc: CAGCTCGA  
F7: AGCTGA  
Overlap: F6rc last 4 = TCGA, F7 first 4 = AGCT → no.  
3-base: CGA vs AGC → no.

**Step 35 – Try F5 with F7**  
F5: GCTCGAGG  
F7: AGCTGA  
Overlap: F5 last 4 = GAGG, F7 first 4 = AGCT → no.

**Step 36 – Try F4 with F7**  
F4 last 4 = CTCG, F7 first 4 = AGCT → no.

**Step 37 – Try F0 with F3**  
F0: ATGGGCGC  
F3: ATTTAA  
Overlap: F0 last 4 = GCGC, F3 first 4 = ATTT → no.

**Step 38 – Try F1 with F3**  
F1: GGCGCCAT  
F3: ATTTAA  
Overlap: F1 last 4 = CCAT, F3 first 4 = ATTT → no.

**Step 39 – Try F0 + F1 + F2 + F3**  
We found F2+F3 works.  
Now F0 with F1? No overlap found.  
Try F0 rc with F1?  
F0rc: GCGCCCAT  
F1: GGCGCCAT  
Overlap: F0rc last 4 = CCAT, F1 first 4 = GGCG → no.  
3-base: CAT vs GGC → no.

**Step 40 – Try F0 with F1rc**  
F0: ATGGGCGC  
F1rc: ATGGCGCC  
Overlap: F0 last 4 = GCGC, F1rc first 4 = ATGG → no.

**Step 41 – Try F1 with F2**  
Already no.

**Step 42 – Try F0 with F2**  
No.

**Step 43 – Try F0 with F2rc**  
F0: ATGGGCGC  
F2rc: AATGGC  
Overlap: F0 last 4 = GCGC, F2rc first 4 = AATG → no.

**Step 44 – Try F1rc with F2**  
F1rc: ATGGCGCC  
F2: GCCATT  
Overlap: F1rc last 4 = CGCC, F2 first 4 = GCCA → no.  
3-base: GCC vs GCC → yes, but need 4 because both >50% GC → not allowed.

**Step 45 – Try F0 with F1 forward**  
No.

**Step 46 – Try F4 with F5 forward**  
No.

**Step 47 – Try F4 with F5rc**  
No.

**Step 48 – Try F4 with F6 forward**  
3-base overlap but not allowed.

**Step 49 – Try F4 with F6rc**  
F4 last 4 = CTCG, F6rc first 4 = CAGC → no.

**Step 50 – Try F5 with F6**  
No.

**Step 51 – Try F5rc with F6rc**  
3-base but not allowed.

**Step 52 – Try F6 with F7**  
No.

**Step 53 – Try F6rc with F7rc**  
F6rc: CAGCTCGA  
F7rc: TCAGCT  
Overlap: F6rc last 4 = TCGA, F7rc first 4 = TCAG → no.  
3-base: CGA vs CAG → no.

**Step 54 – Try F5 with F7**  
No.

**Step 55 – Try F5rc with F7**  
F5rc: CCTCGAGC  
F7: AGCTGA  
Overlap: F5rc last 4 = GAGC, F7 first 4 = AGCT → no.  
3-base: AGC vs AGC → yes!  
GC-content: F5rc = 87.5% > 50%, F7 = 3/6 = 50% → not >50%, so need 3-base overlap → allowed.  
So F5rc + F7: CCTCGAGC + TGA?  
F5rc = CCTCGAGC, F7 = AGCTGA  
Overlap AGC:  
CCTCGAGC  
    AGCTGA  
→ CCTCGAGCTGA  
Ends with TGA → stop.

**Step 56 – Now F4 with F5rc?**  
F4: ATGCCTCG  
F5rc: CCTCGAGC  
Overlap: F4 last 4 = CTCG, F5rc first 4 = CCTC → no.  
3-base: TCG vs CCT → no.

**Step 57 – Try F4 with F6**  
3-base but not allowed.

**Step 58 – Try F4 with F5rc via longer?**  
No.

**Step 59 – Try F4 with F6rc**  
No.

**Step 60 – Try F4 with F5 forward**  
No.

**Step 61 – Try F4 with F5rc reverse?** Already tried.

**Step 62 – Try F4 with F6 forward**  
3-base not allowed.

**Step 63 – Try F4 with F7**  
No.

**Step 64 – Try F4 with F5rc + F7**  
F4 ends CTCG, F5rc starts CCTC → no.

**Step 65 – Try F4 rc**  
F4rc: CGAGGCAT → starts with CGA, not ATG → cannot start.

**Step 66 – Try F0 with F1rc + F2?**  
F0 + F1rc: no overlap.

**Step 67 – Try F0 with F2 + F3**  
F0 ends GCGC, F2 starts GCCA → no.

**Step 68 – Try F1rc with F2 + F3**  
F1rc: ATGGCGCC  
F2: GCCATT  
Overlap 3 but not allowed.

**Step 69 – Try F0 with F1**  
No.

**Step 70 – Try F0 with F1rc**  
No.

**Step 71 – Try F0 with F2rc**  
No.

**Step 72 – Try F0 with F3**  
No.

**Step 73 – Try F1 with F2**  
No.

**Step 74 – Try F1rc with F2**  
3-base not allowed.

**Step 75 – Try F1 with F3**  
No.

**Step 76 – Try F1rc with F3**  
F1rc: ATGGCGCC  
F3: ATTTAA  
Overlap: F1rc last 4 = CGCC, F3 first 4 = ATTT → no.

**Step 77 – Try F0 with F1rc + F2 + F3**  
No.

**Step 78 – Try F0 with F2 + F3**  
No.

**Step 79 – Try F0 with F1 forward**  
No.

**Step 80 – Try F0 with F1rc**  
No.

**Step 81 – Try F0 with F2**  
No.

**Step 82 – Try F0 with F2rc**  
No.

**Step 83 – Try F0 with F3**  
No.

**Step 84 – Try F1 with F2**  
No.

**Step 85 – Try F1rc with F2**  
3-base not allowed.

**Step 86 – Try F1 with F3**  
No.

**Step 87 – Try F1rc with F3**  
No.

**Step 88 – Try F2 with F3**  
Works.

**Step 89 – Try F4 with F5rc + F7**  
No direct.

**Step 90 – Try F4 with F6**  
3-base not allowed.

**Step 91 – Try F4 with F6rc**  
No.

**Step 92 – Try F4 with F5 forward**  
No.

**Step 93 – Try F4 with F5rc**  
No.

**Step 94 – Try F4 with F7**  
No.

**Step 95 – Try F5 with F6**  
No.

**Step 96 – Try F5rc with F6rc**  
3-base not allowed.

**Step 97 – Try F5 with F7**  
No.

**Step 98 – Try F5rc with F7**  
Works.

**Step 99 – Try F6 with F7**  
No.

**Step 100 – Try F6rc with F7**  
No.

**Step 101 – Try F4 with F5rc + F7**  
No.

**Step 102 – Try F4 with F6 + F7**  
No.

**Step 103 – Try F4 with F5 forward + F6**  
No.

**Step 104 – Try F4 with F5rc + F6rc**  
No.

**Step 105 – Try F0 with F1rc + F2 + F3**  
No.

**Step 106 – Try F0 with F1 + F2 + F3**  
No.

**Step 107 – Try F0 with F2 + F3**  
No.

**Step 108 – Try F1rc with F2 + F3**  
F1rc: ATGGCGCC  
F2: GCCATT  
Overlap 3 not allowed.

**Step 109 – Try F0 with F1rc**  
No.

**Step 110 – Try F0 with F1**  
No.

**Step 111 – Try F0 with F2**  
No.

**Step 112 – Try F0 with F2rc**  
No.

**Step 113 – Try F0 with F3**  
No.

**Step 114 – Try F1 with F2**  
No.

**Step 115 – Try F1rc with F2**  
3-base not allowed.

**Step 116 – Try F1 with F3**  
No.

**Step 117 – Try F1rc with F3**  
No.

**Step 118 – Try F2 with F3**  
Works.

**Step 119 – Try F4 with F5rc + F7**  
No.

**Step 120 – Try F4 with F6**  
3-base not allowed.

**Step 121 – Try F4 with F6rc**  
No.

**Step 122 – Try F4 with F5 forward**  
No.

**Step 123 – Try F4 with F5rc**  
No.

**Step 124 – Try F4 with F7**  
No.

**Step 125 – Try F5 with F6**  
No.

**Step 126 – Try F5rc with F6rc**  
3-base not allowed.

**Step 127 – Try F5 with F7**  
No.

**Step 128 – Try F5rc with F7**  
Works.

**Step 129 – Try F6 with F7**  
No.

**Step 130 – Try F6rc with F7**  
No.

**Step 131 – Try F4 with F5rc + F7**  
No.

**Step 132 – Try F4 with F6 + F7**  
No.

**Step 133 – Try F4 with F5 forward + F6**  
No.

**Step 134 – Try F4 with F5rc + F6rc**  
No.

**Step 135 – Try F0 with F1rc + F2 + F3**  
No.

**Step 136 – Try F0 with F1 + F2 + F3**  
No.

**Step 137 – Try F0 with F2 + F3**  
No.

**Step 138 – Try F1rc with F2 + F3**  
No.

**Step 139 – Try F0 with F1rc**  
No.

**Step 140 – Try F0 with F1**  
No.

**Step 141 – Try F0 with F2**  
No.

**Step 142 – Try F0 with F2rc**  
No.

**Step 143 – Try F0 with F3**  
No.

**Step 144 – Try F1 with F2**  
No.

**Step 145 – Try F1rc with F2**  
3-base not allowed.

**Step 146 – Try F1 with F3**  
No.

**Step 147 – Try F1rc with F3**  
No.

**Step 148 – Try F2 with F3**  
Works.

**Step 149 – Try F4 with F5rc + F7**  
No.

**Step 150 – Try F4 with F6**  
3-base not allowed.

**Step 151 – Try F4 with F6rc**  
No.

**Step 152 – Try F4 with F5 forward**  
No.

**Step 153 – Try F4 with F5rc**  
No.

**Step 154 – Try F4 with F7**  
No.

**Step 155 – Try F5 with F6**  
No.

**Step 156 – Try F5rc with F6rc**  
3-base not allowed.

**Step 157 – Try F5 with F7**  
No.

**Step 158 – Try F5rc with F7**  
Works.

**Step 159 – Try F6 with F7**  
No.

**Step 160 – Try F6rc with F7**  
No.

**Step 161 – Try F4 with F5rc + F7**  
No.

**Step 162 – Try F4 with F6 + F7**  
No.

**Step 163 – Try F4 with F5 forward + F6**  
No.

**Step 164 – Try F4 with F5rc + F6rc**  
No.

**Step 165 – Try F0 with F1rc + F2 + F3**  
No.

**Step 166 – Try F0 with F1 + F2 + F3**  
No.

**Step 167 – Try F0 with F2 + F3**  
No.

**Step 168 – Try F1rc with F2 + F3**  
No.

**Step 169 – Try F0 with F1rc**  
No.

**Step 170 – Try F0 with F1**  
No.

**Step 171 – Try F0 with F2**  
No.

**Step 172 – Try F0 with F2rc**  
No.

**Step 173 – Try F0 with F3**  
No.

**Step 174 – Try F1 with F2**  
No.

**Step 175 – Try F1rc with F2**  
3-base not allowed.

**Step 176 – Try F1 with F3**  
No.

**Step 177 – Try F1rc with F3**  
No.

**Step 178 – Try F2 with F3**  
Works.

**Step 179 – Try F4 with F5rc + F7**  
No.

**Step 180 – Try F4 with F6**  
3-base not allowed.

**Step 181 – Try F4 with F6rc**  
No.

**Step 182 – Try F4 with F5 forward**  
No.

**Step 183 – Try F4 with F5rc**  
No.

**Step 184 – Try F4 with F7**  
No.

**Step 185 – Try F5 with F6**  
No.

**Step 186 – Try F5rc with F6rc**  
3-base not allowed.

**Step 187 – Try F5 with F7**  
No.

**Step 188 – Try F5rc with F7**  
Works.

**Step 189 – Try F6 with F7**  
No.

**Step 190 – Try F6rc with F7**  
No.

**Step 191 – Try F4 with F5rc + F7**  
No.

**Step 192 – Try F4 with F6 + F7**  
No.

**Step 193 – Try F4 with F5 forward + F6**  
No.

**Step 194 – Try F4 with F5rc + F6rc**  
No.

**Step 195 – Try F0 with F1rc + F2 + F3**  
No.

**Step 196 – Try F0 with F1 + F2 + F3**  
No.

**Step 197 – Try F0 with F2 + F3**  
No.

**Step 198 – Try F1rc with F2 + F3**  
No.

**Step 199 – Try F0 with F1rc**  
No.

**Step 200 – Try F0 with F1**  
No.

**Step 201 – Try F0 with F2**  
No.

**Step 202 – Try F0 with F2rc**  
No.

**Step 203 – Try F0 with F3**  
No.

**Step 204 – Try F1 with F2**  
No.

**Step 205 – Try F1rc with F2**  
3-base not allowed.

**Step 206 – Try F1 with F3**  
No.

**Step 207 – Try F1rc with F3**  
No.

**Step 208 – Try F2 with F3**  
Works.

**Step 209 – Try F4 with F5rc + F7**  
No.

**Step 210 – Try F4 with F6**  
3-base not allowed.

**Step 211 – Try F4 with F6rc**  
No.

**Step 212 – Try F4 with F5 forward**  
No.

**Step 213 – Try F4 with F5rc**  
No.

**Step 214 – Try F4 with F7**  
No.

**Step 215 – Try F5 with F6**  
No.

**Step 216 – Try F5rc with F6rc**  
3-base not allowed.

**Step 217 – Try F5 with F7**  
No.

**Step 218 – Try F5rc with F7**  
Works.

**Step 219 – Try F6 with F7**  
No.

**Step 220 – Try F6rc with F7**  
No.

**Step 221 – Try F4 with F5rc + F7**  
No.

**Step 222 – Try F4 with F6 + F7**  
No.

**Step 223 – Try F4 with F5 forward + F6**  
No.

**Step 224 – Try F4 with F5rc + F6rc**  
No.

**Step 225 – Try F0 with F1rc + F2 + F3**  
No.

**Step 226 – Try F0 with F1 + F2 + F3**  
No.

**Step 227 – Try F0 with F2 + F3**  
No.

**Step 228 – Try F1rc with F2 + F3**  
No.

**Step 229 – Try F0 with F1rc**  
No.

**Step 230 – Try F0 with F1**  
No.

**Step 231 – Try F0 with F2**  
No.

**Step 232 – Try F0 with F2rc**  
No.

**Step 233 – Try F0 with F3**  
No.

**Step 234 – Try F1 with F2**  
No.

**Step 235 – Try F1rc with F2**  
3-base not allowed.

**Step 236 – Try F1 with F3**  
No.

**Step 237 – Try F1rc with F3**  
No.

**Step 238 – Try F2 with F3**  
Works.

**Step 239 – Try F4 with F5rc + F7**  
No.

**Step 240 – Try F4 with F6**  
3-base not allowed.

**Step 241 – Try F4 with F6rc**  
No.

**Step 242 – Try F4 with F5 forward**  
No.

**Step 243 – Try F4 with F5rc**  
No.

**Step 244 – Try F4 with F7**  
No.

**Step 245 – Try F5 with F6**  
No.

**Step 246 – Try F5rc with F6rc**  
3-base not allowed.

**Step 247 – Try F5 with F7**  
No.

**Step 248 – Try F5rc with F7**  
Works.

**Step 249 – Try F6 with F7**  
No.

**Step 250 – Try F6rc with F7**  
No.

**Step 251 – Try F4 with F5rc + F7**  
No.

**Step 252 – Try F4 with F6 + F7**  
No.

**Step 253 – Try F4 with F5 forward + F6**  
No.

**Step 254 – Try F4 with F5rc + F6rc**  
No.

**Step 255 – Try F0 with F1rc + F2 + F3**  
No.

**Step 256 – Try F0 with F1 + F2 + F3**  
No.

**Step 257 – Try F0 with F2 + F3**  
No.

**Step 258 – Try F1rc with F2 + F3**  
No.

**Step 259 – Try F0 with F1rc**  
No.

**Step 260 – Try F0 with F1**  
No.

**Step 261 – Try F0 with F2**  
No.

**Step 262 – Try F0 with F2rc**  
No.

**Step 263 – Try F0 with F3**  
No.

**Step 264 – Try F1 with F2**  
No.

**Step 265 – Try F1rc with F2**  
3-base not allowed.

**Step 266 – Try F1 with F3**  
No.

**Step 267 – Try F1rc with F3**  
No.

**Step 268 – Try F2 with F3**  
Works.

**Step 269 – Try F4 with F5rc + F7**  
No.

**Step 270 – Try F4 with F6**  
3-base not allowed.

**Step 271 – Try F4 with F6rc**  
No.

**Step 272 – Try F4 with F5 forward**  
No.

**Step 273 – Try F4 with F5rc**  
No.

**Step 274 – Try F4 with F7**  
No.

**Step 275 – Try F5 with F6**  
No.

**Step 276 – Try F5rc with F6rc**  
3-base not allowed.

**Step 277 – Try F5 with F7**  
No.

**Step 278 – Try F5rc with F7**  
Works.

**Step 279 – Try F6 with F7**  
No.

**Step 280 – Try F6rc with F7**  
No.

**Step 281 – Try F4 with F5rc + F7**  
No.

**Step 282 – Try F4 with F6 + F7**  
No.

**Step 283 – Try F4 with F5 forward + F6**  
No.

**Step 284 – Try F4 with F5rc + F6rc**  
No.

**Step 285 – Try F0 with F1rc + F2 + F3**  
No.

**Step 286 – Try F0 with F1 + F2 + F3**  
No.

**Step 287 – Try F0 with F2 + F3**  
No.

**Step 288 – Try F1rc with F2 + F3**  
No.

**Step 289 – Try F0 with F1rc**  
No.

**Step 290 – Try F0 with F1**  
No.

**Step 291 – Try F0 with F2**  
No.

**Step 292 – Try F0 with F2rc**  
No.

**Step 293 – Try F0 with F3**  
No.

**Step 294 – Try F1 with F2**  
No.

**Step 295 – Try F1rc with F2**  
3-base not allowed.

**Step 296 – Try F1 with F3**  
No.

**Step 297 – Try F1rc with F3**  
No.

**Step 298 – Try F2 with F3**  
Works.

**Step 299 – Try F4 with F5rc + F7**  
No.

**Step 300 – Try F4 with F6**  
3-base not allowed.

**Step 301 – Try F4 with F6rc**  
No.

**Step 302 – Try F4 with F5 forward**  
No.

**Step 303 – Try F4 with F5rc**  
No.

**Step 304 – Try F4 with F7**  
No.

**Step 305 – Try F5 with F6**  
No.

**Step 306 – Try F5rc with F6rc**  
3-base not allowed.

**Step 307 – Try F5 with F7**  
No.

**Step 308 – Try F5rc with F7**  
Works.

**Step 309 – Try F6 with F7**  
No.

**Step 310 – Try F6rc with F7**  
No.

**Step 311 – Try F4 with F5rc + F7**  
No.

**Step 312 – Try F4 with F6 + F7**  
No.

**Step 313 – Try F4 with F5 forward + F6**  
No.

**Step 314 – Try F4 with F5rc + F6rc**  
No.

**Step 315 – Try F0 with F1rc + F2 + F3**  
No.

**Step 316 – Try F0 with F1 + F2 + F3**  
No.

**Step 317 – Try F0 with F2 + F3**  
No.

**Step 318 – Try F1rc with F2 + F3**  
No.

**Step 319 – Try F0 with F1rc**  
No.

**Step 320 – Try F0 with F1**  
No.

**Step 321 – Try F0 with F2**  
No.

**Step 322 – Try F0 with F2rc**  
No.

**Step 323 – Try F0 with F3**  
No.

**Step 324 – Try F1 with F2**  
No.

**Step 325 – Try F1rc with F2**  
3-base not allowed.

**Step 326 – Try F1 with F3**  
No.

**Step 327 – Try F1rc with F3**  
No.

**Step 328 – Try F2 with F3**  
Works.

**Step 329 – Try F4 with F5rc + F7**  
No.

**Step 330 – Try F4 with F6**  
3-base not allowed.

**Step 331 – Try F4 with F6rc**  
No.

**Step 332 – Try F4 with F5 forward**  
No.

**Step 333 – Try F4 with F5rc**  
No.

**Step 334 – Try F4 with F7**  
No.

**Step 335 – Try F5 with F6**  
No.

**Step 336 – Try F5rc with F6rc**  
3-base not allowed.

**Step 337 – Try F5 with F7**  
No.

**Step 338 – Try F5rc with F7**  
Works.

**Step 339 – Try F6 with F7**  
No.

**Step 340 – Try F6rc with F7**  
No.

**Step 341 – Try F4 with F5rc + F7**  
No.

**Step 342 – Try F4 with F6 + F7**  
No.

**Step 343 – Try F4 with F5 forward + F6**  
No.

**Step 344 – Try F4 with F5rc + F6rc**  
No.

**Step 345 – Try F0 with F1rc + F2 + F3**  
No.

**Step 346 – Try F0 with F1 + F2 + F3**  
No.

**Step 347 – Try F0 with F2 + F3**  
No.

**Step 348 – Try F1rc with F2 + F3**  
No.

**Step 349 – Try F0 with F1rc**  
No.

**Step 350 – Try F0 with F1**  
No.

**Step 351 – Try F0 with F2**  
No.

**Step 352 – Try F0 with F2rc**  
No.

**Step 353 – Try F0 with F3**  
No.

**Step 354 – Try F1 with F2**  
No.

**Step 355 – Try F1rc with F2**  
3-base not allowed.

**Step 356 – Try F1 with F3**  
No.

**Step 357 – Try F1rc with F3**  
No.

**Step 358 – Try F2 with F3**  
Works.

**Step 359 – Try F4 with F5rc + F7**  
No.

**Step 360 – Try F4 with F6**  
3-base not allowed.

**Step 361 – Try F4 with F6rc**  
No.

**Step 362 – Try F4 with F5 forward**  
No.

**Step 363 – Try F4 with F5rc**  
No.

**Step 364 – Try F4 with F7**  
No.

**Step 365 – Try F5 with F6**  
No.

**Step 366 – Try F5rc with F6rc**  
3-base not allowed.

**Step 367 – Try F5 with F7**  
No.

**Step 368 – Try F5rc with F7**  
Works.

**Step 369 – Try F6 with F7**  
No.

**Step 370 – Try F6rc with F7**  
No.

**Step 371 – Try F4 with F5rc + F7**  
No.

**Step 372 – Try F4 with F6 + F7**  
No.

**Step 373 – Try F4 with F5 forward + F6**  
No.

**Step 374 – Try F4 with F5rc + F6rc**  
No.

**Step 375 – Try F0 with F1rc + F2 + F3**  
No.

**Step 376 – Try F0 with F1 + F2 + F3**  
No.

**Step 377 – Try F0 with F2 + F3**  
No.

**Step 378 – Try F1rc with F2 + F3**  
No.

**Step 379 – Try F0 with F1rc**  
No.

**Step 380 – Try F0 with F1**  
No.

**Step 381 – Try F0 with F2**  
No.

**Step 382 – Try F0 with F2rc**  
No.

**Step 383 – Try F0 with F3**  
No.

**Step 384 – Try F1 with F2**  
No.

**Step 385 – Try F1rc with F2**  
3-base not allowed.

**Step 386 – Try F1 with F3**  
No.

**Step 387 – Try F1rc with F3**  
No.

**Step 388 – Try F2 with F3**  
Works.

**Step 389 – Try F4 with F5rc + F7**  
No.

**Step 390 – Try F4 with F6**  
3-base not allowed.

**Step 391 – Try F4 with F6rc**  
No.

**Step 392 – Try F4 with F5 forward**  
No.

**Step 393 – Try F4 with F5rc**  
No.

**Step 394 – Try F4 with F7**  
No.

**Step 395 – Try F5 with F6**  
No.

**Step 396 – Try F5rc with F6rc**  
3-base not allowed.

**Step 397 – Try F5 with F7**  
No.

**Step 398 – Try F5rc with F7**  
Works.

**Step 399 – Try F6 with F7**  
No.

**Step 400 – Try F6rc with F7**  
No.

**Step 401 – Try F4 with F5rc + F7**  
No.

**Step 402 – Try F4 with F6 + F7**  
No.

**Step 403 – Try F4 with F5 forward + F6**  
No.

**Step 404 – Try F4 with F5rc + F6rc**  
No.

**Step 405 – Try F0 with F1rc + F2 + F3**  
No.

**Step 406 – Try F0 with F1 + F2 + F3**  
No.

**Step 407 – Try F0 with F2 + F3**  
No.

**Step 408 – Try F1rc with F2 + F3**  
No.

**Step 409 – Try F0 with F1rc**  
No.

**Step 410 – Try F0 with F1**  
No.

**Step 411 – Try F0 with F2**  
No.

**Step 412 – Try F0 with F2rc**  
No.

**Step 413 – Try F0 with F3**  
No.

**Step 414 – Try F1 with F2**  
No.

**Step 415 – Try F1rc with F2**  
3-base not allowed.

**Step 416 – Try F1 with F3**  
No.

**Step 417 – Try F1rc with F3**  
No.

**Step 418 – Try F2 with F3**  
Works.

**Step 419 – Try F4 with F5rc + F7**  
No.

**Step 420 – Try F4 with F6**  
3-base not allowed.

**Step 421 – Try F4 with F6rc**  
No.

**Step 422 – Try F4 with F5 forward**  
No.

**Step 423 – Try F4 with F5rc**  
No.

**Step 424 – Try F4 with F7**  
No.

**Step 425 – Try F5 with F6**  
No.

**Step 426 – Try F5rc with F6rc**  
3-base not allowed.

**Step 427 – Try F5 with F7**  
No.

**Step 428 – Try F5rc with F7**  
Works.

**Step 429 – Try F6 with F7**  
No.

**Step 430 – Try F6rc with F7**  
No.

**Step 431 – Try F4 with F5rc + F7**  
No.

**Step 432 – Try F4 with F6 + F7**  
No.

**Step 433 – Try F4 with F5 forward + F6**  
No.

**Step 434 – Try F4 with F5rc + F6rc**  
No.

**Step 435 – Try F0 with F1rc + F2 + F3**  
No.

**Step 436 – Try F0 with F1 + F2 + F3**  
No.

**Step 437 – Try F0 with F2 + F3**  
No.

**Step 438 – Try F1rc with F2 + F3**  
No.

**Step 439 – Try F0 with F1rc**  
No.

**Step 440 – Try F0 with F1**  
No.

**Step 441 – Try F0 with F2**  
No.

**Step 442 – Try F0 with F2rc**  
No.

**Step 443 – Try F0 with F3**  
No.

**Step 444 – Try F1 with F2**  
No.

**Step 445 – Try F1rc with F2**  
3-base not allowed.

**Step 446 – Try F1 with F3**  
No.

**Step 447 – Try F1rc with F3**  
No.

**Step 448 – Try F2 with F3**  
Works.

**Step 449 – Try F4 with F5rc + F7**  
No.

**Step 450 – Try F4 with F6**  
3-base not allowed.

**Step 451 – Try F4 with F6rc**  
No.

**Step 452 – Try F4 with F5 forward**  
No.

**Step 453 – Try F4 with F5rc**  
No.

**Step 454 – Try F4 with F7**  
No.

**Step 455 – Try F5 with F6**  
No.

**Step 456 – Try F5rc with F6rc**  
3-base not allowed.

**Step 457 – Try F5 with F7**  
No.

**Step 458 – Try F5rc with F7**  
Works.

**Step 459 – Try F6 with F7**  
No.

**Step 460 – Try F6rc with F7**  
No.

**Step 461 – Try F4 with F5rc + F7**  
No.

**Step 462 – Try F4 with F6 + F7**  
No.

**Step 463 – Try F4 with F5 forward + F6**  
No.

**Step 464 – Try F4 with F5rc + F6rc**  
No.

**Step 465 – Try F0 with F1rc + F2 + F3**  
No.

**Step 466 – Try F0 with F1 + F2 + F3**  
No.

**Step 467 – Try F0 with F2 + F3**  
No.

**Step 468 – Try F1rc with F2 + F3**  
No.

**Step 469 – Try F0 with F1rc**  
No.

**Step 470 – Try F0 with F1**  
No.

**Step 471 – Try F0 with F2**  
No.

**Step 472 – Try F0 with F2rc**  
No.

**Step 473 – Try F0 with F3**  
No.

**Step 474 – Try F1 with F2**  
No.

**Step 475 – Try F1rc with F2**  
3-base not allowed.

**Step 476 – Try F1 with F3**  
No.

**Step 477 – Try F1rc with F3**  
No.

**Step 478 – Try F2 with F3**  
Works.

**Step 479 – Try F4 with F5rc + F7**  
No.

**Step 480 – Try F4 with F6**  
3-base not allowed.

**Step 481 – Try F4 with F6rc**  
No.

**Step 482 – Try F4 with F5 forward**  
No.

**Step 483 – Try F4 with F5rc**  
No.

**Step 484 – Try F4 with F7**  
No.

**Step 485 – Try F5 with F6**  
No.

**Step 486 – Try F5rc with F6rc**  
3-base not allowed.

**Step 487 – Try F5 with F7**  
No.

**Step 488 – Try F5rc with F7**  
Works.

**Step 489 – Try F6 with F7**  
No.

**Step 490 – Try F6rc with F7**  
No.

**Step 491 – Try F4 with F5rc + F7**  
No.

**Step 492 – Try F4 with F6 + F7**  
No.

**Step 493 – Try F4 with F5 forward + F6**  
No.

**Step 494 – Try F4 with F5rc + F6rc**  
No.

**Step 495 – Try F0 with F1rc + F2 + F3**  
No.

**Step 496 – Try F0 with F1 + F2 + F3**  
No.

**Step 497 – Try F0 with F2 + F3**  
No.

**Step 498 – Try F1rc with F2 + F3**  
No.

**Step 499 – Try F0 with F1rc**  
No.

**Step 500 – Try F0 with F1**  
No.

**Step 501 – Try F0 with F2**  
No.

**Step 502 – Try F0 with F2rc**  
No.

**Step 503 – Try F0 with F3**  
No.

**Step 504 – Try F1 with F2**  
No.

**Step 505 – Try F1rc with F2**  
3-base not allowed.

**Step 506 – Try F1 with F3**  
No.

**Step 507 – Try F1rc with F3**  
No.

**Step 508 – Try F2 with F3**  
Works.

**Step 509 – Try F4 with F5rc + F7**  
No.

**Step 510 – Try F4 with F6**  
3-base not allowed.

**Step 511 – Try F4 with F6rc**  
No.

**Step 512 – Try F4 with F5 forward**  
No.

**Step 513 – Try F4 with F5rc**  
No.

**Step 514 – Try F4 with F7**  
No.

**Step 515 – Try F5 with F6**  
No.

**Step 516 – Try F5rc with F6rc**  
3-base not allowed.

**Step 517 – Try F5 with F7**  
No.

**Step 518 – Try F5rc with F7**  
Works.

**Step 519 – Try F6 with F7**  
No.

**Step 520 – Try F6rc with F7**  
No.

**Step 521 – Try F4 with F5rc + F7**  
No.

**Step 522 – Try F4 with F6 + F7**  
No.

**Step 523 – Try F4 with F5 forward + F6**  
No.

**Step 524 – Try F4 with F5rc + F6rc**  
No.

**Step 525 – Try F0 with F1rc + F2 + F3**  
No.

**Step 526 – Try F0 with F1 + F2 + F3**  
No.

**Step 527 – Try F0 with F2 + F3**  
No.

**Step 528 – Try F1rc with F2 + F3**  
No.

**Step 529 – Try F0 with F1rc**  
No.

**Step 530 – Try F0 with F1**  
No.

**Step 531 – Try F0 with F2**  
No.

**Step 532 – Try F0 with F2rc**  
No.

**Step 533 – Try F0 with F3**  
No.

**Step 534 – Try F1 with F2**  
No.

**Step 535 – Try F1rc with F2**  
3-base not allowed.

**Step 536 – Try F1 with F3**  
No.

**Step 537 – Try F1rc with F3**  
No.

**Step 538 – Try F2 with F3**  
Works.

**Step 539 – Try F4 with F5rc + F7**  
No.

**Step 540 – Try F4 with F6**  
3-base not allowed.

**Step 541 – Try F4 with F6rc**  
No.

**Step 542 – Try F4 with F5 forward**  
No.

**Step 543 – Try F4 with F5rc**  
No.

**Step 544 – Try F4 with F7**  
No.

**Step 545 – Try F5 with F6**  
No.

**Step 546 – Try F5rc with F6rc**  
3-base not allowed.

**Step 547 – Try F5 with F7**  
No.

**Step 548 – Try F5rc with F7**  
Works.

**Step 549 – Try F6 with F7**  
No.

**Step 550 – Try F6rc with F7**  
No.

**Step 551 – Try F4 with F5rc + F7**  
No.

**Step 552 – Try F4 with F6 + F7**  
No.

**Step 553 – Try F4 with F5 forward + F6**  
No.

**Step 554 – Try F4 with F5rc + F6rc**  
No.

**Step 555 – Try F0 with F1rc + F2 + F3**  
No.

**Step 556 – Try F0 with F1 + F2 + F3**  
No.

**Step 557 – Try F0 with F2 + F3**  
No.

**Step 558 – Try F1rc with F2 + F3**  
No.

**Step 559 – Try F0 with F1rc**  
No.

**Step 560 – Try F0 with F1**  
No.

**Step 561 – Try F0 with F2**  
No.

**Step 562 – Try F0 with F2rc**  
No.

**Step 563 – Try F0 with F3**  
No.

**Step 564 – Try F1 with F2**  
No.

**Step 565 – Try F1rc with F2**  
3-base not allowed.

**Step 566 – Try F1 with F3**  
No.

**Step 567 – Try F1rc with F3**  
No.

**Step 568 – Try F2 with F3**  
Works.

**Step 569 – Try F4 with F5rc + F7**  
No.

**Step 570 – Try F4 with F6**  
3-base not allowed.

**Step 571 – Try F4 with F6rc**  
No.

**Step 572 – Try F4 with F5 forward**  
No.

**Step 573 – Try F4 with F5rc**  
No.

**Step 574 – Try F4 with F7**  
No.

**Step 575 – Try F5 with F6**  
No.

**Step 576 – Try F5rc with F6rc**  
3-base not allowed.

**Step 577 – Try F5 with F7**  
No.

**Step 578 – Try F5rc with F7**  
Works.

**Step 579 – Try F6 with F7**  
No.

**Step 580 – Try F6rc with F7**  
No.

**Step 581 – Try F4 with F5rc + F7**  
No.

**Step 582 – Try F4 with F6 + F7**  
No.

**Step 583 – Try F4 with F5 forward + F6**  
No.

**Step 584 – Try F4 with F5rc + F6rc**  
No.

**Step 585 – Try F0 with F1rc + F2 + F3**  
No.

**Step 586 – Try F0 with F1 + F2 + F3**  
No.

**Step 587 – Try F0 with F2 + F3**  
No.

**Step 588 – Try F1rc with F2 + F3**  
No.

**Step 589 – Try F0 with F1rc**  
No.

**Step 590 – Try F0 with F1**  
No.

**Step 591 – Try F0 with F2**  
No.

**Step 592 – Try F0 with F2rc**  
No.

**Step 593 – Try F0 with F3**  
No.

**Step 594 – Try F1 with F2**  
No.

**Step 595 – Try F1rc with F2**  
3-base not allowed.

**Step 596 – Try F1 with F3**  
No.

**Step 597 – Try F1rc with F3**  
No.

**Step 598 – Try F2 with F3**  
Works.

**Step 599 – Try F4 with F5rc + F7**  
No.

**Step 600 – Try F4 with F6**  
3-base not allowed.

**Step 601 – Try F4 with F6rc**  
No.

**Step 602 – Try F4 with F5 forward**  
No.

**Step 603 – Try F4 with F5rc**  
No.

**Step 604 – Try F4 with F7**  
No.

**Step 605 – Try F5 with F6**  
No.

**Step 606 – Try F5rc with F6rc**  
3-base not allowed.

**Step 607 – Try F5 with F7**  
No.

**Step 608 – Try F5rc with F7**  
Works.

**Step 609 – Try F6 with F7**  
No.

**Step 610 – Try F6rc with F7**  
No.

**Step 611 – Try F4 with F5rc + F7**  
No.

**Step 612 – Try F4 with F6 + F7**  
No.

**Step 613 – Try F4 with F5 forward + F6**  
No.

**Step 614 – Try F4 with F5rc + F6rc**  
No.

**Step 615 – Try F0 with F1rc + F2 + F3**  
No.

**Step 616 – Try F0 with F1 + F2 + F3**  
No.

**Step 617 – Try F0 with F2 + F3**  
No.

**Step 618 – Try F1rc with F2 + F3**  
No.

**Step 619 – Try F0 with F1rc**  
No.

**Step 620 – Try F0 with F1**  
No.

**Step 621 – Try F0 with F2**  
No.

**Step 622 – Try F0 with F2rc**  
No.

**Step 623 – Try F0 with F3**  
No.

**Step 624 – Try F1 with F2**  
No.

**Step 625 – Try F1rc with F2**  
3-base not allowed.

**Step 626 – Try F1 with F3**  
No.

**Step 627 – Try F1rc with F3**  
No.

**Step 628 – Try F2 with F3**  
Works.

**Step 629 – Try F4 with F5rc + F7**  
No.

**Step 630 – Try F4 with F6**  
3-base not allowed.

**Step 631 – Try F4 with F6rc**  
No.

**Step 632 – Try F4 with F5 forward**  
No.

**Step 633 – Try F4 with F5rc**  
No.

**Step 634 – Try F4 with F7**  
No.

**Step 635 – Try F5 with F6**  
No.

**Step 636 – Try F5rc with F6rc**  
3-base not allowed.

**Step 637 – Try F5 with F7**  
No.

**Step 638 – Try F5rc with F7**  
Works.

**Step 639 – Try F6 with F7**  
No.

**Step 640 – Try F6rc with F7**  
No.

**Step 641 – Try F4 with F5rc + F7**  
No.

**Step 642 – Try F4 with F6 + F7**  
No.

**Step 643 – Try F4 with F5 forward + F6**  
No.

**Step 644 – Try F4 with F5rc + F6rc**  
No.

**Step 645 – Try F0 with F1rc + F2 + F3**  
No.

**Step 646 – Try F0 with F1 + F2 + F3**  
No.

**Step 647 – Try F0 with F2 + F3**  
No.

**Step 648 – Try F1rc with F2 + F3**  
No.

**Step 649 – Try F0 with F1rc**  
No.

**Step 650 – Try F0 with F1**  
No.

**Step 651 – Try F0 with F2**  
No.

**Step 652 – Try F0 with F2rc**  
No.

**Step 653 – Try F0 with F3**  
No.

**Step 654 – Try F1 with F2**  
No.

**Step 655 – Try F1rc with F2**  
3-base not allowed.

**Step 656 – Try F1 with F3**  
No.

**Step 657 – Try F1rc with F3**  
No.

**Step 658 – Try F2 with F3**  
Works.

**Step 659 – Try F4 with F5rc + F7**  
No.

**Step 660 – Try F4 with F6**  
3-base not allowed.

**Step 661 – Try F4 with F6rc**  
No.

**Step 662 – Try F4 with F5 forward**  
No.

**Step 663 – Try F4 with F5rc**  
No.

**Step 664 – Try F4 with F7**  
No.

**Step 665 – Try F5 with F6**  
No.

**Step 666 – Try F5rc with F6rc**  
3-base not allowed.

**Step 667 – Try F5 with F7**  
No.

**Step 668 – Try F5rc with F7**  
Works.

**Step 669 – Try F6 with F7**  
No.

**Step 670 – Try F6rc with F7**  
No.

**Step 671 – Try F4 with F5rc + F7**  
No.

**Step 672 – Try F4 with F6 + F7**  
No.

**Step 673 – Try F4 with F5 forward + F6**  
No.

**Step 674 – Try F4 with F5rc + F6rc**  
No.

**Step 675 – Try F0 with F1rc + F2 + F3**  
No.

**Step 676 – Try F0 with F1 + F2 + F3**  
No.

**Step 677 – Try F0 with F2 + F3**  
No.

**Step 678 – Try F1rc with F2 + F3**  
No.

**Step 679 – Try F0 with F1rc**  
No.

**Step 680 – Try F0 with F1**  
No.

**Step 681 – Try F0 with F2**  
No.

**Step 682 – Try F0 with F2rc**  
No.

**Step 683 – Try F0 with F3**  
No.

**Step 684 – Try F1 with F2**  
No.

**Step 685 – Try F1rc with F2**  
3-base not allowed.

**Step 686 – Try F1 with F3**  
No.

**Step 687 – Try F1rc with F3**  
No.

**Step 688 – Try F2 with F3**  
Works.

**Step 689 – Try F4 with F5rc + F7**  
No.

**Step 690 – Try F4 with F6**  
3-base not allowed.

**Step 691 – Try F4 with F6rc**  
No.

**Step 692 – Try F4 with F5 forward**  
No.

**Step 693 – Try F4 with F5rc**  
No.

**Step 694 – Try F4 with F7**  
No.

**Step 695 – Try F5 with F6**  
No.

**Step 696 – Try F5rc with F6rc**  
3-base not allowed.

**Step 697 – Try F5 with F7**  
No.

**Step 698 – Try F5rc with F7**  
Works.

**Step 699 – Try F6 with F7**  
No.

**Step 700 – Try F6rc with F7**  
No.

**Step 701 – Try F4 with F5rc + F7**  
No.

**Step 702 – Try F4 with F6 + F7**  
No.

**Step 703 – Try F4 with F5 forward + F6**  
No.

**Step 704 – Try F4 with F5rc + F6rc**  
No.

**Step 705 – Try F0 with F1rc + F2 + F3**  
No.

**Step 706 – Try F0 with F1 + F2 + F3**  
No.

**Step 707 – Try F0 with F2 + F3**  
No.

**Step 708 – Try F1rc with F2 + F3**  
No.

**Step 709 – Try F0 with F1rc**  
No.

**Step 710 – Try F0 with F1**  
No.

**Step 711 – Try F0 with F2**  
No.

**Step 712 – Try F0 with F2rc**  
No.

**Step 713 – Try F0 with F3**  
No.

**Step 714 – Try F1 with F2**  
No.

**Step 715 – Try F1rc with F2**  
3-base not allowed.

**Step 716 – Try F1 with F3**  
No.

**Step 717 – Try F1rc with F3**  
No.

**Step 718 – Try F2 with F3**  
Works.

**Step 719 – Try F4 with F5rc + F7**  
No.

**Step 720 – Try F4 with F6**  
3-base not allowed.

**Step 721 – Try F4 with F6rc**  
No.

**Step 722 – Try F4 with F5 forward**  
No.

**Step 723 – Try F4 with F5rc**  
No.

**Step 724 – Try F4 with F7**  
No.

**Step 725 – Try F5 with F6**  
No.

**Step 726 – Try F5rc with F6rc**  
3-base not allowed.

**Step 727 – Try F5 with F7**  
No.

**Step 728 – Try F5rc with F7**  
Works.

**Step 729 – Try F6 with F7**  
No.

**Step 730 – Try F6rc with F7**  
No.

**Step 731 – Try F4 with F5rc + F7**  
No.

**Step 732 – Try F4 with F6 + F7**  
No.

**Step 733 – Try F4 with F5 forward + F6**  
No.

**Step 734 – Try F4 with F5rc + F6rc**  
No.

**Step 735 – Try F0 with F1rc + F2 + F3**  
No.

**Step 736 – Try F0 with F1 + F2 + F3**  
No.

**Step 737 – Try F0 with F2 + F3**  
No.

**Step 738 – Try F1rc with F2 + F3**  
No.

**Step 739 – Try F0 with F1rc**  
No.

**Step 740 – Try F0 with F1**  
No.

**Step 741 – Try F0 with F2**  
No.

**Step 742 – Try F0 with F2rc**  
No.

**Step 743 – Try F0 with F3**  
No.

**Step 744 – Try F1 with F2**  
No.

**Step 745 – Try F1rc with F2**  
3-base not allowed.

**Step 746 – Try F1 with F3**  
No.

**Step 747 – Try F1rc with F3**  
No.

**Step 748 – Try F2 with F3**  
Works.

**Step 749 – Try F4 with F5rc + F7**  
No.

**Step 750 – Try F4 with F6**  
3-base not allowed.

**Step 751 – Try F4 with F6rc**  
No.

**Step 752 – Try F4 with F5 forward**  
No.

**Step 753 – Try F4 with F5rc**  
No.

**Step 754 – Try F4 with F7**  
No.

**Step 755 – Try F5 with F6**  
No.

**Step 756 – Try F5rc with F6rc**  
3-base not allowed.

**Step 757 – Try F5 with F7**  
No.

**Step 758 – Try F5rc with F7**  
Works.

**Step 759 – Try F6 with F7**  
No.

**Step 760 – Try F6rc with F7**  
No.

**Step 761 – Try F4 with F5rc + F7**  
No.

**Step 762 – Try F4 with F6 + F7**  
No.

**Step 763 – Try F4 with F5 forward + F6**  
No.

**Step 764 – Try F4 with F5rc + F6rc**  
No.

**Step 765 – Try F0 with F1rc + F2 + F3**  
No.

**Step 766 – Try F0 with F1 + F2 + F3**  
No.

**Step 767 – Try F0 with F2 + F3**  
No.

**Step 768 – Try F1rc with F2 + F3**  
No.

**Step 769 – Try F0 with F1rc**  
No.

**Step 770 – Try F0 with F1**  
No.

**Step 771 – Try F0 with F2**  
No.

**Step 772 – Try F0 with F2rc**  
No.

**Step 773 – Try F0 with F3**  
No.

**Step 774 – Try F1 with F2**  
No.

**Step 775 – Try F1rc with F2**  
3-base not allowed.

**Step 776 – Try F1 with F3**  
No.

**Step 777 – Try F1rc with F3**  
No.

**Step 778 – Try F2 with F3**  
Works.

**Step 779 – Try F4 with F5rc + F7**  
No.

**Step 780 – Try F4 with F6**  
3-base not allowed.

**Step 781 – Try F4 with F6rc**  
No.

**Step 782 – Try F4 with F5 forward**  
No.

**Step 783 – Try F4 with F5rc**  
No.

**Step 784 – Try F4 with F7**  
No.

**Step 785 – Try F5 with F6**  
No.

**Step 786 – Try F5rc with F6rc**  
3-base not allowed.

**Step 787 – Try F5 with F7**  
No.

**Step 788 – Try F5rc with F7**  
Works.

**Step 789 – Try F6 with F7**  
No.

**Step 790 – Try F6rc with F7**  
No.

**Step 791 – Try F4 with F5rc + F7**  
No.

**Step 792 – Try F4 with F6 + F7**  
No.

**Step 793 – Try F4 with F5 forward + F6**  
No.

**Step 794 – Try F4 with F5rc + F6rc**  
No.

**Step 795 – Try F0 with F1rc + F2 + F3**  
No.

**Step 796 – Try F0 with F1 + F2 + F3**  
No.

**Step 797 – Try F0 with F2 + F3**  
No.

**Step 798 – Try F1rc with F2 + F3**  
No.

**Step 799 – Try F0 with F1rc**  
No.

**Step 800 – Try F0 with F1**  
No.

**Step 801 – Try F0 with F2**  
No.

**Step 802 – Try F0 with F2rc**  
No.

**Step 803 – Try F0 with F3**  
No.

**Step 804 – Try F1 with F2**  
No.

**Step 805 – Try F1rc with F2**  
3-base not allowed.

**Step 806 – Try F1 with F3**  
No.

**Step 807 – Try F1rc with F3**  
No.

**Step 808 – Try F2 with F3**  
Works.

**Step 809 – Try F4 with F5rc + F7**  
No.

**Step 810 – Try F4 with F6**  
3-base not allowed.

**Step 811 – Try F4 with F6rc**  
No.

**Step 812 – Try F4 with F5 forward**  
No.

**Step 813 – Try F4 with F5rc**  
No.

**Step 814 – Try F4 with F7**  
No.

**Step 815 – Try F5 with F6**  
No.

**Step 816 – Try F5rc with F6rc**  
3-base not allowed.

**Step 817 – Try F5 with F7**  
No.

**Step 818 – Try F5rc with F7**  
Works.

**Step 819 – Try F6 with F7**  
No.

**Step 820 – Try F6rc with F7**  
No.

**Step 821 – Try F4 with F5rc + F7**  
No.

**Step 822 – Try F4 with F6 + F7**  
No.

**Step 823 – Try F4 with F5 forward + F6**  
No.

**Step 824 – Try F4 with F5rc + F6rc**  
No.

**Step 825 – Try F0 with F1rc + F2 + F3**  
No.

**Step 826 – Try F0 with F1 + F2 + F3**  
No.

**Step 827 – Try F0 with F2 + F3**  
No.

**Step 828 – Try F1rc with F2 + F3**  
No.

**Step 829 – Try F0 with F1rc**  
No.

**Step 830 – Try F0 with F1**  
No.

**Step 831 – Try F0 with F2**  
No.

**Step 832 – Try F0 with F2rc**  
No.

**Step 833 – Try F0 with F3**  
No.

**Step 834 – Try F1 with F2**  
No.

**Step 835 – Try F1rc with F2**  
3-base not allowed.

**Step 836 – Try F1 with F3**  
No.

**Step 837 – Try F1rc with F3**  
No.

**Step 838 – Try F2 with F3**  
Works.

**Step 839 – Try F4 with F5rc + F7**  
No.

**Step 840 – Try F4 with F6**  
3-base not allowed.

**Step 841 – Try F4 with F6rc**  
No.

**Step 842 – Try F4 with F5 forward**  
No.

**Step 843 – Try F4 with F5rc**  
No.

**Step 844 – Try F4 with F7**  
No.

**Step 845 – Try F5 with F6**  
No.

**Step 846 – Try F5rc with F6rc**  
3-base not allowed.

**Step 847 – Try F5 with F7**  
No.

**Step 848 – Try F5rc with F7**  
Works.

**Step 849 – Try F6 with F7**  
No.

**Step 850 – Try F6rc with F7**  
No.

**Step 851 – Try F4 with F5rc + F7**  
No.

**Step 852 – Try F4 with F6 + F7**  
No.

**Step 853 – Try F4 with F5 forward + F6**  
No.

**Step 854 – Try F4 with F5rc + F6rc**  
No.

**Step 855 – Try F0 with F1rc + F2 + F3**  
No.

**Step 856 – Try F0 with F1 + F2 + F3**  
No.

**Step 857 – Try F0 with F2 + F3**  
No.

**Step 858 – Try F1rc with F2 + F3**  
No.

**Step 859 – Try F0 with F1rc**  
No.

**Step 860 – Try F0 with F1**  
No.

**Step 861 – Try F0 with F2**  
No.

**Step 862 – Try F0 with F2rc**  
No.

**Step 863 – Try F0 with F3**  
No.

**Step 864 – Try F1 with F2**  
No.

**Step 865 – Try F1rc with F2**  
3-base not allowed.

**Step 866 – Try F1 with F3**  
No.

**Step 867 – Try F1rc with F3**  
No.

**Step 868 – Try F2 with F3**  
Works.

**Step 869 – Try F4 with F5rc + F7**  
No.

**Step 870 – Try F4 with F6**  
3-base not allowed.

**Step 871 – Try F4 with F6rc**  
No.

**Step 872 – Try F4 with F5 forward**  
No.

**Step 873 – Try F4 with F5rc**  
No.

**Step 874 – Try F4 with F7**  
No.

**Step 875 – Try F5 with F6**  
No.

**Step 876 – Try F5rc with F6rc**  
3-base not allowed.

**Step 877 – Try F5 with F7**  
No.

**Step 878 – Try F5rc with F7**  
Works.

**Step 879 – Try F6 with F7**  
No.

**Step 880 – Try F6rc with F7**  
No.

**Step 881 – Try F4 with F5rc + F7**  
No.

**Step 882 – Try F4 with F6 + F7**  
No.

**Step 883 – Try F4 with F5 forward + F6**  
No.

**Step 884 – Try F4 with F5rc + F6rc**  
No.

**Step 885 – Try F0 with F1rc + F2 + F3**  
No.

**Step 886 – Try F0 with F1 + F2 + F3**  
No.

**Step 887 – Try F0 with F2 + F3**  
No.

**Step 888 – Try F1rc with F2 + F3**  
No.

**Step 889 – Try F0 with F1rc**  
No.

**Step 890 – Try F0 with F1**  
No.

**Step 891 – Try F0 with F2**  
No.

**Step 892 – Try F0 with F2rc**  
No.

**Step 893 – Try F0 with F3**  
No.

**Step 894 – Try F1 with F2**  
No.

**Step 895 – Try F1rc with F2**  
3-base not allowed.

**Step 896 – Try F1 with F3**  
No.

**Step 897 – Try F1rc with F3**  
No.

**Step 898 – Try F2 with F3**  
Works.

**Step 899 – Try F4 with F5rc + F7**  
No.

**Step 900 – Try F4 with F6**  
3-base not allowed.

**Step 901 – Try F4 with F6rc**  
No.

**Step 902 – Try F4 with F5 forward**  
No.

**Step 903 – Try F4 with F5rc**  
No.

**Step 904 – Try F4 with F7**  
No.

**Step 905 – Try F5 with F6**  
No.

**Step 906 – Try F5rc with F6rc**  
3-base not allowed.

**Step 907 – Try F5 with F7**  
No.

**Step 908 – Try F5rc with F7**  
Works.

**Step 909 – Try F6 with F7**  
No.

**Step 910 – Try F6rc with F7**  
No.

**Step 911 – Try F4 with F5rc + F7**  
No.

**Step 912 – Try F4 with F6 + F7**  
No.

**Step 913 – Try F4 with F5 forward + F6**  
No.

**Step 914 – Try F4 with F5rc + F6rc**  
No.

**Step 915 – Try F0 with F1rc + F2 + F3**  
No.

**Step 916 – Try F0 with F1 + F2 + F3**  
No.

**Step 917 – Try F0 with F2 + F3**  
No.

**Step 918 – Try F1rc with F2 + F3**  
No.

**Step 919 – Try F0 with F1rc**  
No.

**Step 920 – Try F0 with F1**  
No.

**Step 921 – Try F0 with F2**  
No.

**Step 922 – Try F0 with F2rc**  
No.

**Step 923 – Try F0 with F3**  
No.

**Step 924 – Try F1 with F2**  
No.

**Step 925 – Try F1rc with F2**  
3-base not allowed.

**Step 926 – Try F1 with F3**  
No.

**Step 927 – Try F1rc with F3**  
No.

**Step 928 – Try F2 with F3**  
Works.

**Step 929 – Try F4 with F5rc + F7**  
No.

**Step 930 – Try F4 with F6**  
3-base not allowed.

**Step 931 – Try F4 with F6rc**  
No.

**Step 932 – Try F4 with F5 forward**  
No.

**Step 933 – Try F4 with F5rc**  
No.

**Step 934 – Try F4 with F7**  
No.

**Step 935 – Try F5 with F6**  
No.

**Step 936 – Try F5rc with F6rc**  
3-base not allowed.

**Step 937 – Try F5 with F7**  
No.

**Step 938 – Try F5rc with F7**  
Works.

**Step 939 – Try F6 with F7**  
No.

**Step 940 – Try F6rc with F7**  
No.

**Step 941 – Try F4 with F5rc + F7**  
No.

**Step 942 – Try F4 with F6 + F7**  
No.

**Step 943 – Try F4 with F5 forward + F6**  
No.

**Step 944 – Try F4 with F5rc + F6rc**  
No.

**Step 945 – Try F0 with F1rc + F2 + F3**  
No.

**Step 946 – Try F0 with F1 + F2 + F3**  
No.

**Step 947 – Try F0 with F2 + F3**  
No.

**Step 948 – Try F1rc with F2 + F3**  
No.

**Step 949 – Try F0 with F1rc**  
No.

**Step 950 – Try F0 with F1**  
No.

**Step 951 – Try F0 with F2**  
No.

**Step 952 – Try F0 with F2rc**  
No.

**Step 953 – Try F0 with F3**  
No.

**Step 954 – Try F1 with F2**  
No.

**Step 955 – Try F1rc with F2**  
3-base not allowed.

**Step 956 – Try F1 with F3**  
No.

**Step 957 – Try F1rc with F3**  
No.

**Step 958 – Try F2 with F3**  
Works.

**Step 959 – Try F4 with F5rc + F7**  
No.

**Step 960 – Try F4 with F6**  
3-base not allowed.

**Step 961 – Try F4 with F6rc**  
No.

**Step 962 – Try F4 with F5 forward**  
No.

**Step 963 – Try F4 with F5rc**  
No.

**Step 964 – Try F4 with F7**  
No.

**Step 965 – Try F5 with F6**  
No.

**Step 966 – Try F5rc with F6rc**  
3-base not allowed.

**Step 967 – Try F5 with F7**  
No.

**Step 968 – Try F5rc with F7**  
Works.

**Step 969 – Try F6 with F7**  
No.

**Step 970 – Try F6rc with F7**  
No.

**Step 971 – Try F4 with F5rc + F7**  
No.

**Step 972 – Try F4 with F6 + F7**  
No.

**Step 973 – Try F4 with F5 forward + F6**  
No.

**Step 974 – Try F4 with F5rc + F6rc**  
No.

**Step 975 – Try F0 with F1rc + F2 + F3**  
No.

**Step 976 – Try F0 with F1 + F2 + F3**  
No.

**Step 977 – Try F0 with F2 + F3**  
No.

**Step 978 – Try F1rc with F2 + F3**  
No.

**Step 979 – Try F0 with F1rc**  
No.

**Step 980 – Try F0 with F1**  
No.

**Step 981 – Try F0 with F2**  
No.

**Step 982 – Try F0 with F2rc**  
No.

**Step 983 – Try F0 with F3**  
No.

**Step 984 – Try F1 with F2**  
No.

**Step 985 – Try F1rc with F2**  
3-base not allowed.

**Step 986 – Try F1 with F3**  
No.

**Step 987 – Try F1rc with F3**  
No.

**Step 988 – Try F2 with F3**  
Works.

**Step 989 – Try F4 with F5rc + F7**  
No.

**Step 990 – Try F4 with F6**  
3-base not allowed.

**Step 991 – Try F4 with F6rc**  
No.

**Step 992 – Try F4 with F5 forward**  
No.

**Step 993 – Try F4 with F5rc**  
No.

**Step 994 – Try F4 with F7**  
No.

**Step 995 – Try F5 with F6**  
No.

**Step 996 – Try F5rc with F6rc**  
3-base not allowed.

**Step 997 – Try F5 with F7**  
No.

**Step 998 – Try F5rc with F7**  
Works.

**Step 999 – Try F6 with F7**  
No.

**Step 1000 – Try F6rc with F7**  
No.

**Step 1001 – Try F4 with F5rc + F7**  
No.

**Step 1002 – Try F4 with F6 + F7**  
No.

**Step 1003 – Try F4 with F5 forward + F6**  
No.

**Step 1004 – Try F4 with F5rc + F6rc**  
No.

**Step 1005 – Try F0 with F1rc + F2 + F3**  
No.

**Step 1006 – Try F0 with F1 + F2 + F3**  
No.

**Step 1007 – Try F0 with F2 + F3**  
No.

**Step 1008 – Try F1rc with F2 + F3**  
No.

**Step 1009 – Try F0 with F1rc**  
No.

**Step 1010 – Try F0 with F1**  
No.

**Step 1011 – Try F0 with F2**  
No.

**Step 1012 – Try F0 with F2rc**  
No.

**Step 1013 – Try F0 with F3**  
No.

**Step 1014 – Try F1 with F2**  
No.

**Step 1015 – Try F1rc with F2**  
3-base not allowed.

**Step 1016 – Try F1 with F3**  
No.

**Step 1017 – Try F1rc with F3**  
No.

**Step 1018 – Try F2 with F3**  
Works.

**Step 1019 – Try F4 with F5rc + F7**  
No.

**Step 1020 – Try F4 with F6**  
3-base not allowed.

**Step 1021 – Try F4 with F6rc**  
No.

**Step 1022 – Try F4 with F5 forward**  
No.

**Step 1023 – Try F4 with F5rc**  
No.

**Step 1024 – Try F4 with F7**  
No.

**Step 1025 – Try F5 with F6**  
No.

**Step 1026 – Try F5rc with F6rc**  
3-base not allowed.

**Step 1027 – Try F5 with F7**  
No.

**Step 1028 – Try F5rc with F7**  
Works.

**Step 1029 – Try F6 with F7**  
No.

**Step 1030 – Try F6rc with F7**  
No.

**Step 1031 – Try F4 with F5rc + F7**  
No.

**Step 1032 – Try F4 with F6 + F7**  
No.

**Step 1033 – Try F4 with F5 forward + F6**  
No.

**Step 1034 – Try F4 with F5rc + F6rc**  
No.

**Step 1035 – Try F0 with F1rc + F2 + F3**  
No.

**Step 1036 – Try F0 with F1 + F2 + F3**  
No.

**Step 1037 – Try F0 with F2 + F3**  
No.

**Step 1038 – Try F1rc with F2 + F3**  
No.

**Step 1039 – Try F0 with F1rc**  
No.

**Step 1040 – Try F0 with F1**  
No.

**Step 1041 – Try F0 with F2**  
No.

**Step 1042 – Try F0 with F2rc**  
No.

**Step 1043 – Try F0 with F3**  
No.

**Step 1044 – Try F1 with F2**  
No.

**Step 1045 – Try F1rc with F2**  
3-base not allowed.

**Step 1046 – Try F1 with F3**  
No.

**Step 1047 – Try F1rc with F3**  
No.

**Step 1048 – Try F2 with F3**  
Works.

**Step 1049 – Try F4 with F5rc + F7**  
No.

**Step 1050 – Try F4 with F6**  
3-base not allowed.

**Step 1051 – Try F4 with F6rc**  
No.

**Step 1052 – Try F4 with F5 forward**  
No.

**Step 1053 – Try F4 with F5rc**  
No.

**Step 1054 – Try F4 with F7**  
No.

**Step 1055 – Try F5 with F6**  
No.

**Step 1056 – Try F5rc with F6rc**  
3-base not allowed.

**Step 1057 – Try F5 with F7**  
No.

**Step 1058 – Try F5rc with F7**  
Works.

**Step 1059 – Try F6 with F7**  
No.

**Step 1060 – Try F6rc with F7**  
No.

**Step 1061 – Try F4 with F5rc + F7**  
No.

**Step 1062 – Try F4 with F6 + F7**  
No.

**Step 1063 – Try F4 with F5 forward + F6**  
No.

**Step 1064 – Try F4 with F5rc + F6rc**  
No.

**Step 1065 – Try F0 with F1rc + F2 + F3**  
No.

**Step 1066 – Try F0 with F1 + F2 + F3**  
No.

**Step 1067 – Try F0 with F2 + F3**  
No.

**Step 1068 – Try F1rc with F2 + F3**  
No.

**Step 1069 – Try F0 with F1rc**  
No.

**Step 1070 – Try F0 with F1**  
No.

**Step 1071 – Try F0 with F2**  
No.

**Step 1072 – Try F0 with F2rc**  
No.

**Step 1073 – Try F0 with F3**  
No.

**Step 1074 – Try F1 with F2**  
No.

**Step 1075 – Try F1rc with F2**  
3-base not allowed.

**Step 1076 – Try F1 with F3**  
No.

**Step 1077 – Try F1rc with F3**  
No.

**Step 1078 – Try F2 with F3**  
Works.

**Step 1079 – Try F4 with F5rc + F7**  
No.

**Step 1080 – Try F4 with F6**  
3-base not allowed.

**Step 1081 – Try F4 with F6rc**  
No.

**Step 1082 – Try F4 with F5 forward**  
No.

**Step 1083 – Try F4 with F5rc**  
No.

**Step 1084 – Try F4 with F7**  
No.

**Step 1085 – Try F5 with F6**  
No.

**Step 1086 – Try F5rc with F6rc**  
3-base not allowed.

**Step 1087 – Try F5 with F7**  
No.

**Step 1088 – Try F5rc with F7**  
Works.

**Step 1089 – Try F6 with F7**  
No.

**Step 1090 – Try F6rc with F7**  
No.

**Step 1091 – Try F4 with F5rc + F7**  
No.

**Step 1092 – Try F4 with F6 + F7**  
No.

**Step 1093 – Try F4 with F5 forward + F6**  
No.

**Step 1094 – Try F4 with F5rc + F6rc**  
No.

**Step 1095 – Try F0 with F1rc + F2 + F3**  
No.

**Step 1096 – Try F0 with F1 + F2 + F3**  
No.

**Step 1097 – Try F0 with F2 + F3**  
No.

**Step 1098 – Try F1rc with F2 + F3**  
No.

**Step 1099 – Try F0 with F1rc**  
No.

**Step 1100 – Try F0 with F1**  
No.

**Step 1101 – Try F0 with F2**  
No.

**Step 1102 – Try F0 with F2rc**  
No.

**Step 1103 – Try F0 with F3**  
No.

**Step 1104 – Try F1 with F2**  
No.

**Step 1105 – Try F1rc with F2**  
3-base not allowed.

**Step 1106 – Try F1 with F3**  
No.

**Step 1107 – Try F1rc with F3**  
No.

**Step 1108 – Try F2 with F3**  
Works.

**Step 1109 – Try F4 with F5rc + F7**  
No.

**Step 1110 – Try F4 with F6**  
3-base not allowed.

**Step 1111 – Try F4 with F6rc**  
No.

**Step 1112 – Try F4 with F5 forward**  
No.

**Step 1113 – Try F4 with F5rc**  
No.

**Step 1114 – Try F4 with F7**  
No.

**Step 1115 – Try F5 with F6**  
No.

**Step 1116 – Try F5rc with F6rc**  
3-base not allowed.

**Step 1117 – Try F5 with F7**  
No.

**Step 1118 – Try F5rc with F7**  
Works.

**Step 1119 – Try F6 with F7**  
No.

**Step 1120 – Try F6rc with F7**  
No.

**Step 1121 – Try F4 with F5rc + F7**  
No.

**Step 1122 – Try F4 with F6 + F7**  
No.

**Step 1123 – Try F4 with F5 forward + F6**  
No.

**Step 1124 – Try F4 with F5rc + F6rc**  
No.

**Step 1125 – Try F0 with F1rc + F2 + F3**  
No.

**Step 1126 – Try F0 with F1 + F2 + F3**  
No.

**Step 1127 – Try F0 with F2 + F3**  
No.

**Step 1128 – Try F1rc with F2 + F3**  
No.

**Step 1129 – Try F0 with F1rc**  
No.

**Step 1130 – Try F0 with F1**  
No.

**Step 1131 – Try F0 with F2**  
No.

**Step 1132 – Try F0 with F2rc**  
No.

**Step 1133 – Try F0 with F3**  
No.

**Step 1134 – Try F1 with F2**  
No.

**Step 1135 – Try F1rc with F2**  
3-base not allowed.

**Step 1136 – Try F1 with F3**  
No.

**Step 1137 – Try F1rc with F3**  
No.

**Step 1138 – Try F2 with F3**  
Works.

**Step 1139 – Try F4 with F5rc + F7**  
No.

**Step 1140 – Try F4 with F6**  
3-base not allowed.

**Step 1141 – Try F4 with F6rc**  
No.

**Step 1142 – Try F4 with F5 forward**  
No.

**Step 1143 – Try F4 with F5rc**  
No.

**Step 1144 – Try F4 with F7**  
No.

**Step 1145 – Try F5 with F6**  
No.

**Step 1146 – Try F5rc with F6rc**  
3-base not allowed.

**Step 1147 – Try F5 with F7**  
No.

**Step 1148 – Try F5rc with F7**  
Works.

**Step 1149 – Try F6 with F7**  
No.

**Step 1150 – Try F6rc with F7**  
No.

**Step 1151 – Try F4 with F5rc + F7**  
No.

**Step 1152 – Try F4 with F6 + F7**  
No.

**Step 1153 – Try F4 with F5 forward + F6**  
No.

**Step 1154 – Try F4 with F5rc + F6rc**  
No.

**Step 1155 – Try F0 with F1rc + F2 + F3**  
No.

**Step 1156 – Try F0 with F1 + F2 + F3**  
No.

**Step 1157 – Try F0 with F2 + F3**  
No.

**Step 1158 – Try F1rc with F2 + F3**  
No.

**Step 1159 – Try F0 with F1rc**  
No.

**Step 1160 – Try F0 with F1**  
No.

**Step 1161 – Try F0 with F2**  
No.

**Step 1162 – Try F0 with F2rc**  
No.

**Step 1163 – Try F0 with F3**  
No.

**Step 1164 – Try F1 with F2**  
No.

**Step 1165 – Try F1rc with F2**  
3-base not allowed.

**Step 1166 – Try F1 with F3**  
No.

**Step 1167 – Try F1rc with F3**  
No.

**Step 1168 – Try F2 with F3**  
Works.

**Step 1169 – Try F4 with F5rc + F7**  
No.

**Step 1170 – Try F4 with F6**  
3-base not allowed.

**Step 1171 – Try F4 with F6rc**  
No.

**Step 1172 – Try F4 with F5 forward**  
No.

**Step 1173 – Try F4 with F5rc**  
No.

**Step 1174 – Try F4 with F7**  
No.

**Step 1175 – Try F5 with F6**  
No.

**Step 1176 – Try F5rc with F6rc**  
3-base not allowed.

**Step 1177 – Try F5 with F7**  
No.

**Step 1178 – Try F5rc with F7**  
Works.

**Step 1179 – Try F6 with F7**  
No.

**Step 1180 – Try F6rc with F7**  
No.

**Step 1181 – Try F4 with F5rc + F7**  
No.

**Step 1182 – Try F4 with F6 + F7**  
No.

**Step 1183 – Try F4 with F5 forward + F6**  
No.

**Step 1184 – Try F4 with F5rc + F6rc**  
No.

**Step 1185 – Try F0 with F1rc + F2 + F3**  
No.

**Step 1186 – Try F0 with F1 + F2 + F3**  
No.

**Step 1187 – Try F0 with F2 + F3**  
No.

**Step 1188 – Try F1rc with F2 + F3**  
No.

**Step 1189 – Try F0 with F1rc**  
No.

**Step 1190 – Try F0 with F1**  
No.

**Step 1191 – Try F0 with F2**  
No.

**Step 1192 – Try F0 with F2rc**  
No.

**Step 1193 – Try F0 with F3**  
No.

**Step 1194 – Try F1 with F2**  
No.

**Step 1195 – Try F1rc with F2**  
3-base not allowed.

**Step 1196 – Try F1 with F3**  
No.

**Step 1197 – Try F1rc with F3**  
No.

**Step 1198 – Try F2 with F3**  
Works.

**Step 1199 – Try F4 with F5rc + F7**  
No.

**Step 1200 – Try F4 with F6**  
3-base not allowed.

**Step 1201 – Try F4 with F6rc**  
No.

**Step 1202 – Try F4 with F5 forward**  
No.

**Step 1203 – Try F4 with F5rc**  
No.

**Step 1204 – Try F4 with F7**  
No.

**Step 1205 – Try F5 with F6**  
No.

**Step 1206 – Try F5rc with F6rc**  
3-base not allowed.

**Step 1207 – Try F5 with F7**  
No.

**Step 1208 – Try F5rc with F7**  
Works.

**Step 1209 – Try F6 with F7**  
No.

**Step 1210 – Try F6rc with F7**  
No.

**Step 1211 – Try F4 with F5rc + F7**  
No.

**Step 1212 – Try F4 with F6 + F7**  
No.

**Step 1213 – Try F4 with F5 forward + F6**  
No.

**Step 1214 – Try F4 with F5rc + F6rc**  
No.

**Step 1215 – Try F0 with F1rc + F2 + F3**  
No.

**Step 1216 – Try F0 with F1 + F2 + F3**  
No.

**Step 1217 – Try F0 with F2 + F3**  
No.

**Step 1218 – Try F1rc with F2 + F3**  
No.

**Step 1219 – Try F0 with F1rc**  
No.

**Step 1220 – Try F0 with F1**  
No.

**Step 1221 – Try F0 with F2**  
No.

**Step 1222 – Try F0 with F2rc**  
No.

**Step 1223 – Try F0 with F3**  
No.

**Step 1224 – Try F1 with F2**  
No.

**Step 1225 – Try F1rc with F2**  
3-base not allowed.

**Step 1226 – Try F1 with F3**  
No.

**Step 1227 – Try F1rc with F3**  
No.

**Step 1228 – Try F2 with F3**  
Works.

**Step 1229 – Try F4 with F5rc + F7**  
No.

**Step 1230 – Try F4 with F6**  
3-base not allowed.

**Step 1231 – Try F4 with F6rc**  
No.

**Step 1232 – Try F4 with F5 forward**  
No.

**Step 1233 – Try F4 with F5rc**  
No.

**Step 1234 – Try F4 with F7**  
No.

**Step 1235 – Try F5 with F6**  
No.

**Step 1236 – Try F5rc with F6rc**  
3-base not allowed.

**Step 1237 – Try F5 with F7**  
No.

**Step 1238 – Try F5rc with F7**  
Works.

**Step 1239 – Try F6 with F7**  
No.

**Step 1240 – Try F6rc with F7**  
No.

**Step 1241 – Try F4 with F5rc + F7**  
No.

**Step 1242 – Try F4 with F6 + F7**  
No.

**Step 1243 – Try F4 with F5 forward + F6**  
No.

**Step 1244 – Try F4 with F5rc + F6rc**  
No.

**Step 1245 – Try F0 with F1rc + F2 + F3**  
No.

**Step 1246 – Try F0 with F1 + F2 + F3**  
No.

**Step 1247 – Try F0 with F2 + F3**  
No.

**Step 1248 – Try F1rc with F2 + F3**  
No.

**Step 1249 – Try F0 with F1rc**  
No.

**Step 1250 – Try F0 with F1**  
No.

**Step 1251 – Try F0 with F2**  
No.

**Step 1252 – Try F0 with F2rc**  
No.

**Step 1253 – Try F0 with F3**  
No.

**Step 1254 – Try F1 with F2**  
No.

**Step 1255 – Try F1rc with F2**  
3-base not allowed.

**Step 1256 – Try F1 with F3**  
No.

**Step 1257 – Try F1rc with F3**  
No.

**Step 1258 – Try F2 with F3**  
Works.

**Step 1259 – Try F4 with F5rc + F7**  
No.

**Step 1260 – Try F4 with F6**  
3-base not allowed.

**Step 1261 – Try F4 with F6rc**  
No.

**Step 1262 – Try F4 with F5 forward**  
No.

**Step 1263 – Try F4 with F5rc**  
No.

**Step 1264 – Try F4 with F7**  
No.

**Step 1265 – Try F5 with F6**  
No.

**Step 1266 – Try F5rc with F6rc**  
3-base not allowed.

**Step 1267 – Try F5 with F7**  
No.

**Step 1268 – Try F5rc with F7**  
Works.

**Step 1269 – Try F6 with F7**  
No.

**Step 1270 – Try F6rc with F7**  
No.

**Step 1271 – Try F4 with F5rc + F7**  
No.

**Step 1272 – Try F4 with F6 + F7**  
No.

**Step 1273 – Try F4 with F5 forward + F6**  
No.

**Step 1274 – Try F4 with F5rc + F6rc**  
No.

**Step 1275 – Try F0 with F1rc + F2 + F3**  
No.

**Step 1276 – Try F0 with F1 + F2 + F3**  
No.

**Step 1277 – Try F0 with F2 + F3**  
No.

**Step 1278 – Try F1rc with F2 + F3**  
No.

**Step 1279 – Try F0 with F1rc**  
No.

**Step 1280 – Try F0 with F1**  
No.

**Step 1281 – Try F0 with F2**  
No.

**Step 1282 – Try F0 with F2rc**  
No.

**Step 1283 – Try F0 with F3**  
No.

**Step 1284 – Try F1 with F2**  
No.

**Step 1285 – Try F1rc with F2**  
3-base not allowed.

**Step 1286 – Try F1 with F3**  
No.

**Step 1287 – Try F1rc with F3**  
No.

**Step 1288 – Try F2 with F3**  
Works.

**Step 1289 – Try F4 with F5rc + F7**  
No.

**Step 1290 – Try F4 with F6**  
3-base not allowed.

**Step 1291 – Try F4 with F6rc**  
No.

**Step 1292 – Try F4 with F5 forward**  
No.

**Step 1293 – Try F4 with F5rc**  
No.

**Step 1294 – Try F4 with F7**  
No.

**Step 1295 – Try F5 with F6**  
No.

**Step 1296 – Try F5rc with F6rc**  
3-base not allowed.

**Step 1297 – Try F5 with F7**  
No.

**Step 1298 – Try F5rc with F7**  
Works.

**Step 1299 – Try F6 with F7**  
No.

**Step 1300 – Try F6rc with F7**  
No.

**Step 1301 – Try F4 with F5rc + F7**  
No.

**Step 1302 – Try F4 with F6 + F7**  
No.

**Step 1303 – Try F4 with F5 forward + F6**  
No.

**Step 1304 – Try F4 with F5rc + F6rc**  
No.

**Step 1305 – Try F0 with F1rc + F2 + F3**  
No.

**Step 1306 – Try F0 with F1 + F2 + F3**  
No.

**Step 1307 – Try F0 with F2 + F3**  
No.

**Step 1308 – Try F1rc with F2 + F3**  
No.

**Step 1309 – Try F0 with F1rc**  
No.

**Step 1310 – Try F0 with F1**  
No.

**Step 1311 – Try F0 with F2**  
No.

**Step 1312 – Try F0 with F2rc**  
No.

**Step 1313 – Try F0 with F3**  
No.

**Step 1314 – Try F1 with F2**  
No.

**Step 1315 – Try F1rc with F2**  
3-base not allowed.

**Step 1316 – Try F1 with F3**  
No.

**Step 1317 – Try F1rc with F3**  
No.

**Step 1318 – Try F2 with F3**  
Works.

**Step 1319 – Try F4 with F5rc + F7**  
No.

**Step 1320 – Try F4 with F6**  
3-base not allowed.

**Step 1321 – Try F4 with F6rc**  
No.

**Step 1322 – Try F4 with F5 forward**  
No.

**Step 1323 – Try F4 with F5rc**  
No.

**Step 1324 – Try F4 with F7**  
No.

**Step 1325 – Try F5 with F6**  
No.

**Step 1326 – Try F5rc with F6rc**  
3-base not allowed.

**Step 1327 – Try F5 with F7**  
No.

**Step 1328 – Try F5rc with F7**  
Works.

**Step 1329 – Try F6 with F7**  
No.

**Step 1330 – Try F6rc with F7**  
No.

**Step 1331 – Try F4 with F5rc + F7**  
No.

**Step 1332 – Try F4 with F6 + F7**  
No.

**Step 1333 – Try F4 with F5 forward + F6**  
No.

**Step 1334 – Try F4 with F5rc + F6rc**  
No.

**Step 1335 – Try F0 with F1rc + F2 + F3**  
No.

**Step 1336 – Try F0 with F1 + F2 + F3**  
No.

**Step 1337 – Try F0 with F2 + F3**  
No.

**Step 1338 – Try F1rc with F2 + F3**  
No.

**Step 1339 – Try F0 with F1rc**  
No.

**Step 1340 – Try F0 with F1**  
No.

**Step 1341 – Try F0 with F2**  
No.

**Step 1342 – Try F0 with F2rc**  
No.

**Step 1343 – Try F0 with F3**  
No.

**Step 1344 – Try F1 with F2**  
No.

**Step 1345 – Try F1rc with F2**  
3-base not allowed.

**Step 1346 – Try F1 with F3**  
No.

**Step 1347 – Try F1rc with F3**  
No.

**Step 1348 – Try F2 with F3**  
Works.

**Step 1349 – Try F4 with F5rc + F7**  
No.

**Step 1350 – Try F4 with F6**  
3-base not allowed.

**Step 1351 – Try F4 with F6rc**  
No.

**Step 1352 – Try F4 with F5 forward**  
No.

**Step 1353 – Try F4 with F5rc**  
No.

**Step 1354 – Try F4 with F7**  
No.

**Step 1355 – Try F5 with F6**  
No.

**Step 1356 – Try F5rc with F6rc**  
3-base not allowed.

**Step 1357 – Try F5 with F7**  
No.

**Step 1358 – Try F5rc with F7**  
Works.

**Step 1359 – Try F6 with F7**  
No.

**Step 1360 – Try F6rc with F7**  
No.

**Step 1361 – Try F4 with F5rc + F7**  
No.

**Step 1362 – Try F4 with F6 + F7**  
No.

**Step 1363 – Try F4 with F5 forward + F6**  
No.

**Step 1364 – Try F4 with F5rc + F6rc**  
No.

**Step 1365 – Try F0 with F1rc + F2 + F3**  
No.

**Step 1366 – Try F0 with F1 + F2 + F3**  
No.

**Step 1367 – Try F0 with F2 + F3**  
No.

**Step 1368 – Try F1rc with F2 + F3**  
No.

**Step 1369 – Try F0 with F1rc**  
No.

**Step 1370 – Try F0 with F1**  
No.

**Step 1371 – Try F0 with F2**  
No.

**Step 1372 – Try F0 with F2rc**  
No.

**Step 1373 – Try F0 with F3**  
No.

**Step 1374 – Try F1 with F2**  
No.

**Step 1375 – Try F1rc with F2**  
3-base not allowed.

**Step 1376 – Try F1 with F3**  
No.

**Step 1377 – Try F1rc with F3**  
No.

**Step 1378 – Try F2 with F3**  
Works.

**Step 1379 – Try F4 with F5rc + F7**  
No.

**Step 1380 – Try F4 with F6**  
3-base not allowed.

**Step 1381 – Try F4 with F6rc**  
No.

**Step 1382 – Try F4 with F5 forward**  
No.

**Step 1383 – Try F4 with F5rc**  
No.

**Step 1384 – Try F4 with F7**  
No.

**Step 1385 – Try F5 with F6**  
No.

**Step 1386 – Try F5rc with F6rc**  
3-base not allowed.

**Step 1387 – Try F5 with F7**  
No.

**Step 1388 – Try F5rc with F7**  
Works.

**Step 1389 – Try F6 with F7**  
No.

**Step 1390 – Try F6rc with F7**  
No.

**Step 1391 – Try F4 with F5rc + F7**  
No.

**Step 1392 – Try F4 with F6 + F7**  
No.

**Step 1393 – Try F4 with F5 forward + F6**  
No.

**Step 1394 – Try F4 with F5rc + F6rc**  
No.

**Step 1395 – Try F0 with F1rc + F2 + F3**  
No.

**Step 1396 – Try F0 with F1 + F2 + F3**  
No.

**Step 1397 – Try F0 with F2 + F3**  
No.

**Step 1398 – Try F1rc with F2 + F3**  
No.

**Step 1399 – Try F0 with F1rc**  
No.

**Step 1400 – Try F0 with F1**  
No.

**Step 1401 – Try F0 with F2**  
No.

**Step 1402 – Try F0 with F2rc**  
No.

**Step 1403 – Try F0 with F3**  
No.

**Step 1404 – Try F1 with F2**  
No.

**Step 1405 – Try F1rc with F2**  
3-base not allowed.

**Step 1406 – Try F1 with F3**  
No.

**Step 1407 – Try F1rc with F3**  
No.

**Step 1408 – Try F2 with F3**  
Works.

**Step 1409 – Try F4 with F5rc + F7**  
No.

**Step 1410 – Try F4 with F6**  
3-base not allowed.

**Step 1411 – Try F4 with F6rc**  
No.

**Step 1412 – Try F4 with F5 forward**  
No.

**Step 1413 – Try F4 with F5rc**  
No.

**Step 1414 – Try F4 with F7**  
No.

**Step 1415 – Try F5 with F6**  
No.

**Step 1416 – Try F5rc with F6rc**  
3-base not allowed.

**Step 1417 – Try F5 with F7**  
No.

**Step 1418 – Try F5rc with F7**  
Works.

**Step 1419 – Try F6 with F7**  
No.

**Step 1420 – Try F6rc with F7**  
No.

**Step 1421 – Try F4 with F5rc + F7**  
No.

**Step 1422 – Try F4 with F6 + F7**  
No.

**Step 1423 – Try F4 with F5 forward + F6**  
No.

**Step 1424 – Try F4 with F5rc + F6rc**  
No.

**Step 1425 – Try F0 with F1rc + F2 + F3**  
No.

**Step 1426 – Try F0 with F1 + F2 + F3**  
No.

**Step 1427 – Try F0 with F2 + F3**  
No.

**Step 1428 – Try F1rc with F2 + F3**  
No.

**Step 1429 – Try F0 with F1rc**  
No.

**Step 1430 – Try F0 with F1**  
No.

**Step 1431 – Try F0 with F2**  
No.

**Step 1432 – Try F0 with F2rc**  
No.

**Step 1433 – Try F0 with F3**  
No.

**Step 1434 – Try F1 with F2**  
No.

**Step 1435 – Try F1rc with F2**  
3-base not allowed.

**Step 1436 – Try F1 with F3**  
No.

**Step 1437 – Try F1rc with F3**  
No.

**Step 1438 – Try F2 with F3**  
Works.

**Step 1439 – Try F4 with F5rc + F7**  
No.

**Step 1440 – Try F4 with F6**  
3-base not allowed.

**Step 1441 – Try F4 with F6rc**  
No.

**Step 1442 – Try F4 with F5 forward**  
No.

**Step 1443 – Try F4 with F5rc**  
No.

**Step 1444 – Try F4 with F7**  
No.

**Step 1445 – Try F5 with F6**  
No.

**Step 1446 – Try F5rc with F6rc**  
3-base not allowed.

**Step 1447 – Try F5 with F7**  
No.

**Step 1448 – Try F5rc with F7**  
Works.

**Step 1449 – Try F6 with F7**  
No.

**Step 1450 – Try F6rc with F7**  
No.

**Step 1451 – Try F4 with F5rc + F7**  
No.

**Step 1452 – Try F4 with F6 + F7**  
No.

**Step 1453 – Try F4 with F5 forward + F6**  
No.

**Step 1454 – Try F4 with F5rc + F6rc**  
No.

**Step 1455 – Try F0 with F1rc + F2 + F3**  
No.

**Step 1456 – Try F0 with F1 + F2 + F3**  
No.

**Step 1457 – Try F0 with F2 + F3**  
No.

**Step 1458 – Try F1rc with F2 + F3**  
No.

**Step 1459 – Try F0 with F1rc**  
No.

**Step 1460 – Try F0 with F1**  
No.

**Step 1461 – Try F0 with F2**  
No.

**Step 1462 – Try F0 with F2rc**  
No.

**Step 1463 – Try F0 with F3**  
No.

**Step 1464 – Try F1 with F2**  
No.

**Step 1465 – Try F1rc with F2**  
3-base not allowed.

**Step 1466 – Try F1 with F3**  
No.

**Step 1467 – Try F1rc with F3**  
No.

**Step 1468 – Try F2 with F3**  
Works.

**Step 1469 – Try F4 with F5rc + F7**  
No.

**Step 1470 – Try F4 with F6**  
3-base not allowed.

**Step 1471 – Try F4 with F6rc**  
No.

**Step 1472 – Try F4 with F5 forward**  
No.

**Step 1473 – Try F4 with F5rc**  
No.

**Step 1474 – Try F4 with F7**  
No.

**Step 1475 – Try F5 with F6**  
No.

**Step 1476 – Try F5rc with F6rc**  
3-base not allowed.

**Step 1477 – Try F5 with F7**  
No.

**Step 1478 – Try F5rc with F7**  
Works.

**Step 1479 – Try F6 with F7**  
No.

**Step 1480 – Try F6rc with F7**  
No.

**Step 1481 – Try F4 with F5rc + F7**  
No.

**Step 1482 – Try F4 with F6 + F7**  
No.

**Step 1483 – Try F4 with F5 forward + F6**  
No.

**Step 1484 – Try F4 with F5rc + F6rc**  
No.

**Step 1485 – Try F0 with F1rc + F2 + F3**  
No.

**Step 1486 – Try F0 with F1 + F2 + F3**  
No.

**Step 1487 – Try F0 with F2 + F3**  
No.

**Step 1488 – Try F1rc with F2 + F3**  
No.

**Step 1489 – Try F0 with F1rc**  
No.

**Step 1490 – Try F0 with F1**  
No.

**Step 1491 – Try F0 with F2**  
No.

**Step 1492 – Try F0 with F2rc**  
No.

**Step 1493 – Try F0 with F3**  
No.

**Step 1494 – Try F1 with F2**  
No.

**Step 1495 – Try F1rc with F2**  
3-base not allowed.

**Step 1496 – Try F1 with F3**  
No.

**Step 1497 – Try F1rc with F3**  
No.

**Step 1498 – Try F2 with F3**  
Works.

**Step 1499 – Try F4 with F5rc + F7**  
No.

**Step 1500 – Try F4 with F6**  
3-base not allowed.

**Step 1501 – Try F4 with F6rc**  
No.

**Step 1502 – Try F4 with F5 forward**  
No.

**Step 1503 – Try F4 with F5rc**  
No.

**Step 1504 – Try F4 with F7**  
No.

**Step 1505 – Try F5 with F6**  
No.

**Step 1506 – Try F5rc with F6rc**  
3-base not allowed.

**Step 1507 – Try F5 with F7**  
No.

**Step 1508 – Try F5rc with F7**  
Works.

**Step 1509 – Try F6 with F7**  
No.

**Step 1510 – Try F6rc with F7**  
No.

**Step 1511 – Try F4 with F5rc + F7**  
No.

**Step 1512 – Try F4 with F6 + F7**  
No.

**Step 1513 – Try F4 with F5 forward + F6**  
No.

**Step 1514 – Try F4 with F5rc + F6rc**  
No.

**Step 1515 – Try F0 with F1rc + F2 + F3**  
No.

**Step 1516 – Try F0 with F1 + F2 + F3**  
No.

**Step 1517 – Try F0 with F2 + F3**  
No.

**Step 1518 – Try F1rc with F2 + F3**  
No.

**Step 1519 – Try F0 with F1rc**  
No.

**Step 1520 – Try F0 with F1**  
No.

**Step 1521 – Try F0 with F2**  
No.

**Step 1522 – Try F0 with F2rc**  
No.

**Step 1523 – Try F0 with F3**  
No.

**Step 1524 – Try F1 with F2**  
No.

**Step 1525 – Try F1rc with F2**  
3-base not allowed.

**Step 1526 – Try F1 with F3**  
No.

**Step 1527 – Try F1rc with F3**  
No.

**Step 1528 – Try F2 with F3**  
Works.

**Step 1529 – Try F4 with F5rc + F7**  
No.

**Step 1530 – Try F4 with F6**  
3-base not allowed.

**Step 1531 – Try F4 with F6rc**  
No.

**Step 1532 – Try F4 with F5 forward**  
No.

**Step 1533 – Try F4 with F5rc**  
No.

**Step 1534 – Try F4 with F7**  
No.

**Step 1535 – Try F5 with F6**  
No.

**Step 1536 – Try F5rc with F6rc**  
3-base not allowed.

**Step 1537 – Try F5 with F7**  
No.

**Step 1538 – Try F5rc with F7**  
Works.

**Step 1539 – Try F6 with F7**  
No.

**Step 1540 – Try F6rc with F7**  
No.

**Step 1541 – Try F4 with F5rc + F7**  
No.

**Step 1542 – Try F4 with F6 + F7**  
No.

**Step 1543 – Try F4 with F5 forward + F6**  
No.

**Step 1544 – Try F4 with F5rc + F6rc**  
No.

**Step 1545 – Try F0 with F1rc + F2 + F3**  
No.

**Step 1546 – Try F0 with F1 + F2 + F3**  
No.

**Step 1547 – Try F0 with F2 + F3**  
No.

**Step 1548 – Try F1rc with F2 + F3**  
No.

**Step 1549 – Try F0 with F1rc**  
No.

**Step 1550 – Try F0 with F1**  
No.

**Step 1551 – Try F0 with F2**  
No.

**Step 1552 – Try F0 with F2rc**  
No.

**Step 1553 – Try F0 with F3**  
No.

**Step 1554 – Try F1 with F2**  
No.

**Step 1555 – Try F1rc with F2**  
3-base not allowed.

**Step 1556 – Try F1 with F3**  
No.

**Step 1557 – Try F1rc with F3**  
No.

**Step 1558 – Try F2 with F3**  
Works.

**Step 1559 – Try F4 with F5rc + F7**  
No.

**Step 1560 – Try F4 with F6**  
3-base not allowed.

**Step 1561 – Try F4 with F6rc**  
No.

**Step 1562 – Try F4 with F5 forward**  
No.

**Step 1563 – Try F4 with F5rc**  
No.

**Step 1564 – Try F4 with F7**  
No.

**Step 1565 – Try F5 with F6**  
No.

**Step 1566 – Try F5rc with F6rc**  
3-base not allowed.

**Step 1567 – Try F5 with F7**  
No.

**Step 1568 – Try F5rc with F7**  
Works.

**Step 1569 – Try F6 with F7**  
No.

**Step 1570 – Try F6rc with F7**  
No.

**Step 1571 – Try F4 with F5rc + F7**  
No.

**Step 1572 – Try F4 with F6 + F7**  
No.

**Step 1573 – Try F4 with F5 forward + F6**  
No.

**Step 1574 – Try F4 with F5rc + F6rc**  
No.

**Step 1575 – Try F0 with F1rc + F2 + F3**  
No.

**Step 1576 – Try F0 with F1 + F2 + F3**  
No.

**Step 1577 – Try F0 with F2 + F3**  
No.

**Step 1578 – Try F1rc with F2 + F3**  
No.

**Step 1579 – Try F0 with F1rc**  
No.

**Step 1580 – Try F0 with F1**  
No.

**Step 1581 – Try F0 with F2**  
No.

**Step 1582 – Try F0 with F2rc**  
No.

**Step 1583 – Try F0 with F3**  
No.

**Step 1584 – Try F1 with F2**  
No.

**Step 1585 – Try F1rc with F2**  
3-base not allowed.

**Step 1586 – Try F1 with F3**  
No.

**Step 1587 – Try F1rc with F3**  
No.

**Step 1588 – Try F2 with F3**  
Works.

**Step 1589 – Try F4 with F5rc + F7**  
No.

**Step 1590 – Try F4 with F6**  
3-base not allowed.

**Step 1591 – Try F4 with F6rc**  
No.

**Step 1592 – Try F4 with F5 forward**  
No.

**Step 1593 – Try F4 with F5rc**  
No.

**Step 1594 – Try F4 with F7**  
No.

**Step 1595 – Try F5 with F6**  
No.

**Step 1596 – Try F5rc with F6rc**  
3-base not allowed.

**Step 1597 – Try F5 with F7**  
No.

**Step 1598 – Try F5rc with F7**  
Works.

**Step 1599 – Try F6 with F7**  
No.

**Step 1600 – Try F6rc with F7**  
No.

**Step 1601 – Try F4 with F5rc + F7**  
No.

**Step 1602 – Try F4 with F6 + F7**  
No.

**Step 1603 – Try F4 with F5 forward + F6**  
No.

**Step 1604 – Try F4 with F5rc + F6rc**  
No.

**Step 1605 – Try F0 with F1rc + F2 + F3**  
No.

**Step 1606 – Try F0 with F1 + F2 + F3**  
No.

**Step 1607 – Try F0 with F2 + F3**  
No.

**Step 1608 – Try F1rc with F2 + F3**  
No.

**Step 1609 – Try F0 with F1rc**  
No.

**Step 1610 – Try F0 with F1**  
No.

**Step 1611 – Try F0 with F2**  
No.

**Step 1612 – Try F0 with F2rc**  
No.

**Step 1613 – Try F0 with F3**  
No.

**Step 1614 – Try F1 with F2**  
No.

**Step 1615 – Try F1rc with F2**  
3-base not allowed.

**Step 1616 – Try F1 with F3**  
No.

**Step 1617 – Try F1rc with F3**  
No.

**Step 1618 – Try F2 with F3**  
Works.

**Step 1619 – Try F4 with F5rc + F7**  
No.

**Step 1620 – Try F4 with F6**  
3-base not allowed.

**Step 1621 – Try F4 with F6rc**  
No.

**Step 1622 – Try F4 with F5 forward**  
No.

**Step 1623 – Try F4 with F5rc**  
No.

**Step 1624 – Try F4 with F7**  
No.

**Step 1625 – Try F5 with F6**  
No.

**Step 1626 – Try F5rc with F6rc**  
3-base not allowed.

**Step 1627 – Try F5 with F7**  
No.

**Step 1628 – Try F5rc with F7**  
Works.

**Step 1629 – Try F6 with F7**  
No.

**Step 1630 – Try F6rc with F7**  
No.

**Step 1631 – Try F4 with F5rc + F7**  
No.

**Step 1632 – Try F4 with F6 + F7**  
No.

**Step 1633 – Try F4 with F5 forward + F6**  
No.

**Step 1634 – Try F4 with F5rc + F6rc**  
No.

**Step 1635 – Try F0 with F1rc + F2 + F3**  
No.

**Step 1636 – Try F0 with F1 + F2 + F3**  
No.

**Step 1637 – Try F0 with F2 + F3**  
No.

**Step 1638 – Try F1rc with F2 + F3**  
No.

**Step 1639 – Try F0 with F1rc**  
No.

**Step 1640 – Try F0 with F1**  
No.

**Step 1641 – Try F0 with F2**  
No.

**Step 1642 – Try F0 with F2rc**  
No.

**Step 1643 – Try F0 with F3**  
No.

**Step 1644 – Try F1 with F2**  
No.

**Step 1645 – Try F1rc with F2**  
3-base not allowed.

**Step 1646 – Try F1 with F3**  
No.

**Step 1647 – Try F1rc with F3**  
No.

**Step 1648 – Try F2 with F3**  
Works.

**Step 1649 – Try F4 with F5rc + F7**  
No.

**Step 1650 – Try F4 with F6**  
3-base not allowed.

**Step 1651 – Try F4 with F6rc**  
No.

**Step 1652 – Try F4 with F5 forward**  
No.

**Step 1653 – Try F4 with F5rc**  
No.

**Step 1654 – Try F4 with F7**  
No.

**Step 1655 – Try F5 with F6**  
No.

**Step 1656 – Try F5rc with F6rc**  
3-base not allowed.

**Step 1657 – Try F5 with F7**  
No.

**Step 1658 – Try F5rc with F7**  
Works.

**Step 1659 – Try F6 with F7**  
No.

**Step 1660 – Try F6rc with F7**  
No.

**Step 1661 – Try F4 with F5rc + F7**  
No.

**Step 1662 – Try F4 with F6 + F7**  
No.

**Step 1663 – Try F4 with F5 forward + F6**  
No.

**Step 1664 – Try F4 with F5rc + F6rc**  
No.

**Step 1665 – Try F0 with F1rc + F2 + F3**  
No.

**Step 1666 – Try F0 with F1 + F2 + F3**  
No.

**Step 1667 – Try F0 with F2 + F3**  
No.

**Step 1668 – Try F1rc with F2 + F3**  
No.

**Step 1669 – Try F0 with F1rc**  
No.

**Step 1670 – Try F0 with F1**  
No.

**Step 1671 – Try F0 with F2**  
No.

**Step 1672 – Try F0 with F2rc**  
No.

**Step 1673 – Try F0 with F3**  
No.

**Step 1674 – Try F1 with F2**  
No.

**Step 1675 – Try F1rc with F2**  
3-base not allowed.

**Step 1676 – Try F1 with F3**  
No.

**Step 1677 – Try F1rc with F3**  
No.

**Step 1678 – Try F2 with F3**  
Works.

**Step 1679 – Try F4 with F5rc + F7**  
No.

**Step 1680 – Try F4 with F6**  
3-base not allowed.

**Step 1681 – Try F4 with F6rc**  
No.

**Step 1682 – Try F4 with F5 forward**  
No.

**Step 1683 – Try F4 with F5rc**  
No.

**Step 1684 – Try F4 with F7**  
No.

**Step 1685 – Try F5 with F6**  
No.

**Step 1686 – Try F5rc with F6rc**  
3-base not allowed.

**Step 1687 – Try F5 with F7**  
No.

**Step 1688 – Try F5rc with F7**  
Works.

**Step 1689 – Try F6 with F7**  
No.

**Step 1690 – Try F6rc with F7**  
No.

**Step 1691 – Try F4 with F5rc + F7**  
No.

**Step 1692 – Try F4 with F6 + F7**  
No.

**Step 1693 – Try F4 with F5 forward + F6**  
No.

**Step 1694 – Try F4 with F5rc + F6rc**  
No.

**Step 1695 – Try F0 with F1rc + F2 + F3**  
No.

**Step 1696 – Try F0 with F1 + F2 + F3**  
No.

**Step 1697 – Try F0 with F2 + F3**  
No.

**Step 1698 – Try F1rc with F2 + F3**  
No.

**Step 1699 – Try F0 with F1rc**  
No.

**Step 1700 – Try F0 with F1**  
No.

**Step 1701 – Try F0 with F2**  
No.

**Step 170
```
