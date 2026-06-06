fof(city_types, axiom, city(billings) & city(butte) & city(helena) & city(missoula) & city(white_sulphur_springs) & city(st_pierre) & city(bismarck) & city(bristol) & city(texarkana) & city(texhoma) & city(union_city)).
fof(state_type, axiom, state(montana)).
fof(premise1, axiom, in_city(billings, montana)).
fof(premise2, axiom, in_city(butte, montana) & in_city(helena, montana) & in_city(missoula, montana)).
fof(premise3, axiom, in_city(white_sulphur_springs, montana)).
fof(premise4, axiom, ~in_city(st_pierre, montana)).
fof(exception_cities, axiom, exception(bristol) & exception(texarkana) & exception(texhoma) & exception(union_city)).
fof(uniqueness_rule, axiom, ! [X, Y1, Y2] : (city(X) & in_city(X, Y1) & in_city(X, Y2) => Y1 = Y2)).
fof(every_city_in_state, axiom, ! [X] : (city(X) => ? [Y] : in_city(X, Y))).
fof(goal, conjecture, ? [S] : (in_city(st_pierre, S) & in_city(bismarck, S))).