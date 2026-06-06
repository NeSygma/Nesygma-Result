% Workers
worker(quinn). worker(ruiz). worker(smith). worker(taylor). worker(verma). worker(wells). worker(xue).

% Define each option as a scenario
% Option A: Ruiz (leader), Taylor, Wells
option_a_member(ruiz). option_a_member(taylor). option_a_member(wells).
option_a_leader(ruiz).

% Option B: Verma (leader), Quinn, Taylor
option_b_member(verma). option_b_member(quinn). option_b_member(taylor).
option_b_leader(verma).

% Option C: Verma (leader), Smith, Taylor
option_c_member(verma). option_c_member(smith). option_c_member(taylor).
option_c_leader(verma).

% Option D: Verma (leader), Smith, Xue
option_d_member(verma). option_d_member(smith). option_d_member(xue).
option_d_leader(verma).

% Option E: Xue (leader), Verma, Wells
option_e_member(xue). option_e_member(verma). option_e_member(wells).
option_e_leader(xue).

% Check constraints for each option
% Constraint 1: Quinn or Ruiz can be a member only if leading
% If Quinn is member, Quinn must be leader
% If Ruiz is member, Ruiz must be leader
% Constraint 2: If Smith is member, Taylor must be member
% Constraint 3: If Wells is member, neither Ruiz nor Verma can be member

% Helper: check if an option violates any constraint
% Violation if Quinn is member but not leader
violates_a :- option_a_member(quinn), not option_a_leader(quinn).
violates_a :- option_a_member(ruiz), not option_a_leader(ruiz).
violates_a :- option_a_member(smith), not option_a_member(taylor).
violates_a :- option_a_member(wells), option_a_member(ruiz).
violates_a :- option_a_member(wells), option_a_member(verma).

violates_b :- option_b_member(quinn), not option_b_leader(quinn).
violates_b :- option_b_member(ruiz), not option_b_leader(ruiz).
violates_b :- option_b_member(smith), not option_b_member(taylor).
violates_b :- option_b_member(wells), option_b_member(ruiz).
violates_b :- option_b_member(wells), option_b_member(verma).

violates_c :- option_c_member(quinn), not option_c_leader(quinn).
violates_c :- option_c_member(ruiz), not option_c_leader(ruiz).
violates_c :- option_c_member(smith), not option_c_member(taylor).
violates_c :- option_c_member(wells), option_c_member(ruiz).
violates_c :- option_c_member(wells), option_c_member(verma).

violates_d :- option_d_member(quinn), not option_d_leader(quinn).
violates_d :- option_d_member(ruiz), not option_d_leader(ruiz).
violates_d :- option_d_member(smith), not option_d_member(taylor).
violates_d :- option_d_member(wells), option_d_member(ruiz).
violates_d :- option_d_member(wells), option_d_member(verma).

violates_e :- option_e_member(quinn), not option_e_leader(quinn).
violates_e :- option_e_member(ruiz), not option_e_leader(ruiz).
violates_e :- option_e_member(smith), not option_e_member(taylor).
violates_e :- option_e_member(wells), option_e_member(ruiz).
violates_e :- option_e_member(wells), option_e_member(verma).

% An option is acceptable if it does not violate any constraint
acceptable(a) :- not violates_a.
acceptable(b) :- not violates_b.
acceptable(c) :- not violates_c.
acceptable(d) :- not violates_d.
acceptable(e) :- not violates_e.

% Map to option/1
option(a) :- acceptable(a).
option(b) :- acceptable(b).
option(c) :- acceptable(c).
option(d) :- acceptable(d).
option(e) :- acceptable(e).

#show option/1.