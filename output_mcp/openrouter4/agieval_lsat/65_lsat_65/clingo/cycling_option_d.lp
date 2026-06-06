% Riders
rider(reynaldo; seamus; theresa; yuki).

% Bicycles
bicycle(f; g; h; j).

% Days
day(1; 2).

% Each rider tests exactly 1 bicycle per day
1 { assignment(R, B, D) : bicycle(B) } 1 :- rider(R), day(D).

% Each bicycle is tested by exactly 1 rider per day
1 { assignment(R, B, D) : rider(R) } 1 :- bicycle(B), day(D).

% Each rider tests a different bicycle each day
:- assignment(R, B1, 1), assignment(R, B2, 2), B1 = B2.

% Condition 1: Reynaldo cannot test F
:- assignment(reynaldo, f, D), day(D).

% Condition 2: Yuki cannot test J
:- assignment(yuki, j, D), day(D).

% Condition 3: Theresa must test H at least once
1 { assignment(theresa, h, D) : day(D) } 1.

% Condition 4: Yuki's day 1 bike is tested by Seamus on day 2
:- assignment(yuki, B, 1), not assignment(seamus, B, 2).

% Option D: Both Seamus and Theresa test G
:- not assignment(seamus, g, _).  % Seamus must test G on some day
:- not assignment(theresa, g, _).  % Theresa must test G on some day

#show assignment/3.