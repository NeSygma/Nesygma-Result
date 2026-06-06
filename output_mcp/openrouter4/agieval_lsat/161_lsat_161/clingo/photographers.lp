% Photographers assignment problem
% Find all valid assignments and determine which option is equivalent to the original constraint 4

% Domain
photographer(f; g; h; k; l; m).
ceremony(silva; thorne).

% Each photographer can be assigned to at most one ceremony (or unassigned)
0 { assign(P, C) : ceremony(C) } 1 :- photographer(P).

% At least 2 photographers per ceremony
:- #count { P : assign(P, silva) } < 2.
:- #count { P : assign(P, thorne) } < 2.

% No photographer assigned to both (already ensured by choice rule, but explicit)
% :- assign(P, silva), assign(P, thorne).

% Constraint 1: Frost and Heideck must be together at the same ceremony and both assigned
:- assign(f, C1), assign(h, C2), C1 != C2.
% Ensure both are assigned
assigned(P) :- assign(P, _).
:- not assigned(f).
:- not assigned(h).

% Constraint 2: If Lai and Mays are both assigned, they must be at different ceremonies
:- assign(l, C), assign(m, C).

% Constraint 3: If Gonzalez is assigned to Silva, then Lai must be assigned to Thorne
:- assign(g, silva), not assign(l, thorne).

% --- Define original constraint 4 ---
% If Knutson is not assigned to Thorne, then both Heideck and Mays must be assigned to Thorne
original_satisfied :- assign(k, thorne).
original_satisfied :- assign(h, thorne), assign(m, thorne).
:- not original_satisfied.

% Now define each option's constraint and check if it produces the same set

% Option A: If Knutson is assigned to Silva, then Heideck and Mays cannot both be assigned to that ceremony
% assign(k, silva) -> not (assign(h, silva) and assign(m, silva))
option_a_violated :- assign(k, silva), assign(h, silva), assign(m, silva).
:- option_a_violated.

% Option B: If Knutson is assigned to Silva, then Lai must also be assigned to that ceremony
% assign(k, silva) -> assign(l, silva)
option_b_violated :- assign(k, silva), not assign(l, silva).
:- option_b_violated.

% Option C: Unless Knutson is assigned to Thorne, both Frost and Mays must be assigned to Thorne
% not assign(k, thorne) -> (assign(f, thorne) and assign(m, thorne))
option_c_satisfied :- assign(k, thorne).
option_c_satisfied :- assign(f, thorne), assign(m, thorne).
:- not option_c_satisfied.

% Option D: Unless Knutson is assigned to Thorne, Heideck cannot be assigned to the same ceremony as Lai
% not assign(k, thorne) -> not exists C (assign(h, C) and assign(l, C))
option_d_violated :- not assign(k, thorne), assign(h, C), assign(l, C).
:- option_d_violated.

% Option E: Unless either Heideck or Mays is assigned to Thorne, Knutson must be assigned to that ceremony
% not (assign(h, thorne) or assign(m, thorne)) -> assign(k, thorne)
% Equivalent: assign(h, thorne) or assign(m, thorne) or assign(k, thorne)
option_e_violated :- not assign(h, thorne), not assign(m, thorne), not assign(k, thorne).
:- option_e_violated.

% To check equivalence: we compute which models satisfy the original and which satisfy each option.
% We need to see if for EVERY possible assignment, original_satisfied <-> option_X_satisfied.

% So we can check if there's any assignment where original_satisfied and not option_X_satisfied (original stronger)
% or where option_X_satisfied and not original_satisfied (option_X weaker)

% Let's find counterexamples for each option

% Counterexample type 1: original holds but option fails
model_id(1..2). % Use to distinguish models, but we'll use #show

% We'll just enumerate all solutions and check equivalence by comparing satisfaction.

% Actually simpler: We can define a predicate that checks equivalence logically.
% But since we want to see which option is equivalent, let's just output the options and see.

% Let's check each option:
% If there exists an assignment where original holds but option doesn't, then option is too strict.
% If there exists an assignment where option holds but original doesn't, then option is too weak.

% We'll use #show to output assignments and satisfaction status.

#show assign/2.
#show original_satisfied/0.
#show option_a_violated/0.
#show option_b_violated/0.
#show option_c_satisfied/0.
#show option_d_violated/0.
#show option_e_violated/0.