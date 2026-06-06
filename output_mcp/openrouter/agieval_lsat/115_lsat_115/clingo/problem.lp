% Articles and topics
article(g). article(h). article(j). article(q). article(r). article(s). article(y).

finance(g). finance(h). finance(j).
nutrition(q). nutrition(r). nutrition(s).
wildlife(y).

topic(A, finance) :- finance(A).
topic(A, nutrition) :- nutrition(A).
topic(A, wildlife) :- wildlife(A).

% Positions
posnum(1..7).

% Choose positions for each article (bijection)
1 { pos(A,P) : posnum(P) } 1 :- article(A).
1 { pos(A,P) : article(A) } 1 :- posnum(P).

% Helper predicates
before(A,B) :- pos(A,PA), pos(B,PB), PA < PB.

% Constraints
% No consecutive same topic
:- pos(A,PA), pos(B,PB), PA = PB+1, topic(A,T), topic(B,T).

% S before Q only if Q is third
:- before(s,q), not pos(q,3).

% S before Y
:- not before(s,y).

% J before G
:- not before(j,g).

% G before R
:- not before(g,r).

% Option choice
1 { chosen(a); chosen(b); chosen(c); chosen(d); chosen(e) } 1.

% Enforce conditions based on chosen option
:- chosen(a), not pos(h,4).
:- chosen(b), not pos(h,6).
:- chosen(c), not pos(r,4).
:- chosen(d), not pos(r,7).
:- chosen(e), not pos(y,5).

% Map to option/1
option(a) :- chosen(a).
option(b) :- chosen(b).
option(c) :- chosen(c).
option(d) :- chosen(d).
option(e) :- chosen(e).

#show option/1.