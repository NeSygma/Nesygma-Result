fof(prem1, axiom, ! [X] : (can_transport_multiple(X) => ~one_seater(X))).
fof(prem2, axiom, ! [X] : (tesla_model_3(X) => can_transport_multiple(X))).
fof(prem3, axiom, ! [X] : (single_seat_electric(X) => one_seater(X))).
fof(prem4, axiom, ! [X] : (solo_ev(X) => single_seat_electric(X))).
fof(prem5, axiom, ~single_seat_electric(john_car) | tesla_model_3(john_car)).
fof(goal, conjecture, tesla_model_3(john_car)).