% Define the employees and parking spaces.
employee(robertson).
employee(souza).
employee(togowa).
employee(vaughn).
employee(xu).
employee(young).

space(1..6).

% Assign exactly one space to each employee.
1 { assigned(E, S) : space(S) } 1 :- employee(E).

% Ensure no two employees share the same space.
:- assigned(E1, S), assigned(E2, S), E1 != E2.

% Constraints from the problem:
% 1. Young must be assigned a higher-numbered space than Togowa.
:- assigned(togowa, S1), assigned(young, S2), S2 <= S1.

% 2. Xu must be assigned a higher-numbered space than Souza.
:- assigned(souza, S1), assigned(xu, S2), S2 <= S1.

% 3. Robertson must be assigned a higher-numbered space than Young.
:- assigned(young, S1), assigned(robertson, S2), S2 <= S1.

% 4. Robertson must be assigned space #1, #2, #3, or #4.
:- assigned(robertson, S), S > 4.

% Additional constraint: Robertson is assigned space #3 (given in the question).
:- not assigned(robertson, 3).

% Helper predicates to determine the assignments of other employees.
assigned_space(E, S) :- assigned(E, S).

% Conditions for each option:
% (A) Souza is assigned space #4.
option(a) :- assigned_space(souza, 4).

% (B) Togowa is assigned space #2.
option(b) :- assigned_space(togowa, 2).

% (C) Vaughn is assigned space #5.
option(c) :- assigned_space(vaughn, 5).

% (D) Xu is assigned space #6.
option(d) :- assigned_space(xu, 6).

% (E) Young is assigned space #2.
option(e) :- assigned_space(young, 2).

#show option/1.