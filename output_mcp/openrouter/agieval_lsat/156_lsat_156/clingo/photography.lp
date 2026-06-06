% Photographers and ceremonies
photographer(frost). photographer(gonzalez). photographer(heideck). photographer(knutson). photographer(lai). photographer(mays).
ceremony(silva). ceremony(thorne).

% Choice: each photographer may be assigned to at most one ceremony (or none)
{assigned(P, silva); assigned(P, thorne)} 1 :- photographer(P).

% At least two photographers per ceremony
:- #count{P : assigned(P, silva)} < 2.
:- #count{P : assigned(P, thorne)} < 2.

% Frost and Heideck must be together at the same ceremony, and both must be assigned
:- assigned(frost, C1), assigned(heideck, C2), C1 != C2.
:- not assigned(frost, silva), not assigned(frost, thorne).
:- not assigned(heideck, silva), not assigned(heideck, thorne).

% If Lai and Mays both assigned, they must be to different ceremonies
:- assigned(lai, C), assigned(mays, C).

% If Gonzalez assigned to Silva then Lai must be assigned to Thorne
:- assigned(gonzalez, silva), not assigned(lai, thorne).

% If Knutson not assigned to Thorne then both Heideck and Mays must be assigned to Thorne
:- not assigned(knutson, thorne), not assigned(heideck, thorne).
:- not assigned(knutson, thorne), not assigned(mays, thorne).

% Premise: Heideck assigned to same ceremony as Lai
:- assigned(heideck, C1), assigned(lai, C2), C1 != C2.

% Option conditions
option(a) :- assigned(frost, thorne).
option(b) :- assigned(gonzalez, silva).
option(c) :- not assigned(gonzalez, silva), not assigned(gonzalez, thorne).
option(d) :- assigned(knutson, thorne).
option(e) :- assigned(lai, thorne).

% Ensure exactly one option holds
:- option(a), option(b).
:- option(a), option(c).
:- option(a), option(d).
:- option(a), option(e).
:- option(b), option(c).
:- option(b), option(d).
:- option(b), option(e).
:- option(c), option(d).
:- option(c), option(e).
:- option(d), option(e).

% At least one option must hold
:- not option(a), not option(b), not option(c), not option(d), not option(e).

#show option/1.