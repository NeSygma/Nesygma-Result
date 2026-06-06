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

% Each rider tests different bicycles on the two days
:- rider(R), bike(B1), bike(B2), B1 != B2, test(R, B1, 1), test(R, B2, 2).
% Actually, let me rephrase: the rider's day1 bike != day2 bike 
:- rider(R), bike(B), test(R, B, 1), test(R, B, 2).

% Condition 1: Reynaldo cannot test F
:- test(reynaldo, f, _).

% Condition 2: Yuki cannot test J
:- test(yuki, j, _).

% Condition 3: Theresa must be one of the testers for H (on at least one day)
:- not test(theresa, h, 1), not test(theresa, h, 2).

% Condition 4: The bicycle that Yuki tests on day 1 must be tested by Seamus on day 2
:- test(yuki, B, 1), not test(seamus, B, 2).

% --- Option Testing ---
% We'll test each option by seeing if it's possible.

% Option A: Reynaldo tests G on the second day.
option(a) :- not possible_not_a.
possible_not_a :- not test(reynaldo, g, 2).

% Option B: Seamus tests F on the first day.
option(b) :- not possible_not_b.
possible_not_b :- not test(seamus, f, 1).

% Option C: Theresa tests F on the second day.
option(c) :- not possible_not_c.
possible_not_c :- not test(theresa, f, 2).

% Option D: Reynaldo tests H on the first day.
option(d) :- not possible_not_d.
possible_not_d :- not test(reynaldo, h, 1).

% Option E: Yuki tests F on the second day.
option(e) :- not possible_not_e.
possible_not_e :- not test(yuki, f, 2).

#show option/1.