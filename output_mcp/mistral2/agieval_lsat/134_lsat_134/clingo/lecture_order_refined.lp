% Define the lectures and locations
lecture(1..5).
location("Gladwyn Hall").
location("Howard Auditorium").

% Bird types
bird(oystercatchers).
bird(petrels).
bird(rails).
bird(sandpipers).
bird(terns).

% Assign locations to lectures
1 { location_lecture(Loc, L) : location(Loc) } 1 :- lecture(L).

% Ensure the first lecture is in Gladwyn Hall
:- not location_lecture("Gladwyn Hall", 1).

% Ensure the fourth lecture is in Howard Auditorium
:- not location_lecture("Howard Auditorium", 4).

% Exactly three lectures are in Gladwyn Hall
:- 3 != #count { L : location_lecture("Gladwyn Hall", L) }.

% Assign birds to lectures
1 { assigned_lecture(B, L) : bird(B) } 1 :- lecture(L).

% Ensure each bird is assigned to exactly one lecture
:- bird(B), not 1 { assigned_lecture(B, L) : lecture(L) } 1.

% The lecture on sandpipers is in Howard Auditorium and is earlier than the lecture on oystercatchers
:- assigned_lecture(sandpipers, L1),
   assigned_lecture(oystercatchers, L2),
   L1 >= L2.
:- assigned_lecture(sandpipers, L),
   not location_lecture("Howard Auditorium", L).

% The lecture on terns is earlier than the lecture on petrels, which is in Gladwyn Hall
:- assigned_lecture(terns, L1),
   assigned_lecture(petrels, L2),
   L1 >= L2.
:- assigned_lecture(petrels, L),
   not location_lecture("Gladwyn Hall", L).

% Option A: oystercatchers, petrels, rails, sandpipers, terns
option(a) :- assigned_lecture(oystercatchers, 1),
             assigned_lecture(petrels, 2),
             assigned_lecture(rails, 3),
             assigned_lecture(sandpipers, 4),
             assigned_lecture(terns, 5),
             location_lecture("Gladwyn Hall", 1),
             location_lecture("Gladwyn Hall", 2),
             location_lecture("Gladwyn Hall", 3),
             location_lecture("Howard Auditorium", 4),
             location_lecture("Gladwyn Hall", 5).

% Option B: petrels, sandpipers, oystercatchers, terns, rails
option(b) :- assigned_lecture(petrels, 1),
             assigned_lecture(sandpipers, 2),
             assigned_lecture(oystercatchers, 3),
             assigned_lecture(terns, 4),
             assigned_lecture(rails, 5),
             location_lecture("Gladwyn Hall", 1),
             location_lecture("Howard Auditorium", 2),
             location_lecture("Gladwyn Hall", 3),
             location_lecture("Gladwyn Hall", 4),
             location_lecture("Howard Auditorium", 5).

% Option C: rails, sandpipers, terns, petrels, oystercatchers
option(c) :- assigned_lecture(rails, 1),
             assigned_lecture(sandpipers, 2),
             assigned_lecture(terns, 3),
             assigned_lecture(petrels, 4),
             assigned_lecture(oystercatchers, 5),
             location_lecture("Gladwyn Hall", 1),
             location_lecture("Howard Auditorium", 2),
             location_lecture("Gladwyn Hall", 3),
             location_lecture("Gladwyn Hall", 4),
             location_lecture("Howard Auditorium", 5).

% Option D: sandpipers, terns, oystercatchers, rails, petrels
option(d) :- assigned_lecture(sandpipers, 1),
             assigned_lecture(terns, 2),
             assigned_lecture(oystercatchers, 3),
             assigned_lecture(rails, 4),
             assigned_lecture(petrels, 5),
             location_lecture("Gladwyn Hall", 1),
             location_lecture("Gladwyn Hall", 2),
             location_lecture("Gladwyn Hall", 3),
             location_lecture("Howard Auditorium", 4),
             location_lecture("Gladwyn Hall", 5).

% Option E: terns, petrels, sandpipers, oystercatchers, rails
option(e) :- assigned_lecture(terns, 1),
             assigned_lecture(petrels, 2),
             assigned_lecture(sandpipers, 3),
             assigned_lecture(oystercatchers, 4),
             assigned_lecture(rails, 5),
             location_lecture("Gladwyn Hall", 1),
             location_lecture("Gladwyn Hall", 2),
             location_lecture("Howard Auditorium", 3),
             location_lecture("Howard Auditorium", 4),
             location_lecture("Gladwyn Hall", 5).

#show option/1.