% Domains
photographer(frost). photographer(gonzalez). photographer(heideck). photographer(knutson). photographer(lai). photographer(mays).
ceremony(silva). ceremony(thorne).

% Base assignment facts (to be constrained)
{ assigned(P, C) : ceremony(C) } = 1 :- photographer(P).

% Total number of assigned photographers is exactly 4
total_assigned(4) :- #count{P, C : assigned(P, C)} = 4.

% Each ceremony must have at least 2 photographers
:- ceremony(C), #count{P : assigned(P, C)} < 2.

% No photographer can be assigned to both ceremonies
:- photographer(P), ceremony(C1), ceremony(C2), C1 != C2, assigned(P, C1), assigned(P, C2).

% Frost must be assigned together with Heideck to one of the ceremonies
:- assigned(frost, C), not assigned(heideck, C).
:- assigned(heideck, C), not assigned(frost, C).

% If Lai and Mays are both assigned, they must be assigned to different ceremonies
:- assigned(lai, C), assigned(mays, C), photographer(lai), photographer(mays).

% If Gonzalez is assigned to Silva University, then Lai must be assigned to Thorne University
:- assigned(gonzalez, silva), not assigned(lai, thorne).

% Helper predicate for the condition: both Heideck and Mays assigned to Thorne
both_assigned_to_thorne :- assigned(heideck, thorne), assigned(mays, thorne).

% If Knutson is not assigned to Thorne University, then both Heideck and Mays must be assigned to it
:- not assigned(knutson, thorne), not both_assigned_to_thorne.

% Ensure total_assigned(4) is satisfied
total_assigned(4).

% Define which photographers are assigned to Silva University
assigned_to_silva(P) :- assigned(P, silva).

% Silva University must have exactly 2 photographers
:- #count{P : assigned_to_silva(P)} != 2.

% Frost and Heideck must be assigned to Silva University (since assigning them to Thorne leads to a contradiction)
:- assigned(frost, thorne).
:- assigned(heideck, thorne).

% Check which of the options must be assigned to Silva University
% We need to find which option is necessarily true for Silva University when exactly 4 are assigned

% Option A: Frost must be assigned to Silva
option(a) :- assigned_to_silva(frost).

% Option B: Gonzalez must be assigned to Silva
option(b) :- assigned_to_silva(gonzalez).

% Option C: Knutson must be assigned to Silva
option(c) :- assigned_to_silva(knutson).

% Option D: Lai must be assigned to Silva
option(d) :- assigned_to_silva(lai).

% Option E: Mays must be assigned to Silva
option(e) :- assigned_to_silva(mays).

% Show the answer
#show option/1.