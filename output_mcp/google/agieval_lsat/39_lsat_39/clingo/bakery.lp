% Days and Cookies
day(mon; tue; wed; thu; fri).
cookie(o; pb; s).
batch(1; 2; 3).

% Each batch is made on a single day
1 { made(C, B, D) : day(D) } 1 :- cookie(C), batch(B).

% No two batches of the same kind on the same day
:- made(C, B1, D), made(C, B2, D), B1 != B2.

% At least one batch on Monday
:- not 1 { made(C, B, mon) : cookie(C), batch(B) }.

% The second batch of oatmeal cookies is made on the same day as the first batch of peanut butter cookies
made(o, 2, D) :- made(pb, 1, D).

% The second batch of sugar cookies is made on Thursday
made(s, 2, thu).

% Condition: The first batch of peanut butter cookies is made on Tuesday
made(pb, 1, tue).

% Check possibility
possible_a :- 2 { made(C, 1, mon) : cookie(C) }.
possible_b :- 2 { made(C, 1, tue) : cookie(C) }.
possible_c :- 2 { made(C, 2, wed) : cookie(C) }.
possible_d :- 2 { made(C, 2, thu) : cookie(C) }.
possible_e :- 2 { made(C, 3, fri) : cookie(C) }.

% We want to find the one that is NOT possible.
% Let's force the solver to find a model where each one is true.
% If it's impossible, the solver will return UNSAT.
% But I need to do this in one file.

% Let's define a choice rule to pick which one we are testing.
{ test(a); test(b); test(c); test(d); test(e) } = 1.

:- test(a), not possible_a.
:- test(b), not possible_b.
:- test(c), not possible_c.
:- test(d), not possible_d.
:- test(e), not possible_e.

#show test/1.