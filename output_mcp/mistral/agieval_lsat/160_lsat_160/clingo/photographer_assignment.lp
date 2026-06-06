% Photographer assignment problem

% Domains
photographer(frost; gonzalez; heideck; knutson; lai; mays).
ceremony(silva; thorne).

% Define the Thorne University assignments for each option
% Option A: Thorne = {frost, gonzalez, heideck, mays}
% Option B: Thorne = {frost, heideck, knutson, mays}
% Option C: Thorne = {gonzalez, knutson, lai}
% Option D: Thorne = {gonzalez, knutson, mays}
% Option E: Thorne = {knutson, mays}

% Helper predicates to define the Thorne assignment for each option
thorne_assignment(a, frost).
thorne_assignment(a, gonzalez).
thorne_assignment(a, heideck).
thorne_assignment(a, mays).

thorne_assignment(b, frost).
thorne_assignment(b, heideck).
thorne_assignment(b, knutson).
thorne_assignment(b, mays).

thorne_assignment(c, gonzalez).
thorne_assignment(c, knutson).
thorne_assignment(c, lai).

thorne_assignment(d, gonzalez).
thorne_assignment(d, knutson).
thorne_assignment(d, mays).

thorne_assignment(e, knutson).
thorne_assignment(e, mays).

% Base assignment rule: assign each photographer to at most one ceremony
{ assigned(P, C) : ceremony(C) } 1 :- photographer(P).

% For each option, enforce the Thorne assignment and derive Silva assignment
% Option A: Thorne = {frost, gonzalez, heideck, mays}, Silva = {knutson, lai}
:- option(a),
   not assigned(frost, thorne),
   not assigned(gonzalez, thorne),
   not assigned(heideck, thorne),
   not assigned(mays, thorne),
   assigned(knutson, silva),
   assigned(lai, silva).

% Option B: Thorne = {frost, heideck, knutson, mays}, Silva = {gonzalez, lai}
:- option(b),
   not assigned(frost, thorne),
   not assigned(heideck, thorne),
   not assigned(knutson, thorne),
   not assigned(mays, thorne),
   assigned(gonzalez, silva),
   assigned(lai, silva).

% Option C: Thorne = {gonzalez, knutson, lai}, Silva = {frost, heideck, mays}
:- option(c),
   not assigned(gonzalez, thorne),
   not assigned(knutson, thorne),
   not assigned(lai, thorne),
   assigned(frost, silva),
   assigned(heideck, silva),
   assigned(mays, silva).

% Option D: Thorne = {gonzalez, knutson, mays}, Silva = {frost, heideck, lai}
:- option(d),
   not assigned(gonzalez, thorne),
   not assigned(knutson, thorne),
   not assigned(mays, thorne),
   assigned(frost, silva),
   assigned(heideck, silva),
   assigned(lai, silva).

% Option E: Thorne = {knutson, mays}, Silva = {frost, gonzalez, heideck, lai}
:- option(e),
   not assigned(knutson, thorne),
   not assigned(mays, thorne),
   assigned(frost, silva),
   assigned(gonzalez, silva),
   assigned(heideck, silva),
   assigned(lai, silva).

% Base constraints
% 1. Each ceremony has at least 2 photographers
:- ceremony(C), #count{P: assigned(P, C)} < 2.

% 2. No photographer assigned to both ceremonies
:- assigned(P, silva), assigned(P, thorne).

% 3. Frost must be assigned together with Heideck to one of the ceremonies
:- assigned(frost, C), not assigned(heideck, C).
:- assigned(heideck, C), not assigned(frost, C).

% 4. If Lai and Mays are both assigned, they must be assigned to different ceremonies
:- assigned(lai, C), assigned(mays, C).

% 5. If Gonzalez is assigned to Silva University, then Lai must be assigned to Thorne University
:- assigned(gonzalez, silva), not assigned(lai, thorne).

% 6. If Knutson is not assigned to Thorne University, then both Heideck and Mays must be assigned to it
:- not assigned(knutson, thorne), not assigned(heideck, thorne).
:- not assigned(knutson, thorne), not assigned(mays, thorne).

% Define which option is being considered
{ option(a; b; c; d; e) } 1.

% Check for constraint violations for each option
constraint_violated(O) :- option(O), ceremony(C), #count{P: assigned(P, C)} < 2.
constraint_violated(O) :- option(O), assigned(P, silva), assigned(P, thorne).
constraint_violated(O) :- option(O), assigned(frost, C), not assigned(heideck, C).
constraint_violated(O) :- option(O), assigned(heideck, C), not assigned(frost, C).
constraint_violated(O) :- option(O), assigned(lai, C), assigned(mays, C).
constraint_violated(O) :- option(O), assigned(gonzalez, silva), not assigned(lai, thorne).
constraint_violated(O) :- option(O), not assigned(knutson, thorne), not assigned(heideck, thorne).
constraint_violated(O) :- option(O), not assigned(knutson, thorne), not assigned(mays, thorne).

% Mark options as invalid if they violate constraints
option_a_invalid :- option(a), constraint_violated(a).
option_b_invalid :- option(b), constraint_violated(b).
option_c_invalid :- option(c), constraint_violated(c).
option_d_invalid :- option(d), constraint_violated(d).
option_e_invalid :- option(e), constraint_violated(e).

% Map the correct answer to option/1
% The correct answer is the option that is invalid (cannot be the assignment)
option(a) :- option_a_invalid, not option_b_invalid, not option_c_invalid, not option_d_invalid, not option_e_invalid.
option(b) :- option_b_invalid, not option_a_invalid, not option_c_invalid, not option_d_invalid, not option_e_invalid.
option(c) :- option_c_invalid, not option_a_invalid, not option_b_invalid, not option_d_invalid, not option_e_invalid.
option(d) :- option_d_invalid, not option_a_invalid, not option_b_invalid, not option_c_invalid, not option_e_invalid.
option(e) :- option_e_invalid, not option_a_invalid, not option_b_invalid, not option_c_invalid, not option_d_invalid.

% Show the answer
#show option/1.