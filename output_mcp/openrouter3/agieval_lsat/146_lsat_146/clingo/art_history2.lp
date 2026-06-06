% Domain declarations
time(1..4).
historian(farley). historian(garcia). historian(holden). historian(jiang).
topic(lithographs). topic(oil_paintings). topic(sculptures). topic(watercolors).

% Assignment: historian gives topic at time
{ assign(H, T, Topic) } :- historian(H), time(T), topic(Topic).

% Each historian gives exactly one lecture at exactly one time
1 { assign(H, T, Topic) : time(T), topic(Topic) } 1 :- historian(H).
% Each time slot has exactly one historian giving one topic
1 { assign(H, T, Topic) : historian(H), topic(Topic) } 1 :- time(T).
% Each topic is given exactly once
1 { assign(H, T, Topic) : historian(H), time(T) } 1 :- topic(Topic).

% Watercolors lecture is third
:- assign(_, 3, Topic), Topic != watercolors.

% Helper predicates
oil_time(T) :- assign(_, T, oil_paintings).
water_time(T) :- assign(_, T, watercolors).
litho_time(T) :- assign(_, T, lithographs).
farley_time(T) :- assign(farley, T, _).
holden_time(T) :- assign(holden, T, _).
garcia_time(T) :- assign(garcia, T, _).
jiang_time(T) :- assign(jiang, T, _).

% Constraint 1: Oil paintings and watercolors must both be earlier than lithographs
:- oil_time(O), litho_time(L), O >= L.
:- water_time(W), litho_time(L), W >= L.

% Constraint 2: Farley's lecture must be earlier than oil paintings lecture
:- farley_time(F), oil_time(O), F >= O.

% Constraint 3: Holden's lecture must be earlier than both Garcia's and Jiang's lectures
:- holden_time(H), garcia_time(G), H >= G.
:- holden_time(H), jiang_time(J), H >= J.

% Map the correct answer to option/1 (MANDATORY)
% Option A: Farley gives the watercolors lecture
option(a) :- assign(farley, 3, watercolors).

% Option B: Garcia gives the oil paintings lecture
option(b) :- assign(garcia, _, oil_paintings).

% Option C: Garcia gives the sculptures lecture
option(c) :- assign(garcia, _, sculptures).

% Option D: Holden gives the sculptures lecture
option(d) :- assign(holden, _, sculptures).

% Option E: Jiang gives the lithographs lecture
option(e) :- assign(jiang, _, lithographs).

#show option/1.