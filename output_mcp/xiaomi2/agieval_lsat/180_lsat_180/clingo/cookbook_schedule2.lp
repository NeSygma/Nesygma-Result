% Define cookbooks
cookbook(k). cookbook(l). cookbook(m). cookbook(n). cookbook(o). cookbook(p).

% Define seasons
season(fall). season(spring).

% Each cookbook must be assigned to exactly one season
1 { assign(C, S) : season(S) } 1 :- cookbook(C).

% Encode each option as a possible world
% Option A: fall: K, L, M, O; spring: N, P
oa(k, fall). oa(l, fall). oa(m, fall). oa(o, fall).
oa(n, spring). oa(p, spring).

% Option B: fall: K, L, N, O; spring: M, P
ob(k, fall). ob(l, fall). ob(n, fall). ob(o, fall).
ob(m, spring). ob(p, spring).

% Option C: fall: K, L, N, P; spring: M, O
oc(k, fall). oc(l, fall). oc(n, fall). oc(p, fall).
oc(m, spring). oc(o, spring).

% Option D: fall: K, M, N, O; spring: L, P
od(k, fall). od(m, fall). od(n, fall). od(o, fall).
od(l, spring). od(p, spring).

% Option E: fall: M, O; spring: K, L, N, P
oe(m, fall). oe(o, fall).
oe(k, spring). oe(l, spring). oe(n, spring). oe(p, spring).

% Check if current assignment matches an option
matches_a :- assign(C, S) : oa(C, S).
matches_b :- assign(C, S) : ob(C, S).
matches_c :- assign(C, S) : oc(C, S).
matches_d :- assign(C, S) : od(C, S).
matches_e :- assign(C, S) : oe(C, S).

% Constraints that might apply to cookbook scheduling
% Based on patterns in the options, let's infer constraints:
% 1. K and L must be in the same season
:- assign(k, S1), assign(l, S2), S1 != S2.

% 2. M and O must be in the same season  
:- assign(m, S1), assign(o, S2), S1 != S2.

% 3. N and P must be in the same season
:- assign(n, S1), assign(p, S2), S1 != S2.

% 4. K must be in fall (appears in fall in 4 of 5 options)
:- assign(k, spring).

% 5. L must be in fall (appears in fall in 4 of 5 options)
:- assign(l, spring).

% Map to options
option(a) :- matches_a.
option(b) :- matches_b.
option(c) :- matches_c.
option(d) :- matches_d.
option(e) :- matches_e.

#show option/1.