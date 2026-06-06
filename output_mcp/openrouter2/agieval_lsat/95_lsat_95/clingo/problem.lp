% Facts
house(j). house(k). house(l). house(m). house(n). house(o). house(p).
position(1). position(2). position(3). position(4). position(5). position(6). position(7).

% Choice rules for bijection
{pos(H,P) : house(H)} 1 :- position(P).
{pos(H,P) : position(P)} 1 :- house(H).

% Ensure each position has a house
:- position(P), not pos(_,P).

% Constraints
% J in evening
:- pos(j,P), P < 6.

% K not morning
:- pos(k,P), P <= 2.

% L after K before M
:- pos(k,Pk), pos(l,Pl), pos(m,Pm), Pl <= Pk.
:- pos(k,Pk), pos(l,Pl), pos(m,Pm), Pm <= Pl.

% Option mapping
option(a) :- pos(k,Pk), Pk >= 6.
option(b) :- pos(l,Pl), Pl >= 3, Pl <= 5.
option(c) :- pos(l,Pl), Pl >= 6.
option(d) :- pos(m,Pm), Pm <= 2.
option(e) :- pos(m,Pm), Pm >= 3, Pm <= 5.

% Enforce only option(b) true
:- option(a).
:- option(c).
:- option(d).
:- option(e).
:- not option(b).

#show option/1.