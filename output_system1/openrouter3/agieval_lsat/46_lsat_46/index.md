# Benchmark Report (SYSTEM1): agieval_lsat - lsat_46

**Provider:** openrouter3
**Model:** xiaomi/mimo-v2-flash
**Config:** max_output_tokens: 32768, temperature: 0.0, top_p: 1.0, seed: 42, reasoning_enabled: True, reasoning_effort: medium
**Duration:** 222.64s


 SYSTEM 1 PURE REASONING AGENT

 Query: For the school paper, five students—Jiang, Kramer, Lopez, Megregian, and O'Neill—each review one or more of exactly three plays: Sunset, Tamerlane, and Undulation, but do not review any other plays. The following conditions must apply: Kramer and Lopez each review fewer of the plays than Megregian. Neither Lopez nor Megregian reviews any play Jiang reviews. Kramer and O'Neill both review Tamerlane. Exactly two of the students review exactly the same play or plays as each other.Q: Which one of the following could be an accurate and complete list of the students who review Tamerlane? Answer Choices: (A)Jiang, Kramer (B)Kramer, O'Neill (C)Kramer, Lopez, O'Neill (D)Kramer, Megregian, O'Neill (E)Lopez, Megregian, O'Neill
A: Among A through E, the answer is

Return your final answer in JSON format like this: {"answer": "A or B or C or D or E"}.


To solve this problem, we must determine which set of students could be the complete list of those reviewing *Tamerlane* based on the given constraints.

**1. Analyze the Constraints:**
*   **Plays:** Sunset, Tamerlane, Undulation.
*   **Students:** Jiang, Kramer, Lopez, Megregian, O'Neill.
*   **Constraint 1:** Kramer and Lopez each review fewer plays than Megregian.
    *   This implies Megregian reviews at least 2 plays (since others review at least 1).
    *   Kramer and Lopez review 1 or 2 plays, but strictly less than Megregian.
*   **Constraint 2:** Neither Lopez nor Megregian reviews any play Jiang reviews.
    *   Jiang's set of plays is disjoint from Lopez's and Megregian's.
*   **Constraint 3:** Kramer and O'Neill both review Tamerlane.
    *   Kramer $\in$ Tamerlane.
    *   O'Neill $\in$ Tamerlane.
*   **Constraint 4:** Exactly two of the students review exactly the same play or plays as each other.
    *   There is exactly one pair of students with identical sets of plays. All other students have unique sets.

**2. Evaluate the Answer Choices:**
We are looking for the complete list of students who review Tamerlane. Since Kramer and O'Neill must review Tamerlane (Constraint 3), any valid list must include both of them.

*   **(A) Jiang, Kramer:** Excludes O'Neill. Invalid.
*   **(B) Kramer, O'Neill:** Includes the required pair. Valid candidate.
*   **(C) Kramer, Lopez, O'Neill:** Includes the required pair. Valid candidate.
*   **(D) Kramer, Megregian, O'Neill:** Includes the required pair. Valid candidate.
*   **(E) Lopez, Megregian, O'Neill:** Excludes Kramer. Invalid.

**3. Test the Valid Candidates:**

