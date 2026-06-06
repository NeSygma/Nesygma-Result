% --- Domains ---
day(day1; day2).
rider(reynaldo; seamus; theresa; yuki).
bicycle(f; g; h; j).

% --- Base Constraints ---
% Reynaldo cannot test F
:- assign(reynaldo, f, D), day(D).

% Yuki cannot test J
:- assign(yuki, j, D), day(D).

% Theresa must test H
assign(theresa, h, D) :- day(D).

% The bicycle that Yuki tests on day1 must be tested by Seamus on day2
:- assign(yuki, B, day1), bicycle(B),
   not assign(seamus, B, day2).

% Each rider tests exactly one bicycle per day
{ assign(R, B, D) : bicycle(B) } 1 :- rider(R), day(D).

% Each bicycle is tested by exactly one rider per day
{ assign(R, B, D) : rider(R) } 1 :- bicycle(B), day(D).

% Riders must test a different bicycle on day2 than on day1
:- assign(R, B, day1), assign(R, B, day2).

% --- Define options ---
% Option A: Both Reynaldo and Seamus test J
% This means:
%   assign(reynaldo, j, day1), assign(seamus, j, day2)
%   or
%   assign(reynaldo, j, day2), assign(seamus, j, day1)
option(a) :-
    assign(reynaldo, j, day1), assign(seamus, j, day2).
option(a) :-
    assign(reynaldo, j, day2), assign(seamus, j, day1).

% Option B: Both Reynaldo and Theresa test J
% This is impossible because Theresa must test H.
option(b) :- false.

% Option C: Both Reynaldo and Yuki test G
% This means:
%   assign(reynaldo, g, D1), assign(yuki, g, D2)
option(c) :-
    assign(reynaldo, g, _), assign(yuki, g, _).

% Option D: Both Seamus and Theresa test G
% This is impossible because Theresa must test H.
option(d) :- false.

% Option E: Both Theresa and Yuki test F
% This means:
%   assign(theresa, f, D1), assign(yuki, f, D2)
option(e) :-
    assign(theresa, f, _), assign(yuki, f, _).

% --- Derive the answer ---
% The correct answer is the option that cannot be true.
answer(a) :- option(a), not option(b), not option(c), not option(d), not option(e).
answer(b) :- not option(b), option(a), not option(c), not option(d), not option(e).
answer(c) :- not option(c), option(a), option(b), not option(d), not option(e).
answer(d) :- not option(d), option(a), option(b), option(c), not option(e).
answer(e) :- not option(e), option(a), option(b), option(c), option(d).

#show answer/1.