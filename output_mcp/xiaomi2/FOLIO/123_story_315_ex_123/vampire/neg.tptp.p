fof(p1, axiom, ! [X] : (can_transport_multiple(X) => ~is_one_seater(X))).
fof(p2, axiom, ! [X] : (is_tesla_model_3(X) => can_transport_multiple(X))).
fof(p3, axiom, ! [X] : (is_single_seat_electric(X) => is_one_seater(X))).
fof(p4, axiom, ! [X] : (is_solo_ev(X) => is_single_seat_electric(X))).
fof(p5, axiom, ~is_tesla_model_3(johns_car) => (~is_tesla_model_3(johns_car) & ~is_single_seat_electric(johns_car))).
fof(goal, conjecture, ~is_solo_ev(johns_car)).