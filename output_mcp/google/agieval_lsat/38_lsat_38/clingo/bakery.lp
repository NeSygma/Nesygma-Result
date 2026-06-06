% Days and Types
day(mon; tue; wed; thu; fri).
type(oatmeal; peanut_butter; sugar).
batch(Type, 1..3) :- type(Type).

% Each batch is made on a single day
1 { made(Type, Batch, Day) : day(Day) } 1 :- batch(Type, Batch).

% No two batches of the same kind on the same day
:- made(Type, B1, Day), made(Type, B2, Day), B1 != B2.

% At least one batch on Monday
:- not 1 { made(Type, Batch, mon) : batch(Type, Batch) }.

% The second batch of oatmeal cookies is made on the same day as the first batch of peanut butter cookies
made(oatmeal, 2, Day) :- made(peanut_butter, 1, Day).
made(peanut_butter, 1, Day) :- made(oatmeal, 2, Day).

% The second batch of sugar cookies is made on Thursday
made(sugar, 2, thu).

% Count batches per day
batches_on_day(Day, N) :- day(Day), N = #count { Type, Batch : made(Type, Batch, Day) }.

% A day has at most two batches if N <= 2
at_most_two(Day) :- batches_on_day(Day, N), N <= 2.

% We want to know how many days satisfy this in ALL valid models.
% Let's check if the number of batches per day is constant across all models.
% If it's not constant, the question might be interpreted differently.
% Let's see if there are multiple models.
#show made/3.
#show batches_on_day/2.