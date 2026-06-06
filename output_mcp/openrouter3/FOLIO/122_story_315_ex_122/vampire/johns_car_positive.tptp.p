% John's car problem - Positive version
fof(premise_1, axiom, ! [X] : (transport_multiple(X) => ~one_seater(X))).
fof(premise_2, axiom, transport_multiple(tesla_model_3)).
fof(premise_3, axiom, ! [X] : (single_seat_electric(X) => one_seater(X))).
fof(premise_4, axiom, ! [X] : (solo_ev(X) => single_seat_electric(X))).
fof(premise_5, axiom, ~tesla_model_3(johns_car) => (~tesla_model_3(johns_car) | single_seat_electric(johns_car))).
fof(distinct_entities, axiom, (johns_car != tesla_model_3 & johns_car != solo_ev & tesla_model_3 != solo_ev)).
fof(goal, conjecture, tesla_model_3(johns_car)).