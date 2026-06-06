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
option_holds(a) :-
    assign(reynaldo, j, day1), assign(seamus, j, day2).
option_holds(a) :-
    assign(reynaldo, j, day2), assign(seamus, j, day1).

% Option B: Both Reynaldo and Theresa test J
% This means:
%   assign(reynaldo, j, D1), assign(theresa, j, D2)
% But Theresa must test H, so this is impossible.
option_holds(b) :- assign(reynaldo, j, _), assign(theresa, j, _).

% Option C: Both Reynaldo and Yuki test G
% This means:
%   assign(reynaldo, g, D1), assign(yuki, g, D2)
option_holds(c) :-
    assign(reynaldo, g, _), assign(yuki, g, _).

% Option D: Both Seamus and Theresa test G
% This means:
%   assign(seamus, g, D1), assign(theresa, g, D2)
% But Theresa must test H, so this is impossible.
option_holds(d) :- assign(seamus, g, _), assign(theresa, g, _).

% Option E: Both Theresa and Yuki test F
% This means:
%   assign(theresa, f, D1), assign(yuki, f, D2)
option_holds(e) :-
    assign(theresa, f, _), assign(yuki, f, _).

% --- Derive the answer ---
% The correct answer is the option that cannot be true.
answer(a) :- option_holds(a), not option_holds(b), not option_holds(c), not option_holds(d), not option_holds(e).
answer(b) :- not option_holds(b), option_holds(a), not option_holds(c), not option_holds(d), not option_holds(e).
answer(c) :- not option_holds(c), option_holds(a), option_holds(b), not option_holds(d), not option_holds(e).
answer(d) :- not option_holds(d), option_holds(a), option_holds(b), option_holds(c), not option_holds(e).
answer(e) :- not option_holds(e), option_holds(a), option_holds(b), option_holds(c), option_holds(d).

#show answer/1.