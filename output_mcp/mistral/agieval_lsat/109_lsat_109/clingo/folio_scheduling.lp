% Define which option we're considering
option(a). option(b). option(c). option(d). option(e).

% Define the articles and their topics
article(g; h; j; q; r; s; y).
topic(g, finance; h, finance; j, finance).
topic(q, nutrition; r, nutrition; s, nutrition).
topic(y, wildlife).

% Define the sequence positions
position(1..7).

% Assign articles to positions for each option
% Option A: H, S, J, Q, Y, G, R
assigned(h, 1) :- option(a).
assigned(s, 2) :- option(a).
assigned(j, 3) :- option(a).
assigned(q, 4) :- option(a).
assigned(y, 5) :- option(a).
assigned(g, 6) :- option(a).
assigned(r, 7) :- option(a).

% Option B: J, Q, G, H, S, Y, R
assigned(j, 1) :- option(b).
assigned(q, 2) :- option(b).
assigned(g, 3) :- option(b).
assigned(h, 4) :- option(b).
assigned(s, 5) :- option(b).
assigned(y, 6) :- option(b).
assigned(r, 7) :- option(b).

% Option C: Q, J, S, H, Y, G, R
assigned(q, 1) :- option(c).
assigned(j, 2) :- option(c).
assigned(s, 3) :- option(c).
assigned(h, 4) :- option(c).
assigned(y, 5) :- option(c).
assigned(g, 6) :- option(c).
assigned(r, 7) :- option(c).

% Option D: Q, J, Y, S, G, R, H
assigned(q, 1) :- option(d).
assigned(j, 2) :- option(d).
assigned(y, 3) :- option(d).
assigned(s, 4) :- option(d).
assigned(g, 5) :- option(d).
assigned(r, 6) :- option(d).
assigned(h, 7) :- option(d).

% Option E: S, G, Q, J, Y, R, H
assigned(s, 1) :- option(e).
assigned(g, 2) :- option(e).
assigned(q, 3) :- option(e).
assigned(j, 4) :- option(e).
assigned(y, 5) :- option(e).
assigned(r, 6) :- option(e).
assigned(h, 7) :- option(e).

% Consecutive articles cannot cover the same topic
:- option(Opt),
   position(Pos), Pos < 7,
   assigned(Art1, Pos), assigned(Art2, Pos+1),
   topic(Art1, Topic), topic(Art2, Topic).

% S can be earlier than Q only if Q is third
:- option(Opt),
   assigned(s, PosS), assigned(q, PosQ),
   PosS < PosQ, PosQ != 3.

% S must be earlier than Y
:- option(Opt),
   assigned(s, PosS), assigned(y, PosY),
   PosS >= PosY.

% J must be earlier than G
:- option(Opt),
   assigned(j, PosJ), assigned(g, PosG),
   PosJ >= PosG.

% G must be earlier than R
:- option(Opt),
   assigned(g, PosG), assigned(r, PosR),
   PosG >= PosR.

% Map the correct answer to option/1
answer(a) :- option(a), not invalid(a).
answer(b) :- option(b), not invalid(b).
answer(c) :- option(c), not invalid(c).
answer(d) :- option(d), not invalid(d).
answer(e) :- option(e), not invalid(e).

% Check if an option is invalid (violates constraints)
invalid(a) :- option(a),
    ( % Consecutive same topic
      position(Pos), Pos < 7,
      assigned(Art1, Pos), assigned(Art2, Pos+1),
      topic(Art1, Topic), topic(Art2, Topic)
    ;
      % S before Q without Q at position 3
      assigned(s, PosS), assigned(q, PosQ), PosS < PosQ, PosQ != 3
    ;
      % S not before Y
      assigned(s, PosS), assigned(y, PosY), PosS >= PosY
    ;
      % J not before G
      assigned(j, PosJ), assigned(g, PosG), PosJ >= PosG
    ;
      % G not before R
      assigned(g, PosG), assigned(r, PosR), PosG >= PosR
    ).

#show answer/1.