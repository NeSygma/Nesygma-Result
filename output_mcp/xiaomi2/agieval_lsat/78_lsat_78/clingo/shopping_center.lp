% Domains
space(1..7).
business(opt). business(pharm). business(rest). business(shoe). business(toy). business(vet).

% Assign each space exactly one business
{ assigned(S, B) : business(B) } 1 :- space(S).

% Count constraints: each business appears required number of times
:- #count{S : assigned(S, pharm)} != 1.
:- #count{S : assigned(S, opt)} != 1.
:- #count{S : assigned(S, shoe)} != 1.
:- #count{S : assigned(S, toy)} != 1.
:- #count{S : assigned(S, vet)} != 1.
:- #count{S : assigned(S, rest)} != 2.

% Given: veterinarian in space 5
assigned(5, vet).

% Constraint 1: Pharmacy at one end, restaurant at the other
end_pharm_rest :- assigned(1, pharm), assigned(7, rest).
end_pharm_rest :- assigned(7, pharm), assigned(1, rest).
:- not end_pharm_rest.

% Constraint 2: Two restaurants separated by at least two other businesses
rest_pos(P) :- assigned(P, rest).
:- rest_pos(P1), rest_pos(P2), P1 < P2, P2 - P1 < 3.

% Constraint 3: Pharmacy next to optometrist or veterinarian
pharm_pos(P) :- assigned(P, pharm).
opt_pos(Q) :- assigned(Q, opt).
vet_pos(Q) :- assigned(Q, vet).
pharm_next_opt :- pharm_pos(P), opt_pos(Q), |P - Q| = 1.
pharm_next_vet :- pharm_pos(P), vet_pos(Q), |P - Q| = 1.
:- not pharm_next_opt, not pharm_next_vet.

% Constraint 4: Toy store not next to veterinarian
toy_pos(T) :- assigned(T, toy).
:- toy_pos(T), vet_pos(V), |T - V| = 1.

% Define conditions for each answer choice
cond_a :- assigned(2, opt).
cond_b :- assigned(7, pharm).
cond_c :- assigned(4, rest).
cond_d :- assigned(6, shoe).
cond_e :- assigned(3, toy).

% For each option, check if it can be false (i.e., there exists a model where condition is false)
% We'll use a choice rule to guess a counterexample for each option
{ counterexample_a } :- not cond_a.
{ counterexample_b } :- not cond_b.
{ counterexample_c } :- not cond_c.
{ counterexample_d } :- not cond_d.
{ counterexample_e } :- not cond_e.

% If a counterexample exists, then the option is not necessarily true
not_necessarily_a :- counterexample_a.
not_necessarily_b :- counterexample_b.
not_necessarily_c :- counterexample_c.
not_necessarily_d :- counterexample_d.
not_necessarily_e :- counterexample_e.

% The correct option is the one that has no counterexample
option(a) :- not not_necessarily_a.
option(b) :- not not_necessarily_b.
option(c) :- not not_necessarily_c.
option(d) :- not not_necessarily_d.
option(e) :- not not_necessarily_e.

#show option/1.