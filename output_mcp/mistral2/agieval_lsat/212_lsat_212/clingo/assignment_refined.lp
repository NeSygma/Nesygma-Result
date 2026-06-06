% Base facts: students and teams
student(juana).
student(kelly).
student(lateefah).
student(mei).
student(olga).
team(green).
team(red).

% Assign each student to exactly one team
1 { assigned_to(S, T) : team(T) } 1 :- student(S).

% Lateefah is assigned to the green team
:- not assigned_to(lateefah, green).

% Juana is assigned to a different team than Olga
:- assigned_to(juana, T), assigned_to(olga, T), team(T).

% Team sizes: one team has 2 members, the other has 3
:- { assigned_to(S, green) : student(S) } != 2, { assigned_to(S, green) : student(S) } != 3.
:- { assigned_to(S, red) : student(S) } != 2, { assigned_to(S, red) : student(S) } != 3.
:- { assigned_to(S, green) : student(S) } = 2, { assigned_to(S, red) : student(S) } = 2.
:- { assigned_to(S, green) : student(S) } = 3, { assigned_to(S, red) : student(S) } = 3.

% Facilitator assignment: exactly one facilitator per team
1 { facilitator(S, T) : student(S) } 1 :- team(T).

% Kelly is not a facilitator
:- facilitator(kelly, _).

% Olga is a facilitator
:- not facilitator(olga, _).

% Facilitator must be a member of the team they facilitate
:- facilitator(S, T), not assigned_to(S, T).

% If Mei is assigned to the green team, derive the answer
mei_green :- assigned_to(mei, green).

% Define the conditions for each option
% (A) Juana is assigned to the green team.
option_a_holds :- mei_green, assigned_to(juana, green).

% (B) Kelly is assigned to the red team.
option_b_holds :- mei_green, assigned_to(kelly, red).

% (C) Olga is assigned to the green team.
option_c_holds :- mei_green, assigned_to(olga, green).

% (D) Lateefah is a facilitator.
option_d_holds :- mei_green, facilitator(lateefah, _).

% (E) Mei is a facilitator.
option_e_holds :- mei_green, facilitator(mei, _).

% Ensure only one option can be true when mei_green holds
:- mei_green, option_a_holds, option_b_holds.
:- mei_green, option_a_holds, option_c_holds.
:- mei_green, option_a_holds, option_d_holds.
:- mei_green, option_a_holds, option_e_holds.
:- mei_green, option_b_holds, option_c_holds.
:- mei_green, option_b_holds, option_d_holds.
:- mei_green, option_b_holds, option_e_holds.
:- mei_green, option_c_holds, option_d_holds.
:- mei_green, option_c_holds, option_e_holds.
:- mei_green, option_d_holds, option_e_holds.

% Map the correct answer to option/1
option(a) :- option_a_holds.
option(b) :- option_b_holds.
option(c) :- option_c_holds.
option(d) :- option_d_holds.
option(e) :- option_e_holds.

#show option/1.