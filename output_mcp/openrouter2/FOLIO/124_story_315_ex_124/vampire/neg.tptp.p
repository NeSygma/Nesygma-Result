fof(p1, axiom, ! [X] : (can_transport_multiple_passengers(X) => ~one_seater(X))).
fof(p2, axiom, ! [X] : (tesla_model3(X) => can_transport_multiple_passengers(X))).
fof(p3, axiom, ! [X] : (single_seat_electric_car(X) => one_seater(X))).
fof(p4, axiom, ! [X] : (solo_ev(X) => single_seat_electric_car(X))).
fof(p5, axiom, (~tesla_model3(john_car) => (~tesla_model3(john_car) | single_seat_electric_car(john_car)))).
fof(conjecture, conjecture, solo_ev(john_car)).