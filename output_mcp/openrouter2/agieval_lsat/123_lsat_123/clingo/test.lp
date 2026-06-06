selected_b(orte). selected_b(paine). selected_b(thomson). selected_b(zayre).
:- selected_b(myers), selected_b(orte).
:- selected_b(myers), selected_b(paine).
:- selected_b(schmidt), not selected_b(paine).
:- selected_b(schmidt), not selected_b(thomson).
:- selected_b(wong), not selected_b(myers).
:- selected_b(wong), not selected_b(yoder).
#show selected_b/1.