% Option A selection facts
selected_a(myers). selected_a(paine). selected_a(schmidt). selected_a(thomson).

% Option B selection facts
selected_b(orte). selected_b(paine). selected_b(thomson). selected_b(zayre).

% Option C selection facts
selected_c(paine). selected_c(schmidt). selected_c(yoder). selected_c(zayre).

% Option D selection facts
selected_d(schmidt). selected_d(thomson). selected_d(yoder). selected_d(zayre).

% Option E selection facts
selected_e(thomson). selected_e(wong). selected_e(yoder). selected_e(zayre).

% Constraints for selected_a
:- selected_a(myers), selected_a(orte).
:- selected_a(myers), selected_a(paine).
:- selected_a(schmidt), not selected_a(paine).
:- selected_a(schmidt), not selected_a(thomson).
:- selected_a(wong), not selected_a(myers).
:- selected_a(wong), not selected_a(yoder).

% Constraints for selected_b
:- selected_b(myers), selected_b(orte).
:- selected_b(myers), selected_b(paine).
:- selected_b(schmidt), not selected_b(paine).
:- selected_b(schmidt), not selected_b(thomson).
:- selected_b(wong), not selected_b(myers).
:- selected_b(wong), not selected_b(yoder).

% Constraints for selected_c
:- selected_c(myers), selected_c(orte).
:- selected_c(myers), selected_c(paine).
:- selected_c(schmidt), not selected_c(paine).
:- selected_c(schmidt), not selected_c(thomson).
:- selected_c(wong), not selected_c(myers).
:- selected_c(wong), not selected_c(yoder).

% Constraints for selected_d
:- selected_d(myers), selected_d(orte).
:- selected_d(myers), selected_d(paine).
:- selected_d(schmidt), not selected_d(paine).
:- selected_d(schmidt), not selected_d(thomson).
:- selected_d(wong), not selected_d(myers).
:- selected_d(wong), not selected_d(yoder).

% Constraints for selected_e
:- selected_e(myers), selected_e(orte).
:- selected_e(myers), selected_e(paine).
:- selected_e(schmidt), not selected_e(paine).
:- selected_e(schmidt), not selected_e(thomson).
:- selected_e(wong), not selected_e(myers).
:- selected_e(wong), not selected_e(yoder).

% Map the correct answer to option/1
option(a) :- selected_a(myers), selected_a(paine), selected_a(schmidt), selected_a(thomson).
option(b) :- selected_b(orte), selected_b(paine), selected_b(thomson), selected_b(zayre).
option(c) :- selected_c(paine), selected_c(schmidt), selected_c(yoder), selected_c(zayre).
option(d) :- selected_d(schmidt), selected_d(thomson), selected_d(yoder), selected_d(zayre).
option(e) :- selected_e(thomson), selected_e(wong), selected_e(yoder), selected_e(zayre).

#show option/1.