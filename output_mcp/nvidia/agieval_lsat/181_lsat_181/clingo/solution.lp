book(k). book(l). book(m). book(n). book(o). book(p).
fall(X) | spring(X) :- book(X).
fall(m).
:- fall(p).
:- fall(k), not fall(n).
:- fall(n), not fall(k).
:- fall(k), not fall(o).
:- fall(n).
option(a) :- fall(k), fall(o).
option(b) :- fall(l), fall(n).
option(c) :- fall(l), fall(o).
option(d) :- fall(n), fall(p).
option(e) :- fall(o), fall(p).
#show option/1.