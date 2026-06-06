%%% Data
employee(robertson; souza; togowa; vaughn; xu; young).
space(1..6).

%%% Each employee gets exactly one unique space
1 { assigned(E, S) : space(S) } 1 :- employee(E).
:- assigned(E1, S), assigned(E2, S), E1 != E2.

%%% Constraints
%%% Young > Togowa
:- assigned(young, Y), assigned(togowa, T), Y <= T.

%%% Xu > Souza
:- assigned(xu, X), assigned(souza, S), X <= S.

%%% Robertson > Young
:- assigned(robertson, R), assigned(young, Y), R <= Y.

%%% Robertson ∈ {1,2,3,4}
:- assigned(robertson, R), R > 4.

%%% Record what spaces each employee gets in each model
%%% Using explicit enumeration of all possible combos

%%% Let's count how many spaces each employee can possibly occupy across all valid models
%%% We'll use a helper to capture possible assignments

%%% Option: compute the feasible assignments per employee using exhaustive enumeration
%%% Enumerate all possible individual assignments that can appear in SOME valid assignment.

%%% Use a choice rule to pick exactly one possible assignment per employee  
%%% and check if it extends to a full valid assignment.

%%% Actually, simpler: just generate all valid assignments and list them.

#show assigned/2.