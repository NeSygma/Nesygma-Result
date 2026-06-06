% Art Historians and Lectures Scheduling

% Domains
person(farley). person(garcia). person(holden). person(jiang).
topic(lithographs). topic(oil). topic(sculptures). topic(watercolors).
position(1..4).

% Assign each person to exactly one topic
1 { person_topic(P, T) : topic(T) } 1 :- person(P).

% Assign each topic to exactly one position
1 { topic_position(T, Pos) : position(Pos) } 1 :- topic(T).

% Ensure each topic is assigned to exactly one person
1 { person_topic(P, T) : person(P) } 1 :- topic(T).

% Derive person's position from topic assignment
person_position(P, Pos) :- person_topic(P, T), topic_position(T, Pos).

% Constraints
% Oil and watercolors must be earlier than lithographs
:- topic_position(oil, PosOil), topic_position(lithographs, PosLith), PosOil >= PosLith.
:- topic_position(watercolors, PosWater), topic_position(lithographs, PosLith), PosWater >= PosLith.

% Farley's lecture must be earlier than oil paintings lecture
:- person_position(farley, PosF), topic_position(oil, PosOil), PosF >= PosOil.

% Holden's lecture must be earlier than both Garcia's and Jiang's lectures
:- person_position(holden, PosH), person_position(garcia, PosG), PosH >= PosG.
:- person_position(holden, PosH), person_position(jiang, PosJ), PosH >= PosJ.

% Given: Garcia gives the sculptures lecture
person_topic(garcia, sculptures).

% Evaluate the answer choices
% (A) The lithographs lecture is third.
option(a) :- topic_position(lithographs, 3).

% (B) The oil paintings lecture is third.
option(b) :- topic_position(oil, 3).

% (C) The sculptures lecture is first.
option(c) :- topic_position(sculptures, 1).

% (D) The sculptures lecture is second.
option(d) :- topic_position(sculptures, 2).

% (E) The watercolors lecture is second.
option(e) :- topic_position(watercolors, 2).

#show option/1.