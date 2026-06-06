% Domains
rider(reynaldo; seamus; theresa; yuki).
bicycle(f; g; h; j).
day(1; 2).

% Generate all possible assignments
{ assign(R, B, D) : bicycle(B) } 1 :- rider(R), day(D).
{ assign(R, B, D) : rider(R) } 1 :- bicycle(B), day(D).

% Each rider tests a different bicycle on day 2 than day 1
:- assign(R, B, 1), assign(R, B, 2).

% Problem constraints
% Reynaldo cannot test F
:- assign(reynaldo, f, D).

% Yuki cannot test J
:- assign(yuki, j, D).

% Theresa must test H on at least one day
:- not assign(theresa, h, 1), not assign(theresa, h, 2).

% If Yuki tests B on day 1, Seamus must test B on day 2
:- assign(yuki, B, 1), not assign(seamus, B, 2).

% Define helper predicates for each option
% (A) Both Reynaldo and Seamus test J (on possibly different days)
assume_a :- assign(reynaldo, j, 1), assign(seamus, j, 2).
assume_a :- assign(reynaldo, j, 2), assign(seamus, j, 1).

% (B) Both Reynaldo and Theresa test J
assume_b :- assign(reynaldo, j, 1), assign(theresa, j, 2).
assume_b :- assign(reynaldo, j, 2), assign(theresa, j, 1).

% (C) Both Reynaldo and Yuki test G
assume_c :- assign(reynaldo, g, 1), assign(yuki, g, 2).
assume_c :- assign(reynaldo, g, 2), assign(yuki, g, 1).

% (D) Both Seamus and Theresa test G
assume_d :- assign(seamus, g, 1), assign(theresa, g, 2).
assume_d :- assign(seamus, g, 2), assign(theresa, g, 1).

% (E) Both Theresa and Yuki test F
assume_e :- assign(theresa, f, 1), assign(yuki, f, 2).
assume_e :- assign(theresa, f, 2), assign(yuki, f, 1).

% Check for contradiction under each assumption
% If assuming an option leads to a contradiction, it cannot be true
:- assume_a, not contradiction_a.
contradiction_a :- assign(reynaldo, j, D1), assign(seamus, j, D2), D1 != D2, assign(theresa, h, _), assign(yuki, B, 1), B != j.

:- assume_b, not contradiction_b.
contradiction_b :- assign(reynaldo, j, D1), assign(theresa, j, D2), D1 != D2, assign(theresa, h, _), assign(yuki, B, 1), B != j.

:- assume_c, not contradiction_c.
contradiction_c :- assign(reynaldo, g, D1), assign(yuki, g, D2), D1 != D2, assign(theresa, h, _), assign(yuki, B, 1), B != j.

:- assume_d, not contradiction_d.
contradiction_d :- assign(seamus, g, D1), assign(theresa, g, D2), D1 != D2, assign(theresa, h, _), assign(yuki, B, 1), B != j.

:- assume_e, not contradiction_e.
contradiction_e :- assign(theresa, f, D1), assign(yuki, f, D2), D1 != D2, assign(theresa, h, _), assign(yuki, B, 1), B != j.

% The correct answer is the option that leads to a contradiction
answer(a) :- assume_a, contradiction_a.
answer(b) :- assume_b, contradiction_b.
answer(c) :- assume_c, contradiction_c.
answer(d) :- assume_d, contradiction_d.
answer(e) :- assume_e, contradiction_e.

#show answer/1.