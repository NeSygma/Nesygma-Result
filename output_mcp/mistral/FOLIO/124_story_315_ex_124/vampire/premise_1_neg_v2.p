fof(all_premises, axiom, 
    (! [X] : (can_transport_multiple(X) => ~one_seater(X))) &
    (! [X] : (tesla_model_3(X) => can_transport_multiple(X))) &
    (! [X] : (single_seat_electric_car(X) => one_seater(X))) &
    (! [X] : (solo_ev(X) => single_seat_electric_car(X))) &
    (! [X] : (~tesla_model_3(X) => (~tesla_model_3(X) | ~single_seat_electric_car(X))))).

fof(johns_car_constant, axiom, johns_car).

fof(conclusion, conjecture, solo_ev(johns_car)).