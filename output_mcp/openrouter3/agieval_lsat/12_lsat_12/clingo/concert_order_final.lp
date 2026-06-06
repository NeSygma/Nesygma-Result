% Compositions
composition(f). composition(h). composition(l). composition(o). composition(p). composition(r). composition(s). composition(t).

% Positions 1 through 8
position(1..8).

% Each composition appears exactly once at a position
1 { at(C, P) : composition(C) } 1 :- position(P).
1 { at(C, P) : position(P) } 1 :- composition(C).

% Helper: composition at position
pos(C, P) :- at(C, P).

% Define the five options as possible assignments
% Option A: L, P, S, R, O, T, F, H
option_a :- pos(l,1), pos(p,2), pos(s,3), pos(r,4), pos(o,5), pos(t,6), pos(f,7), pos(h,8).

% Option B: O, T, P, F, S, H, R, L
option_b :- pos(o,1), pos(t,2), pos(p,3), pos(f,4), pos(s,5), pos(h,6), pos(r,7), pos(l,8).

% Option C: P, T, F, S, L, R, O, H
option_c :- pos(p,1), pos(t,2), pos(f,3), pos(s,4), pos(l,5), pos(r,6), pos(o,7), pos(h,8).

% Option D: P, T, F, S, O, R, L, H
option_d :- pos(p,1), pos(t,2), pos(f,3), pos(s,4), pos(o,5), pos(r,6), pos(l,7), pos(h,8).

% Option E: T, F, P, R, O, L, S, H
option_e :- pos(t,1), pos(f,2), pos(p,3), pos(r,4), pos(o,5), pos(l,6), pos(s,7), pos(h,8).

% Constraint 1: T is performed either immediately before F or immediately after R
valid_t_f_r :- pos(t, P), pos(f, P+1).
valid_t_f_r :- pos(r, P), pos(t, P+1).
:- not valid_t_f_r.

% Constraint 2: At least two compositions are performed either after F and before R, or after R and before F
% Count compositions between F and R in either order
count_between_fr(N) :- N = #count{C : pos(C, P), pos(f, PF), pos(r, PR), PF < P, P < PR}.
count_between_rf(N) :- N = #count{C : pos(C, P), pos(r, PR), pos(f, PF), PR < P, P < PF}.
:- count_between_fr(N1), count_between_rf(N2), N1 < 2, N2 < 2.

% Constraint 3: O is performed either first or fifth
valid_o_position :- pos(o, 1).
valid_o_position :- pos(o, 5).
:- not valid_o_position.

% Constraint 4: The eighth composition is either L or H
valid_eighth :- pos(l, 8).
valid_eighth :- pos(h, 8).
:- not valid_eighth.

% Constraint 5: P is performed before S
:- pos(p, P1), pos(s, P2), P1 >= P2.

% Constraint 6: At least one composition is performed either after O and before S, or after S and before O
% Count compositions between O and S in either order
count_between_os(N) :- N = #count{C : pos(C, P), pos(o, PO), pos(s, PS), PO < P, P < PS}.
count_between_so(N) :- N = #count{C : pos(C, P), pos(s, PS), pos(o, PO), PS < P, P < PO}.
:- count_between_os(N1), count_between_so(N2), N1 < 1, N2 < 1.

% Map the correct answer to option/1 (MANDATORY)
option(a) :- option_a.
option(b) :- option_b.
option(c) :- option_c.
option(d) :- option_d.
option(e) :- option_e.

#show option/1.