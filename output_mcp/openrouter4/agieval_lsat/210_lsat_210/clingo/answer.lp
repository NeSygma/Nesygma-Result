% --- Base problem encoding ---

% Students
student(juana; kelly; lateefah; mei; olga).

% Teams
team(green; red).

% Each student assigned to exactly one team
{ assigned(S, T) : team(T) } 1 :- student(S).

% Team sizes: one team has 2, the other has 3
size(T, N) :- N = #count{ S : assigned(S, T) }, team(T).
:- size(green, N1), size(red, N2), N1 + N2 != 5.
:- size(_, N), N < 2.
:- size(_, N), N > 3.
:- size(green, N), size(red, N).

% Each team has exactly one facilitator
1 { facilitator(S) : student(S), assigned(S, T) } 1 :- team(T).

% Juana and Olga are on different teams
:- assigned(juana, T), assigned(olga, T).

% Lateefah is on green team
assigned(lateefah, green).

% Kelly is not a facilitator
:- facilitator(kelly).

% Olga is a facilitator
facilitator(olga).

% --- Option definitions ---

% Option A: Lateefah is facilitator, same team as Kelly
option_a_true :- facilitator(lateefah), assigned(lateefah, T), assigned(kelly, T).

% Option B: Mei is facilitator, same team as Kelly
option_b_true :- facilitator(mei), assigned(mei, T), assigned(kelly, T).

% Option C: Olga is facilitator, same team as Mei
option_c_true :- assigned(olga, T), assigned(mei, T).

% Option D: Lateefah is facilitator, different team than Juana
option_d_true :- facilitator(lateefah), assigned(lateefah, T1), assigned(juana, T2), T1 != T2.

% Option E: Mei is facilitator, different team than Olga
option_e_true :- facilitator(mei), assigned(mei, T1), assigned(olga, T2), T1 != T2.

% --- Determine which option must be false ---
% An option "must be false" if there is NO valid assignment where it is true.
% We test each option by forcing it to be true and checking for unsatisfiability.

% Use a disjunction to try each option in turn
% We create 5 scenarios: test_a, test_b, test_c, test_d, test_e
% In each scenario, we force the corresponding option to be true.

{ test_a; test_b; test_c; test_d; test_e }.

% Cannot test more than one at a time (to isolate)
:- 2 { test_a; test_b; test_c; test_d; test_e }.

% Must test at least one
1 { test_a; test_b; test_c; test_d; test_e }.

% Force the option to be true in its test scenario
:- test_a, not option_a_true.
:- test_b, not option_b_true.
:- test_c, not option_c_true.
:- test_d, not option_d_true.
:- test_e, not option_e_true.

% If a test scenario is unsatisfiable, that option must be false
% We can detect which scenarios are impossible by checking if they appear in any answer set
% Only possible scenarios will have answer sets.

% Map the answer
% The option that must be false is the one where the test scenario yields UNSAT
% Since UNSAT models are not returned, we can derive:
% option_d is the answer iff option_d_true cannot happen in any valid assignment

% Actually, a simpler approach: directly check which option is impossible
% We know from the problem that exactly one must be false.
% We can use the fact that option_d_true never appears in any answer set.

% Let me use a different strategy: collect which options are possible
possible_a :- option_a_true.
possible_b :- option_b_true.
possible_c :- option_c_true.
possible_d :- option_d_true.
possible_e :- option_e_true.

% Find the option that is NOT possible (must be false)
% This is the answer
option(a) :- not possible_a, possible_b, possible_c, possible_d, possible_e.
option(b) :- possible_a, not possible_b, possible_c, possible_d, possible_e.
option(c) :- possible_a, possible_b, not possible_c, possible_d, possible_e.
option(d) :- possible_a, possible_b, possible_c, not possible_d, possible_e.
option(e) :- possible_a, possible_b, possible_c, possible_d, not possible_e.

#show option/1.