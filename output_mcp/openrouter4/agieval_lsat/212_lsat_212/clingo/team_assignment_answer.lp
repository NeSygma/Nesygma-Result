% Domains
student(juana; kelly; lateefah; mei; olga).
team(green; red).

% Each student assigned to exactly one team
1 { assigned(S, T) : team(T) } 1 :- student(S).

% Team sizes: one team has 2 members, the other has 3
green_count(N) :- N = #count{ S : assigned(S, green) }.
:- green_count(N), N != 2, N != 3.
:- green_count(N1), #count{ S : assigned(S, red) } = N2, N1 = N2.

% Each team has exactly one facilitator
1 { facilitator(S) : assigned(S, T) } 1 :- team(T).

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

% Now determine which option must be true.
% An option "must be true" if it holds in all answer sets.
% We can test this by checking if adding the negation of the option
% makes the problem unsatisfiable.

% (A) Juana is on green -> test if not(juana on green) is possible
% (B) Kelly is on red -> test if not(kelly on red) is possible
% (C) Olga is on green -> test if not(olga on green) is possible
% (D) Lateefah is facilitator -> test if not(lateefah facilitator) is possible
% (E) Mei is facilitator -> test if not(mei facilitator) is possible

% Use a scenario approach: try each option with its negation forced
% and see which leads to unsatisfiability

% We'll compute a "must_be_true" predicate by checking contrapositive
% Option X must be true if: premises + not(X) is unsatisfiable.

% Let's encode this: For each option, if every model has the option true,
% then the option is forced.

% We can check by looking at all answer sets and deriving what's common.
% Let's collect all answer sets using a projection technique.

% First, let's just enumerate what we already found.
% From the previous run, we saw 4 models, and in ALL of them, kelly is on red.
% Let me verify this by adding constraints.

% Check if option A is forced: can Juana be on red?
% Let's see if there's a model where Juana is NOT on green.
% From previous output: Model 1 has juana on red, so A is not forced.

% Check if option B is forced: can Kelly be on green?
% Let's test by forcing Kelly on green.
:- not option_b_forced.

% Actually, let me use a cleaner approach. Let me just run separate checks.

% Remove all option checks and just show the models to verify.
#show assigned/2.
#show facilitator/1.