% Houses: J, K, L, M, N, O, P
% Positions: 1..7 (morning: 1-2, afternoon: 3-5, evening: 6-7)

position(1..7).

% Valid combinations of positions for K, L, M, J (distinct, satisfying constraints)
valid_combo(Pk, Pl, Pm, Pj) :-
    position(Pk), position(Pl), position(Pm), position(Pj),
    Pk < Pl, Pl < Pm,          % K < L < M
    Pj >= 6,                    % J in evening (6 or 7)
    Pk != 1, Pk != 2,          % K not in morning
    Pk != Pl, Pk != Pm, Pk != Pj,
    Pl != Pm, Pl != Pj,
    Pm != Pj.

% --- Option A: J and K consecutive (|Pj - Pk| = 1) ---
option_possible(a) :- valid_combo(Pk, Pl, Pm, Pj), Pj = Pk + 1.
option_possible(a) :- valid_combo(Pk, Pl, Pm, Pj), Pj = Pk - 1.

% --- Option B: J and M consecutive ---
option_possible(b) :- valid_combo(Pk, Pl, Pm, Pj), Pj = Pm + 1.
option_possible(b) :- valid_combo(Pk, Pl, Pm, Pj), Pj = Pm - 1.

% --- Option C: J and O consecutive ---
% O can be any position not used by K,L,M,J
option_possible(c) :- valid_combo(Pk, Pl, Pm, Pj), position(Po),
                      Po != Pk, Po != Pl, Po != Pm, Po != Pj,
                      Pj = Po + 1.
option_possible(c) :- valid_combo(Pk, Pl, Pm, Pj), position(Po),
                      Po != Pk, Po != Pl, Po != Pm, Po != Pj,
                      Pj = Po - 1.

% --- Option D: J and P consecutive ---
option_possible(d) :- valid_combo(Pk, Pl, Pm, Pj), position(Pp),
                      Pp != Pk, Pp != Pl, Pp != Pm, Pp != Pj,
                      Pj = Pp + 1.
option_possible(d) :- valid_combo(Pk, Pl, Pm, Pj), position(Pp),
                      Pp != Pk, Pp != Pl, Pp != Pm, Pp != Pj,
                      Pj = Pp - 1.

% --- Option E: M and P consecutive ---
option_possible(e) :- valid_combo(Pk, Pl, Pm, Pj), position(Pp),
                      Pp != Pk, Pp != Pl, Pp != Pm, Pp != Pj,
                      Pm = Pp + 1.
option_possible(e) :- valid_combo(Pk, Pl, Pm, Pj), position(Pp),
                      Pp != Pk, Pp != Pl, Pp != Pm, Pp != Pj,
                      Pm = Pp - 1.

% The answer is the option that is NOT possible
option(a) :- not option_possible(a).
option(b) :- not option_possible(b).
option(c) :- not option_possible(c).
option(d) :- not option_possible(d).
option(e) :- not option_possible(e).

#show option/1.