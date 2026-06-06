% Domains and basic facts
photographer(frost).
photographer(gonzalez).
photographer(heideck).
photographer(knutson).
photographer(lai).
photographer(mays).

university(silva).
university(thorne).

% Assignments: assigned(P, U) means photographer P is assigned to university U
% We use a choice rule to allow assignments
{ assigned(P, U) : university(U) } :- photographer(P).

% At least two photographers must be assigned to each university
:- university(U), #count{ P : assigned(P, U) } < 2.

% No photographer can be assigned to both ceremonies
:- photographer(P), university(U1), university(U2), U1 != U2, assigned(P, U1), assigned(P, U2).

% Frost must be assigned together with Heideck to one of the graduation ceremonies
:- photographer(frost), photographer(heideck), not (assigned(frost, silva), assigned(heideck, silva)), not (assigned(frost, thorne), assigned(heideck, thorne)).

% If Lai and Mays are both assigned, it must be to different ceremonies
:- photographer(lai), photographer(mays), assigned(lai, silva), assigned(mays, silva).
:- photographer(lai), photographer(mays), assigned(lai, thorne), assigned(mays, thorne).

% If Gonzalez is assigned to the Silva University ceremony, then Lai must be assigned to the Thorne University ceremony
:- assigned(gonzalez, silva), not assigned(lai, thorne).

% If Knutson is not assigned to the Thorne University ceremony, then both Heideck and Mays must be assigned to it
:- not assigned(knutson, thorne), not assigned(heideck, thorne).
:- not assigned(knutson, thorne), not assigned(mays, thorne).

% Additional constraint: Heideck is assigned to the same graduation ceremony as Lai
:- assigned(lai, U), assigned(heideck, V), U != V.
assigned(heideck, U) :- assigned(lai, U).

% --- Answer Mapping ---
% We need to determine which of the options (A-E) must be true under the given conditions.

% (A) Frost is assigned to the Thorne University ceremony.
option(a) :- assigned(frost, thorne).

% (B) Gonzalez is assigned to the Silva University ceremony.
option(b) :- assigned(gonzalez, silva).

% (C) Gonzalez is assigned to neither graduation ceremony.
option(c) :- not assigned(gonzalez, silva), not assigned(gonzalez, thorne).

% (D) Knutson is assigned to the Thorne University ceremony.
option(d) :- assigned(knutson, thorne).

% (E) Lai is assigned to the Thorne University ceremony.
option(e) :- assigned(lai, thorne).

#show option/1.