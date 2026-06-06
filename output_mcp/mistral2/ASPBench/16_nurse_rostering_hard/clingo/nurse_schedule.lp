% Declare nurses, days, and shifts
nurse(1..5).
day(1..10).
shift(1..3). % 1: Morning, 2: Evening, 3: Night

% Required coverage for each shift
required(day(D), shift(1), 2) :- day(D).
required(day(D), shift(2), 1) :- day(D).
required(day(D), shift(3), 1) :- day(D).

% Choice rule: Assign nurses to shifts for each day
{ assigned(Nurse, Day, Shift) : nurse(Nurse) } = Required :-
    day(Day),
    shift(Shift),
    required(day(Day), shift(Shift), Required).

% Constraint: Ensure exactly the required number of nurses are assigned to each shift
:- day(Day), shift(Shift), required(day(Day), shift(Shift), Required),
   #count { Nurse : assigned(Nurse, Day, Shift) } != Required.

% Constraint: Single assignment per day (at most one shift per nurse per day)
:- nurse(Nurse), day(Day), assigned(Nurse, Day, Shift1), assigned(Nurse, Day, Shift2), Shift1 != Shift2.

% Constraint: Rest period (no nurse can work morning shift the day after a night shift)
:- assigned(Nurse, Day, 3), assigned(Nurse, NextDay, 1),
   NextDay = Day + 1.

% Show the assignments
#show assigned/3.