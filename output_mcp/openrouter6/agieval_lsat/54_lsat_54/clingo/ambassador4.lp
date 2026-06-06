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

% Helper: kn(C) true if C is kayne or novetzke
kn(kayne). kn(novetzke).

% Compute kn_count per option
kn_count(Option, N) :- N = #count{C : assign(Option, C, kayne); C : assign(Option, C, novetzke)}.

% Constraint 1: Exactly one of kayne or novetzke is assigned
:- kn_count(Option, N), N != 1.

% Constraint 2: If Jaramillo is assigned then Kayne is assigned
:- assign(Option, _, jaramillo), not assign(Option, _, kayne).

% Constraint 3: If Ong is assigned to Venezuela then Kayne is not assigned to Yemen
:- assign(Option, venezuela, ong), assign(Option, yemen, kayne).

% Constraint 4: If Landon is assigned then it is to Zambia (i.e., not to Venezuela or Yemen)
:- assign(Option, venezuela, landon).
:- assign(Option, yemen, landon).

% Ensure each candidate appears at most once per option (already satisfied by distinctness)
% But we can add a constraint to be safe
:- assign(Option, C1, Cand), assign(Option, C2, Cand), C1 != C2.

% Define invalid(Option) if any constraint is violated for that option
invalid(Option) :- kn_count(Option, N), N != 1.
invalid(Option) :- assign(Option, _, jaramillo), not assign(Option, _, kayne).
invalid(Option) :- assign(Option, venezuela, ong), assign(Option, yemen, kayne).
invalid(Option) :- assign(Option, venezuela, landon).
invalid(Option) :- assign(Option, yemen, landon).

% Option is valid if not invalid
option(Option) :- assign(Option, _, _), not invalid(Option).

#show option/1.