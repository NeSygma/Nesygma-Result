% Countries and candidates
country(venezuela). country(yemen). country(zambia).
candidate(jaramillo). candidate(kayne). candidate(landon). candidate(novetzke). candidate(ong).

% Option assignments
assign(a, venezuela, jaramillo).
assign(a, yemen, ong).
assign(a, zambia, novetzke).

assign(b, venezuela, kayne).
assign(b, yemen, jaramillo).
assign(b, zambia, landon).

assign(c, venezuela, landon).
assign(c, yemen, novetzke).
assign(c, zambia, ong).

assign(d, venezuela, novetzke).
assign(d, yemen, jaramillo).
assign(d, zambia, kayne).

assign(e, venezuela, ong).
assign(e, yemen, kayne).
assign(e, zambia, landon).

% Helper: exactly one of kayne or novetzke is assigned for a given option
exactly_one_kayne_novetzke(Option) :-
    #count{C : assign(Option, C, kayne)} + #count{C : assign(Option, C, novetzke)} = 1.

% Constraint 2: If Jaramillo is assigned then Kayne is assigned
jaramillo_implies_kayne(Option) :-
    assign(Option, _, jaramillo),
    assign(Option, _, kayne).

% Constraint 3: If Ong is assigned to Venezuela then Kayne is not assigned to Yemen
ong_venezuela_implies_not_kayne_yemen(Option) :-
    assign(Option, venezuela, ong),
    not assign(Option, yemen, kayne).

% Constraint 4: If Landon is assigned then it is to Zambia (i.e., not to Venezuela or Yemen)
landon_only_zambia(Option) :-
    not assign(Option, venezuela, landon),
    not assign(Option, yemen, landon).

% Validity for each option
valid(Option) :-
    % each country gets exactly one candidate (ensured by distinctness)
    assign(Option, venezuela, V1),
    assign(Option, yemen, V2),
    assign(Option, zambia, V3),
    V1 != V2, V1 != V3, V2 != V3,
    exactly_one_kayne_novetzke(Option),
    jaramillo_implies_kayne(Option),
    ong_venezuela_implies_not_kayne_yemen(Option),
    landon_only_zambia(Option).

% Map the correct answer to option/1
option(a) :- valid(a).
option(b) :- valid(b).
option(c) :- valid(c).
option(d) :- valid(d).
option(e) :- valid(e).

#show option/1.