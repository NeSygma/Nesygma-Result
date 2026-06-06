% Concert promoter problem

% Bands and slots
band(uneasy; vegemite; wellspring; xpert; yardsign; zircon).
slot(1..6).

% Generate all permutations: each band gets exactly one slot, each slot used exactly once
1 { band_slot(B, S) : slot(S) } 1 :- band(B).
1 { band_slot(B, S) : band(B) } 1 :- slot(S).

% Base constraints (always present)
:- band_slot(vegemite, S1), band_slot(zircon, S2), S1 >= S2.
:- band_slot(uneasy, S), S <= 3.
:- band_slot(yardsign, S), S >= 4.

% Original constraint 2 (hard)
original_constraint :- band_slot(wellspring, Sw), band_slot(xpert, Sx), Sw < Sx,
                       band_slot(zircon, Sz), band_slot(xpert, Sx), Sz < Sx.

% Candidate A: Only Uneasy can perform in a later slot than Xpert.
% Means: No other band (besides Uneasy) performs later than Xpert.
has_other_later :- band_slot(B, S), band_slot(xpert, Sx), S > Sx, B != uneasy.
candidate_a :- not has_other_later.

% Candidate B: Vegemite < Wellspring < Zircon.
candidate_b :- band_slot(vegemite, Sv), band_slot(wellspring, Sw), band_slot(zircon, Sz),
               Sv < Sw, Sw < Sz.

% Candidate C: Vegemite and Wellspring each earlier than Xpert.
candidate_c :- band_slot(vegemite, Sv), band_slot(xpert, Sx), Sv < Sx,
               band_slot(wellspring, Sw), Sw < Sx.

% Candidate D: Xpert performs either immediately before or immediately after Uneasy.
candidate_d :- band_slot(xpert, Sx), band_slot(uneasy, Su), Su - Sx = 1.
candidate_d :- band_slot(xpert, Sx), band_slot(uneasy, Su), Sx - Su = 1.

% Candidate E: Xpert performs in either slot five or slot six.
candidate_e :- band_slot(xpert, 5).
candidate_e :- band_slot(xpert, 6).

% Compute a unique ID for each permutation (based on slots of each band)
assignment_id(ID) :- band_slot(uneasy, U), band_slot(vegemite, V), band_slot(wellspring, W),
                     band_slot(xpert, X), band_slot(yardsign, Y), band_slot(zircon, Z),
                     ID = U * 100000 + V * 10000 + W * 1000 + X * 100 + Y * 10 + Z.

% Permutations that satisfy base constraints (already enforced as hard constraints)
satisfies_base(ID) :- assignment_id(ID).

% Permutations that satisfy base + original constraint 2
satisfies_original(ID) :- satisfies_base(ID), original_constraint.

% Permutations that satisfy base + candidate constraint
satisfies_candidate_a(ID) :- satisfies_base(ID), candidate_a.
satisfies_candidate_b(ID) :- satisfies_base(ID), candidate_b.
satisfies_candidate_c(ID) :- satisfies_base(ID), candidate_c.
satisfies_candidate_d(ID) :- satisfies_base(ID), candidate_d.
satisfies_candidate_e(ID) :- satisfies_base(ID), candidate_e.

% Count permutations for each scenario
count_original(N) :- N = #count { ID : satisfies_original(ID) }.
count_candidate_a(N) :- N = #count { ID : satisfies_candidate_a(ID) }.
count_candidate_b(N) :- N = #count { ID : satisfies_candidate_b(ID) }.
count_candidate_c(N) :- N = #count { ID : satisfies_candidate_c(ID) }.
count_candidate_d(N) :- N = #count { ID : satisfies_candidate_d(ID) }.
count_candidate_e(N) :- N = #count { ID : satisfies_candidate_e(ID) }.

% Count permutations that satisfy both original and candidate
count_both_a(N) :- N = #count { ID : satisfies_original(ID), satisfies_candidate_a(ID) }.
count_both_b(N) :- N = #count { ID : satisfies_original(ID), satisfies_candidate_b(ID) }.
count_both_c(N) :- N = #count { ID : satisfies_original(ID), satisfies_candidate_c(ID) }.
count_both_d(N) :- N = #count { ID : satisfies_original(ID), satisfies_candidate_d(ID) }.
count_both_e(N) :- N = #count { ID : satisfies_original(ID), satisfies_candidate_e(ID) }.

% Derive equivalence for each candidate
equivalent_a :- count_original(N), count_candidate_a(M), count_both_a(P), N = M, M = P.
equivalent_b :- count_original(N), count_candidate_b(M), count_both_b(P), N = M, M = P.
equivalent_c :- count_original(N), count_candidate_c(M), count_both_c(P), N = M, M = P.
equivalent_d :- count_original(N), count_candidate_d(M), count_both_d(P), N = M, M = P.
equivalent_e :- count_original(N), count_candidate_e(M), count_both_e(P), N = M, M = P.

% Map to options
option(a) :- equivalent_a.
option(b) :- equivalent_b.
option(c) :- equivalent_c.
option(d) :- equivalent_d.
option(e) :- equivalent_e.

#show option/1.