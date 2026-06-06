% Domain facts
chapter(1). chapter(2). chapter(3). chapter(4). chapter(5). chapter(6). chapter(7).
clue(r). clue(s). clue(t). clue(u). clue(w). clue(x). clue(z).

% Each clue appears exactly once
1 { pos(C, Ch) : chapter(Ch) } 1 :- clue(C).
1 { pos(C, Ch) : clue(C) } 1 :- chapter(Ch).

% U is in chapter 3
pos(u,3).

% Constraints
% T not in chapter 1
:- pos(t,1).

% T before W with exactly two chapters between
:- pos(t, TCh), pos(w, WCh), WCh != TCh + 3.
:- pos(t, TCh), TCh > 4.

% S and Z not adjacent
:- pos(s, SCh), pos(z, ZCh), SCh = ZCh + 1.
:- pos(s, SCh), pos(z, ZCh), ZCh = SCh + 1.

% W and X not adjacent
:- pos(w, WCh), pos(x, XCh), WCh = XCh + 1.
:- pos(w, WCh), pos(x, XCh), XCh = WCh + 1.

% U and X adjacent
:- pos(u, UCh), pos(x, XCh), UCh = XCh + 1.
:- pos(u, UCh), pos(x, XCh), XCh = UCh + 1.

% Options
option(a) :- pos(r,1).
option(b) :- pos(r,5).
option(c) :- pos(s,7).
option(d) :- pos(w,6).
option(e) :- pos(x,4).

% Exactly one option true
1 { option(a); option(b); option(c); option(d); option(e) } 1.

#show option/1.