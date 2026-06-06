% Domains
student(juana; kelly; lateefah; mei; olga).
team(green; red).

% Each student assigned to exactly one team
1 { assigned(S, T) : team(T) } 1 :- student(S).

% One team has 2 members, the other has 3
green_count(N) :- N = #count{ S : assigned(S, green) }.
:- green_count(N), N != 2, N != 3.

% Each team has exactly one facilitator
1 { facilitator(S) : student(S), assigned(S, T) } 1 :- team(T).

% Constraint 1: Juana and Olga on different teams
:- assigned(juana, T), assigned(olga, T).

% Constraint 2: Lateefah is on green
assigned(lateefah, green).

% Constraint 3: Kelly is not a facilitator
:- facilitator(kelly).

% Constraint 4: Olga is a facilitator
facilitator(olga).

% Given condition: Mei is assigned to the green team
assigned(mei, green).

% --- Determine which options hold in each model ---
holds_in_model(a) :- assigned(juana, green).
holds_in_model(b) :- assigned(kelly, red).
holds_in_model(c) :- assigned(olga, green).
holds_in_model(d) :- facilitator(lateefah).
holds_in_model(e) :- facilitator(mei).

% --- Count models that satisfy each option ---
model_count(Opt, C) :- 
    student(Opt; Opt; Opt; Opt; Opt),
    C = #count{ holds_in_model(Opt) }.

% --- Helper: count total models ---
total_models(C) :- C = #count{ }.

% --- Derive which option holds in ALL models (must be true) ---
% We'll compute the answer by checking if the option is always true
must_be_true(Opt) :- 
    option(Opt), 
    total_models(T), 
    model_count(Opt, T).

% Map answers
option(a) :- must_be_true(a).
option(b) :- must_be_true(b).
option(c) :- must_be_true(c).
option(d) :- must_be_true(d).
option(e) :- must_be_true(e).

#show option/1.
#show assigned/2.
#show facilitator/1.