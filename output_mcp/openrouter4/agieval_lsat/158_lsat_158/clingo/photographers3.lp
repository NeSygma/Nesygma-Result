% Define photographers
photographer(frost; gonzalez; heideck; knutson; lai; mays).

% Define ceremonies
ceremony(silva; thorne).

% Each photographer can be assigned to at most one ceremony, or not assigned at all
{ assigned(P, C) : ceremony(C) } <= 1 :- photographer(P).

% Constraint 1: At least 2 photographers assigned to each ceremony
:- ceremony(C), #count { P : assigned(P, C) } < 2.

% Constraint 4: Frost and Heideck together at one ceremony
1 { assigned(frost, C) : ceremony(C) } 1.
assigned(heideck, C) :- assigned(frost, C).

% Constraint 5: If Lai and Mays are both assigned, they must be to different ceremonies
both_lai_mays_assigned :- assigned(lai, _), assigned(mays, _).
:- both_lai_mays_assigned, assigned(lai, C), assigned(mays, C).

% Constraint 6: If Gonzalez is assigned to Silva, then Lai must be assigned to Thorne
:- assigned(gonzalez, silva), not assigned(lai, thorne).

% Constraint 7: If Knutson is not assigned to Thorne, then both Heideck and Mays must be assigned to it
:- not assigned(knutson, thorne), not assigned(heideck, thorne).
:- not assigned(knutson, thorne), not assigned(mays, thorne).

% Helper: photographer is assigned somewhere
assigned_any(P) :- assigned(P, _).

% Show all assignments
#show assigned/2.