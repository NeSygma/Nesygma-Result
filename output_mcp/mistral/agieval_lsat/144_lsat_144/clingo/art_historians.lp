% Domains
time(1..4).
historian(farley; garcia; holden; jiang).
topic(lithographs; oil_paintings; sculptures; watercolors).

% Schedule: exactly one lecture per historian, topic, and time
1 { lecture(H, T, Time) : topic(T), time(Time) } 1 :- historian(H).
1 { lecture(H, T, Time) : historian(H), time(Time) } 1 :- topic(T).
1 { lecture(H, T, Time) : historian(H), topic(T) } 1 :- time(Time).

% Helper predicates for times
oil_time(T) :- lecture(_, oil_paintings, T).
water_time(T) :- lecture(_, watercolors, T).
litho_time(T) :- lecture(_, lithographs, T).
farley_time(T) :- lecture(farley, _, T).
holden_time(T) :- lecture(holden, _, T).
garcia_time(T) :- lecture(garcia, _, T).
jiang_time(T) :- lecture(jiang, _, T).

% Constraints
% 1. Oil paintings and watercolors must be earlier than lithographs
:- oil_time(T_oil), litho_time(T_litho), T_oil >= T_litho.
:- water_time(T_water), litho_time(T_litho), T_water >= T_litho.

% 2. Farley's lecture must be earlier than oil paintings
:- farley_time(T_farley), oil_time(T_oil), T_farley >= T_oil.

% 3. Holden's lecture must be earlier than Garcia's and Jiang's
:- holden_time(T_holden), garcia_time(T_garcia), T_holden >= T_garcia.
:- holden_time(T_holden), jiang_time(T_jiang), T_holden >= T_jiang.

% Define the answer choices
% Choice A: Farley: sculptures; Holden: lithographs; Garcia: oil paintings; Jiang: watercolors
:- not lecture(farley, sculptures, 1), answer(a).
:- not lecture(holden, lithographs, 2), answer(a).
:- not lecture(garcia, oil_paintings, 3), answer(a).
:- not lecture(jiang, watercolors, 4), answer(a).

% Choice B: Farley: watercolors; Jiang: oil paintings; Holden: sculptures; Garcia: lithographs
:- not lecture(farley, watercolors, 1), answer(b).
:- not lecture(jiang, oil_paintings, 2), answer(b).
:- not lecture(holden, sculptures, 3), answer(b).
:- not lecture(garcia, lithographs, 4), answer(b).

% Choice C: Garcia: sculptures; Farley: watercolors; Holden: oil paintings; Jiang: lithographs
:- not lecture(garcia, sculptures, 1), answer(c).
:- not lecture(farley, watercolors, 2), answer(c).
:- not lecture(holden, oil_paintings, 3), answer(c).
:- not lecture(jiang, lithographs, 4), answer(c).

% Choice D: Holden: oil paintings; Jiang: watercolors; Farley: lithographs; Garcia: sculptures
:- not lecture(holden, oil_paintings, 1), answer(d).
:- not lecture(jiang, watercolors, 2), answer(d).
:- not lecture(farley, lithographs, 3), answer(d).
:- not lecture(garcia, sculptures, 4), answer(d).

% Choice E: Holden: sculptures; Farley: watercolors; Jiang: oil paintings; Garcia: lithographs
:- not lecture(holden, sculptures, 1), answer(e).
:- not lecture(farley, watercolors, 2), answer(e).
:- not lecture(jiang, oil_paintings, 3), answer(e).
:- not lecture(garcia, lithographs, 4), answer(e).

% Exactly one answer is correct
1 { answer(a; b; c; d; e) } 1.

% Map to option/1 as required
option(a) :- answer(a).
option(b) :- answer(b).
option(c) :- answer(c).
option(d) :- answer(d).
option(e) :- answer(e).

#show option/1.