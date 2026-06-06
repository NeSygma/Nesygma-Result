% Domains
ceremony(silva).
ceremony(thorne).

photographer(frost).
photographer(gonzalez).
photographer(heideck).
photographer(knutson).
photographer(lai).
photographer(mays).

% Assignments
% assigned(P, C) means photographer P is assigned to ceremony C.
{ assigned(P, C) : ceremony(C) } :- photographer(P).

% Constraint 1: At least two photographers to each ceremony.
:- #count { P : assigned(P, silva) } < 2.
:- #count { P : assigned(P, thorne) } < 2.

% Constraint 2: No photographer can be assigned to both ceremonies.
:- assigned(P, C1), assigned(P, C2), C1 != C2.

% Constraint 3: Frost must be assigned together with Heideck to one of the graduation ceremonies.
% This means they must be assigned to the SAME ceremony.
% If Frost is assigned to C, Heideck must be assigned to C.
assigned(heideck, C) :- assigned(frost, C).
assigned(frost, C) :- assigned(heideck, C).

% Constraint 4: If Lai and Mays are both assigned, it must be to different ceremonies.
:- assigned(lai, C), assigned(mays, C).

% Constraint 5: If Gonzalez is assigned to the Silva University ceremony, then Lai must be assigned to the Thorne University ceremony.
assigned(lai, thorne) :- assigned(gonzalez, silva).

% Constraint 6: If Knutson is not assigned to the Thorne University ceremony, then both Heideck and Mays must be assigned to it.
assigned(heideck, thorne) :- not assigned(knutson, thorne).
assigned(mays, thorne) :- not assigned(knutson, thorne).

% Define the options based on the provided choices
% Option A: Silva: Gonzalez, Lai; Thorne: Frost, Heideck, Mays
opt_a :- assigned(gonzalez, silva), assigned(lai, silva), assigned(frost, thorne), assigned(heideck, thorne), assigned(mays, thorne),
         not assigned(frost, silva), not assigned(heideck, silva), not assigned(mays, silva), not assigned(gonzalez, thorne), not assigned(lai, thorne),
         not assigned(knutson, silva), not assigned(knutson, thorne).

% Option B: Silva: Gonzalez, Mays; Thorne: Knutson, Lai
opt_b :- assigned(gonzalez, silva), assigned(mays, silva), assigned(knutson, thorne), assigned(lai, thorne),
         not assigned(gonzalez, thorne), not assigned(mays, thorne), not assigned(knutson, silva), not assigned(lai, silva),
         not assigned(frost, silva), not assigned(frost, thorne), not assigned(heideck, silva), not assigned(heideck, thorne).

% Option C: Silva: Frost, Gonzalez, Heideck; Thorne: Knutson, Lai, Mays
opt_c :- assigned(frost, silva), assigned(gonzalez, silva), assigned(heideck, silva), assigned(knutson, thorne), assigned(lai, thorne), assigned(mays, thorne),
         not assigned(frost, thorne), not assigned(gonzalez, thorne), not assigned(heideck, thorne), not assigned(knutson, silva), not assigned(lai, silva), not assigned(mays, silva).

% Option D: Silva: Frost, Heideck, Mays; Thorne: Gonzalez, Lai
opt_d :- assigned(frost, silva), assigned(heideck, silva), assigned(mays, silva), assigned(gonzalez, thorne), assigned(lai, thorne),
         not assigned(frost, thorne), not assigned(heideck, thorne), not assigned(mays, thorne), not assigned(gonzalez, silva), not assigned(lai, silva),
         not assigned(knutson, silva), not assigned(knutson, thorne).

% Option E: Silva: Frost, Heideck, Mays; Thorne: Gonzalez, Knutson, Lai
opt_e :- assigned(frost, silva), assigned(heideck, silva), assigned(mays, silva), assigned(gonzalez, thorne), assigned(knutson, thorne), assigned(lai, thorne),
         not assigned(frost, thorne), not assigned(heideck, thorne), not assigned(mays, thorne), not assigned(gonzalez, silva), not assigned(knutson, silva), not assigned(lai, silva).

option(a) :- opt_a.
option(b) :- opt_b.
option(c) :- opt_c.
option(d) :- opt_d.
option(e) :- opt_e.

#show option/1.