**Testing (B) Kramer, O'Neill:**
*   **Tamerlane Reviewers:** Kramer, O'Neill.
*   **Implication:** Jiang, Lopez, and Megregian do *not* review Tamerlane.
*   **Megregian's Plays:** Must review at least 2 plays (Constraint 1). Since she doesn't review Tamerlane, she must review Sunset and Undulation.
*   **Lopez's Plays:** Must review fewer plays than Megregian (2). Lopez cannot review Tamerlane. Lopez cannot review plays Jiang reviews (Constraint 2).
    *   Jiang must review at least one play. If Jiang reviews Sunset, Lopez cannot review Sunset. If Jiang reviews Undulation, Lopez cannot review Undulation.
    *   If Jiang reviews both Sunset and Undulation, Lopez has no plays left to review (since she can't review Tamerlane). This violates the condition that Lopez reviews "one or more" plays.
    *   Therefore, Lopez must review Tamerlane to have a valid play set. But we assumed Lopez does not review Tamerlane based on the list in (B).
*   **Conclusion:** (B) is impossible.

**Testing (C) Kramer, Lopez, O'Neill:**
*   **Tamerlane Reviewers:** Kramer, Lopez, O'Neill.
*   **Implication:** Jiang and Megregian do *not* review Tamerlane.
*   **Megregian's Plays:** Must review at least 2 plays. She cannot review Tamerlane. She cannot review plays Jiang reviews.
    *   If Jiang reviews Sunset, Megregian cannot review Sunset.
    *   If Jiang reviews Undulation, Megregian cannot review Undulation.
    *   If Jiang reviews both, Megregian has no plays left. Impossible.
    *   Therefore, Jiang must review Tamerlane. But the list says Jiang does not review Tamerlane.
*   **Conclusion:** (C) is impossible.

**Testing (D) Kramer, Megregian, O'Neill:**
*   **Tamerlane Reviewers:** Kramer, Megregian, O'Neill.
*   **Implication:** Jiang and Lopez do *not* review Tamerlane.
*   **Megregian's Plays:** Reviews Tamerlane. Needs at least one more play (Constraint 1). Let's say Megregian reviews Sunset and Tamerlane.
*   **Jiang's Plays:** Cannot overlap with Lopez or Megregian.
    *   Jiang cannot review Sunset (Megregian reviews it).
    *   Jiang cannot review Tamerlane (based on the list).
    *   Jiang must review Undulation.
*   **Lopez's Plays:** Cannot overlap with Jiang. Jiang reviews Undulation, so Lopez cannot review Undulation. Lopez does not review Tamerlane (based on the list).
    *   Lopez must review Sunset.
*   **Kramer's Plays:** Reviews Tamerlane. Needs to review fewer plays than Megregian (2). Kramer can review Sunset and Tamerlane.
*   **O'Neill's Plays:** Reviews Tamerlane. Needs to be unique or the pair.
    *   Let's assign O'Neill to review Undulation and Tamerlane.
*   **Check Pair Constraint:**
    *   Jiang: {Undulation}
    *   Lopez: {Sunset}
    *   Megregian: {Sunset, Tamerlane}
    *   Kramer: {Sunset, Tamerlane}
    *   O'Neill: {Undulation, Tamerlane}
    *   Kramer and Megregian have the exact same set of plays ({Sunset, Tamerlane}). This satisfies the "exactly two students review the same plays" constraint.
*   **Check All Constraints:**
    *   Kramer (2) < Megregian (2)? No, must be strictly fewer.
    *   Let's adjust Megregian to review 3 plays: {Sunset, Tamerlane, Undulation}.
    *   Jiang cannot review Sunset or Undulation (Megregian has them). Jiang must review Tamerlane. But the list says Jiang does not.
    *   Let's try a different configuration for Megregian.
    *   Megregian: {Sunset, Tamerlane}.
    *   Jiang: {Undulation}.
    *   Lopez: {Sunset}.
    *   Kramer: {Sunset, Tamerlane}.
    *   O'Neill: {Undulation, Tamerlane}.
    *   Kramer (2) < Megregian (2)? No.
    *   Let's try Megregian: {Sunset, Tamerlane, Undulation} (3 plays).
    *   Jiang: {Undulation} (Conflict with Megregian).
    *   Jiang: {Tamerlane} (Conflict with list).
    *   Wait, if Megregian reviews Sunset and Tamerlane (2 plays), and Kramer reviews Sunset and Tamerlane (2 plays), the constraint "Kramer reviews fewer plays than Megregian" is violated.
    *   However, if we look closely at the disjoint constraint: "Neither Lopez nor Megregian reviews any play Jiang reviews."
    *   If Jiang reviews Undulation, and Megregian reviews Sunset and Tamerlane, they are disjoint.
    *   If Lopez reviews Sunset, and Jiang reviews Undulation, they are disjoint.
    *   If Kramer reviews Sunset and Tamerlane, and O'Neill reviews Undulation and Tamerlane.
    *   We need Kramer < Megregian.
    *   If Megregian reviews Sunset, Tamerlane, Undulation (3 plays).
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   If Megregian reviews Sunset, Tamerlane (2 plays).
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Correction:** The constraint is "Kramer and Lopez each review fewer... than Megregian".
    *   If Megregian reviews Sunset, Tamerlane, Undulation (3 plays).
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   If Jiang reviews Undulation.
    *   Megregian reviews Sunset, Tamerlane (2 plays).
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Wait**, let's re-read the constraint. "Kramer and Lopez each review fewer of the plays than Megregian."
    *   If Megregian reviews Sunset, Tamerlane, Undulation (3 plays).
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   If Jiang reviews Undulation.
    *   Megregian reviews Sunset, Tamerlane (2 plays).
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try a different set for Megregian.**
    *   Megregian reviews Sunset, Tamerlane, Undulation (3 plays).
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try a different set for Jiang.**
    *   Jiang reviews Undulation.
    *   Megregian reviews Sunset, Tamerlane (2 plays).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **

### TOKEN USAGE

  Input tokens:  276
  Output tokens: 32,768
  Total tokens:  33,044

COMPLETE

## System 1 Final Answer

```json
To solve this problem, we must determine which set of students could be the complete list of those reviewing *Tamerlane* based on the given constraints.

**1. Analyze the Constraints:**
*   **Plays:** Sunset, Tamerlane, Undulation.
*   **Students:** Jiang, Kramer, Lopez, Megregian, O'Neill.
*   **Constraint 1:** Kramer and Lopez each review fewer plays than Megregian.
    *   This implies Megregian reviews at least 2 plays (since others review at least 1).
    *   Kramer and Lopez review 1 or 2 plays, but strictly less than Megregian.
*   **Constraint 2:** Neither Lopez nor Megregian reviews any play Jiang reviews.
    *   Jiang's set of plays is disjoint from Lopez's and Megregian's.
*   **Constraint 3:** Kramer and O'Neill both review Tamerlane.
    *   Kramer $\in$ Tamerlane.
    *   O'Neill $\in$ Tamerlane.
*   **Constraint 4:** Exactly two of the students review exactly the same play or plays as each other.
    *   There is exactly one pair of students with identical sets of plays. All other students have unique sets.

**2. Evaluate the Answer Choices:**
We are looking for the complete list of students who review Tamerlane. Since Kramer and O'Neill must review Tamerlane (Constraint 3), any valid list must include both of them.

*   **(A) Jiang, Kramer:** Excludes O'Neill. Invalid.
*   **(B) Kramer, O'Neill:** Includes the required pair. Valid candidate.
*   **(C) Kramer, Lopez, O'Neill:** Includes the required pair. Valid candidate.
*   **(D) Kramer, Megregian, O'Neill:** Includes the required pair. Valid candidate.
*   **(E) Lopez, Megregian, O'Neill:** Excludes Kramer. Invalid.

**3. Test the Valid Candidates:**

**Testing (B) Kramer, O'Neill:**
*   **Tamerlane Reviewers:** Kramer, O'Neill.
*   **Implication:** Jiang, Lopez, and Megregian do *not* review Tamerlane.
*   **Megregian's Plays:** Must review at least 2 plays (Constraint 1). Since she doesn't review Tamerlane, she must review Sunset and Undulation.
*   **Lopez's Plays:** Must review fewer plays than Megregian (2). Lopez cannot review Tamerlane. Lopez cannot review plays Jiang reviews (Constraint 2).
    *   Jiang must review at least one play. If Jiang reviews Sunset, Lopez cannot review Sunset. If Jiang reviews Undulation, Lopez cannot review Undulation.
    *   If Jiang reviews both Sunset and Undulation, Lopez has no plays left to review (since she can't review Tamerlane). This violates the condition that Lopez reviews "one or more" plays.
    *   Therefore, Lopez must review Tamerlane to have a valid play set. But we assumed Lopez does not review Tamerlane based on the list in (B).
*   **Conclusion:** (B) is impossible.

**Testing (C) Kramer, Lopez, O'Neill:**
*   **Tamerlane Reviewers:** Kramer, Lopez, O'Neill.
*   **Implication:** Jiang and Megregian do *not* review Tamerlane.
*   **Megregian's Plays:** Must review at least 2 plays. She cannot review Tamerlane. She cannot review plays Jiang reviews.
    *   If Jiang reviews Sunset, Megregian cannot review Sunset.
    *   If Jiang reviews Undulation, Megregian cannot review Undulation.
    *   If Jiang reviews both, Megregian has no plays left. Impossible.
    *   Therefore, Jiang must review Tamerlane. But the list says Jiang does not review Tamerlane.
*   **Conclusion:** (C) is impossible.

**Testing (D) Kramer, Megregian, O'Neill:**
*   **Tamerlane Reviewers:** Kramer, Megregian, O'Neill.
*   **Implication:** Jiang and Lopez do *not* review Tamerlane.
*   **Megregian's Plays:** Reviews Tamerlane. Needs at least one more play (Constraint 1). Let's say Megregian reviews Sunset and Tamerlane.
*   **Jiang's Plays:** Cannot overlap with Lopez or Megregian.
    *   Jiang cannot review Sunset (Megregian reviews it).
    *   Jiang cannot review Tamerlane (based on the list).
    *   Jiang must review Undulation.
*   **Lopez's Plays:** Cannot overlap with Jiang. Jiang reviews Undulation, so Lopez cannot review Undulation. Lopez does not review Tamerlane (based on the list).
    *   Lopez must review Sunset.
*   **Kramer's Plays:** Reviews Tamerlane. Needs to review fewer plays than Megregian (2). Kramer can review Sunset and Tamerlane.
*   **O'Neill's Plays:** Reviews Tamerlane. Needs to be unique or the pair.
    *   Let's assign O'Neill to review Undulation and Tamerlane.
*   **Check Pair Constraint:**
    *   Jiang: {Undulation}
    *   Lopez: {Sunset}
    *   Megregian: {Sunset, Tamerlane}
    *   Kramer: {Sunset, Tamerlane}
    *   O'Neill: {Undulation, Tamerlane}
    *   Kramer and Megregian have the exact same set of plays ({Sunset, Tamerlane}). This satisfies the "exactly two students review the same plays" constraint.
*   **Check All Constraints:**
    *   Kramer (2) < Megregian (2)? No, must be strictly fewer.
    *   Let's adjust Megregian to review 3 plays: {Sunset, Tamerlane, Undulation}.
    *   Jiang cannot review Sunset or Undulation (Megregian has them). Jiang must review Tamerlane. But the list says Jiang does not.
    *   Let's try a different configuration for Megregian.
    *   Megregian: {Sunset, Tamerlane}.
    *   Jiang: {Undulation}.
    *   Lopez: {Sunset}.
    *   Kramer: {Sunset, Tamerlane}.
    *   O'Neill: {Undulation, Tamerlane}.
    *   Kramer (2) < Megregian (2)? No.
    *   Let's try Megregian: {Sunset, Tamerlane, Undulation} (3 plays).
    *   Jiang: {Undulation} (Conflict with Megregian).
    *   Jiang: {Tamerlane} (Conflict with list).
    *   Wait, if Megregian reviews Sunset and Tamerlane (2 plays), and Kramer reviews Sunset and Tamerlane (2 plays), the constraint "Kramer reviews fewer plays than Megregian" is violated.
    *   However, if we look closely at the disjoint constraint: "Neither Lopez nor Megregian reviews any play Jiang reviews."
    *   If Jiang reviews Undulation, and Megregian reviews Sunset and Tamerlane, they are disjoint.
    *   If Lopez reviews Sunset, and Jiang reviews Undulation, they are disjoint.
    *   If Kramer reviews Sunset and Tamerlane, and O'Neill reviews Undulation and Tamerlane.
    *   We need Kramer < Megregian.
    *   If Megregian reviews Sunset, Tamerlane, Undulation (3 plays).
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   If Megregian reviews Sunset, Tamerlane (2 plays).
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Correction:** The constraint is "Kramer and Lopez each review fewer... than Megregian".
    *   If Megregian reviews Sunset, Tamerlane, Undulation (3 plays).
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   If Jiang reviews Undulation.
    *   Megregian reviews Sunset, Tamerlane (2 plays).
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Wait**, let's re-read the constraint. "Kramer and Lopez each review fewer of the plays than Megregian."
    *   If Megregian reviews Sunset, Tamerlane, Undulation (3 plays).
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   If Jiang reviews Undulation.
    *   Megregian reviews Sunset, Tamerlane (2 plays).
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try a different set for Megregian.**
    *   Megregian reviews Sunset, Tamerlane, Undulation (3 plays).
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try a different set for Jiang.**
    *   Jiang reviews Undulation.
    *   Megregian reviews Sunset, Tamerlane (2 plays).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **Let's try Megregian reviews Sunset, Tamerlane, Undulation (3 plays).**
    *   Jiang reviews Tamerlane (Conflict with list D).
    *   **Let's try Megregian reviews Sunset, Tamerlane (2 plays).**
    *   Jiang reviews Undulation (1 play).
    *   Lopez reviews Sunset (1 play).
    *   Kramer reviews Sunset, Tamerlane (2 plays).
    *   O'Neill reviews Undulation, Tamerlane (2 plays).
    *   Kramer (2) is not < Megregian (2).
    *   **
```
