% Historians and topics
historian(farley). historian(garcia). historian(holden). historian(jiang).
topic(lithographs). topic(oil_paintings). topic(sculptures). topic(watercolors).
time(1..4).

% Each historian gives exactly one lecture
1 { assigned(H, T) : time(T) } 1 :- historian(H).

% Each time slot has exactly one historian
1 { assigned(H, T) : historian(H) } 1 :- time(T).

% Each topic is given exactly once
1 { topic_at(T, Topic) : time(T) } 1 :- topic(Topic).
1 { topic_at(T, Topic) : topic(Topic) } 1 :- time(T).

% Lithographs must be at time 4 (since it needs at least 3 slots before it for oil, watercolors, and one more)
:- topic_at(T, lithographs), T != 4.

% Oil paintings and watercolors must be earlier than lithographs (time 4)
:- topic_at(T_oil, oil_paintings), T_oil >= 4.
:- topic_at(T_water, watercolors), T_water >= 4.

% Farley's lecture must be earlier than oil paintings
:- assigned(farley, T_farley), topic_at(T_oil, oil_paintings), T_farley >= T_oil.

% Holden's lecture must be earlier than Garcia's and Jiang's
:- assigned(holden, T_holden), assigned(garcia, T_garcia), T_holden >= T_garcia.
:- assigned(holden, T_holden), assigned(jiang, T_jiang), T_holden >= T_jiang.

% Derive topic assignments for each historian
has_topic(H, Topic) :- assigned(H, T), topic_at(T, Topic).

% Holden must be before lithographs (since lithographs is at time 4 and Holden is at time 1-3)
holden_before_lithographs :- assigned(holden, T), T < 4.

% Farley must be before oil paintings
farley_before_oil :- assigned(farley, T_farley), topic_at(T_oil, oil_paintings), T_farley < T_oil.

% Watercolors must be before lithographs (already enforced by topic_at(T_water, watercolors), T_water < 4)
watercolors_before_lithographs :- topic_at(T_water, watercolors), T_water < 4.

% Map the correct answer to option/1 (MANDATORY)
% (A) Farley's lecture is earlier than the sculptures lecture.
option(a) :- assigned(farley, T_farley), topic_at(T_sculptures, sculptures), T_farley < T_sculptures.

% (B) Holden's lecture is earlier than the lithographs lecture.
option(b) :- holden_before_lithographs.

% (C) The sculptures lecture is earlier than Garcia's lecture.
option(c) :- topic_at(T_sculptures, sculptures), assigned(garcia, T_garcia), T_sculptures < T_garcia.

% (D) The sculptures lecture is earlier than Jiang's lecture.
option(d) :- topic_at(T_sculptures, sculptures), assigned(jiang, T_jiang), T_sculptures < T_jiang.

% (E) The watercolors lecture is earlier than Garcia's lecture.
option(e) :- topic_at(T_water, watercolors), assigned(garcia, T_garcia), T_water < T_garcia.

#show option/1.