% Negative: negated claim as conjecture
fof(p1, axiom, ! [X] : (can_transport_multiple(X) => ~one_seater(X))).
fof(p2, axiom, ! [X] : (tesla_model_3(X) => can_transport_multiple(X))).
fof(p3, axiom, ! [X] : (single_seat_electric_car(X) => one_seater(X))).
fof(p4, axiom, ! [X] : (solo_ev_car(X) => single_seat_electric_car(X))).
fof(p5, axiom, (~tesla_model_3(johns_car) => ~(tesla_model_3(johns_car) | single_seat_electric_car(johns_car)))).
fof(goal, conjecture, ~tesla_model_3(johns_car)).