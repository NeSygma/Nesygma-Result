% Domains
photographer(frost).
photographer(gonzalez).
photographer(heideck).
photographer(knutson).
photographer(lai).
photographer(mays).

ceremony(silva).
ceremony(thorne).

% Each photographer is assigned to at most one ceremony
{ assigned(P, C) : ceremony(C) } 1 :- photographer(P).

% Each ceremony must have at least two photographers
:- ceremony(C), #count{ P : assigned(P, C) } < 2.

% Exactly four photographers are assigned overall
:- #count{ P : assigned(P, C) } != 4.

% Constraint 1: Frost and Heideck must be assigned together to the same ceremony
assigned(frost, C) :- assigned(heideck, C).
assigned(heideck, C) :- assigned(frost, C).
% Force both to be assigned (interpretation: they must be assigned)
:- not assigned(frost, _).
:- not assigned(heideck, _).

% Constraint 2: If Lai and Mays are both assigned, they must be in different ceremonies
:- assigned(lai, C), assigned(mays, C).

% Constraint 3: If Gonzalez is assigned to Silva, then Lai must be assigned to Thorne
:- assigned(gonzalez, silva), not assigned(lai, thorne).

% Constraint 4: If Knutson is not assigned to Thorne, then Heideck and Mays must be assigned to Thorne
assigned(heideck, thorne) :- not assigned(knutson, thorne).
assigned(mays, thorne) :- not assigned(knutson, thorne).

% Map the correct answer to option/1
option(a) :- assigned(frost, silva).
option(b) :- assigned(gonzalez, silva).
option(c) :- assigned(knutson, silva).
option(d) :- assigned(lai, silva).
option(e) :- assigned(mays, silva).

#show option/1.