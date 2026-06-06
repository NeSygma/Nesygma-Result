% Articles and positions
article(g;h;j;q;r;s;y).
position(1..7).

% Topics
topic(g,finance). topic(h,finance). topic(j,finance).
topic(q,nutrition). topic(r,nutrition). topic(s,nutrition).
topic(y,wildlife).

% Exactly one position per article
1 { pos(A,P) : position(P) } 1 :- article(A).
% Exactly one article per position
1 { pos(A,P) : article(A) } 1 :- position(P).

% Y is fourth
pos(y,4).

% Consecutive articles cannot have same topic
:- pos(A,P), pos(B,P1), P1 = P+1, topic(A,T), topic(B,T).

% S earlier than Y
:- pos(s,Ps), pos(y,Py), Ps >= Py.

% S earlier than Q only if Q is third
:- pos(s,Ps), pos(q,Pq), Ps < Pq, Pq != 3.

% J earlier than G
:- pos(j,Pj), pos(g,Pg), Pj >= Pg.

% G earlier than R
:- pos(g,Pg), pos(r,Pr), Pg >= Pr.

% Options mapping
option(a) :- pos(j,2).
option(b) :- pos(j,3).
option(c) :- pos(q,1).
option(d) :- pos(q,3).
option(e) :- pos(r,7).

% Minimize number of options true
#minimize {1,O : option(O)}.

#show option/1.