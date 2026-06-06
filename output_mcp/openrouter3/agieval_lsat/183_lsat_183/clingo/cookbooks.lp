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

% Helper: Count number of solutions
num_solutions(N) :- N = #count { C1,S1,C2,S2,C3,S3,C4,S4,C5,S5,C6,S6 : 
    published(k,S1), published(l,S2), published(m,S3), 
    published(n,S4), published(o,S5), published(p,S6) }.

% For each answer choice, check if it leads to exactly one solution
% We'll use a separate predicate for each choice

% Choice A: K is published in the fall and L is published in the spring
condition_a :- published(k, fall), published(l, spring).
option(a) :- condition_a, num_solutions(1).

% Choice B: O is published in the fall and P is published in the spring
% Note: The problem says "0" but I assume it's "O" (letter O)
condition_b :- published(o, fall), published(p, spring).
option(b) :- condition_b, num_solutions(1).

% Choice C: P is published in the fall and L is published in the spring
condition_c :- published(p, fall), published(l, spring).
option(c) :- condition_c, num_solutions(1).

% Choice D: Both K and L are published in the spring
condition_d :- published(k, spring), published(l, spring).
option(d) :- condition_d, num_solutions(1).

% Choice E: Both M and L are published in the fall
condition_e :- published(m, fall), published(l, fall).
option(e) :- condition_e, num_solutions(1).

#show option/1.