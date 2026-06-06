% Test equivalence: check if each option, when substituted for constraint 4, produces the same set of assignments.

% Domain
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

% --- Now define original constraint 4 and each option ---

% Original constraint 4:
% If Knutson is not assigned to Thorne, then both Heideck and Mays must be assigned to Thorne
orig_sat :- assign(k, thorne).
orig_sat :- assign(h, thorne), assign(m, thorne).
orig_violated :- not orig_sat.

% Option A: If Knutson is assigned to Silva, then Heideck and Mays cannot both be assigned to that ceremony
optA_violated :- assign(k, silva), assign(h, silva), assign(m, silva).

% Option B: If Knutson is assigned to Silva, then Lai must also be assigned to that ceremony
optB_violated :- assign(k, silva), not assign(l, silva).

% Option C: Unless Knutson is assigned to Thorne, both Frost and Mays must be assigned to Thorne
optC_sat :- assign(k, thorne).
optC_sat :- assign(f, thorne), assign(m, thorne).
optC_violated :- not optC_sat.

% Option D: Unless Knutson is assigned to Thorne, Heideck cannot be assigned to the same ceremony as Lai
optD_violated :- not assign(k, thorne), assign(h, C), assign(l, C).

% Option E: Unless either Heideck or Mays is assigned to Thorne, Knutson must be assigned to that ceremony
optE_violated :- not assign(h, thorne), not assign(m, thorne), not assign(k, thorne).

% Check equivalence: we need to find if there's a counterexample where original and option diverge.

% For each option, we check if there exists a model where:
% - original holds but option violated (option is too strict)
% - original violated but option holds (option is too weak)

% Since we want to check substitution, we need to check:
% Base constraints + original_constraint -> models
% vs Base constraints + option_constraint -> models

% We can check by enumerating all assignments that satisfy base constraints,
% and then checking which additional constraints are satisfied.

% Let's enumerate all assignments that satisfy the base constraints (1,2,3, at-least-2)
% and then compare which options are violated.

% We already have base constraints. Let's just find models that satisfy them,
% and then output the satisfaction of each constraint version.

#show assign/2.
#show orig_violated/0.
#show optA_violated/0.
#show optB_violated/0.
#show optC_violated/0.
#show optD_violated/0.
#show optE_violated/0.

% Find ALL models
#program check.
% We want to see if any model has orig_violated and not optC_violated (option C weaker)
% or not orig_violated and optC_violated (option C stronger)
% If neither, option C is equivalent.