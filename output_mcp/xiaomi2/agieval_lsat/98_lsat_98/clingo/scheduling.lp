% Witnesses and days
witness(franco). witness(garcia). witness(hong). witness(iturbe). witness(jackson).
day(monday). day(tuesday). day(wednesday).

% Option domain
option_name(a). option_name(b). option_name(c). option_name(d). option_name(e).

% Option assignments: option_assigned(Option, Witness, Day)
% Option A: Monday: Franco; Tuesday: Hong, Iturbe; Wednesday: Garcia, Jackson
option_assigned(a, franco, monday).
option_assigned(a, hong, tuesday).
option_assigned(a, iturbe, tuesday).
option_assigned(a, garcia, wednesday).
option_assigned(a, jackson, wednesday).

% Option B: Monday: Franco, Hong; Tuesday: Iturbe, Jackson; Wednesday: Garcia
option_assigned(b, franco, monday).
option_assigned(b, hong, monday).
option_assigned(b, iturbe, tuesday).
option_assigned(b, jackson, tuesday).
option_assigned(b, garcia, wednesday).

% Option C: Monday: Garcia; Tuesday: Franco, Iturbe; Wednesday: Hong, Jackson
option_assigned(c, garcia, monday).
option_assigned(c, franco, tuesday).
option_assigned(c, iturbe, tuesday).
option_assigned(c, hong, wednesday).
option_assigned(c, jackson, wednesday).

% Option D: Monday: Garcia, Jackson; Tuesday: Franco, Hong; Wednesday: Iturbe
option_assigned(d, garcia, monday).
option_assigned(d, jackson, monday).
option_assigned(d, franco, tuesday).
option_assigned(d, hong, tuesday).
option_assigned(d, iturbe, wednesday).

% Option E: Monday: Garcia, Jackson; Tuesday: Hong; Wednesday: Franco, Iturbe
option_assigned(e, garcia, monday).
option_assigned(e, jackson, monday).
option_assigned(e, hong, tuesday).
option_assigned(e, franco, wednesday).
option_assigned(e, iturbe, wednesday).

% Each witness must testify exactly once per option
violates(O) :- option_name(O), witness(W), #count{D : option_assigned(O, W, D)} != 1.

% Constraint 1: Franco and Garcia not on same day
violates(O) :- option_assigned(O, franco, D), option_assigned(O, garcia, D).

% Constraint 2: Iturbe must be on Wednesday
violates(O) :- option_assigned(O, iturbe, D), D != wednesday.

% Constraint 3: Exactly two witnesses on Tuesday
count_tuesday(O, N) :- option_name(O), N = #count{W : option_assigned(O, W, tuesday)}.
violates(O) :- count_tuesday(O, N), N != 2.

% Constraint 4: Hong not on Monday
violates(O) :- option_assigned(O, hong, monday).

% Constraint 5: At least one witness on Monday
count_monday(O, N) :- option_name(O), N = #count{W : option_assigned(O, W, monday)}.
violates(O) :- count_monday(O, N), N < 1.

% An option is valid if it does not violate any constraint
option_valid(O) :- option_name(O), not violates(O).

% Map to option/1
option(a) :- option_valid(a).
option(b) :- option_valid(b).
option(c) :- option_valid(c).
option(d) :- option_valid(d).
option(e) :- option_valid(e).

#show option/1.