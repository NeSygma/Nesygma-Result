% Compositions
composition(f). composition(h). composition(l). composition(o). composition(p). composition(r). composition(s). composition(t).

% Positions 1 through 8
position(1..8).

% Each composition appears exactly once at a position
1 { at(C, P) : composition(C) } 1 :- position(P).
1 { at(C, P) : position(P) } 1 :- composition(C).

% Helper: composition at position
pos(C, P) :- at(C, P).

% Constraint 1: T is performed either immediately before F or immediately after R
% T immediately before F: pos(T, P), pos(F, P+1)
% T immediately after R: pos(R, P), pos(T, P+1)
valid_t_f_r :- pos(T, P), pos(F, P+1).
valid_t_f_r :- pos(R, P), pos(T, P+1).
:- not valid_t_f_r.

% Constraint 2: At least two compositions are performed either after F and before R, or after R and before F
% Count compositions between F and R in either order
count_between_fr(N) :- N = #count{C : pos(C, P), pos(F, PF), pos(R, PR), PF < P, P < PR}.
count_between_rf(N) :- N = #count{C : pos(C, P), pos(R, PR), pos(F, PF), PR < P, P < PF}.
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
:- pos(P, P1), pos(S, P2), P1 >= P2.

% Constraint 6: At least one composition is performed either after O and before S, or after S and before O
% Count compositions between O and S in either order
count_between_os(N) :- N = #count{C : pos(C, P), pos(O, PO), pos(S, PS), PO < P, P < PS}.
count_between_so(N) :- N = #count{C : pos(C, P), pos(S, PS), pos(O, PO), PS < P, P < PO}.
:- count_between_os(N1), count_between_so(N2), N1 < 1, N2 < 1.

% Map the correct answer to option/1
% For each choice, check if it satisfies all constraints
option(a) :- pos(l,1), pos(p,2), pos(s,3), pos(r,4), pos(o,5), pos(t,6), pos(f,7), pos(h,8).
option(b) :- pos(o,1), pos(t,2), pos(p,3), pos(f,4), pos(s,5), pos(h,6), pos(r,7), pos(l,8).
option(c) :- pos(p,1), pos(t,2), pos(f,3), pos(s,4), pos(l,5), pos(r,6), pos(o,7), pos(h,8).
option(d) :- pos(p,1), pos(t,2), pos(f,3), pos(s,4), pos(o,5), pos(r,6), pos(l,7), pos(h,8).
option(e) :- pos(t,1), pos(f,2), pos(p,3), pos(r,4), pos(o,5), pos(l,6), pos(s,7), pos(h,8).

#show option/1.