% Domains
photographer(frost).
photographer(gonzalez).
photographer(heideck).
photographer(knutson).
photographer(lai).
photographer(mays).

ceremony(silva).
ceremony(thorne).

% Each photographer can be assigned to at most one ceremony (or none)
{ assigned(P, C) : ceremony(C) } 1 :- photographer(P).

% At least two photographers per ceremony
:- ceremony(C), #count { P : assigned(P, C) } < 2.

% Constraint 1: Frost and Heideck must be assigned together to the same ceremony
assigned(frost, C) :- assigned(heideck, C).
assigned(heideck, C) :- assigned(frost, C).
:- assigned(frost, C1), assigned(heideck, C2), C1 != C2.

% Constraint 2: If Lai and Mays are both assigned, they must be to different ceremonies
:- assigned(lai, C), assigned(mays, C).

% Constraint 3: If Gonzalez is assigned to Silva, then Lai must be assigned to Thorne
assigned(lai, thorne) :- assigned(gonzalez, silva).

% Constraint 4: If Knutson is not assigned to Thorne, then both Heideck and Mays must be assigned to Thorne
assigned(heideck, thorne) :- not assigned(knutson, thorne).
assigned(mays, thorne) :- not assigned(knutson, thorne).

% Condition for the question: Heideck and Lai are assigned to the same ceremony
same_ceremony(heideck, lai) :- assigned(heideck, C), assigned(lai, C).
:- not same_ceremony(heideck, lai).

% Define option conditions
option_a :- assigned(frost, thorne).
option_b :- assigned(gonzalez, silva).
option_c :- not assigned(gonzalez, _).
option_d :- assigned(knutson, thorne).
option_e :- assigned(lai, thorne).

% Map to answer options
option(a) :- option_a.
option(b) :- option_b.
option(c) :- option_c.
option(d) :- option_d.
option(e) :- option_e.

#show assigned/2.
#show option/1.