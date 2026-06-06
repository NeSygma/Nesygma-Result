% --- Domains ---
photographer(frost; gonzalez; heideck; knutson; lai; mays).
ceremony(silva; thorne).
option_id(a; b; c; d; e).

% Option photographer sets
option_photographers(a, frost).   option_photographers(a, gonzalez). option_photographers(a, heideck). option_photographers(a, mays).
option_photographers(b, frost).   option_photographers(b, heideck).  option_photographers(b, knutson). option_photographers(b, mays).
option_photographers(c, gonzalez). option_photographers(c, knutson). option_photographers(c, lai).
option_photographers(d, gonzalez). option_photographers(d, knutson). option_photographers(d, mays).
option_photographers(e, knutson).  option_photographers(e, mays).

% --- Scenario selection: pick exactly one option to test ---
1 { scenario(O) : option_id(O) } 1.

% --- Thorne assignment is fixed by the chosen scenario ---
thorne(P) :- scenario(O), option_photographers(O, P).

% --- Silva assignment: choose from remaining photographers ---
{ silva(P) } :- photographer(P), not thorne(P).

% A photographer cannot be at both ceremonies
:- thorne(P), silva(P).

% --- Constraints ---

% At least 2 photographers at each ceremony
:- #count { P : thorne(P) } < 2.
:- #count { P : silva(P) } < 2.

% Constraint 1: Frost and Heideck must be together (same ceremony)
both_th :- thorne(frost), thorne(heideck).
both_si :- silva(frost), silva(heideck).
:- not both_th, not both_si.

% Both Frost and Heideck must be assigned (not unassigned)
:- not thorne(frost), not silva(frost).
:- not thorne(heideck), not silva(heideck).

% Constraint 2: If Lai and Mays both assigned, they must be different ceremonies
:- thorne(lai), thorne(mays).
:- silva(lai), silva(mays).

% Constraint 3: If Gonzalez at Silva, then Lai at Thorne
:- silva(gonzalez), not thorne(lai).

% Constraint 4: If Knutson not at Thorne, then Heideck and Mays at Thorne
:- not thorne(knutson), not thorne(heideck).
:- not thorne(knutson), not thorne(mays).

% --- Derive which option is possible ---
possible(O) :- scenario(O).

% Show results
#show scenario/1.
#show possible/1.