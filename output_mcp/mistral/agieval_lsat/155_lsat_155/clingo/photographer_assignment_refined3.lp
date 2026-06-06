% Base facts
photographer(frost).
photographer(gonzalez).
photographer(heideck).
photographer(knutson).
photographer(lai).
photographer(mays).

ceremony(silva).
ceremony(thorne).

% Base constraints
% Each ceremony must have at least 2 photographers
:- ceremony(C), #count{P: assigned(P, C)} < 2.

% No photographer can be assigned to both ceremonies
:- photographer(P), assigned(P, silva), assigned(P, thorne).

% Frost must be assigned together with Heideck to one ceremony
:- assigned(frost, C1), assigned(heideck, C2), C1 != C2.

% If Lai and Mays are both assigned, they must be at different ceremonies
:- assigned(lai, C), assigned(mays, C), assigned(lai, _), assigned(mays, _).

% If Gonzalez is assigned to Silva, then Lai must be assigned to Thorne
:- assigned(gonzalez, silva), not assigned(lai, thorne).

% If Knutson is not assigned to Thorne, then both Heideck and Mays must be assigned to Thorne
:- not assigned(knutson, thorne), not assigned(heideck, thorne).
:- not assigned(knutson, thorne), not assigned(mays, thorne).

% Define the specific assignments for each option as facts
% Option A: Silva: Gonzalez, Lai; Thorne: Frost, Heideck, Mays
% Check if this assignment satisfies all constraints
option_a_valid :- assigned(gonzalez, silva), assigned(lai, silva),
                  assigned(frost, thorne), assigned(heideck, thorne), assigned(mays, thorne),
                  % Additional constraints for Option A
                  not assigned(frost, silva), not assigned(heideck, silva),
                  not assigned(knutson, silva), not assigned(knutson, thorne).

% Option B: Silva: Gonzalez, Mays; Thorne: Knutson, Lai
option_b_valid :- assigned(gonzalez, silva), assigned(mays, silva),
                  assigned(knutson, thorne), assigned(lai, thorne),
                  % Additional constraints for Option B
                  not assigned(frost, _), not assigned(heideck, _).

% Option C: Silva: Frost, Gonzalez, Heideck; Thorne: Knutson, Lai, Mays
option_c_valid :- assigned(frost, silva), assigned(gonzalez, silva), assigned(heideck, silva),
                  assigned(knutson, thorne), assigned(lai, thorne), assigned(mays, thorne),
                  % Additional constraints for Option C
                  not assigned(knutson, silva), not assigned(lai, silva), not assigned(mays, silva).

% Option D: Silva: Frost, Heideck, Mays; Thorne: Gonzalez, Lai
option_d_valid :- assigned(frost, silva), assigned(heideck, silva), assigned(mays, silva),
                  assigned(gonzalez, thorne), assigned(lai, thorne),
                  % Additional constraints for Option D
                  not assigned(knutson, thorne), not assigned(knutson, silva).

% Option E: Silva: Frost, Heideck, Mays; Thorne: Gonzalez, Knutson, Lai
option_e_valid :- assigned(frost, silva), assigned(heideck, silva), assigned(mays, silva),
                  assigned(gonzalez, thorne), assigned(knutson, thorne), assigned(lai, thorne),
                  % Additional constraints for Option E
                  not assigned(knutson, silva), not assigned(gonzalez, silva).

% Map the correct answer to option/1
option(a) :- option_a_valid.
option(b) :- option_b_valid.
option(c) :- option_c_valid.
option(d) :- option_d_valid.
option(e) :- option_e_valid.

#show option/1.