% Domain
rider(reynaldo).
rider(seamus).
rider(theresa).
rider(yuki).

bike(f).
bike(g).
bike(h).
bike(j).

day(1).
day(2).

% Each rider tests exactly one bike per day
1 { tests(R, B, D) : bike(B) } 1 :- rider(R), day(D).

% Each bike is tested by exactly one rider per day
1 { tests(R, B, D) : rider(R) } 1 :- bike(B), day(D).

% Each rider tests a different bike on day 2 than day 1
:- tests(R, B, 1), tests(R, B, 2).

% Constraint 1: Reynaldo cannot test F (on any day)
:- tests(reynaldo, f, D).

% Constraint 2: Yuki cannot test J (on any day)
:- tests(yuki, j, D).

% Constraint 3: Theresa must test H on at least one day
tests(theresa, h, 1) | tests(theresa, h, 2).

% Constraint 4: The bike Yuki tests on day 1 must be tested by Seamus on day 2
tests(seamus, B, 2) :- tests(yuki, B, 1).

% Check each option
% Option A: Both Reynaldo and Seamus test J (on some days)
opt_a :- tests(reynaldo, j, _), tests(seamus, j, _).

% Option B: Both Reynaldo and Theresa test J
opt_b :- tests(reynaldo, j, _), tests(theresa, j, _).

% Option C: Both Reynaldo and Yuki test G
opt_c :- tests(reynaldo, g, _), tests(yuki, g, _).

% Option D: Both Seamus and Theresa test G
opt_d :- tests(seamus, g, _), tests(theresa, g, _).

% Option E: Both Theresa and Yuki test F
opt_e :- tests(theresa, f, _), tests(yuki, f, _).

% Try to maximize all options
#maximize { 1@5,opt_a; 1@4,opt_b; 1@3,opt_c; 1@2,opt_d; 1@1,opt_e }.

#show opt_a/0.
#show opt_b/0.
#show opt_c/0.
#show opt_d/0.
#show opt_e/0.
#show tests/3.