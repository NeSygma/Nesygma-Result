% Negative version
fof(p1, axiom, ! [X] : (transport_multiple(X) => ~one_seater(X))).
fof(p2, axiom, ! [X] : (tesla_model3(X) => transport_multiple(X))).
fof(p3, axiom, ! [X] : (single_seat_electric_car(X) => one_seater(X))).
fof(p4, axiom, ! [X] : (solo_ev(X) => single_seat_electric_car(X))).
fof(p5, axiom, (~tesla_model3(john) => (~tesla_model3(john) | ~single_seat_electric_car(john)))).
fof(goal, conjecture, ~solo_ev(john)).