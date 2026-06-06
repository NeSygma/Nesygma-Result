% Base facts
photographer(frost).
photographer(gonzalez).
photographer(heideck).
photographer(knutson).
photographer(lai).
photographer(mays).

ceremony(silva).
ceremony(thorne).

% Choice rule for assignments
{ assigned(P, C) : photographer(P), ceremony(C) }.

% Each ceremony must have at least 2 photographers
:- ceremony(C), #count{P: assigned(P, C)} < 2.

% No photographer can be assigned to both ceremonies
:- photographer(P), assigned(P, silva), assigned(P, thorne).

% Frost must be assigned together with Heideck to one ceremony
% This means both must be assigned, and to the same ceremony
:- photographer(frost), not assigned(frost, _).
:- photographer(heideck), not assigned(heideck, _).
:- assigned(frost, C1), assigned(heideck, C2), C1 != C2.

% If Lai and Mays are both assigned, they must be at different ceremonies
:- assigned(lai, C), assigned(mays, C), assigned(lai, _), assigned(mays, _).

% If Gonzalez is assigned to Silva, then Lai must be assigned to Thorne
:- assigned(gonzalez, silva), not assigned(lai, thorne).

% If Knutson is not assigned to Thorne, then both Heideck and Mays must be assigned to Thorne
:- not assigned(knutson, thorne), not assigned(heideck, thorne).
:- not assigned(knutson, thorne), not assigned(mays, thorne).

% Define the specific assignments for each option
% Option A: Silva: Gonzalez, Lai; Thorne: Frost, Heideck, Mays
% This option is invalid because Gonzalez at Silva requires Lai at Thorne, but Lai is at Silva
option(a) :- assigned(gonzalez, silva), assigned(lai, silva),
             assigned(frost, thorne), assigned(heideck, thorne), assigned(mays, thorne),
             not assigned(knutson, silva), not assigned(knutson, thorne).

% Option B: Silva: Gonzalez, Mays; Thorne: Knutson, Lai
% This option is invalid because Frost and Heideck are not assigned
option(b) :- assigned(gonzalez, silva), assigned(mays, silva),
             assigned(knutson, thorne), assigned(lai, thorne),
             not assigned(frost, silva), not assigned(frost, thorne),
             not assigned(heideck, silva), not assigned(heideck, thorne).

% Option C: Silva: Frost, Gonzalez, Heideck; Thorne: Knutson, Lai, Mays
% This option is invalid because Lai and Mays are both at Thorne
option(c) :- assigned(frost, silva), assigned(gonzalez, silva), assigned(heideck, silva),
             assigned(knutson, thorne), assigned(lai, thorne), assigned(mays, thorne).

% Option D: Silva: Frost, Heideck, Mays; Thorne: Gonzalez, Lai
% This option is invalid because Knutson is not at Thorne, but neither Heideck nor Mays is at Thorne
option(d) :- assigned(frost, silva), assigned(heideck, silva), assigned(mays, silva),
             assigned(gonzalez, thorne), assigned(lai, thorne),
             not assigned(knutson, silva), not assigned(knutson, thorne).

% Option E: Silva: Frost, Heideck, Mays; Thorne: Gonzalez, Knutson, Lai
% This option should be valid
option(e) :- assigned(frost, silva), assigned(heideck, silva), assigned(mays, silva),
             assigned(gonzalez, thorne), assigned(knutson, thorne), assigned(lai, thorne).

#show option/1.