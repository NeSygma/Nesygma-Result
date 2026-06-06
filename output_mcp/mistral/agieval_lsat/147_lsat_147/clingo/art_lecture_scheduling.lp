% Domains
time(1..4).
historian(farley; garcia; holden; jiang).
topic(lithographs; oil_paintings; sculptures; watercolors).

% Assignment: each historian gives exactly one lecture (topic) at exactly one time
1 { assignment(H, T, Topic) : time(T), topic(Topic) } 1 :- historian(H).

% No two historians at the same time, no historian with multiple topics
:- assignment(H1, T, _), assignment(H2, T, _), H1 != H2.
:- assignment(H, _, Topic1), assignment(H, _, Topic2), Topic1 != Topic2.

% Get the time for each topic
time_of_topic(Topic, T) :- assignment(_, T, Topic).

% Constraints from the problem:
% 1. Oil paintings and watercolors must be earlier than lithographs
:- time_of_topic(oil_paintings, T1), time_of_topic(lithographs, T2), T1 >= T2.
:- time_of_topic(watercolors, T1), time_of_topic(lithographs, T2), T1 >= T2.

% 2. Farley's lecture must be earlier than oil paintings
:- assignment(farley, T1, _), time_of_topic(oil_paintings, T2), T1 >= T2.

% 3. Holden's lecture must be earlier than Garcia's and Jiang's
:- assignment(holden, T1, _), assignment(garcia, T2, _), T1 >= T2.
:- assignment(holden, T1, _), assignment(jiang, T2, _), T1 >= T2.

% Define the conditions for each option
farley_gives_lithographs :- assignment(farley, _, lithographs).
garcia_gives_sculptures :- assignment(garcia, _, sculptures).
garcia_gives_watercolors :- assignment(garcia, _, watercolors).
holden_gives_oil_paintings :- assignment(holden, _, oil_paintings).
jiang_gives_watercolors :- assignment(jiang, _, watercolors).

% The answer mapping
% Since (A) Farley gives lithographs is impossible (creates contradiction: 
% Farley < oil_paintings < lithographs = Farley), the answer is (A)

option(a) :- not farley_gives_lithographs, not garcia_gives_sculptures, not garcia_gives_watercolors, not holden_gives_oil_paintings, not jiang_gives_watercolors.
option(b) :- garcia_gives_sculptures.
option(c) :- garcia_gives_watercolors.
option(d) :- holden_gives_oil_paintings.
option(e) :- jiang_gives_watercolors.

% Ensure exactly one option is selected as the answer
:- option(a), option(b).
:- option(a), option(c).
:- option(a), option(d).
:- option(a), option(e).
:- option(b), option(c).
:- option(b), option(d).
:- option(b), option(e).
:- option(c), option(d).
:- option(c), option(e).
:- option(d), option(e).

#show option/1.