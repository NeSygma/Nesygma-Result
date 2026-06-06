% Domains and basic facts
art_historian(farley).
art_historian(garcia).
art_historian(holden).
art_historian(jiang).

topic(lithographs).
topic(oil_paintings).
topic(sculptures).
topic(watercolors).

% Lecture positions (1st to 4th)
position(1..4).

% Assign each lecture to a unique art historian and topic
% Each position has exactly one art historian and one topic
1 { assigned_art_historian(P, H) : art_historian(H) } 1 :- position(P).
1 { assigned_topic(P, T) : topic(T) } 1 :- position(P).

% Ensure each art historian gives exactly one lecture
:- art_historian(H), #count { P : assigned_art_historian(P, H) } != 1.

% Ensure each topic is covered exactly once
:- topic(T), #count { P : assigned_topic(P, T) } != 1.

% Constraints from the problem statement

% 1. The oil paintings lecture and the watercolors lecture must both be earlier than the lithographs lecture.
% Ensure oil_paintings and watercolors are before lithographs
:- assigned_topic(P1, oil_paintings), assigned_topic(P2, lithographs), P1 >= P2.
:- assigned_topic(P1, watercolors), assigned_topic(P2, lithographs), P1 >= P2.

% 2. Farley's lecture must be earlier than the oil paintings lecture.
:- assigned_art_historian(P1, farley), assigned_topic(P2, oil_paintings), P1 >= P2.

% 3. Holden's lecture must be earlier than both Garcia's lecture and Jiang's lecture.
:- assigned_art_historian(P1, holden), assigned_art_historian(P2, garcia), P1 >= P2.
:- assigned_art_historian(P1, holden), assigned_art_historian(P2, jiang), P1 >= P2.

% Additional constraint: The watercolors lecture is third
:- assigned_topic(3, T), T != watercolors.

% Map the correct answer to option/1 (MANDATORY)
% (A) Farley gives the watercolors lecture.
option(a) :- assigned_art_historian(3, farley).

% (B) Garcia gives the oil paintings lecture.
option(b) :- assigned_art_historian(P, garcia), assigned_topic(P, oil_paintings).

% (C) Garcia gives the sculptures lecture.
option(c) :- assigned_art_historian(P, garcia), assigned_topic(P, sculptures).

% (D) Holden gives the sculptures lecture.
option(d) :- assigned_art_historian(P, holden), assigned_topic(P, sculptures).

% (E) Jiang gives the lithographs lecture.
option(e) :- assigned_art_historian(P, jiang), assigned_topic(P, lithographs).

% Ensure only one option is true at a time
:- option(X), option(Y), X != Y.

% Show all option atoms explicitly
#show option/1.
#show assigned_art_historian/2.
#show assigned_topic/2.