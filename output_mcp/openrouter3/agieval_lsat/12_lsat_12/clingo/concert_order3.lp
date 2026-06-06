% Compositions
composition(f). composition(h). composition(l). composition(o). composition(p). composition(r). composition(s). composition(t).

% Positions 1 through 8
position(1..8).

% Each composition appears exactly once at a position
1 { at(C, P) : composition(C) } 1 :- position(P).
1 { at(C, P) : position(P) } 1 :- composition(C).

% Helper: composition at position
pos(C, P) :- at(C, P).

% Test option (a) manually
pos(l,1). pos(p,2). pos(s,3). pos(r,4). pos(o,5). pos(t,6). pos(f,7). pos(h,8).

% Constraint 1: T is performed either immediately before F or immediately after R
% T immediately before F: pos(T, P), pos(F, P+1)
% T immediately after R: pos(R, P), pos(T, P+1)
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

#show pos/2.