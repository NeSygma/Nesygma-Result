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

%%% Now: for each employee, check which spaces are possible
%%% We need to see ALL possible assignments.
%%% Let's use a different approach: compute the possible spaces per employee
%%% by checking if there exists an assignment where E gets S.

%%% Find all possible (Employee, Space) pairs that appear in at least one solution.
%%% We'll use a projection trick.

%%% Don't show individual assignments; show only the summary.
#show employee/1.
#show space/1.