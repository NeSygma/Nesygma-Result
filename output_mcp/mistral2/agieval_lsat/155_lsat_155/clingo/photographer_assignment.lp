% Base facts: photographers and ceremonies
photographer(frost).
photographer(gonzalez).
photographer(heideck).
photographer(knutson).
photographer(lai).
photographer(mays).

ceremony(silva).
ceremony(thorne).

% Assign each photographer to at most one ceremony
1 { assigned(P, C) : ceremony(C) } 1 :- photographer(P).

% At least two photographers must be assigned to each ceremony
:- ceremony(C), #count { P : assigned(P, C) } < 2.

% No photographer can be assigned to both ceremonies (enforced by the choice rule above)

% Constraint 1: Frost must be assigned together with Heideck to one of the ceremonies
:- assigned(frost, C), not assigned(heideck, C).
:- assigned(heideck, C), not assigned(frost, C).

% Constraint 2: If Lai and Mays are both assigned, they must be assigned to different ceremonies
:- assigned(lai, C1), assigned(mays, C1), ceremony(C1).

% Constraint 3: If Gonzalez is assigned to Silva, then Lai must be assigned to Thorne
:- assigned(gonzalez, silva), not assigned(lai, thorne).

% Constraint 4: If Knutson is not assigned to Thorne, then both Heideck and Mays must be assigned to Thorne
:- not assigned(knutson, thorne), not assigned(heideck, thorne).
:- not assigned(knutson, thorne), not assigned(mays, thorne).

% Define the options for the multiple-choice question
% Option A: Silva University: Gonzalez, Lai; Thorne University: Frost, Heideck, Mays
option(a) :- assigned(gonzalez, silva),
             assigned(lai, silva),
             assigned(frost, thorne),
             assigned(heideck, thorne),
             assigned(mays, thorne),
             not assigned(knutson, silva),
             not assigned(knutson, thorne).

% Option B: Silva University: Gonzalez, Mays; Thorne University: Knutson, Lai
option(b) :- assigned(gonzalez, silva),
             assigned(mays, silva),
             assigned(knutson, thorne),
             assigned(lai, thorne),
             not assigned(frost, silva),
             not assigned(frost, thorne),
             not assigned(heideck, silva),
             not assigned(heideck, thorne),
             not assigned(knutson, silva),
             not assigned(lai, silva).

% Option C: Silva University: Frost, Gonzalez, Heideck; Thorne University: Knutson, Lai, Mays
option(c) :- assigned(frost, silva),
             assigned(gonzalez, silva),
             assigned(heideck, silva),
             assigned(knutson, thorne),
             assigned(lai, thorne),
             assigned(mays, thorne),
             not assigned(frost, thorne),
             not assigned(gonzalez, thorne),
             not assigned(heideck, thorne),
             not assigned(knutson, silva),
             not assigned(lai, silva),
             not assigned(mays, silva).

% Option D: Silva University: Frost, Heideck, Mays; Thorne University: Gonzalez, Lai
option(d) :- assigned(frost, silva),
             assigned(heideck, silva),
             assigned(mays, silva),
             assigned(gonzalez, thorne),
             assigned(lai, thorne),
             not assigned(frost, thorne),
             not assigned(heideck, thorne),
             not assigned(mays, thorne),
             not assigned(gonzalez, silva),
             not assigned(lai, silva).

% Option E: Silva University: Frost, Heideck, Mays; Thorne University: Gonzalez, Knutson, Lai
option(e) :- assigned(frost, silva),
             assigned(heideck, silva),
             assigned(mays, silva),
             assigned(gonzalez, thorne),
             assigned(knutson, thorne),
             assigned(lai, thorne),
             not assigned(frost, thorne),
             not assigned(heideck, thorne),
             not assigned(mays, thorne),
             not assigned(gonzalez, silva),
             not assigned(knutson, silva),
             not assigned(lai, silva).

#show option/1.