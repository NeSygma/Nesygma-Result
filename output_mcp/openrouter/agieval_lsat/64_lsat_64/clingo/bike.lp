% Domains
rider(reynaldo). rider(seamus). rider(theresa). rider(yuki).

bike(f). bike(g). bike(h). bike(j).

time(1). time(2).

% Assignment choice: each rider gets exactly one bike each day
1 { assign(R,B,T) : bike(B) } 1 :- rider(R), time(T).
% each bike assigned to exactly one rider each day
1 { assign(R,B,T) : rider(R) } 1 :- bike(B), time(T).

% Constraints
% Reynaldo cannot test F
:- assign(reynaldo, f, T).
% Yuki cannot test J
:- assign(yuki, j, T).
% Theresa must test H on some day
:- not assign(theresa, h, 1), not assign(theresa, h, 2).
% Theresa tests J on day 1 (given premise)
assign(theresa, j, 1).
% Yuki's bike day1 must be tested by Seamus day2
:- assign(yuki, B, 1), not assign(seamus, B, 2).

% Conditions for options
cond_a :- assign(reynaldo, g, 2).
cond_b :- assign(seamus, h, 1).
cond_c :- assign(yuki, h, 2).
cond_d :- assign(seamus, j, T).
cond_e :- assign(theresa, g, T).

% Option mapping
option(a) :- cond_a.
option(b) :- cond_b.
option(c) :- cond_c.
option(d) :- cond_d.
option(e) :- cond_e.

% Equivalence constraints
:- option(a), not cond_a.
:- not option(a), cond_a.
:- option(b), not cond_b.
:- not option(b), cond_b.
:- option(c), not cond_c.
:- not option(c), cond_c.
:- option(d), not cond_d.
:- not option(d), cond_d.
:- option(e), not cond_e.
:- not option(e), cond_e.

% Exactly one option true
1 { option(a); option(b); option(c); option(d); option(e) } 1.

#show option/1.