% Domains
position(1..5).
bird(oystercatchers; petrels; rails; sandpipers; terns).
location(howard; gladwyn).

% Assign exactly one bird to each position
1 { lecture(P, B) : bird(B) } 1 :- position(P).

% Assign exactly one location to each position
1 { at(P, L) : location(L) } 1 :- position(P).

% Constraint 1: First lecture is in Gladwyn Hall
at(1, gladwyn).

% Constraint 2: Fourth lecture is in Howard Auditorium
at(4, howard).

% Constraint 3: Exactly three lectures are in Gladwyn Hall
:- #count { P : at(P, gladwyn) } != 3.

% Constraint 4: Sandpipers is in Howard and earlier than oystercatchers
:- lecture(P1, sandpipers), at(P1, gladwyn).
:- lecture(P1, sandpipers), lecture(P2, oystercatchers), P1 >= P2.

% Constraint 5: Terns is earlier than petrels, and petrels is in Gladwyn
:- lecture(P1, terns), lecture(P2, petrels), P1 >= P2.
:- lecture(P2, petrels), at(P2, howard).

% Given condition: terns is in Howard
:- lecture(P, terns), at(P, gladwyn).

% Map answer choices
% A: third lecture is oystercatchers and is in Gladwyn Hall
could_be_a :- lecture(3, oystercatchers), at(3, gladwyn).

% B: third lecture is rails and in Howard Auditorium
could_be_b :- lecture(3, rails), at(3, howard).

% C: third lecture is rails and in Gladwyn Hall
could_be_c :- lecture(3, rails), at(3, gladwyn).

% D: third lecture is sandpipers and in Howard Auditorium
could_be_d :- lecture(3, sandpipers), at(3, howard).

% E: third lecture is terns and in Howard Auditorium
could_be_e :- lecture(3, terns), at(3, howard).

% Ensure exactly one option is selected
1 { selected_option(a) : could_be_a; selected_option(b) : could_be_b; selected_option(c) : could_be_c; selected_option(d) : could_be_d; selected_option(e) : could_be_e } 1.

% Map the correct answer to option/1 (MANDATORY)
option(a) :- selected_option(a).
option(b) :- selected_option(b).
option(c) :- selected_option(c).
option(d) :- selected_option(d).
option(e) :- selected_option(e).

#show option/1.