% Domains
building(garza; yates; zimmer; flores; lynch; king; meyer; ortiz).
company(realprop; southco; trustcorp).
class(1;2;3).

% Class of each building
class(garza,1).
class(yates,3).
class(zimmer,3).
class(flores,1).
class(lynch,2).
class(king,2).
class(meyer,2).
class(ortiz,2).

% Time steps
max_time(10).
time(0..max_time).

% Initial ownership at time 0
owner(garza, realprop, 0).
owner(yates, realprop, 0).
owner(zimmer, realprop, 0).
owner(flores, southco, 0).
owner(lynch, southco, 0).
owner(king, trustcorp, 0).
owner(meyer, trustcorp, 0).
owner(ortiz, trustcorp, 0).

% Each building owned by exactly one company at each time
1 { owner(B, C, T) : company(C) } 1 :- building(B), time(T).

% Trade actions (choice rules)
% Type 1: swap one building of same class between A and B
{ trade1(A,B,X,Y,T) : building(X), building(Y), X != Y, class(X,C), class(Y,C), owner(X,A,T), owner(Y,B,T) } 1 :- 
    company(A), company(B), A != B, time(T), T < max_time.

% Type 2: A gives one class1 building to B, receives two class2 buildings from B
{ trade2(A,B,X,Y,Z,T) : building(X), class(X,1), owner(X,A,T), building(Y), class(Y,2), owner(Y,B,T), building(Z), class(Z,2), owner(Z,B,T), Y != Z } 1 :- 
    company(A), company(B), A != B, time(T), T < max_time.

% Type 3: A gives one class2 building to B, receives two class3 buildings from B
{ trade3(A,B,X,Y,Z,T) : building(X), class(X,2), owner(X,A,T), building(Y), class(Y,3), owner(Y,B,T), building(Z), class(Z,3), owner(Z,B,T), Y != Z } 1 :- 
    company(A), company(B), A != B, time(T), T < max_time.

% At most one trade per time step
occurs(T) :- trade1(_,_,_,_,T).
occurs(T) :- trade2(_,_,_,_,_,T).
occurs(T) :- trade3(_,_,_,_,_,T).
:- time(T), T < max_time, 2 { occurs(T) }.

% Frame axiom: ownership persists if not changed
changed(B, T) :- trade1(_,_,B,_,T).
changed(B, T) :- trade1(_,_,_,B,T).
changed(B, T) :- trade2(_,_,B,_,_,T).
changed(B, T) :- trade2(_,_,_,B,_,T).
changed(B, T) :- trade2(_,_,_,_,B,T).
changed(B, T) :- trade3(_,_,B,_,_,T).
changed(B, T) :- trade3(_,_,_,B,_,T).
changed(B, T) :- trade3(_,_,_,_,B,T).

owner(B, C, T+1) :- owner(B, C, T), time(T+1), not changed(B, T).

% Effects of trades
% Type 1: swap X and Y
owner(X, B, T+1) :- trade1(A,B,X,Y,T).
owner(Y, A, T+1) :- trade1(A,B,X,Y,T).

% Type 2: X from A to B, Y and Z from B to A
owner(X, B, T+1) :- trade2(A,B,X,Y,Z,T).
owner(Y, A, T+1) :- trade2(A,B,X,Y,Z,T).
owner(Z, A, T+1) :- trade2(A,B,X,Y,Z,T).

% Type 3: X from A to B, Y and Z from B to A
owner(X, B, T+1) :- trade3(A,B,X,Y,Z,T).
owner(Y, A, T+1) :- trade3(A,B,X,Y,Z,T).
owner(Z, A, T+1) :- trade3(A,B,X,Y,Z,T).

% Target conditions for each option
% Option A: RealProp owns exactly Flores and Garza
satisfies(a, T) :- time(T),
    owner(flores, realprop, T),
    owner(garza, realprop, T),
    #count { B : building(B), owner(B, realprop, T) } = 2.

% Option B: Southco owns exactly Flores and Meyer
satisfies(b, T) :- time(T),
    owner(flores, southco, T),
    owner(meyer, southco, T),
    #count { B : building(B), owner(B, southco, T) } = 2.

% Option C: Southco owns exactly Garza and Lynch
satisfies(c, T) :- time(T),
    owner(garza, southco, T),
    owner(lynch, southco, T),
    #count { B : building(B), owner(B, southco, T) } = 2.

% Option D: Trustcorp owns exactly Flores and Ortiz
satisfies(d, T) :- time(T),
    owner(flores, trustcorp, T),
    owner(ortiz, trustcorp, T),
    #count { B : building(B), owner(B, trustcorp, T) } = 2.

% Option E: Trustcorp owns exactly Garza and Meyer
satisfies(e, T) :- time(T),
    owner(garza, trustcorp, T),
    owner(meyer, trustcorp, T),
    #count { B : building(B), owner(B, trustcorp, T) } = 2.

% An option is possible if it is satisfied at some time
possible(O) :- satisfies(O, T).

% The answer is the option that is not possible
option(O) :- not possible(O).

#show option/1.