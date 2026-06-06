% Define photographers and ceremonies
photographer(frost; gonzalez; heideck; knutson; lai; mays).
ceremony(silva; thorne).

% Define each option as a set of assignments
% Option A: Silva: Gonzalez, Lai | Thorne: Frost, Heideck, Mays
option_a_assign(frost, thorne).
option_a_assign(gonzalez, silva).
option_a_assign(heideck, thorne).
option_a_assign(lai, silva).
option_a_assign(mays, thorne).

% Option B: Silva: Gonzalez, Mays | Thorne: Knutson, Lai
option_b_assign(gonzalez, silva).
option_b_assign(mays, silva).
option_b_assign(knutson, thorne).
option_b_assign(lai, thorne).

% Option C: Silva: Frost, Gonzalez, Heideck | Thorne: Knutson, Lai, Mays
option_c_assign(frost, silva).
option_c_assign(gonzalez, silva).
option_c_assign(heideck, silva).
option_c_assign(knutson, thorne).
option_c_assign(lai, thorne).
option_c_assign(mays, thorne).

% Option D: Silva: Frost, Heideck, Mays | Thorne: Gonzalez, Lai
option_d_assign(frost, silva).
option_d_assign(heideck, silva).
option_d_assign(mays, silva).
option_d_assign(gonzalez, thorne).
option_d_assign(lai, thorne).

% Option E: Silva: Frost, Heideck, Mays | Thorne: Gonzalez, Knutson, Lai
option_e_assign(frost, silva).
option_e_assign(heideck, silva).
option_e_assign(mays, silva).
option_e_assign(gonzalez, thorne).
option_e_assign(knutson, thorne).
option_e_assign(lai, thorne).

% Predicate to check a specific option
% We'll use a choice to pick which option to test
{ selected_option(a; b; c; d; e) } = 1.

% Derive assigned(P, C) from the selected option
assigned(P, C) :- selected_option(a), option_a_assign(P, C).
assigned(P, C) :- selected_option(b), option_b_assign(P, C).
assigned(P, C) :- selected_option(c), option_c_assign(P, C).
assigned(P, C) :- selected_option(d), option_d_assign(P, C).
assigned(P, C) :- selected_option(e), option_e_assign(P, C).

% A photographer is assigned if assigned to some ceremony
is_assigned(P) :- assigned(P, _).

% Constraint: At least 2 photographers per ceremony
:- ceremony(C), #count { P : assigned(P, C) } < 2.

% Constraint: No photographer assigned to both ceremonies
:- photographer(P), assigned(P, silva), assigned(P, thorne).

% Constraint 1: Frost must be assigned together with Heideck to one ceremony
% Meaning: Frost and Heideck must be assigned to the SAME ceremony
:- is_assigned(frost), is_assigned(heideck), assigned(frost, C1), assigned(heideck, C2), C1 != C2.
% Also: if one is assigned and not the other, that violates "must be together"
% Actually "must be assigned together to one ceremony" means if one is assigned, 
% the other must be assigned to the same ceremony.
% But also, could they both be unassigned? The phrasing says "Frost must be assigned together with Heideck"
% implying they ARE assigned (to some ceremony, together).
% Let me re-read: "Frost must be assigned together with Heideck to one of the graduation ceremonies."
% This means they are both assigned, to the same ceremony.
:- not is_assigned(frost).
:- not is_assigned(heideck).
:- assigned(frost, C1), assigned(heideck, C2), C1 != C2.

% Constraint 2: If Lai and Mays are both assigned, it must be to different ceremonies
:- is_assigned(lai), is_assigned(mays), assigned(lai, C), assigned(mays, C).

% Constraint 3: If Gonzalez is assigned to Silva, then Lai must be assigned to Thorne
:- assigned(gonzalez, silva), not assigned(lai, thorne).

% Constraint 4: If Knutson is not assigned to Thorne, then both Heideck and Mays must be assigned to it
:- not assigned(knutson, thorne), not assigned(heideck, thorne).
:- not assigned(knutson, thorne), not assigned(mays, thorne).

% A selected option is valid if all constraints are satisfied
valid :- selected_option(_).

% Map to answer
option(a) :- selected_option(a).
option(b) :- selected_option(b).
option(c) :- selected_option(c).
option(d) :- selected_option(d).
option(e) :- selected_option(e).

#show option/1.