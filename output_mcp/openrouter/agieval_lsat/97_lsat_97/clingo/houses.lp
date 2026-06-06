% Houses and positions
house(j). house(k). house(l). house(m). house(n). house(o). house(p).
pos(1..7).

% Assignment of houses to positions (schedule)
1 { assign(H,P) : pos(P) } 1 :- house(H).
1 { assign(H,P) : house(H) } 1 :- pos(P).

% Constraints for the schedule
% J must be in the evening (positions 6 or 7)
:- assign(j,P), P <= 5.
% K cannot be in the morning (positions 1 or 2)
:- assign(k,P), P <= 2.
% L after K and before M: L > K and L < M
:- assign(l,Pl), assign(k,Pk), Pl <= Pk.
:- assign(l,Pl), assign(m,Pm), Pl >= Pm.
% P must be in the afternoon (positions 3..5)
:- assign(p,Pp), Pp < 3.
:- assign(p,Pp), Pp > 5.

% Second schedule to test the negation of each option
1 { assign2(H,P) : pos(P) } 1 :- house(H).
1 { assign2(H,P) : house(H) } 1 :- pos(P).

% Same constraints for the second schedule
:- assign2(j,P), P <= 5.
:- assign2(k,P), P <= 2.
:- assign2(l,Pl), assign2(k,Pk), Pl <= Pk.
:- assign2(l,Pl), assign2(m,Pm), Pl >= Pm.
:- assign2(p,Pp), Pp < 3.
:- assign2(p,Pp), Pp > 5.

% Detect existence of a schedule violating each option condition
possible_not_a :- assign2(j,P), P != 7.                % J not seventh
possible_not_b :- assign2(k,P), P != 3.                % K not third
possible_not_c :- assign2(n,P), P != 1.                % N not first
possible_not_d :- assign2(m,P), P < 3.
possible_not_d :- assign2(m,P), P > 5.                % M not in the afternoon
possible_not_e :- assign2(o,P), P > 2.                % O not in the morning

% Options are true only if their negation is impossible
option(a) :- not possible_not_a.
option(b) :- not possible_not_b.
option(c) :- not possible_not_c.
option(d) :- not possible_not_d.
option(e) :- not possible_not_e.

#show option/1.