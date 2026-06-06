% Define riders, bicycles, and days
rider(reynaldo). rider(seamus). rider(theresa). rider(yuki).
bicycle(f). bicycle(g). bicycle(h). bicycle(j).
day(day1). day(day2).

% Base constraints (always active)
:- assign(reynaldo, f, D).
:- assign(yuki, j, D).
:- not assign(theresa, h, _).
:- assign(yuki, B, day1), not assign(seamus, B, day2).

% Each bicycle has exactly one rider per day
1 { assign(R, B, D) : rider(R) } 1 :- bicycle(B), day(D).

% Each rider tests exactly one bicycle per day
1 { assign(R, B, D) : bicycle(B) } 1 :- rider(R), day(D).

% Option A
assign(seamus, f, day1) :- option_a.
assign(reynaldo, f, day2) :- option_a.
assign(yuki, g, day1) :- option_a.
assign(seamus, g, day2) :- option_a.
assign(theresa, h, day1) :- option_a.
assign(yuki, h, day2) :- option_a.
assign(reynaldo, j, day1) :- option_a.
assign(theresa, j, day2) :- option_a.

% Option B
assign(seamus, f, day1) :- option_b.
assign(yuki, f, day2) :- option_b.
assign(reynaldo, g, day1) :- option_b.
assign(theresa, g, day2) :- option_b.
assign(yuki, h, day1) :- option_b.
assign(seamus, h, day2) :- option_b.
assign(theresa, j, day1) :- option_b.
assign(reynaldo, j, day2) :- option_b.

% Option C
assign(yuki, f, day1) :- option_c.
assign(seamus, f, day2) :- option_c.
assign(seamus, g, day1) :- option_c.
assign(reynaldo, g, day2) :- option_c.
assign(theresa, h, day1) :- option_c.
assign(yuki, h, day2) :- option_c.
assign(reynaldo, j, day1) :- option_c.
assign(theresa, j, day2) :- option_c.

% Option D
assign(yuki, f, day1) :- option_d.
assign(seamus, f, day2) :- option_d.
assign(theresa, g, day1) :- option_d.
assign(reynaldo, g, day2) :- option_d.
assign(reynaldo, h, day1) :- option_d.
assign(theresa, h, day2) :- option_d.
assign(seamus, j, day1) :- option_d.
assign(yuki, j, day2) :- option_d.

% Option E
assign(yuki, f, day1) :- option_e.
assign(theresa, f, day2) :- option_e.
assign(seamus, g, day1) :- option_e.
assign(yuki, g, day2) :- option_e.
assign(theresa, h, day1) :- option_e.
assign(reynaldo, h, day2) :- option_e.
assign(reynaldo, j, day1) :- option_e.
assign(seamus, j, day2) :- option_e.

% Only one option can be selected
1 { option_a; option_b; option_c; option_d; option_e } 1.

% Map the correct answer to option/1
option(a) :- option_a.
option(b) :- option_b.
option(c) :- option_c.
option(d) :- option_d.
option(e) :- option_e.

#show option/1.