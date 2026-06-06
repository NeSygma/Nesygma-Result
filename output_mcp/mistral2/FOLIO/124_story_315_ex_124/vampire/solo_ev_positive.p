fof(premise1, axiom,
    ! [X] : (can_transport_multiple_passengers(X) => ~one_seater(X))).

fof(premise2, axiom,
    ! [X] : (is_tesla_model_3(X) => can_transport_multiple_passengers(X))).

fof(premise3, axiom,
    ! [X] : (is_single_seat_electric_car(X) => one_seater(X))).

fof(premise4, axiom,
    ! [X] : (is_solo_ev(X) => is_single_seat_electric_car(X))).

fof(premise5, axiom,
    ~is_tesla_model_3(johns_car) => ~is_single_seat_electric_car(johns_car)).

fof(goal, conjecture,
    ~is_solo_ev(johns_car)).