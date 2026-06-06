% Domains
space(1..7).
business(opt; pharm; rest1; rest2; shoe; toy; vet).

% Generate assignments: each business assigned to exactly one space
{ assign(B,S) : space(S) } 1 :- business(B).

% Each space has exactly one business
1 { assign(B,S) : business(B) } 1 :- space(S).

% Constraint 1: Pharmacy at one end and a restaurant at the other.
assign(pharm,1); assign(pharm,7) :- pharmacy_end.
assign(pharm,1); assign(pharm,7).
:- assign(pharm,1), not assign(rest1,7), not assign(rest2,7).
:- assign(pharm,7), not assign(rest1,1), not assign(rest2,1).

% Constraint 2: Two restaurants separated by at least two other businesses.
:- assign(rest1,S1), assign(rest2,S2), |S1-S2| < 3.

% Constraint 3: Pharmacy next to either opt or vet.
:- assign(pharm,S), S > 1, S < 7, not assign(opt,S-1), not assign(opt,S+1), not assign(vet,S-1), not assign(vet,S+1).
:- assign(pharm,1), not assign(opt,2), not assign(vet,2).
:- assign(pharm,7), not assign(opt,6), not assign(vet,6).

% Constraint 4: Toy not next to vet.
:- assign(toy,S1), assign(vet,S2), |S1-S2| = 1.

% Condition: opt next to shoe.
:- assign(opt,S1), assign(shoe,S2), |S1-S2| != 1.

% Compute pair start (leftmost of opt-shoe pair)
pair_start(S) :- assign(opt,S), assign(shoe,S2), S2 = S+1.
pair_start(S) :- assign(shoe,S), assign(opt,S2), S2 = S+1.

% Left and right neighbors of the pair
left_biz(B) :- pair_start(S), S > 1, assign(B,S-1).
right_biz(B) :- pair_start(S), S+2 <= 7, assign(B,S+2).

% Check which answer options hold
has_pharm_left :- left_biz(pharm).
has_pharm_right :- right_biz(pharm).
has_pharm :- has_pharm_left. has_pharm :- has_pharm_right.

has_rest1_left :- left_biz(rest1).
has_rest1_right :- right_biz(rest1).
has_rest1 :- has_rest1_left. has_rest1 :- has_rest1_right.

has_rest2_left :- left_biz(rest2).
has_rest2_right :- right_biz(rest2).
has_rest2 :- has_rest2_left. has_rest2 :- has_rest2_right.

has_toy_left :- left_biz(toy).
has_toy_right :- right_biz(toy).
has_toy :- has_toy_left. has_toy :- has_toy_right.

has_vet_left :- left_biz(vet).
has_vet_right :- right_biz(vet).
has_vet :- has_vet_left. has_vet :- has_vet_right.

% Option A: pharmacy and a restaurant
opt_a :- has_pharm, has_rest1.
opt_a :- has_pharm, has_rest2.

% Option B: pharmacy and toy store
opt_b :- has_pharm, has_toy.

% Option C: two restaurants
opt_c :- has_rest1, has_rest2.

% Option D: restaurant and toy store
opt_d :- has_rest1, has_toy.
opt_d :- has_rest2, has_toy.

% Option E: restaurant and veterinarian
opt_e :- has_rest1, has_vet.
opt_e :- has_rest2, has_vet.

% Show which options are satisfied in each model
show_a :- opt_a.
show_b :- opt_b.
show_c :- opt_c.
show_d :- opt_d.
show_e :- opt_e.

#show show_a/0.
#show show_b/0.
#show show_c/0.
#show show_d/0.
#show show_e/0.
#show assign/2.