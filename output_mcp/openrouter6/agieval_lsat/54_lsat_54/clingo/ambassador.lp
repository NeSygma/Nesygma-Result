% Countries and candidates
country(venezuela). country(yemen). country(zambia).
candidate(jaramillo). candidate(kayne). candidate(landon). candidate(novetzke). candidate(ong).

% Option A assignment
assign_a(venezuela, jaramillo).
assign_a(yemen, ong).
assign_a(zambia, novetzke).

% Option B assignment
assign_b(venezuela, kayne).
assign_b(yemen, jaramillo).
assign_b(zambia, landon).

% Option C assignment
assign_c(venezuela, landon).
assign_c(yemen, novetzke).
assign_c(zambia, ong).

% Option D assignment
assign_d(venezuela, novetzke).
assign_d(yemen, jaramillo).
assign_d(zambia, kayne).

% Option E assignment
assign_e(venezuela, ong).
assign_e(yemen, kayne).
assign_e(zambia, landon).

% Helper: exactly one of kayne or novetzke is assigned
exactly_one_kayne_novetzke(V1,V2,V3) :-
    (V1 = kayne; V2 = kayne; V3 = kayne),
    not (V1 = novetzke; V2 = novetzke; V3 = novetzke).
exactly_one_kayne_novetzke(V1,V2,V3) :-
    (V1 = novetzke; V2 = novetzke; V3 = novetzke),
    not (V1 = kayne; V2 = kayne; V3 = kayne).

% Check validity for each option
valid_a :-
    assign_a(venezuela, V1), assign_a(yemen, V2), assign_a(zambia, V3),
    % each candidate at most once
    V1 != V2, V1 != V3, V2 != V3,
    % constraint 1: exactly one of kayne or novetzke
    exactly_one_kayne_novetzke(V1,V2,V3),
    % constraint 2: if jaramillo then kayne
    ( (V1 = jaramillo; V2 = jaramillo; V3 = jaramillo) -> (V1 = kayne; V2 = kayne; V3 = kayne) ),
    % constraint 3: if ong in venezuela then not kayne in yemen
    ( V1 = ong -> not (V2 = kayne) ),
    % constraint 4: if landon then in zambia
    ( (V1 = landon; V2 = landon) -> V3 = landon ).

valid_b :-
    assign_b(venezuela, V1), assign_b(yemen, V2), assign_b(zambia, V3),
    V1 != V2, V1 != V3, V2 != V3,
    exactly_one_kayne_novetzke(V1,V2,V3),
    ( (V1 = jaramillo; V2 = jaramillo; V3 = jaramillo) -> (V1 = kayne; V2 = kayne; V3 = kayne) ),
    ( V1 = ong -> not (V2 = kayne) ),
    ( (V1 = landon; V2 = landon) -> V3 = landon ).

valid_c :-
    assign_c(venezuela, V1), assign_c(yemen, V2), assign_c(zambia, V3),
    V1 != V2, V1 != V3, V2 != V3,
    exactly_one_kayne_novetzke(V1,V2,V3),
    ( (V1 = jaramillo; V2 = jaramillo; V3 = jaramillo) -> (V1 = kayne; V2 = kayne; V3 = kayne) ),
    ( V1 = ong -> not (V2 = kayne) ),
    ( (V1 = landon; V2 = landon) -> V3 = landon ).

valid_d :-
    assign_d(venezuela, V1), assign_d(yemen, V2), assign_d(zambia, V3),
    V1 != V2, V1 != V3, V2 != V3,
    exactly_one_kayne_novetzke(V1,V2,V3),
    ( (V1 = jaramillo; V2 = jaramillo; V3 = jaramillo) -> (V1 = kayne; V2 = kayne; V3 = kayne) ),
    ( V1 = ong -> not (V2 = kayne) ),
    ( (V1 = landon; V2 = landon) -> V3 = landon ).

valid_e :-
    assign_e(venezuela, V1), assign_e(yemen, V2), assign_e(zambia, V3),
    V1 != V2, V1 != V3, V2 != V3,
    exactly_one_kayne_novetzke(V1,V2,V3),
    ( (V1 = jaramillo; V2 = jaramillo; V3 = jaramillo) -> (V1 = kayne; V2 = kayne; V3 = kayne) ),
    ( V1 = ong -> not (V2 = kayne) ),
    ( (V1 = landon; V2 = landon) -> V3 = landon ).

% Map the correct answer to option/1
option(a) :- valid_a.
option(b) :- valid_b.
option(c) :- valid_c.
option(d) :- valid_d.
option(e) :- valid_e.

#show option/1.