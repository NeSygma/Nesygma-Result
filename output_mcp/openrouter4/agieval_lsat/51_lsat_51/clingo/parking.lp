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

%%% For each employee, find which spaces they COULD be assigned
%%% We'll collect all possible assignments
#show assigned/2.