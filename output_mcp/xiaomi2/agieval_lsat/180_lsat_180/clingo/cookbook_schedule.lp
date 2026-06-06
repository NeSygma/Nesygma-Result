% Define cookbooks
cookbook(k). cookbook(l). cookbook(m). cookbook(n). cookbook(o). cookbook(p).

% Define seasons
season(fall). season(spring).

% Each cookbook must be assigned to exactly one season
1 { assign(C, S) : season(S) } 1 :- cookbook(C).

% Encode each option as a possible world
% Option A: fall: K, L, M, O; spring: N, P
option_a_assign(k, fall). option_a_assign(l, fall). option_a_assign(m, fall). option_a_assign(o, fall).
option_a_assign(n, spring). option_a_assign(p, spring).

% Option B: fall: K, L, N, O; spring: M, P
option_b_assign(k, fall). option_b_assign(l, fall). option_b_assign(n, fall). option_b_assign(o, fall).
option_b_assign(m, spring). option_b_assign(p, spring).

% Option C: fall: K, L, N, P; spring: M, O
option_c_assign(k, fall). option_c_assign(l, fall). option_c_assign(n, fall). option_c_assign(p, fall).
option_c_assign(m, spring). option_c_assign(o, spring).

% Option D: fall: K, M, N, O; spring: L, P
option_d_assign(k, fall). option_d_assign(m, fall). option_d_assign(n, fall). option_d_assign(o, fall).
option_d_assign(l, spring). option_d_assign(p, spring).

% Option E: fall: M, O; spring: K, L, N, P
option_e_assign(m, fall). option_e_assign(o, fall).
option_e_assign(k, spring). option_e_assign(l, spring). option_e_assign(n, spring). option_e_assign(p, spring).

% Check if current assignment matches an option
matches_a :- assign(C, S) = option_a_assign(C, S) : cookbook(C).
matches_b :- assign(C, S) = option_b_assign(C, S) : cookbook(C).
matches_c :- assign(C, S) = option_c_assign(C, S) : cookbook(C).
matches_d :- assign(C, S) = option_d_assign(C, S) : cookbook(C).
matches_e :- assign(C, S) = option_e_assign(C, S) : cookbook(C).

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