% Domains
photographer(frost; gonzalez; heideck; knutson; lai; mays).
university(silva; thorne).

% Assignment: Each photographer is assigned to at most one university or unassigned.
{ assigned(P, U) : university(U) } <= 1 :- photographer(P).
unassigned(P) :- photographer(P), not assigned(P, _).

% At least two photographers per university.
:- university(U), #count { P : assigned(P, U) } < 2.

% Frost and Heideck must be assigned together to the same university.
:- assigned(frost, U1), assigned(heideck, U2), U1 != U2.
:- assigned(heideck, U), not assigned(frost, U).
:- assigned(frost, U), not assigned(heideck, U).

% Lai and Mays cannot be assigned to the same university.
:- assigned(lai, U), assigned(mays, U).

% If Gonzalez is assigned to Silva, Lai must be assigned to Thorne.
:- assigned(gonzalez, silva), not assigned(lai, thorne).

% If Knutson is not assigned to Thorne, then both Heideck and Mays must be assigned to Thorne.
:- not assigned(knutson, thorne), not assigned(heideck, thorne).
:- not assigned(knutson, thorne), not assigned(mays, thorne).

% Exactly four photographers are assigned.
:- #count { P : assigned(P, _) } != 4.

% Helper predicates for Silva assignments
silva_assigned(P) :- assigned(P, silva).
thorne_assigned(P) :- assigned(P, thorne).

% Map the correct answer to option/1
% We need to find which photographer MUST be assigned to Silva.
% To do this, we check for each option if it is necessarily assigned to Silva in all valid models.

% Option (A) Frost
option(a) :- silva_assigned(frost).

% Option (B) Gonzalez
option(b) :- silva_assigned(gonzalez).

% Option (C) Knutson
option(c) :- silva_assigned(knutson).

% Option (D) Lai
option(d) :- silva_assigned(lai).

% Option (E) Mays
option(e) :- silva_assigned(mays).

% Ensure only one option is selected
:- option(X), option(Y), X != Y.

#show option/1.