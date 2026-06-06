% Domain: cookbooks and seasons
cookbook(k). cookbook(l). cookbook(m). cookbook(n). cookbook(o). cookbook(p).
season(fall). season(spring).

% Each cookbook is published in exactly one season
{ published(C, S) : season(S) } 1 :- cookbook(C).

% Constraint 1: M and P cannot be in the same season
:- published(m, S), published(p, S).

% Constraint 2: K and N must be in the same season
:- published(k, S1), published(n, S2), S1 != S2.

% Constraint 3: If K is in fall, then O must be in fall
:- published(k, fall), not published(o, fall).

% Constraint 4: If M is in fall, then N must be in spring
:- published(m, fall), not published(n, spring).

% For each answer choice, we'll check if it leads to exactly one solution
% We'll use a helper predicate to count the number of valid assignments

% Count the number of valid assignments for each choice
% We need to count all possible assignments that satisfy the constraints plus the choice condition

% For choice A: K is published in the fall and L is published in the spring
count_a(N) :- N = #count { 1 : published(k, fall), published(l, spring) }.

% For choice B: O is published in the fall and P is published in the spring
count_b(N) :- N = #count { 1 : published(o, fall), published(p, spring) }.

% For choice C: P is published in the fall and L is published in the spring
count_c(N) :- N = #count { 1 : published(p, fall), published(l, spring) }.

% For choice D: Both K and L are published in the spring
count_d(N) :- N = #count { 1 : published(k, spring), published(l, spring) }.

% For choice E: Both M and L are published in the fall
count_e(N) :- N = #count { 1 : published(m, fall), published(l, fall) }.

% An option is correct if its count is exactly 1
option(a) :- count_a(1).
option(b) :- count_b(1).
option(c) :- count_c(1).
option(d) :- count_d(1).
option(e) :- count_e(1).

#show option/1.