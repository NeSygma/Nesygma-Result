% Domain: positions 1 through 8
position(1..8).

% The eight compositions
composition(f; h; l; o; p; r; s; t).

% Each composition is performed exactly once, at exactly one position
1 { perf(C, P) : position(P) } 1 :- composition(C).
1 { perf(C, P) : composition(C) } 1 :- position(P).

% T is performed either immediately before F or immediately after R.
% T immediately before F: perf(T, P), perf(F, P+1)
% T immediately after R: perf(R, P), perf(T, P+1)
:- not (
    (perf(t, P), perf(f, P+1), position(P), position(P+1));
    (perf(r, P), perf(t, P+1), position(P), position(P+1))
).

% At least two compositions are performed either after F and before R, or after R and before F.
% Count compositions between F and R (exclusive)
between_F_R(N) :- N = #count { C, P : composition(C), perf(C, P), perf(f, PF), perf(r, PR), PF < P, P < PR }.
between_R_F(N) :- N = #count { C, P : composition(C), perf(C, P), perf(r, PR), perf(f, PF), PR < P, P < PF }.
:- between_F_R(N), between_R_F(M), N < 2, M < 2.

% O is performed either first or fifth.
:- not (perf(o, 1); perf(o, 5)).

% The eighth composition performed is either L or H.
:- not (perf(l, 8); perf(h, 8)).

% P is performed at some time before S.
:- perf(p, PP), perf(s, PS), PP >= PS.

% At least one composition is performed either after O and before S, or after S and before O.
between_O_S(N) :- N = #count { C, P : composition(C), perf(C, P), perf(o, PO), perf(s, PS), PO < P, P < PS }.
between_S_O(N) :- N = #count { C, P : composition(C), perf(C, P), perf(s, PS), perf(o, PO), PS < P, P < PO }.
:- between_O_S(N), between_S_O(M), N < 1, M < 1.

% Given: T is performed fifth and F is performed sixth.
perf(t, 5).
perf(f, 6).

% Show all assignments
#show perf/2.