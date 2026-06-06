% Define the lectures and their possible bird types
lecture(1..5).

% Bird types
bird(oystercatchers).
bird(petrels).
bird(rails).
bird(sandpipers).
bird(terns).

% Locations
location(gladwyn).
location(howard).

% Assign a bird to each lecture
1 { bird_assignment(L, B) : bird(B) } 1 :- lecture(L).

% Assign a location to each lecture
1 { location_assignment(L, Loc) : location(Loc) } 1 :- lecture(L).

% Constraint 1: The first lecture is in Gladwyn Hall
:- location_assignment(1, Loc), Loc != gladwyn.

% Constraint 2: The fourth lecture is in Howard Auditorium
:- location_assignment(4, Loc), Loc != howard.

% Constraint 3: Exactly three of the lectures are in Gladwyn Hall
:- { location_assignment(L, gladwyn) } != 3.

% Constraint 4: The lecture on sandpipers is in Howard Auditorium and is given earlier than the lecture on oystercatchers
:- bird_assignment(L, sandpipers), location_assignment(L, Loc), Loc != howard.
:- bird_assignment(L1, sandpipers), bird_assignment(L2, oystercatchers), L1 >= L2.

% Constraint 5: The lecture on terns is given earlier than the lecture on petrels, which is in Gladwyn Hall
:- bird_assignment(L1, terns), bird_assignment(L2, petrels), L1 >= L2.
:- bird_assignment(L, petrels), location_assignment(L, Loc), Loc != gladwyn.

% Ensure each bird is assigned to exactly one lecture
:- bird(B), 2 { bird_assignment(L, B) }.

% Ensure each location is assigned to exactly one lecture per lecture (already ensured by 1 { ... } 1)

% Define the fifth lecture
fifth_lecture(5).

% The fifth lecture cannot be sandpipers (since sandpipers is in Howard and earlier than oystercatchers)
:- bird_assignment(5, sandpipers).

% The fifth lecture cannot be petrels (since petrels is in Gladwyn and after terns)
:- bird_assignment(5, petrels).

% The fifth lecture cannot be terns if it would violate the terns < petrels constraint
% (This is already ensured by the earlier constraint)

% The fifth lecture must be either oystercatchers, rails, or terns

% Map the correct answer to option/1
% (A) It is on oystercatchers and is in Gladwyn Hall.
option(a) :- bird_assignment(5, oystercatchers), location_assignment(5, gladwyn).

% (B) It is on petrels and is in Howard Auditorium.
option(b) :- bird_assignment(5, petrels), location_assignment(5, howard).

% (C) It is on rails and is in Howard Auditorium.
option(c) :- bird_assignment(5, rails), location_assignment(5, howard).

% (D) It is on sandpipers and is in Howard Auditorium.
option(d) :- bird_assignment(5, sandpipers), location_assignment(5, howard).

% (E) It is on terns and is in Gladwyn Hall.
option(e) :- bird_assignment(5, terns), location_assignment(5, gladwyn).

% Ensure only one option is true
:- option(X), option(Y), X != Y.

#show option/1.