% Photographers
photographer(frost; gonzalez; heideck; knutson; lai; mays).
ceremony(silva; thorne).

% Choice: Each photographer can be assigned to at most one ceremony
{ assigned(P, C) : ceremony(C) } 1 :- photographer(P).

% Helper: is_assigned
is_assigned(P) :- assigned(P, _).

% Constraint: At least two photographers per ceremony
:- { assigned(P, silva) } < 2.
:- { assigned(P, thorne) } < 2.

% Constraint: Frost must be assigned together with Heideck
assigned(frost, C) :- assigned(heideck, C).
assigned(heideck, C) :- assigned(frost, C).
:- is_assigned(frost), not is_assigned(heideck).
:- is_assigned(heideck), not is_assigned(frost).

% Constraint: If Lai and Mays are both assigned, they must be to different ceremonies
:- assigned(lai, C), assigned(mays, C).

% Constraint: If Gonzalez is assigned to Silva, then Lai must be assigned to Thorne
:- assigned(gonzalez, silva), not assigned(lai, thorne).

% Constraint: If Knutson is not assigned to Thorne, then both Heideck and Mays must be assigned to Thorne
:- not assigned(knutson, thorne), not assigned(heideck, thorne).
:- not assigned(knutson, thorne), not assigned(mays, thorne).

% Identify photographers who are assigned in a specific model
assigned_in_model(P) :- assigned(P, _).

% We want to find photographers who are assigned in ALL valid models.
% A photographer P is "must_be_assigned" if there is no model where P is not assigned.
must_be_assigned(P) :- photographer(P), not not_assigned_in_some_model(P).
not_assigned_in_some_model(P) :- photographer(P), not assigned(P, _).

#show must_be_assigned/1.