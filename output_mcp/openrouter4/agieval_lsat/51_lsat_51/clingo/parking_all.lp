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

%%% For each employee, record which spaces they could possibly get
%%% We do this by asserting possible_assignment for each valid assignment
possible(E, S) :- assigned(E, S).

%%% Count how many possible spaces each employee has
num_possible(E, N) :- N = #count { S : possible(E, S) }, employee(E).

%%% Count how many employees have exactly 2 possible spaces
employees_with_2(N) :- N = #count { E : num_possible(E, 2) }.

#show num_possible/2.
#show employees_with_2/1.