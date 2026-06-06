% Domains
country(venezuela).
country(yemen).
country(zambia).

candidate(jaramillo).
candidate(kayne).
candidate(landon).
candidate(novetzke).
candidate(ong).

% Option identifiers
opt(a). opt(b). opt(c). opt(d). opt(e).

% Assignments for each option
% Option A: Venezuela: Jaramillo Yemen: Ong Zambia: Novetzke
assign(a, venezuela, jaramillo).
assign(a, yemen, ong).
assign(a, zambia, novetzke).

% Option B: Venezuela: Kayne Yemen: Jaramillo Zambia: Landon
assign(b, venezuela, kayne).
assign(b, yemen, jaramillo).
assign(b, zambia, landon).

% Option C: Venezuela: Landon Yemen: Novetzke Zambia: Ong
assign(c, venezuela, landon).
assign(c, yemen, novetzke).
assign(c, zambia, ong).

% Option D: Venezuela: Novetzke Yemen: Jaramillo Zambia: Kayne
assign(d, venezuela, novetzke).
assign(d, yemen, jaramillo).
assign(d, zambia, kayne).

% Option E: Venezuela: Ong Yemen: Kayne Zambia: Landon
assign(e, venezuela, ong).
assign(e, yemen, kayne).
assign(e, zambia, landon).

% Constraint 1: Exactly one of Kayne or Novetzke is assigned (but not both)
violation1(O) :- opt(O), assign(O, _, kayne), assign(O, _, novetzke).
violation2(O) :- opt(O), not assign(O, _, kayne), not assign(O, _, novetzke).

% Constraint 2: If Jaramillo is assigned, then Kayne is assigned
violation3(O) :- opt(O), assign(O, _, jaramillo), not assign(O, _, kayne).

% Constraint 3: If Ong is assigned to Venezuela, then Kayne is not assigned to Yemen
violation4(O) :- opt(O), assign(O, venezuela, ong), assign(O, yemen, kayne).

% Constraint 4: If Landon is assigned, it must be to Zambia
violation5(O) :- opt(O), assign(O, C, landon), C != zambia.

% An option is valid if no violations occur
valid(O) :- opt(O),
            not violation1(O),
            not violation2(O),
            not violation3(O),
            not violation4(O),
            not violation5(O).

% Map valid options to option/1
option(a) :- valid(a).
option(b) :- valid(b).
option(c) :- valid(c).
option(d) :- valid(d).
option(e) :- valid(e).

#show option/1.