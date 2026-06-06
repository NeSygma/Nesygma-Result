% Facts for options
order(a,1,h). order(a,2,s). order(a,3,j). order(a,4,q). order(a,5,y). order(a,6,g). order(a,7,r).
order(b,1,j). order(b,2,q). order(b,3,g). order(b,4,h). order(b,5,s). order(b,6,y). order(b,7,r).
order(c,1,q). order(c,2,j). order(c,3,s). order(c,4,h). order(c,5,y). order(c,6,g). order(c,7,r).
order(d,1,q). order(d,2,j). order(d,3,y). order(d,4,s). order(d,5,g). order(d,6,r). order(d,7,h).
order(e,1,s). order(e,2,g). order(e,3,q). order(e,4,j). order(e,5,y). order(e,6,r). order(e,7,h).

% Topics
topic(g,finance). topic(h,finance). topic(j,finance).
topic(q,nutrition). topic(r,nutrition). topic(s,nutrition).
topic(y,wildlife).

% Violation rules
violation(Option) :- order(Option,Pos,Art1), order(Option,Pos1,Art2), Pos1 = Pos+1, topic(Art1,Topic), topic(Art2,Topic).
violation(Option) :- order(Option,PosS,s), order(Option,PosQ,q), PosS < PosQ, PosQ != 3.
violation(Option) :- order(Option,PosS,s), order(Option,PosY,y), PosS >= PosY.
violation(Option) :- order(Option,PosJ,j), order(Option,PosG,g), PosJ >= PosG.
violation(Option) :- order(Option,PosG,g), order(Option,PosR,r), PosG >= PosR.

% Option derivation
option(a) :- not violation(a).
option(b) :- not violation(b).
option(c) :- not violation(c).
option(d) :- not violation(d).
option(e) :- not violation(e).

% Exactly one option
1 { option(a); option(b); option(c); option(d); option(e) } 1.

#show option/1.