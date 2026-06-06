% Paint facts
paint(franz, oil).
paint(franz, water).
paint(greene, oil).
paint(greene, water).
paint(hidalgo, oil).
paint(hidalgo, water).
paint(isaacs, oil).
paint(isaacs, water).

% Walls
wall(1..4).

% Each wall has exactly one upper painting
1 { upper(W,S,T) : paint(S,T) } 1 :- wall(W).
% Each wall has exactly one lower painting
1 { lower(W,S,T) : paint(S,T) } 1 :- wall(W).
% Each painting appears exactly once (either upper or lower)
1 { upper(W,S,T) : wall(W) ; lower(W,S,T) : wall(W) } 1 :- paint(S,T).

% No wall has only watercolors
:- upper(W,_,water), lower(W,_,water).
% No wall has only one student
:- upper(W,Student,_), lower(W,Student,_).
% No wall has both Franz and Isaacs
:- upper(W,franz,_), lower(W,isaacs,_).
:- upper(W,isaacs,_), lower(W,franz,_).

% Greene's watercolor is upper of wall where Franz's oil is lower
upper(W,greene,water) :- lower(W,franz,oil).
lower(W,franz,oil) :- upper(W,greene,water).
% Greene's watercolor not lower
:- lower(W,greene,water).

% Isaacs's oil lower wall 4
lower(4,isaacs,oil).

% Option selection (exactly one)
1 { option(a); option(b); option(c); option(d); option(e) } 1.

% Option A constraints
lower(1,franz,oil) :- option(a).
lower(2,franz,water) :- option(a).
lower(3,greene,oil) :- option(a).
lower(4,isaacs,oil) :- option(a).

% Option B constraints
lower(1,franz,oil) :- option(b).
lower(2,hidalgo,water) :- option(b).
lower(3,isaacs,water) :- option(b).
lower(4,isaacs,oil) :- option(b).

% Option C constraints
lower(1,greene,oil) :- option(c).
lower(2,franz,oil) :- option(c).
lower(3,isaacs,oil) :- option(c).
lower(4,hidalgo,oil) :- option(c).

% Option D constraints
lower(1,hidalgo,oil) :- option(d).
lower(2,greene,oil) :- option(d).
lower(3,greene,water) :- option(d).
lower(4,isaacs,oil) :- option(d).

% Option E constraints
lower(1,hidalgo,water) :- option(e).
lower(2,franz,oil) :- option(e).
lower(3,greene,oil) :- option(e).
lower(4,isaacs,oil) :- option(e).

#show option/1.