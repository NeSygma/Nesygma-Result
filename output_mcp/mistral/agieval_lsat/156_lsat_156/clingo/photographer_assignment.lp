% Photographers and ceremonies
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
% Ensure no photographer is assigned to both ceremonies (redundant with above, but explicit)
:- assigned(P, C1), assigned(P, C2), C1 != C2.

% At least two photographers per ceremony
:- ceremony(C), #count{P: assigned(P, C)} < 2.

% Frost must be assigned together with Heideck to one of the ceremonies
:- assigned(frost, C), not assigned(heideck, C).
:- assigned(heideck, C), not assigned(frost, C).

% If Lai and Mays are both assigned, they must be at different ceremonies
:- assigned(lai, C), assigned(mays, C).

% If Gonzalez is assigned to Silva University, then Lai must be assigned to Thorne University
:- assigned(gonzalez, silva), not assigned(lai, thorne).

% If Knutson is not assigned to Thorne University, then both Heideck and Mays must be assigned to Thorne University
:- not assigned(knutson, thorne), not assigned(heideck, thorne).
:- not assigned(knutson, thorne), not assigned(mays, thorne).

% Question condition: Heideck is assigned to the same graduation ceremony as Lai
:- assigned(heideck, C), assigned(lai, C1), C != C1.

% Map the correct answer to option/1 (MANDATORY)
option(a) :- assigned(frost, thorne).
option(b) :- assigned(gonzalez, silva).
option(c) :- not assigned(gonzalez, silva), not assigned(gonzalez, thorne).
option(d) :- assigned(knutson, thorne).
option(e) :- assigned(lai, thorne).

#show option/1.