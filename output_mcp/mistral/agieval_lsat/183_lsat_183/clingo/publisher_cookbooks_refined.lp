% Base entities
cookbook(k; l; m; n; o; p).
season(fall; spring).

% Assign each cookbook to a season
1 { assigned(C, S) : season(S) } 1 :- cookbook(C).

% Constraint 1: M and P cannot be in the same season
:- assigned(m, S), assigned(p, S).

% Constraint 2: K and N must be in the same season
:- assigned(k, S1), assigned(n, S2), S1 != S2.

% Constraint 3: If K is fall, O must be fall
:- assigned(k, fall), assigned(o, spring).

% Constraint 4: If M is fall, N must be spring
:- assigned(m, fall), assigned(n, fall).

% Define the conditions for each option
option_a_condition :- assigned(k, fall), assigned(l, spring).
option_b_condition :- assigned(o, fall), assigned(p, spring).
option_c_condition :- assigned(p, fall), assigned(l, spring).
option_d_condition :- assigned(k, spring), assigned(l, spring).
option_e_condition :- assigned(m, fall), assigned(l, fall).

% Check if the schedule is fully determined under each option's condition
% Option A: If A's condition holds, the schedule is fully determined
fully_determined_a :- option_a_condition,
                     assigned(k, fall), assigned(n, fall),
                     assigned(m, spring), assigned(p, fall),
                     assigned(o, fall), assigned(l, spring).

% Option B: If B's condition holds, the schedule is fully determined
fully_determined_b :- option_b_condition,
                     assigned(k, fall), assigned(n, fall),
                     assigned(m, spring), assigned(p, fall),
                     assigned(o, fall), assigned(l, spring).

% Option C: If C's condition holds, the schedule is fully determined
fully_determined_c :- option_c_condition,
                     assigned(k, fall), assigned(n, fall),
                     assigned(m, spring), assigned(p, fall),
                     assigned(o, fall), assigned(l, spring).

% Option D: If D's condition holds, the schedule is fully determined
fully_determined_d :- option_d_condition,
                     assigned(k, spring), assigned(n, spring),
                     assigned(m, fall), assigned(p, spring),
                     assigned(o, spring), assigned(l, spring).

% Option E: If E's condition holds, the schedule is fully determined
fully_determined_e :- option_e_condition,
                     assigned(k, fall), assigned(n, fall),
                     assigned(m, fall), assigned(p, spring),
                     assigned(o, fall), assigned(l, fall).

% Map the correct answer to option/1
option(a) :- fully_determined_a.
option(b) :- fully_determined_b.
option(c) :- fully_determined_c.
option(d) :- fully_determined_d.
option(e) :- fully_determined_e.

#show option/1.