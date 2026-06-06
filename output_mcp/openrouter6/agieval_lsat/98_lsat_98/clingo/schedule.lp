% Witnesses and days
witness(franco). witness(garcia). witness(hong). witness(iturbe). witness(jackson).
day(monday). day(tuesday). day(wednesday).

% Choice of exactly one option
{ choose(a); choose(b); choose(c); choose(d); choose(e) } 1.

% Schedule for each option (conditional on choose)
testifies(franco, monday) :- choose(a).
testifies(hong, tuesday) :- choose(a).
testifies(iturbe, tuesday) :- choose(a).
testifies(garcia, wednesday) :- choose(a).
testifies(jackson, wednesday) :- choose(a).

testifies(franco, monday) :- choose(b).
testifies(hong, monday) :- choose(b).
testifies(iturbe, tuesday) :- choose(b).
testifies(jackson, tuesday) :- choose(b).
testifies(garcia, wednesday) :- choose(b).

testifies(garcia, monday) :- choose(c).
testifies(franco, tuesday) :- choose(c).
testifies(iturbe, tuesday) :- choose(c).
testifies(hong, wednesday) :- choose(c).
testifies(jackson, wednesday) :- choose(c).

testifies(garcia, monday) :- choose(d).
testifies(jackson, monday) :- choose(d).
testifies(franco, tuesday) :- choose(d).
testifies(hong, tuesday) :- choose(d).
testifies(iturbe, wednesday) :- choose(d).

testifies(garcia, monday) :- choose(e).
testifies(jackson, monday) :- choose(e).
testifies(hong, tuesday) :- choose(e).
testifies(franco, wednesday) :- choose(e).
testifies(iturbe, wednesday) :- choose(e).

% Each witness testifies exactly one day
1 { testifies(W, D) : day(D) } 1 :- witness(W).

% Iturbe testifies on Wednesday (fact)
testifies(iturbe, wednesday).

% Constraints
:- testifies(franco, D), testifies(garcia, D).          % Franco and Garcia not same day
:- testifies(hong, monday).                             % Hong not on Monday
:- #count{ W : testifies(W, tuesday) } != 2.            % Exactly two on Tuesday
:- #count{ W : testifies(W, monday) } < 1.              % At least one on Monday

% Map the correct answer to option/1
option(a) :- choose(a).
option(b) :- choose(b).
option(c) :- choose(c).
option(d) :- choose(d).
option(e) :- choose(e).

#show option/1.