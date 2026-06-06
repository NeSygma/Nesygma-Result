% Check equivalence of each option with original constraint 4

% --- Base Model ---
photographer(f; g; h; k; l; m).
ceremony(silva; thorne).

0 { assign(P, C) : ceremony(C) } 1 :- photographer(P).

% At least 2 per ceremony
:- #count { P : assign(P, silva) } < 2.
:- #count { P : assign(P, thorne) } < 2.

% Constraint 1: Frost and Heideck together at same ceremony, both assigned
:- assign(f, C1), assign(h, C2), C1 != C2.
assigned(P) :- assign(P, _).
:- not assigned(f).
:- not assigned(h).

% Constraint 2: Lai and Mays cannot be at same ceremony if both assigned
:- assign(l, C), assign(m, C).

% Constraint 3: Gonzalez at Silva -> Lai at Thorne
:- assign(g, silva), not assign(l, thorne).

% --- Original Constraint 4 ---
% If Knutson is not assigned to Thorne, then both Heideck and Mays must be assigned to Thorne
satisfies_original :- assign(k, thorne).
satisfies_original :- assign(h, thorne), assign(m, thorne).
:- not satisfies_original.

% --- Option A ---
% If Knutson is assigned to Silva, then Heideck and Mays cannot both be assigned to that ceremony.
% i.e., Knutson at Silva -> not (Heideck at Silva and Mays at Silva)
violates_a :- assign(k, silva), assign(h, silva), assign(m, silva).
satisfies_a :- not violates_a.
:- not satisfies_a.

% --- Option B ---
% If Knutson is assigned to Silva, then Lai must also be assigned to that ceremony.
violates_b :- assign(k, silva), not assign(l, silva).
satisfies_b :- not violates_b.
:- not satisfies_b.

% --- Option C ---
% Unless Knutson is assigned to Thorne, both Frost and Mays must be assigned to that ceremony.
% unless X means: if not X then... So: unless K is at Thorne -> F at Thorne and M at Thorne
% i.e., not assign(k, thorne) -> (assign(f, thorne) and assign(m, thorne))
% Equivalently: not assign(k, thorne), not assign(f, thorne) is forbidden
% or: not assign(k, thorne), not assign(m, thorne) is forbidden
violates_c :- not assign(k, thorne), not assign(f, thorne).
violates_c :- not assign(k, thorne), not assign(m, thorne).
satisfies_c :- not violates_c.
:- not satisfies_c.

% --- Option D ---
% Unless Knutson is assigned to Thorne, Heideck cannot be assigned to the same ceremony as Lai.
% unless K at Thorne -> not (H and L at same ceremony)
% i.e., not assign(k, thorne) -> not exists C such that assign(h, C) and assign(l, C)
% So: if not assign(k, thorne), and assign(h, C) and assign(l, C), that's forbidden
violates_d :- not assign(k, thorne), assign(h, C), assign(l, C).
satisfies_d :- not violates_d.
:- not satisfies_d.

% --- Option E ---
% Unless either Heideck or Mays is assigned to Thorne, Knutson must be assigned to that ceremony.
% unless (H at Thorne or M at Thorne) -> K at Thorne
% i.e., not (assign(h, thorne) or assign(m, thorne)) -> assign(k, thorne)
% Equivalently: not assign(h, thorne), not assign(m, thorne), and not assign(k, thorne) is forbidden
violates_e :- not assign(h, thorne), not assign(m, thorne), not assign(k, thorne).
satisfies_e :- not violates_e.
:- not satisfies_e.

% --- Now check which options are equivalent ---
% For each option, check: does there exist a model that satisfies original + base but violates option?
% And does there exist a model that satisfies option + base but violates original?

% We want to find counterexamples:
% Look for assignments that satisfy everything (all constraints above) but where
% the option differs from original.

% Let's just output assignments and see which options hold along with original
#show assign/2.
#show satisfies_original/0.
#show satisfies_a/0.
#show satisfies_b/0.
#show satisfies_c/0.
#show satisfies_d/0.
#show satisfies_e/0.