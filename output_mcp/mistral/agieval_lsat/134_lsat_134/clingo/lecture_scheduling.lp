% Define bird types
bird(oystercatchers).
bird(petrels).
bird(rails).
bird(sandpipers).
bird(terns).

% Define locations
location(gladwyn).
location(howard).

% Define time slots (1st to 5th)
time(1..5).

% Assign each bird to a unique time slot
1 { assigned(B, T) : time(T) } 1 :- bird(B).

% Assign each bird to a location
{ assigned_location(B, L) : location(L) } 1 :- bird(B).

% --- BASE CONSTRAINTS ---

% Constraint 1: First lecture is in Gladwyn Hall
:- assigned(B, 1), assigned_location(B, howard).

% Constraint 2: Fourth lecture is in Howard Auditorium
:- assigned(B, 4), assigned_location(B, gladwyn).

% Constraint 3: Exactly three of the lectures are in Gladwyn Hall
:- { assigned_location(B, gladwyn) : bird(B) } != 3.

% Constraint 4: Sandpipers is in Howard Auditorium and is given earlier than oystercatchers
:- assigned_location(sandpipers, gladwyn).
:- assigned(sandpipers, T1), assigned(oystercatchers, T2), T1 >= T2.

% Constraint 5: Terns is given earlier than petrels, which is in Gladwyn Hall
:- assigned(terns, T1), assigned(petrels, T2), T1 >= T2.
:- assigned_location(petrels, howard).

% --- MULTIPLE CHOICE OPTIONS ---

% Option A: oystercatchers, petrels, rails, sandpipers, terns
% Time: 1:oystercatchers, 2:petrels, 3:rails, 4:sandpipers, 5:terns
% Locations: oystercatchers (Gladwyn), petrels (Gladwyn), rails (Gladwyn), sandpipers (Howard), terns (Gladwyn)
% Constraints: sandpipers (4) must be earlier than oystercatchers (1) -> false
option(a) :- 
    assigned(oystercatchers, 1), assigned(petrels, 2), assigned(rails, 3), 
    assigned(sandpipers, 4), assigned(terns, 5),
    assigned_location(oystercatchers, gladwyn),
    assigned_location(petrels, gladwyn),
    assigned_location(rails, gladwyn),
    assigned_location(sandpipers, howard),
    assigned_location(terns, gladwyn).

% Option B: petrels, sandpipers, oystercatchers, terns, rails
% Time: 1:petrels, 2:sandpipers, 3:oystercatchers, 4:terns, 5:rails
% Locations: petrels (Gladwyn), sandpipers (Howard), oystercatchers (Howard), terns (Gladwyn), rails (Gladwyn)
% Constraints: terns (4) must be earlier than petrels (1) -> false
option(b) :- 
    assigned(petrels, 1), assigned(sandpipers, 2), assigned(oystercatchers, 3), 
    assigned(terns, 4), assigned(rails, 5),
    assigned_location(petrels, gladwyn),
    assigned_location(sandpipers, howard),
    assigned_location(oystercatchers, howard),
    assigned_location(terns, gladwyn),
    assigned_location(rails, gladwyn).

% Option C: rails, sandpipers, terns, petrels, oystercatchers
% Time: 1:rails, 2:sandpipers, 3:terns, 4:petrels, 5:oystercatchers
% Locations: rails (Gladwyn), sandpipers (Howard), terns (Gladwyn), petrels (Gladwyn), oystercatchers (Howard)
% Constraints: sandpipers (2) < oystercatchers (5), terns (3) < petrels (4), petrels in Gladwyn, sandpipers in Howard
option(c) :- 
    assigned(rails, 1), assigned(sandpipers, 2), assigned(terns, 3), 
    assigned(petrels, 4), assigned(oystercatchers, 5),
    assigned_location(rails, gladwyn),
    assigned_location(sandpipers, howard),
    assigned_location(terns, gladwyn),
    assigned_location(petrels, gladwyn),
    assigned_location(oystercatchers, howard).

% Option D: sandpipers, terns, oystercatchers, rails, petrels
% Time: 1:sandpipers, 2:terns, 3:oystercatchers, 4:rails, 5:petrels
% Locations: sandpipers (Howard), terns (Gladwyn), oystercatchers (Howard), rails (Gladwyn), petrels (Gladwyn)
% Constraints: time 1 must be in Gladwyn, but sandpipers is in Howard -> false
option(d) :- 
    assigned(sandpipers, 1), assigned(terns, 2), assigned(oystercatchers, 3), 
    assigned(rails, 4), assigned(petrels, 5),
    assigned_location(sandpipers, howard),
    assigned_location(terns, gladwyn),
    assigned_location(oystercatchers, howard),
    assigned_location(rails, gladwyn),
    assigned_location(petrels, gladwyn).

% Option E: terns, petrels, sandpipers, oystercatchers, rails
% Time: 1:terns, 2:petrels, 3:sandpipers, 4:oystercatchers, 5:rails
% Locations: terns (Gladwyn), petrels (Gladwyn), sandpipers (Howard), oystercatchers (Howard), rails (Gladwyn)
% Constraints: time 4 must be in Howard (oystercatchers), Gladwyn count: terns, petrels, rails -> 3 (ok)
% Terns (1) < Petrels (2) (ok), Sandpipers (3) in Howard, Oystercatchers (4) in Howard
option(e) :- 
    assigned(terns, 1), assigned(petrels, 2), assigned(sandpipers, 3), 
    assigned(oystercatchers, 4), assigned(rails, 5),
    assigned_location(terns, gladwyn),
    assigned_location(petrels, gladwyn),
    assigned_location(sandpipers, howard),
    assigned_location(oystercatchers, howard),
    assigned_location(rails, gladwyn).

#show option/1.