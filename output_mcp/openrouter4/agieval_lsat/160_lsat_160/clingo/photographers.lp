% --- Domain definitions ---
photographer(frost; gonzalez; heideck; knutson; lai; mays).
ceremony(silva; thorne).
option_id(a; b; c; d; e).

% --- Assignment: each photographer assigned to at most one ceremony ---
{ assigned(P, C) : ceremony(C) } 1 :- photographer(P).

% --- Constraints ---

% At least two photographers per ceremony
:- ceremony(C), #count { P : assigned(P, C) } < 2.

% 1. Frost and Heideck together (same ceremony) and both assigned
1 { assigned(frost, C) : ceremony(C) } 1.
assigned(heideck, C) :- assigned(frost, C).
assigned(frost, C) :- assigned(heideck, C).

% 2. If Lai and Mays are both assigned, they must be to different ceremonies.
:- assigned(lai, C), assigned(mays, C).

% 3. If Gonzalez is assigned to Silva, then Lai must be assigned to Thorne.
:- assigned(gonzalez, silva), not assigned(lai, thorne).

% 4. If Knutson is not assigned to Thorne, then both Heideck and Mays must be assigned to it.
assigned(heideck, thorne) :- not assigned(knutson, thorne).
assigned(mays, thorne) :- not assigned(knutson, thorne).

% --- Scenario testing for each option ---
% We select exactly one option to test.
1 { scenario(O) : option_id(O) } 1.

% Option photographer sets
option_photographers(a, frost).   option_photographers(a, gonzalez). option_photographers(a, heideck). option_photographers(a, mays).
option_photographers(b, frost).   option_photographers(b, heideck).  option_photographers(b, knutson). option_photographers(b, mays).
option_photographers(c, gonzalez). option_photographers(c, knutson). option_photographers(c, lai).
option_photographers(d, gonzalez). option_photographers(d, knutson). option_photographers(d, mays).
option_photographers(e, knutson).  option_photographers(e, mays).

% Thorne assignment exactly equals the option's set
assigned(P, thorne) :- scenario(O), option_photographers(O, P).
:- scenario(O), assigned(P, thorne), not option_photographers(O, P).

% --- Determine possible / impossible options ---
possible(O) :- scenario(O).
impossible(O) :- option_id(O), not possible(O).

% --- Map answer ---
answer(O) :- impossible(O).

#show answer/1.
#show possible/1.