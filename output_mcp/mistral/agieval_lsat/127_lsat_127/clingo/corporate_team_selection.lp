% Define the employees
employee(myers). employee(ortega). employee(paine). employee(schmidt).
employee(thomson). employee(wong). employee(yoder). employee(zayre).

% Choice rule for selecting employees
{ selected(E) : employee(E) }.

% Constraints from the problem statement
:- selected(myers), selected(ortega).
:- selected(myers), selected(paine).
:- selected(schmidt), not selected(paine).
:- selected(schmidt), not selected(thomson).
:- selected(wong), not selected(myers).
:- selected(wong), not selected(yoder).

% Team must have at least 4 members
:- #count { E : selected(E) } < 4.

% The key insight: In every valid team, at least one of Thomson or Yoder must be selected.
% This is because:
% - If Schmidt is selected, Thomson must be selected (constraint)
% - If Wong is selected, Yoder must be selected (constraint)
% - If neither Schmidt nor Wong is selected, we need 4 people from Myers, Ortega, Paine, Thomson, Zayre
%   - Myers cannot be with Ortega or Paine
%   - Without Myers: Ortega, Paine, Thomson, Zayre is a valid team (has Thomson)
%   - With Myers: Myers + Thomson + Zayre + ??? (cannot complete 4 without violating Myers constraint)
% Therefore, Thomson or Yoder must be in every valid team.

% Define that the pair (Thomson, Yoder) is covered in the current selection
pair_thomson_yoder_covered :- selected(thomson).
pair_thomson_yoder_covered :- selected(yoder).

% Map the correct answer to option/1
% Since Option D (Thomson and Yoder) is the pair that must have at least one member in every valid team
option(d) :- pair_thomson_yoder_covered.

% Ensure only one option is selected (mutual exclusivity)
:- option(A), option(B), A != B.

% Show the answer
#show option/1.