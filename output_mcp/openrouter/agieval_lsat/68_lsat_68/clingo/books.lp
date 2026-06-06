% books and shelves
book(f). book(g). book(h). book(i). book(k). book(l). book(m). book(o).

shelf(top). shelf(middle). shelf(bottom).

% assign each book to exactly one shelf
1 { placed(B,S) : shelf(S) } 1 :- book(B).

% at least two books per shelf
:- shelf(S), N = #count{B : placed(B,S)}, N < 2.

% more books on bottom than top
:- Nb = #count{B : placed(B,bottom)}, Nt = #count{B : placed(B,top)}, Nb <= Nt.

% constraints
placed(i,middle).
% F and M same shelf
:- placed(f,S1), placed(m,S2), S1 != S2.

% higher relation (strictly higher)
higher(top,middle). higher(top,bottom). higher(middle,bottom).

% K higher than F
:- placed(k,Sk), placed(f,Sf), not higher(Sk,Sf).

% O higher than L
:- placed(o,So), placed(l,Sl), not higher(So,Sl).

% option conditions
option(a) :- placed(o,So), placed(m,Sm), higher(So,Sm).
option(b) :- placed(k,Sk), placed(g,Sg), higher(Sk,Sg).
option(c) :- placed(i,Si), placed(f,Sf), higher(Si,Sf).
option(d) :- placed(g,Sg), placed(o,So), higher(Sg,So).
option(e) :- placed(f,Sf), placed(l,Sl), higher(Sf,Sl).

% forbid other options
:- option(b).
:- option(c).
:- option(d).
:- option(e).

% ensure option a holds
:- not option(a).

#show option/1.