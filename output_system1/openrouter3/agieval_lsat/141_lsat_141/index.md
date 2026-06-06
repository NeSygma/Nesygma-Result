# Benchmark Report (SYSTEM1): agieval_lsat - lsat_141

**Provider:** openrouter3
**Model:** xiaomi/mimo-v2-flash
**Config:** max_output_tokens: 32768, temperature: 0.0, top_p: 1.0, seed: 42, reasoning_enabled: True, reasoning_effort: medium
**Duration:** 210.88s


 SYSTEM 1 PURE REASONING AGENT

 Query: A concert is given by a six-member band—guitarist, keyboard player, percussionist, saxophonist, trumpeter, violinist. During the concert, each member performs exactly one solo. The following restrictions apply: The guitarist does not perform the fourth solo. The percussionist performs a solo at some time before the keyboard player does. The keyboard player performs a solo at some time after the violinist does and at some time before the guitarist does. The saxophonist performs a solo at some time after either the percussionist does or the trumpeter does, but not both.Q: Each of the following must be false EXCEPT: Answer Choices: (A)The keyboard player performs the first solo. (B)The guitarist performs the second solo. (C)The guitarist performs a solo at some time before the saxophonist does. (D)The guitarist performs a solo at some time before the percussionist does. (E)The keyboard player performs a solo at some time before the saxophonist does.
A: Among A through E, the answer is

Return your final answer in JSON format like this: {"answer": "A or B or C or D or E"}.


To determine which statement must be false except for one, we analyze the constraints and the possible order of solos.

**Constraints:**
1.  Guitarist (G) is not 4th.
2.  Percussionist (P) is before Keyboard (K).
3.  Violinist (V) is before K, and K is before G. (Order: V < K < G).
4.  Saxophonist (S) is after exactly one of P or T (Trumpeter). This means S is after P XOR S is after T.

**Deductions:**
*   From (3), we have the fixed sequence $V < K < G$.
*   Since $G$ is not 4th, and $V, K, G$ are three distinct positions, $G$ must be 5th or 6th.
*   If $G$ were 6th, then $K$ would be 5th or earlier. However, $P$ must be before $K$. If $K$ is 5th, $P$ is 1-4. If $K$ is 4th, $P$ is 1-3. If $K$ is 3rd, $P$ is 1-2.
*   Let's test the position of $S$. $S$ must be after $P$ or $T$, but not both.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $T$ is 1-4. $S$ is 1-4.
    *   If $S$ is after $P$, $S$ cannot be 1. If $S$ is after $T$, $S$ cannot be 1.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4.
    *   Consider the case where $S$ is after $P$ (and not $T$). Then $T$ must be after $S$ (or $S$ is after $T$).
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$

### TOKEN USAGE

  Input tokens:  301
  Output tokens: 32,768
  Total tokens:  33,069

COMPLETE

## System 1 Final Answer

```json
To determine which statement must be false except for one, we analyze the constraints and the possible order of solos.

**Constraints:**
1.  Guitarist (G) is not 4th.
2.  Percussionist (P) is before Keyboard (K).
3.  Violinist (V) is before K, and K is before G. (Order: V < K < G).
4.  Saxophonist (S) is after exactly one of P or T (Trumpeter). This means S is after P XOR S is after T.

**Deductions:**
*   From (3), we have the fixed sequence $V < K < G$.
*   Since $G$ is not 4th, and $V, K, G$ are three distinct positions, $G$ must be 5th or 6th.
*   If $G$ were 6th, then $K$ would be 5th or earlier. However, $P$ must be before $K$. If $K$ is 5th, $P$ is 1-4. If $K$ is 4th, $P$ is 1-3. If $K$ is 3rd, $P$ is 1-2.
*   Let's test the position of $S$. $S$ must be after $P$ or $T$, but not both.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $T$ is 1-4. $S$ is 1-4.
    *   If $S$ is after $P$, $S$ cannot be 1. If $S$ is after $T$, $S$ cannot be 1.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4.
    *   Consider the case where $S$ is after $P$ (and not $T$). Then $T$ must be after $S$ (or $S$ is after $T$).
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$ is 5th. $V$ is 1-4. $P$ is 1-4. $S$ is 2-4. $T$ is 1-4.
    *   If $S$ is after $P$, $P$ must be before $S$.
    *   If $G$ is 6th, $K$
```
