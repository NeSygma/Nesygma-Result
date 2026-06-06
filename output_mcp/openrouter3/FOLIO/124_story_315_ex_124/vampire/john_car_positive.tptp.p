fof(transport_multiple_not_one_seater, axiom, 
    ! [X] : (transport_multiple_passengers(X) => ~one_seater(X))).

fof(tesla_transport_multiple, axiom, 
    ! [X] : (tesla_model_3(X) => transport_multiple_passengers(X))).

fof(single_seat_electric_is_one_seater, axiom, 
    ! [X] : (single_seat_electric(X) => one_seater(X))).

fof(solo_ev_is_single_seat_electric, axiom, 
    ! [X] : (solo_ev(X) => single_seat_electric(X))).

fof(john_car_not_tesla_implication, axiom, 
    ~tesla_model_3(john_car) => (~tesla_model_3(john_car) | single_seat_electric(john_car))).

fof(goal, conjecture, ~solo_ev(john_car)).