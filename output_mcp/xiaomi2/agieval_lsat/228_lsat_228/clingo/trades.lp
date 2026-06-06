% Time steps
max_time(4).
time(0..4).

% Buildings
building(garza).
building(yates).
building(zimmer).
building(flores).
building(lynch).
building(king).
building(meyer).
building(ortiz).

% Classes
class(garza,1).
class(yates,3).
class(zimmer,3).
class(flores,1).
class(lynch,2).
class(king,2).
class(meyer,2).
class(ortiz,2).

% Companies
company(realprop).
company(southco).
company(trustcorp).

% Initial ownership at time 0
owns(realprop, garza, 0).
owns(realprop, yates, 0).
owns(realprop, zimmer, 0).
owns(southco, flores, 0).
owns(southco, lynch, 0).
owns(trustcorp, king, 0).
owns(trustcorp, meyer, 0).
owns(trustcorp, ortiz, 0).

% Generate possible trades
possible_trade1(C1,C2,B1,B2,T) :- 
    company(C1), company(C2), C1 != C2,
    building(B1), building(B2), B1 != B2,
    class(B1,K), class(B2,K),
    time(T), T < 4.

possible_trade2(C1,C2,B1,B2a,B2b,T) :- 
    company(C1), company(C2), C1 != C2,
    building(B1), class(B1,1),
    building(B2a), class(B2a,2),
    building(B2b), class(B2b,2), B2a != B2b,
    time(T), T < 4.

possible_trade3(C1,C2,B1,B2a,B2b,T) :- 
    company(C1), company(C2), C1 != C2,
    building(B1), class(B1,2),
    building(B2a), class(B2a,3),
    building(B2b), class(B2b,3), B2a != B2b,
    time(T), T < 4.

% Choose exactly one action per time step (including noop)
1 { 
    noop(T) ; 
    trade1(C1,C2,B1,B2,T) : possible_trade1(C1,C2,B1,B2,T) ; 
    trade2(C1,C2,B1,B2a,B2b,T) : possible_trade2(C1,C2,B1,B2a,B2b,T) ; 
    trade3(C1,C2,B1,B2a,B2b,T) : possible_trade3(C1,C2,B1,B2a,B2b,T) 
} 1 :- time(T), T < 4.

% Preconditions: companies must own the buildings they give
:- trade1(C1,C2,B1,B2,T), not owns(C1,B1,T).
:- trade1(C1,C2,B1,B2,T), not owns(C2,B2,T).
:- trade2(C1,C2,B1,B2a,B2b,T), not owns(C1,B1,T).
:- trade2(C1,C2,B1,B2a,B2b,T), not owns(C2,B2a,T).
:- trade2(C1,C2,B1,B2a,B2b,T), not owns(C2,B2b,T).
:- trade3(C1,C2,B1,B2a,B2b,T), not owns(C1,B1,T).
:- trade3(C1,C2,B1,B2a,B2b,T), not owns(C2,B2a,T).
:- trade3(C1,C2,B1,B2a,B2b,T), not owns(C2,B2b,T).

% Mark buildings whose ownership changes
changed_ownership(B,T) :- trade1(_,_,B,_,T).
changed_ownership(B,T) :- trade1(_,_,_,B,T).
changed_ownership(B,T) :- trade2(_,_,B,_,_,T).
changed_ownership(B,T) :- trade2(_,_,_,B,_,T).
changed_ownership(B,T) :- trade2(_,_,_,_,B,T).
changed_ownership(B,T) :- trade3(_,_,B,_,_,T).
changed_ownership(B,T) :- trade3(_,_,_,B,_,T).
changed_ownership(B,T) :- trade3(_,_,_,_,B,T).

% Frame axiom: ownership persists if not changed
owns(C,B,T+1) :- owns(C,B,T), time(T+1), not changed_ownership(B,T).

% Effects of trades
% Type1: swap
owns(C1,B2,T+1) :- trade1(C1,C2,B1,B2,T).
owns(C2,B1,T+1) :- trade1(C1,C2,B1,B2,T).

% Type2: C1 gives class1, gets two class2; C2 gives two class2, gets class1
owns(C1,B2a,T+1) :- trade2(C1,C2,B1,B2a,B2b,T).
owns(C1,B2b,T+1) :- trade2(C1,C2,B1,B2a,B2b,T).
owns(C2,B1,T+1) :- trade2(C1,C2,B1,B2a,B2b,T).

% Type3: C1 gives class2, gets two class3; C2 gives two class3, gets class2
owns(C1,B2a,T+1) :- trade3(C1,C2,B1,B2a,B2b,T).
owns(C1,B2b,T+1) :- trade3(C1,C2,B1,B2a,B2b,T).
owns(C2,B1,T+1) :- trade3(C1,C2,B1,B2a,B2b,T).

% Final condition: RealProp owns only class 2 buildings at time 4
realprop_has_non_class2 :- owns(realprop, B, 4), class(B, K), K != 2.
:- realprop_has_non_class2.

% Define answer choices at final time
choice_a :- owns(trustcorp, B, 4), class(B,1).
choice_b :- owns(trustcorp, meyer, 4).
choice_c :- owns(southco, B, 4), class(B,2).
choice_d :- owns(southco, yates, 4), owns(southco, zimmer, 4).
choice_e :- owns(southco, flores, 4).

% We want to see which choices are true in all models.
% We'll output them conditionally.
option(a) :- choice_a.
option(b) :- choice_b.
option(c) :- choice_c.
option(d) :- choice_d.
option(e) :- choice_e.

#show option/1.