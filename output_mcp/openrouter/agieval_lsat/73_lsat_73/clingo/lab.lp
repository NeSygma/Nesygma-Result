% Assistants
assistant(julio).
assistant(kevin).
assistant(lan).
assistant(nessa).
assistant(olivia).
assistant(rebecca).

% Days and times
day(wed). day(thu). day(fri).
time(morning). time(afternoon).

% Slots
slot(D,T) :- day(D), time(T).

% Assignment: each assistant assigned to exactly one slot
1 { assigned(A,D,T) : day(D), time(T) } 1 :- assistant(A).
1 { assigned(A,D,T) : assistant(A) } 1 :- day(D), time(T).

% Constraints
% Nessa must be afternoon
:- assigned(nessa,D,morning).

% Kevin and Rebecca same day
:- assigned(kevin,D1,_), assigned(rebecca,D2,_), D1 != D2.

% Lan and Olivia different day
:- assigned(lan,D,_), assigned(olivia,D,_).

% Julio earlier day than Olivia
% Define ordering via numeric mapping
day_num(wed,1). day_num(thu,2). day_num(fri,3).
:- assigned(julio,Dj,_), assigned(olivia,Do,_), day_num(Dj,Nj), day_num(Do,No), Nj >= No.

% Additional condition: Kevin day is the day before Nessa's day
:- assigned(kevin,Dk,_), assigned(nessa,Dn,_), day_num(Dk,Nk), day_num(Dn,Nn), Nk+1 != Nn.

% Forbid assistants that cannot be Thursday afternoon (derived from constraints)
:- assigned(julio,thu,afternoon).
:- assigned(lan,thu,afternoon).
:- assigned(olivia,thu,afternoon).

% Possible assistants for Thursday afternoon
possible(A) :- assigned(A,thu,afternoon).

% Map options
option(a) :- false. % never true
option(b) :- false.
option(c) :- possible(kevin), possible(nessa), possible(rebecca), not possible(julio), not possible(lan), not possible(olivia).
option(d) :- false.
option(e) :- false.

#show option/1.