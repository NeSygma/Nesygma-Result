fof(premise1, axiom, ! [X] : (can_transport_multiple_passengers(X) => ~is_one_seater(X))).
fof(premise2, axiom, ! [X] : (tesla_model_3(X) => can_transport_multiple_passengers(X))).
fof(premise3, axiom, ! [X] : (single_seat_electric(X) => is_one_seater(X))).
fof(premise4, axiom, ! [X] : (solo_ev(X) => single_seat_electric(X))).
fof(premise5, axiom, ~tesla_model_3(john_car) => ~(tesla_model_3(john_car) | single_seat_electric(john_car))).
fof(goal, conjecture, ~solo_ev(john_car)).