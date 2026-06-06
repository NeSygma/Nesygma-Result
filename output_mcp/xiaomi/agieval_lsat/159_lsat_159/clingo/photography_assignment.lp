% Define photographers
photographer(frost).
photographer(gonzalez).
photographer(heideck).
photographer(knutson).
photographer(lai).
photographer(mays).

% Define ceremonies
ceremony(silva).
ceremony(thorne).

% Each photographer can be assigned to at most one ceremony (or not assigned)
{ assigned(P, C) : ceremony(C) } 1 :- photographer(P).

% Exactly 4 photographers are assigned total
4 { assigned(P, C) : photographer(P), ceremony(C) } 4.

% At least 2 photographers per ceremony
2 { assigned(P, silva) : photographer(P) } 6.
2 { assigned(P, thorne) : photographer(P) } 6.

% Constraint 1: Frost must be assigned together with Heideck to one ceremony
% This means if Frost is assigned, Heideck must be assigned to the same ceremony
assigned(heideck, C) :- assigned(frost, C), ceremony(C).
assigned(frost, C) :- assigned(heideck, C), ceremony(C).

% Constraint 2: If Lai and Mays are both assigned, they must be at different ceremonies
:- assigned(lai, C), assigned(mays, C), ceremony(C).

% Constraint 3: If Gonzalez is assigned to Silva, then Lai must be assigned to Thorne
:- assigned(gonzalez, silva), not assigned(lai, thorne).

% Constraint 4: If Knutson is not assigned to Thorne, then both Heideck and Mays must be assigned to Thorne
% First, define "Knutson not assigned to Thorne"
knutson_not_thorne :- photographer(knutson), not assigned(knutson, thorne).
% Then enforce the consequence
assigned(heideck, thorne) :- knutson_not_thorne.
assigned(mays, thorne) :- knutson_not_thorne.

% Helper: Check if a photographer is assigned to Silva
assigned_to_silva(P) :- assigned(P, silva).

% We need to find which photographer MUST be assigned to Silva in ALL valid solutions
% We'll use a choice rule to test each option
{ test_option(a) }.
{ test_option(b) }.
{ test_option(c) }.
{ test_option(d) }.
{ test_option(e) }.

% Option A: Frost must be assigned to Silva
option(a) :- test_option(a), assigned_to_silva(frost).

% Option B: Gonzalez must be assigned to Silva
option(b) :- test_option(b), assigned_to_silva(gonzalez).

% Option C: Knutson must be assigned to Silva
option(c) :- test_option(c), assigned_to_silva(knutson).

% Option D: Lai must be assigned to Silva
option(d) :- test_option(d), assigned_to_silva(lai).

% Option E: Mays must be assigned to Silva
option(e) :- test_option(e), assigned_to_silva(mays).

% We want exactly one option to be true
1 { option(X) : X = a; option(X) : X = b; option(X) : X = c; option(X) : X = d; option(X) : X = e } 1.

% Show the assignment for debugging
#show assigned/2.
#show option/1.