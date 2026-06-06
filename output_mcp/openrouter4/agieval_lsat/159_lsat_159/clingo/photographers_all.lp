% Domains
photographer(frost; gonzalez; heideck; knutson; lai; mays).
ceremony(silva; thorne).

% Each photographer can be assigned to at most one ceremony
{ assigned(P, C) : ceremony(C) } 1 :- photographer(P).

% Exactly four photographers are assigned total
total_assigned(N) :- N = #count { P : assigned(P, _) }.
:- total_assigned(N), N != 4.

% At least two photographers per ceremony
:- ceremony(C), #count { P : assigned(P, C) } < 2.

% Constraint 1: Frost and Heideck must be assigned together to one ceremony
% Both must be assigned
:- not assigned(frost, _).
:- not assigned(heideck, _).
% They must be at the same ceremony
:- assigned(frost, C1), assigned(heideck, C2), C1 != C2.

% Constraint 2: If Lai and Mays are both assigned, they must be to different ceremonies
both_lm :- assigned(lai, _), assigned(mays, _).
:- both_lm, assigned(lai, C), assigned(mays, C).

% Constraint 3: If Gonzalez is assigned to Silva, then Lai must be assigned to Thorne
:- assigned(gonzalez, silva), not assigned(lai, thorne).

% Constraint 4: If Knutson is not assigned to Thorne, then both Heideck and Mays must be assigned to it
knutson_not_thorne :- not assigned(knutson, thorne).
:- knutson_not_thorne, not assigned(heideck, thorne).
:- knutson_not_thorne, not assigned(mays, thorne).

% Derive which photographers are assigned to Silva
silva_assignee(P) :- assigned(P, silva).

% Show all assignments
#show assigned/2.