% persons and countries
person(j). person(k). person(l). person(n). person(o).
country(v). country(y). country(z).

% exactly one person per country
1 { assign(C,P) : person(P) } 1 :- country(C).

% each person assigned at most one country
:- assign(C1,P), assign(C2,P), C1 != C2.

% derived assigned predicate
assigned(P) :- assign(_,P).

% problem constraints
% 1. exactly one of Kayne(k) or Novetzke(n) assigned
:- assigned(k), assigned(n).
:- not assigned(k), not assigned(n).
% 2. if J assigned then Kayne assigned
:- assign(_,j), not assigned(k).
% 3. if Ong assigned to Venezuela then Kayne not assigned to Yemen
:- assign(v,o), assign(y,k).
% 4. if Landon assigned, it is to Zambia
:- assign(C,l), C != z.

% detect any violation (for possible checking)
violation_any :- assigned(k), assigned(n).
violation_any :- not assigned(k), not assigned(n).
violation_any :- assign(_,j), not assigned(k).
violation_any :- assign(v,o), assign(y,k).
violation_any :- assign(C,l), C != z.
violation_any :- assign(C1,P), assign(C2,P), C1 != C2.

% scenario conditions for each option
scenario_a :- assign(z,j).   % Jaramillo to Zambia
scenario_b :- assign(z,k).   % Kayne to Zambia
scenario_c :- assign(z,n).   % Novetzke to Zambia
scenario_d :- not assigned(l). % Landon not assigned
scenario_e :- not assigned(o). % Ong not assigned

% possible if scenario holds and no violation
possible_a :- scenario_a, not violation_any.
possible_b :- scenario_b, not violation_any.
possible_c :- scenario_c, not violation_any.
possible_d :- scenario_d, not violation_any.
possible_e :- scenario_e, not violation_any.

% option is impossible if not possible
option(a) :- not possible_a.
option(b) :- not possible_b.
option(c) :- not possible_c.
option(d) :- not possible_d.
option(e) :- not possible_e.

#show option/1.