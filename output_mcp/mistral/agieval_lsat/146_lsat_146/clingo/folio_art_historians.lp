% Domains
time(1..4).
historian(farley; garcia; holden; jiang).
topic(lithographs; oil_paintings; sculptures; watercolors).

% Assignments: Each historian is assigned to exactly one time slot, and each topic is assigned to exactly one time slot.
1 { assigned_historian(H, T) : time(T) } 1 :- historian(H).
1 { assigned_topic(Topic, T) : time(T) } 1 :- topic(Topic).

% Ensure no two historians are assigned to the same time slot
:- time(T), historian(H1), historian(H2), H1 != H2, assigned_historian(H1, T), assigned_historian(H2, T).

% Ensure no two topics are assigned to the same time slot
:- time(T), topic(Topic1), topic(Topic2), Topic1 != Topic2, assigned_topic(Topic1, T), assigned_topic(Topic2, T).

% Problem constraints
% 1. Oil paintings and watercolors must be earlier than lithographs
:- assigned_topic(oil_paintings, T1), assigned_topic(lithographs, T2), T1 >= T2.
:- assigned_topic(watercolors, T1), assigned_topic(lithographs, T2), T1 >= T2.

% 2. Farley's lecture must be earlier than oil paintings
:- assigned_historian(farley, T1), assigned_topic(oil_paintings, T2), T1 >= T2.

% 3. Holden's lecture must be earlier than Garcia's and Jiang's
:- assigned_historian(holden, T1), assigned_historian(garcia, T2), T1 >= T2.
:- assigned_historian(holden, T1), assigned_historian(jiang, T2), T1 >= T2.

% 4. Watercolors is third
:- not assigned_topic(watercolors, 3).

% Derive which options are possible
% A: Farley gives the watercolors lecture (at time 3)
option_a :- assigned_historian(farley, 3).

% B: Garcia gives the oil paintings lecture
option_b :- assigned_historian(garcia, T), assigned_topic(oil_paintings, T).

% C: Garcia gives the sculptures lecture
option_c :- assigned_historian(garcia, T), assigned_topic(sculptures, T).

% D: Holden gives the sculptures lecture
option_d :- assigned_historian(holden, T), assigned_topic(sculptures, T).

% E: Jiang gives the lithographs lecture
option_e :- assigned_historian(jiang, T), assigned_topic(lithographs, T).

% Map to option/1 (only one can be true in a valid model)
option(a) :- option_a, not option_b, not option_c, not option_d, not option_e.
option(b) :- option_b, not option_a, not option_c, not option_d, not option_e.
option(c) :- option_c, not option_a, not option_b, not option_d, not option_e.
option(d) :- option_d, not option_a, not option_b, not option_c, not option_e.
option(e) :- option_e, not option_a, not option_b, not option_c, not option_d.

% Show the final answer
#show option/1.