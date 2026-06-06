% Bays and cargo types
bay(1..6).
cargo(fuel; grain; livestock; machinery; produce; textiles).

% Assign each bay a unique cargo
1 { assigned(B, C) : cargo(C) } 1 :- bay(B).
:- assigned(B1, C), assigned(B2, C), B1 != B2.

% Constraints from the problem
% 1. grain > livestock
:- assigned(B_grain, grain), assigned(B_livestock, livestock), B_grain =< B_livestock.
% 2. livestock > textiles
:- assigned(B_livestock, livestock), assigned(B_textiles, textiles), B_livestock =< B_textiles.
% 3. produce > fuel
:- assigned(B_produce, produce), assigned(B_fuel, fuel), B_produce =< B_fuel.
% 4. textiles next to produce
:- assigned(B_textiles, textiles), assigned(B_produce, produce), abs(B_textiles - B_produce) != 1.
% 5. produce next to livestock (condition for this question)
:- assigned(B_produce, produce), assigned(B_livestock, livestock), abs(B_produce - B_livestock) != 1.

% Additional constraint: all bays must be assigned
:- bay(B), not assigned(B, _).

% Define what each option means in a model
satisfies_a :- assigned(2, fuel).
satisfies_b :- assigned(4, produce).
satisfies_c :- assigned(4, textiles).
satisfies_d :- assigned(5, grain).
satisfies_e :- assigned(5, machinery).

% The exception is the option that is NOT satisfied in any valid model
% Since only one option is the exception, we derive option(X) for that one
option(a) :- not satisfies_a, satisfies_b, satisfies_c, satisfies_d, satisfies_e.
option(b) :- not satisfies_b, satisfies_a, satisfies_c, satisfies_d, satisfies_e.
option(c) :- not satisfies_c, satisfies_a, satisfies_b, satisfies_d, satisfies_e.
option(d) :- not satisfies_d, satisfies_a, satisfies_b, satisfies_c, satisfies_e.
option(e) :- not satisfies_e, satisfies_a, satisfies_b, satisfies_c, satisfies_d.

% Ensure only one option is selected (the exception)
:- option(X), option(Y), X != Y.

#show option/1.