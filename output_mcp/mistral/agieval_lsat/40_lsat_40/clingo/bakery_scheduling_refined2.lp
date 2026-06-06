% Base domains
cookie(oatmeal; peanut_butter; sugar).
day(monday; tuesday; thursday; friday).  % Exclude Wednesday as per the condition

% Batches for each cookie type
batch(oatmeal,1..3).
batch(peanut_butter,1..3).
batch(sugar,1..3).

% Each batch is assigned to exactly one day
1 { assigned_to(Batch, Cookie, Day) : day(Day) } 1 :-
    cookie(Cookie),
    batch(Cookie, Batch).

% Constraint 1: No two batches of the same kind on the same day
:- cookie(Cookie),
   day(Day),
   batch(Cookie, B1),
   batch(Cookie, B2),
   B1 < B2,
   assigned_to(B1, Cookie, Day),
   assigned_to(B2, Cookie, Day).

% Constraint 2: At least one batch on Monday
:- not day_has_batch(monday).

% Helper: day_has_batch(Day) means at least one batch is assigned to Day
day_has_batch(Day) :-
    cookie(Cookie),
    batch(Cookie, _),
    assigned_to(_, Cookie, Day).

% Constraint 3: The second batch of oatmeal is made on the same day as the first batch of peanut butter
:- assigned_to(2, oatmeal, DayO),
   assigned_to(1, peanut_butter, DayP),
   DayO != DayP.

% Constraint 4: The second batch of sugar cookies is made on Thursday
:- not assigned_to(2, sugar, thursday).

% Count batches per day
batches_on_day(Day, N) :-
    day(Day),
    N = #count { Cookie, Batch : assigned_to(Batch, Cookie, Day) }.

% Ensure that only one option can be true at a time by making them mutually exclusive
% This is a meta-constraint to ensure a unique answer
:- option(X), option(Y), X != Y.

% Answer choices mapping
% (A) Exactly three batches of cookies are made on Tuesday
option(a) :- batches_on_day(tuesday, 3),
             not option(b),
             not option(c),
             not option(d),
             not option(e).

% (B) Exactly three batches of cookies are made on Friday
option(b) :- batches_on_day(friday, 3),
             not option(a),
             not option(c),
             not option(d),
             not option(e).

% (C) At least two batches of cookies are made on Monday
option(c) :- batches_on_day(monday, N), N >= 2,
             not option(a),
             not option(b),
             not option(d),
             not option(e).

% (D) At least two batches of cookies are made on Thursday
option(d) :- batches_on_day(thursday, N), N >= 2,
             not option(a),
             not option(b),
             not option(c),
             not option(e).

% (E) Fewer batches of cookies are made on Monday than on Tuesday
option(e) :- batches_on_day(monday, N1),
             batches_on_day(tuesday, N2),
             N1 < N2,
             not option(a),
             not option(b),
             not option(c),
             not option(d).

#show option/1.