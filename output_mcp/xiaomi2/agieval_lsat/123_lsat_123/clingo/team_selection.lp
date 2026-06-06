% Domain: employees
employee(myers; ortega; paine; schmidt; thomson; wong; yoder; zayre).

% Define each option as a set of facts
% Option A: Myers, Paine, Schmidt, Thomson
on_team_a(myers). on_team_a(paine). on_team_a(schmidt). on_team_a(thomson).

% Option B: Ortega, Paine, Thomson, Zayre
on_team_b(ortega). on_team_b(paine). on_team_b(thomson). on_team_b(zayre).

% Option C: Paine, Schmidt, Yoder, Zayre
on_team_c(paine). on_team_c(schmidt). on_team_c(yoder). on_team_c(zayre).

% Option D: Schmidt, Thomson, Yoder, Zayre
on_team_d(schmidt). on_team_d(thomson). on_team_d(yoder). on_team_d(zayre).

% Option E: Thomson, Wong, Yoder, Zayre
on_team_e(thomson). on_team_e(wong). on_team_e(yoder). on_team_e(zayre).

% Constraint 1: If Myers is on the team, neither Ortega nor Paine can be.
% Violation: Myers on team AND (Ortega or Paine on team)
violates_a :- on_team_a(myers), on_team_a(ortega).
violates_a :- on_team_a(myers), on_team_a(paine).

violates_b :- on_team_b(myers), on_team_b(ortega).
violates_b :- on_team_b(myers), on_team_b(paine).

violates_c :- on_team_c(myers), on_team_c(ortega).
violates_c :- on_team_c(myers), on_team_c(paine).

violates_d :- on_team_d(myers), on_team_d(ortega).
violates_d :- on_team_d(myers), on_team_d(paine).

violates_e :- on_team_e(myers), on_team_e(ortega).
violates_e :- on_team_e(myers), on_team_e(paine).

% Constraint 2: If Schmidt is on the team, both Paine and Thomson must also be.
% Violation: Schmidt on team AND (Paine not on team OR Thomson not on team)
violates_a :- on_team_a(schmidt), not on_team_a(paine).
violates_a :- on_team_a(schmidt), not on_team_a(thomson).

violates_b :- on_team_b(schmidt), not on_team_b(paine).
violates_b :- on_team_b(schmidt), not on_team_b(thomson).

violates_c :- on_team_c(schmidt), not on_team_c(paine).
violates_c :- on_team_c(schmidt), not on_team_c(thomson).

violates_d :- on_team_d(schmidt), not on_team_d(paine).
violates_d :- on_team_d(schmidt), not on_team_d(thomson).

violates_e :- on_team_e(schmidt), not on_team_e(paine).
violates_e :- on_team_e(schmidt), not on_team_e(thomson).

% Constraint 3: If Wong is on the team, both Myers and Yoder must also be.
% Violation: Wong on team AND (Myers not on team OR Yoder not on team)
violates_a :- on_team_a(wong), not on_team_a(myers).
violates_a :- on_team_a(wong), not on_team_a(yoder).

violates_b :- on_team_b(wong), not on_team_b(myers).
violates_b :- on_team_b(wong), not on_team_b(yoder).

violates_c :- on_team_c(wong), not on_team_c(myers).
violates_c :- on_team_c(wong), not on_team_c(yoder).

violates_d :- on_team_d(wong), not on_team_d(myers).
violates_d :- on_team_d(wong), not on_team_d(yoder).

violates_e :- on_team_e(wong), not on_team_e(myers).
violates_e :- on_team_e(wong), not on_team_e(yoder).

% An option is valid if it does NOT violate any constraint
valid_a :- not violates_a.
valid_b :- not violates_b.
valid_c :- not violates_c.
valid_d :- not violates_d.
valid_e :- not violates_e.

% Map to option/1
option(a) :- valid_a.
option(b) :- valid_b.
option(c) :- valid_c.
option(d) :- valid_d.
option(e) :- valid_e.

#show option/1.