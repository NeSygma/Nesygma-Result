% Base facts
silva(silva).
thorne(thorne).
photographer(frost).
photographer(gonzalez).
photographer(heideck).
photographer(knutson).
photographer(lai).
photographer(mays).

% Each ceremony has at least two photographers
:- silva(C), #count { P : assigned(P, C) } < 2.
:- thorne(C), #count { P : assigned(P, C) } < 2.

% No photographer is assigned to both ceremonies
:- assigned(P, silva), assigned(P, thorne).

% Frost must be assigned together with Heideck to one of the ceremonies
:- assigned(frost, C), not assigned(heideck, C).
:- assigned(heideck, C), not assigned(frost, C).

% If Lai and Mays are both assigned, they must be assigned to different ceremonies
:- assigned(lai, C1), assigned(mays, C2), C1 == C2.

% If Gonzalez is assigned to Silva, then Lai must be assigned to Thorne
:- assigned(gonzalez, silva), not assigned(lai, thorne).

% If Knutson is not assigned to Thorne, then both Heideck and Mays must be assigned to Thorne
:- not assigned(knutson, thorne), not (assigned(heideck, thorne) , assigned(mays, thorne)).

% Choice rule: Each photographer is assigned to at most one ceremony
{ assigned(P, C) : silva(C) ; assigned(P, C) : thorne(C) } 1 :- photographer(P).

% Define the set of photographers assigned to Thorne
thorne_photographers(P) :- assigned(P, thorne).

% Option A: Frost, Gonzalez, Heideck, Mays
option(a) :-
    thorne_photographers(frost),
    thorne_photographers(gonzalez),
    thorne_photographers(heideck),
    thorne_photographers(mays),
    not thorne_photographers(knutson),
    not thorne_photographers(lai),
    #count { P : thorne_photographers(P) } = 4.

% Option B: Frost, Heideck, Knutson, Mays
option(b) :-
    thorne_photographers(frost),
    thorne_photographers(heideck),
    thorne_photographers(knutson),
    thorne_photographers(mays),
    not thorne_photographers(gonzalez),
    not thorne_photographers(lai),
    #count { P : thorne_photographers(P) } = 4.

% Option C: Gonzalez, Knutson, Lai
option(c) :-
    thorne_photographers(gonzalez),
    thorne_photographers(knutson),
    thorne_photographers(lai),
    not thorne_photographers(frost),
    not thorne_photographers(heideck),
    not thorne_photographers(mays),
    #count { P : thorne_photographers(P) } = 3.

% Option D: Gonzalez, Knutson, Mays
option(d) :-
    thorne_photographers(gonzalez),
    thorne_photographers(knutson),
    thorne_photographers(mays),
    not thorne_photographers(frost),
    not thorne_photographers(heideck),
    not thorne_photographers(lai),
    #count { P : thorne_photographers(P) } = 3.

% Option E: Knutson, Mays
option(e) :-
    thorne_photographers(knutson),
    thorne_photographers(mays),
    not thorne_photographers(frost),
    not thorne_photographers(gonzalez),
    not thorne_photographers(heideck),
    not thorne_photographers(lai),
    #count { P : thorne_photographers(P) } = 2.

#show option/1.