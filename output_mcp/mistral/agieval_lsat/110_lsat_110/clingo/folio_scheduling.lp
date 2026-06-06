% Domain: articles and positions
article(g). article(h). article(j). article(q). article(r). article(s). article(y).
position(1..7).

% Topic assignments (facts)
finance(g). finance(h). finance(j).
nutrition(q). nutrition(r). nutrition(s).
wildlife(y).

% Each position has exactly one article
1 { position(Art, Pos) : article(Art) } 1 :- position(Pos).

% Each article appears in exactly one position
1 { position(Art, Pos) : position(Pos) } 1 :- article(Art).

% Y is fourth (given condition)
position(y, 4).

% Helper: Get topic of an article
topic(Art, finance) :- position(Art, _), finance(Art).
topic(Art, nutrition) :- position(Art, _), nutrition(Art).
topic(Art, wildlife) :- position(Art, _), wildlife(Art).

% Consecutive articles cannot cover the same topic
:- position(Art1, Pos), position(Art2, Pos+1), Pos < 7,
   topic(Art1, Topic), topic(Art2, Topic).

% S must be earlier than Y
:- position(s, PosS), position(y, PosY), PosS >= PosY.

% J must be earlier than G, and G must be earlier than R
:- position(j, PosJ), position(g, PosG), PosJ >= PosG.
:- position(g, PosG), position(r, PosR), PosG >= PosR.

% S can be earlier than Q only if Q is third
% This means: if S < Q, then Q must be 3
:- position(s, PosS), position(q, PosQ), PosS < PosQ, PosQ != 3.

% Map the correct answer to option/1 (MANDATORY)
% From our analysis, J must be second (option A)
option(a) :- position(j, 2).
option(b) :- position(j, 3).
option(c) :- position(q, 1).
option(d) :- position(q, 3).
option(e) :- position(r, 7).

#show option/1.