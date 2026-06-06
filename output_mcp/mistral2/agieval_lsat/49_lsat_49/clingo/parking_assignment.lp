% Define the employees and parking spaces.
employee(robertson).
employee(souza).
employee(togowa).
employee(vaughn).
employee(xu).
employee(young).

parking_space(1..6).

% Assign exactly one parking space to each employee.
1 { assigned(E, S) : parking_space(S) } 1 :- employee(E).

% Ensure no two employees share the same parking space.
:- assigned(E1, S), assigned(E2, S), E1 != E2.

% Constraints from the problem statement:
% 1. Young must be assigned a higher-numbered parking space than Togowa.
:- assigned(togowa, S1), assigned(young, S2), S2 <= S1.

% 2. Xu must be assigned a higher-numbered parking space than Souza.
:- assigned(souza, S1), assigned(xu, S2), S2 <= S1.

% 3. Robertson must be assigned a higher-numbered parking space than Young.
:- assigned(young, S1), assigned(robertson, S2), S2 <= S1.

% 4. Robertson must be assigned parking space #1, #2, #3, or #4.
:- assigned(robertson, S), S > 4.

% Helper predicate: Togowa is assigned a higher-numbered parking space than Souza.
togowa_greater_souza :- assigned(togowa, S1), assigned(souza, S2), S1 > S2.

% Condition: Togowa is assigned a higher-numbered parking space than Souza.
condition :- togowas_greater_souza.

% Define the answer choices as possible scenarios under the condition that Togowa > Souza.
% (A) Young is assigned parking space #2.
answer_a :- assigned(young, 2), condition.

% (B) Vaughn is assigned parking space #5.
answer_b :- assigned(vaughn, 5), condition.

% (C) Togowa is assigned parking space #3.
answer_c :- assigned(togowa, 3), condition.

% (D) Souza is assigned parking space #2.
answer_d :- assigned(souza, 2), condition.

% (E) Robertson is assigned parking space #3.
answer_e :- assigned(robertson, 3), condition.

% Map the correct answer to option/1.
option(a) :- answer_a.
option(b) :- answer_b.
option(c) :- answer_c.
option(d) :- answer_d.
option(e) :- answer_e.

% Sentinel atom to confirm the existence of a solution.
solution_exists :- option(_).

#show option/1.
#show solution_exists/0.