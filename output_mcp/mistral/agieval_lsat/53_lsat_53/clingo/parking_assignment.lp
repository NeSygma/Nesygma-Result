% Define the domains
employee(robertson; souza; togowa; vaughn; xu; young).
space(1..6).

% Each employee must be assigned exactly one parking space
1 { assigned(E, S) : space(S) } 1 :- employee(E).

% No two employees can share the same parking space
:- assigned(E1, S), assigned(E2, S), E1 != E2.

% Given condition: Robertson is assigned space 3
assigned(robertson, 3).

% Constraints from the problem:
% Young must be assigned a higher-numbered space than Togowa
:- assigned(young, Y), assigned(togowa, T), Y <= T.
% Xu must be assigned a higher-numbered space than Souza
:- assigned(xu, X), assigned(souza, S), X <= S.
% Robertson must be assigned a higher-numbered space than Young
:- assigned(robertson, R), assigned(young, Y), R <= Y.

% Derive the correct answer
% Since Robertson=3, Young must be 1 or 2.
% But Young > Togowa, and Togowa must be at least 1.
% If Young=1, Togowa must be <1, which is impossible.
% Thus, Young must be 2, and Togowa must be 1.
% This makes option (E) "Young is assigned parking space #2" true.
option(e) :- assigned(young, 2).

#show option/1.