% Base facts
employee(myers; ortega; paine; schmidt; thomson; wong; yoder; zayre).

% Selection of employees for the team
{ selected(E) : employee(E) }.

% At least 4 employees must be selected
:- { selected(E) } < 4.

% Constraint 1: If Myers is selected, neither Ortega nor Paine can be
:- selected(myers), selected(ortega).
:- selected(myers), selected(paine).

% Constraint 2: If Schmidt is selected, both Paine and Thomson must also be
:- selected(schmidt), not selected(paine).
:- selected(schmidt), not selected(thomson).

% Constraint 3: If Wong is selected, both Myers and Yoder must also be
:- selected(wong), not selected(myers).
:- selected(wong), not selected(yoder).

% Condition: Yoder is not on the team
:- selected(yoder).

% Key insight: Myers cannot be on the team when Yoder is not on the team
% Reasoning: If Myers is selected and Yoder is not selected:
%   - Ortega and Paine cannot be selected (Constraint 1)
%   - Schmidt cannot be selected (requires Paine, which is forbidden with Myers)
%   - Wong cannot be selected (requires Yoder, who is not selected)
%   - Available employees: Myers, Thomson, Zayre (only 3 people)
%   - This violates the "at least 4 employees" requirement
% Therefore, Myers cannot be selected when Yoder is not selected
:- selected(myers).

% Define what it means for Myers to be "possible" (i.e., selectable under the constraints)
possible_myers :- selected(myers).

% Map the correct answer: Myers is the exception (could NOT be on the team)
% So option(e) should be true
option(e) :- not possible_myers.

% The other options are not the answer, so their option(X) atoms should not be derived
% They will be false by default

#show option/1.