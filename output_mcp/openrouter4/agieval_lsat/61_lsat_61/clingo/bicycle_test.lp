% Riders
rider(reynaldo; seamus; theresa; yuki).

% Bicycles
bike(f; g; h; j).

% Days
day(1; 2).

% Each rider tests exactly one bike per day
1 { test(R, B, D) : bike(B) } 1 :- rider(R), day(D).

% Each bike is tested by exactly one rider per day
1 { test(R, B, D) : rider(R) } 1 :- bike(B), day(D).

% No rider tests the same bike on both days
:- rider(R), test(R, B, 1), test(R, B, 2).

% Constraint 1: Reynaldo cannot test F
:- test(reynaldo, f, D), day(D).

% Constraint 2: Yuki cannot test J
:- test(yuki, j, D), day(D).

% Constraint 3: Theresa must test H at least once
:- not test(theresa, h, 1), not test(theresa, h, 2).

% Constraint 4: The bike Yuki tests on day 1 must be tested by Seamus on day 2
test(seamus, B, 2) :- test(yuki, B, 1).

% Hypothetical: Theresa tests G on the second day
test(theresa, g, 2).

% --- Option definitions ---

% Option A: Reynaldo tests H on the first day
opt_a :- test(reynaldo, h, 1).

% Option B: Reynaldo tests J on the first day
opt_b :- test(reynaldo, j, 1).

% Option C: Theresa tests H on the second day
opt_c :- test(theresa, h, 2).

% Option D: Theresa tests J on the first day
opt_d :- test(theresa, j, 1).

% Option E: Yuki tests H on the second day
opt_e :- test(yuki, h, 2).

% Derive answer: the option that holds
option(a) :- opt_a.
option(b) :- opt_b.
option(c) :- opt_c.
option(d) :- opt_d.
option(e) :- opt_e.

#show test/3.
#show option/1.