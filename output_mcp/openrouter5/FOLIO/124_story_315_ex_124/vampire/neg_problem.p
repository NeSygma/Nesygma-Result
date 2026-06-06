% Negative version: negated conclusion as conjecture
% Negated conclusion: John's car IS a Solo EV.

fof(premise1, axiom, ! [X] : (can_transport_multiple(X) => ~one_seater(X))).
fof(premise2, axiom, ! [X] : (tesla_model_3(X) => can_transport_multiple(X))).
fof(premise3, axiom, ! [X] : (single_seat_electric(X) => one_seater(X))).
fof(premise4, axiom, ! [X] : (solo_ev(X) => single_seat_electric(X))).
fof(premise5, axiom, (~tesla_model_3(johns_car) => (~tesla_model_3(johns_car) | ~single_seat_electric(johns_car)))).

% Negated conclusion: John's car IS a Solo EV.
fof(neg_conclusion, conjecture, solo_ev(johns_car)).