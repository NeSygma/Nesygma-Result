% Scientists and types
botanist(f). botanist(g). botanist(h).
chemist(k). chemist(l). chemist(m).
zoologist(p). zoologist(q). zoologist(r).
scientist(f). scientist(g). scientist(h). scientist(k). scientist(l). scientist(m). scientist(p). scientist(q). scientist(r).

% Selection of exactly 5 scientists
5 {selected(S) : scientist(S)} 5.

% At least one of each type
:- not 1 {selected(S) : botanist(S)}.
:- not 1 {selected(S) : chemist(S)}.
:- not 1 {selected(S) : zoologist(S)}.

% If more than one botanist then at most one zoologist
:- 2 {selected(S) : botanist(S)}, 2 {selected(Z) : zoologist(Z)}.

% Incompatibilities
:- selected(f), selected(k).
:- selected(k), selected(m).

% If M selected then both P and R must be selected
:- selected(m), not selected(p).
:- selected(m), not selected(r).

% Condition: both G and H must be selected
:- not selected(g).
:- not selected(h).

% Violations for each option
violates_a :- not selected(f), not selected(k).
violates_b :- not selected(f), not selected(m).
violates_c :- not selected(k), not selected(m).
violates_d :- not selected(m), not selected(q).
violates_e :- not selected(p), not selected(q).

option(a) :- not violates_a.
option(b) :- not violates_b.
option(c) :- not violates_c.
option(d) :- not violates_d.
option(e) :- not violates_e.

#show option/1.