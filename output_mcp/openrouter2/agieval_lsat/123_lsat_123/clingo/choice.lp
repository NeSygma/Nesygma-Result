% Domain facts
employee(myers). employee(orte). employee(paine). employee(schmidt). employee(thomson). employee(wong). employee(yoder). employee(zayre).

% Choice of option
{choose(a); choose(b); choose(c); choose(d); choose(e)} 1.

% Selected employees for each option
selected_a(myers). selected_a(paine). selected_a(schmidt). selected_a(thomson).
selected_b(orte). selected_b(paine). selected_b(thomson). selected_b(zayre).
selected_c(paine). selected_c(schmidt). selected_c(yoder). selected_c(zayre).
selected_d(schmidt). selected_d(thomson). selected_d(yoder). selected_d(zayre).
selected_e(thomson). selected_e(wong). selected_e(yoder). selected_e(zayre).

selected(X) :- choose(a), selected_a(X).
selected(X) :- choose(b), selected_b(X).
selected(X) :- choose(c), selected_c(X).
selected(X) :- choose(d), selected_d(X).
selected(X) :- choose(e), selected_e(X).

% Constraints
:- selected(myers), selected(orte).
:- selected(myers), selected(paine).
:- selected(schmidt), not selected(paine).
:- selected(schmidt), not selected(thomson).
:- selected(wong), not selected(myers).
:- selected(wong), not selected(yoder).

% Map the correct answer to option/1
option(a) :- choose(a).
option(b) :- choose(b).
option(c) :- choose(c).
option(d) :- choose(d).
option(e) :- choose(e).

#show option/1.