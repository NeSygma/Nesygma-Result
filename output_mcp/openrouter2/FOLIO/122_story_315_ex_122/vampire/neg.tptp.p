fof(premise1, axiom, ! [X] : (can_transport_multiple_passengers(X) => ~one_seater(X))).
fof(premise2, axiom, ! [X] : (tesla_model3(X) => can_transport_multiple_passengers(X))).
fof(premise3, axiom, ! [X] : (single_seat_electric_car(X) => one_seater(X))).
fof(premise4, axiom, ! [X] : (solo_ev_car(X) => single_seat_electric_car(X))).
fof(premise5, axiom, (~tesla_model3(johns_car) => (~tesla_model3(johns_car) | single_seat_electric_car(johns_car)))).
fof(conjecture, conjecture, ~tesla_model3(johns_car)).