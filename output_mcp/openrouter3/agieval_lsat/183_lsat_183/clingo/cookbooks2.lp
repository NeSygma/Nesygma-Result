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
% We'll use a different approach: check if the condition forces all assignments

% Choice A: K is published in the fall and L is published in the spring
condition_a :- published(k, fall), published(l, spring).
option(a) :- condition_a, 
    % Check that there's exactly one valid assignment
    #count { S_k : published(k, S_k) } = 1,
    #count { S_l : published(l, S_l) } = 1,
    #count { S_m : published(m, S_m) } = 1,
    #count { S_n : published(n, S_n) } = 1,
    #count { S_o : published(o, S_o) } = 1,
    #count { S_p : published(p, S_p) } = 1.

% Choice B: O is published in the fall and P is published in the spring
condition_b :- published(o, fall), published(p, spring).
option(b) :- condition_b,
    #count { S_k : published(k, S_k) } = 1,
    #count { S_l : published(l, S_l) } = 1,
    #count { S_m : published(m, S_m) } = 1,
    #count { S_n : published(n, S_n) } = 1,
    #count { S_o : published(o, S_o) } = 1,
    #count { S_p : published(p, S_p) } = 1.

% Choice C: P is published in the fall and L is published in the spring
condition_c :- published(p, fall), published(l, spring).
option(c) :- condition_c,
    #count { S_k : published(k, S_k) } = 1,
    #count { S_l : published(l, S_l) } = 1,
    #count { S_m : published(m, S_m) } = 1,
    #count { S_n : published(n, S_n) } = 1,
    #count { S_o : published(o, S_o) } = 1,
    #count { S_p : published(p, S_p) } = 1.

% Choice D: Both K and L are published in the spring
condition_d :- published(k, spring), published(l, spring).
option(d) :- condition_d,
    #count { S_k : published(k, S_k) } = 1,
    #count { S_l : published(l, S_l) } = 1,
    #count { S_m : published(m, S_m) } = 1,
    #count { S_n : published(n, S_n) } = 1,
    #count { S_o : published(o, S_o) } = 1,
    #count { S_p : published(p, S_p) } = 1.

% Choice E: Both M and L are published in the fall
condition_e :- published(m, fall), published(l, fall).
option(e) :- condition_e,
    #count { S_k : published(k, S_k) } = 1,
    #count { S_l : published(l, S_l) } = 1,
    #count { S_m : published(m, S_m) } = 1,
    #count { S_n : published(n, S_n) } = 1,
    #count { S_o : published(o, S_o) } = 1,
    #count { S_p : published(p, S_p) } = 1.

#show option/1.