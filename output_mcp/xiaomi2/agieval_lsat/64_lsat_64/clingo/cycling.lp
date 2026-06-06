% Domains
rider(reynaldo).
rider(seamus).
rider(theresa).
rider(yuki).

bicycle(f).
bicycle(g).
bicycle(h).
bicycle(j).

day(1).
day(2).

% Each rider tests exactly one bicycle per day
{ assign(R, B, D) : bicycle(B) } = 1 :- rider(R), day(D).

% Each bicycle is tested by exactly one rider per day
{ assign(R, B, D) : rider(R) } = 1 :- bicycle(B), day(D).

% Each rider tests a different bicycle on day2 than on day1
:- assign(R, B, 1), assign(R, B, 2).

% Reynaldo cannot test F
:- assign(reynaldo, f, D), day(D).

% Yuki cannot test J
:- assign(yuki, j, D), day(D).

% Theresa must test H at least once
test_h(theresa) :- assign(theresa, h, 1).
test_h(theresa) :- assign(theresa, h, 2).
:- not test_h(theresa).

% Yuki's day1 bicycle must be tested by Seamus on day2
:- assign(yuki, B, 1), not assign(seamus, B, 2).

% Conditional: Theresa tests J on day1
assign(theresa, j, 1).

% Define options
option_a :- assign(reynaldo, g, 2).
option_b :- assign(seamus, h, 1).
option_c :- assign(yuki, h, 2).
option_d :- assign(seamus, j, 1).
option_d :- assign(seamus, j, 2).
option_e :- assign(theresa, g, 1).
option_e :- assign(theresa, g, 2).

% We want to know which options could be true.
% We'll allow any subset of options to be true, but we must have at least one.
{ option(a); option(b); option(c); option(d); option(e) }.
:- not option(a), not option(b), not option(c), not option(d), not option(e).

% Link option atoms to conditions
option(a) :- option_a.
option(b) :- option_b.
option(c) :- option_c.
option(d) :- option_d.
option(e) :- option_e.

#show option/1.
#show assign/3.