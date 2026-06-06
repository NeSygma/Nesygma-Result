% Domains and basic facts
photographer(frost).
photographer(gonzalez).
photographer(heideck).
photographer(knutson).
photographer(lai).
photographer(mays).

ceremony(silva).
ceremony(thorne).

% Assignments: assigned(P, C) means photographer P is assigned to ceremony C
% We use a choice rule to allow assignments
{ assigned(P, C) : photographer(P) } :- ceremony(C).

% At least two photographers must be assigned to each ceremony
:- ceremony(C), #count{ P : assigned(P, C) } < 2.

% No photographer can be assigned to both ceremonies
:- photographer(P), ceremony(C1), ceremony(C2), C1 != C2, assigned(P, C1), assigned(P, C2).

% Frost must be assigned together with Heideck to one of the graduation ceremonies
:- photographer(P), P = frost, ceremony(C), not assigned(P, C), assigned(heideck, C).
:- photographer(P), P = heideck, ceremony(C), not assigned(P, C), assigned(frost, C).

% If Lai and Mays are both assigned, it must be to different ceremonies
:- photographer(lai), photographer(mays), ceremony(C1), ceremony(C2), C1 != C2, 
   assigned(lai, C1), assigned(mays, C2).
:- photographer(lai), photographer(mays), ceremony(C1), ceremony(C2), C1 != C2, 
   assigned(lai, C2), assigned(mays, C1).

% If Gonzalez is assigned to the Silva University ceremony, then Lai must be assigned to the Thorne University ceremony
:- photographer(gonzalez), assigned(gonzalez, silva), not assigned(lai, thorne).

% If Knutson is not assigned to the Thorne University ceremony, then both Heideck and Mays must be assigned to it
:- photographer(knutson), not assigned(knutson, thorne), not assigned(heideck, thorne).
:- photographer(knutson), not assigned(knutson, thorne), not assigned(mays, thorne).

% Define the Silva University assignment for each option as a fact
% Option A: Frost, Gonzalez, Heideck, Knutson
silva_option_a :- 
    assigned(frost, silva), 
    assigned(gonzalez, silva), 
    assigned(heideck, silva), 
    assigned(knutson, silva),
    not assigned(lai, silva),
    not assigned(mays, silva).

% Option B: Frost, Gonzalez, Heideck
silva_option_b :-
    assigned(frost, silva), 
    assigned(gonzalez, silva), 
    assigned(heideck, silva),
    not assigned(knutson, silva),
    not assigned(lai, silva),
    not assigned(mays, silva).

% Option C: Gonzalez, Knutson
silva_option_c :-
    not assigned(frost, silva), 
    assigned(gonzalez, silva), 
    not assigned(heideck, silva), 
    assigned(knutson, silva),
    not assigned(lai, silva),
    not assigned(mays, silva).

% Option D: Heideck, Lai
silva_option_d :-
    assigned(heideck, silva), 
    assigned(lai, silva),
    not assigned(frost, silva), 
    not assigned(gonzalez, silva), 
    not assigned(knutson, silva),
    not assigned(mays, silva).

% Option E: Knutson, Mays
silva_option_e :-
    not assigned(frost, silva), 
    not assigned(gonzalez, silva), 
    not assigned(heideck, silva), 
    assigned(knutson, silva),
    not assigned(lai, silva),
    assigned(mays, silva).

% Map the correct answer to option/1
option(a) :- silva_option_a.
option(b) :- silva_option_b.
option(c) :- silva_option_c.
option(d) :- silva_option_d.
option(e) :- silva_option_e.

#show option/1.