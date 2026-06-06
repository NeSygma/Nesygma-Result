% Scientists and their types
botanist(f). botanist(g). botanist(h).
chemist(k). chemist(l). chemist(m).
zoologist(p). zoologist(q). zoologist(r).

% Domain for selection
{ selected(S) : botanist(S) }.
{ selected(S) : chemist(S) }.
{ selected(S) : zoologist(S) }.

% Total panel size is 5
panel_size(N) :- N = #count { S : selected(S) }.
:- panel_size(N), N != 5.

% At least one of each type
:- not 1 { selected(S) : botanist(S) } 1.
:- not 1 { selected(S) : chemist(S) } 1.
:- not 1 { selected(S) : zoologist(S) } 1.

% If more than one botanist is selected, then at most one zoologist is selected
num_botanists(N) :- N = #count { S : selected(S), botanist(S) }.
num_zoologists(N) :- N = #count { S : selected(S), zoologist(S) }.
:- num_botanists(N), N > 1, num_zoologists(M), M > 1.

% F and K cannot both be selected
:- selected(f), selected(k).

% K and M cannot both be selected
:- selected(k), selected(m).

% If M is selected, both P and R must be selected
:- selected(m), not selected(p).
:- selected(m), not selected(r).

% Scenario: Both G and H are selected (i.e., both are in the panel)
scenario_both_g_and_h :- selected(g), selected(h).

% Define conditions for each option
% Option A: If F is not selected, then K must be selected
option_a_holds :- not selected(f), selected(k).
option_a_holds :- selected(f).

% Option B: If F is not selected, then M must be selected
option_b_holds :- not selected(f), selected(m).
option_b_holds :- selected(f).

% Option C: If K is not selected, then M must be selected
option_c_holds :- not selected(k), selected(m).
option_c_holds :- selected(k).

% Option D: If M is not selected, then Q must be selected
option_d_holds :- not selected(m), selected(q).
option_d_holds :- selected(m).

% Option E: If P is not selected, then Q must be selected
option_e_holds :- not selected(p), selected(q).
option_e_holds :- selected(p).

% Now, we want to find which option MUST be true if scenario_both_g_and_h holds.
% We will derive option(X) if the corresponding option_holds is true whenever scenario_both_g_and_h holds.

% To ensure that only one option is correct, we will use the following logic:
% If scenario_both_g_and_h holds, then the correct option must be the one that is necessarily true.

% We will use constraints to ensure that only the correct option is derived.

% If scenario_both_g_and_h holds, then the correct option must be the one that is necessarily true.
% We will derive option(X) if the corresponding option_holds is true in all models where scenario_both_g_and_h holds.

% To do this, we will use the following approach:
% For each option, we will check if it is necessarily true when scenario_both_g_and_h holds.

% We will use the fact that if an option is necessarily true, it will be the only one derived.

% Map the correct answer to option/1
option(a) :- scenario_both_g_and_h, option_a_holds, not option_b_holds, not option_c_holds, not option_d_holds, not option_e_holds.
option(b) :- scenario_both_g_and_h, option_b_holds, not option_a_holds, not option_c_holds, not option_d_holds, not option_e_holds.
option(c) :- scenario_both_g_and_h, option_c_holds, not option_a_holds, not option_b_holds, not option_d_holds, not option_e_holds.
option(d) :- scenario_both_g_and_h, option_d_holds, not option_a_holds, not option_b_holds, not option_c_holds, not option_e_holds.
option(e) :- scenario_both_g_and_h, option_e_holds, not option_a_holds, not option_b_holds, not option_c_holds, not option_d_holds.

#show option/1.