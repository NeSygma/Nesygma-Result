% Employees
employee(myers).
employee(ortega).
employee(paine).
employee(schmidt).
employee(thomson).
employee(wong).
employee(yoder).
employee(zayre).

% Constraints
:- selected(myers), selected(ortega).
:- selected(myers), selected(paine).
:- selected(schmidt), not selected(paine).
:- selected(schmidt), not selected(thomson).
:- selected(wong), not selected(myers).
:- selected(wong), not selected(yoder).

% Only one option can be true
1 { option_a; option_b; option_c; option_d; option_e } 1.

% Define selected employees for each option
selected(myers) :- option_a.
selected(paine) :- option_a.
selected(schmidt) :- option_a.
selected(thomson) :- option_a.

selected(ortega) :- option_b.
selected(paine) :- option_b.
selected(thomson) :- option_b.
selected(zayre) :- option_b.

selected(paine) :- option_c.
selected(schmidt) :- option_c.
selected(yoder) :- option_c.
selected(zayre) :- option_c.

selected(schmidt) :- option_d.
selected(thomson) :- option_d.
selected(yoder) :- option_d.
selected(zayre) :- option_d.

selected(thomson) :- option_e.
selected(wong) :- option_e.
selected(yoder) :- option_e.
selected(zayre) :- option_e.

% Ensure only employees in the selected option are on the team
:- option_a, selected(E), E != myers, E != paine, E != schmidt, E != thomson.
:- option_b, selected(E), E != ortega, E != paine, E != thomson, E != zayre.
:- option_c, selected(E), E != paine, E != schmidt, E != yoder, E != zayre.
:- option_d, selected(E), E != schmidt, E != thomson, E != yoder, E != zayre.
:- option_e, selected(E), E != thomson, E != wong, E != yoder, E != zayre.

% Map to option/1
option(a) :- option_a.
option(b) :- option_b.
option(c) :- option_c.
option(d) :- option_d.
option(e) :- option_e.

#show option/1.