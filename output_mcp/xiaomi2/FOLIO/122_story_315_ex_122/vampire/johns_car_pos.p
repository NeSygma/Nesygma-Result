fof(p1, axiom, ! [X] : (multi_passenger(X) => ~one_seater(X))).
fof(p2, axiom, ! [X] : (tesla_model_3(X) => multi_passenger(X))).
fof(p3, axiom, ! [X] : (single_seat_electric(X) => one_seater(X))).
fof(p4, axiom, ! [X] : (solo_ev(X) => single_seat_electric(X))).
fof(p5, axiom, ~tesla_model_3(johns_car) => ~single_seat_electric(johns_car)).
fof(goal, conjecture, tesla_model_3(johns_car)).