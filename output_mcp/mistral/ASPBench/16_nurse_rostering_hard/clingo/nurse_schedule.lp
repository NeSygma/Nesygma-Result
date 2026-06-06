% Domains
nurse(1..5).
day(1..10).
shift(1..3).  % 1=Morning, 2=Evening, 3=Night

% Choice rule: Assign nurses to shifts on each day
{ assigned(N,D,S) : nurse(N) } = C :- day(D), shift(S), coverage(S,C).

% Coverage requirements (hard constraints)
coverage(1,2).  % Morning shift: exactly 2 nurses
coverage(2,1).  % Evening shift: exactly 1 nurse
coverage(3,1).  % Night shift: exactly 1 nurse

% Constraint 2: Single assignment per day (at most one shift per nurse per day)
:- nurse(N), day(D), 2 { assigned(N,D,S) : shift(S) }.

% Constraint 3: Rest period after night shift
% A nurse working night shift on day D cannot work morning shift on day D+1
:- assigned(N,D,3), assigned(N,D1,1), D1 = D+1.

% Show the assignment
#show assigned/3.