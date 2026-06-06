% Define the domain
bird(oystercatchers).
bird(petrels).
bird(rails).
bird(sandpipers).
bird(terns).

location(howard).
location(gladwyn).

time(1..5).

% Assign each bird to exactly one time slot
1 { assigned(Bird, Time) : bird(Bird) } 1 :- time(Time).

% Assign each time slot to exactly one location
1 { located(Time, Location) : location(Location) } 1 :- time(Time).

% Constraint 1: The first lecture is in Gladwyn Hall
:- located(1, howard).

% Constraint 2: The fourth lecture is in Howard Auditorium
:- located(4, gladwyn).

% Constraint 3: Exactly three lectures are in Gladwyn Hall
:- { located(T, gladwyn) : time(T) } != 3.

% Constraint 4: The lecture on sandpipers is in Howard Auditorium and is given earlier than the lecture on oystercatchers
:- assigned(sandpipers, T1), located(T1, gladwyn).
:- assigned(sandpipers, T1), assigned(oystercatchers, T2), T1 >= T2.

% Constraint 5: The lecture on terns is given earlier than the lecture on petrels, which is in Gladwyn Hall
:- assigned(terns, T1), assigned(petrels, T2), T1 >= T2.
:- assigned(petrels, T), located(T, howard).

% Show all assignments and locations for debugging
#show assigned/2.
#show located/2.

% Map the correct answer to option/1 (MANDATORY)
% We need to check which of the options could be true
% Since we want to find which option COULD be true, we need to see which one is consistent with the constraints

% Option A: Fifth lecture is on oystercatchers and is in Gladwyn Hall
option(a) :- assigned(oystercatchers, 5), located(5, gladwyn).

% Option B: Fifth lecture is on petrels and is in Howard Auditorium
option(b) :- assigned(petrels, 5), located(5, howard).

% Option C: Fifth lecture is on rails and is in Howard Auditorium
option(c) :- assigned(rails, 5), located(5, howard).

% Option D: Fifth lecture is on sandpipers and is in Howard Auditorium
option(d) :- assigned(sandpipers, 5), located(5, howard).

% Option E: Fifth lecture is on terns and is in Gladwyn Hall
option(e) :- assigned(terns, 5), located(5, gladwyn).

#show option/1.