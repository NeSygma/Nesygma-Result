% Initial state
company(rp; sc; tc).
building(garza; yates; zimmer; flores; lynch; king; meyer; ortiz).

class(garza, 1). class(flores, 1).
class(lynch, 2). class(king, 2). class(meyer, 2). class(ortiz, 2).
class(yates, 3). class(zimmer, 3).

% Initial ownership
owns(rp, garza, 0). owns(rp, yates, 0). owns(rp, zimmer, 0).
owns(sc, flores, 0). owns(sc, lynch, 0).
owns(tc, king, 0). owns(tc, meyer, 0). owns(tc, ortiz, 0).

#const max_time = 3.
time(0..max_time).

% Trade rules
% Trade 1: C1, B1 <-> C2, B2 (same class)
{ trade1(C1, B1, C2, B2, T) } :- company(C1), company(C2), building(B1), building(B2), time(T), T < max_time,
    owns(C1, B1, T), owns(C2, B2, T), class(B1, K), class(B2, K), C1 != C2, B1 != B2.

% Trade 2: C1, B1 (class 1) <-> C2, B2 (class 2) + B3 (class 2)
{ trade2(C1, B1, C2, B2, B3, T) } :- company(C1), company(C2), building(B1), building(B2), building(B3), time(T), T < max_time,
    owns(C1, B1, T), owns(C2, B2, T), owns(C2, B3, T),
    class(B1, 1), class(B2, 2), class(B3, 2), C1 != C2, B2 != B3.

% Trade 3: C1, B1 (class 2) <-> C2, B2 (class 3) + B3 (class 3)
{ trade3(C1, B1, C2, B2, B3, T) } :- company(C1), company(C2), building(B1), building(B2), building(B3), time(T), T < max_time,
    owns(C1, B1, T), owns(C2, B2, T), owns(C2, B3, T),
    class(B1, 2), class(B2, 3), class(B3, 3), C1 != C2, B2 != B3.

% State update
involved(B, T) :- trade1(_, B, _, _, T).
involved(B, T) :- trade1(_, _, _, B, T).
involved(B, T) :- trade2(_, B, _, _, _, T).
involved(B, T) :- trade2(_, _, _, B, _, T).
involved(B, T) :- trade2(_, _, _, _, B, T).
involved(B, T) :- trade3(_, B, _, _, _, T).
involved(B, T) :- trade3(_, _, _, B, _, T).
involved(B, T) :- trade3(_, _, _, _, B, T).

owns(C, B, T+1) :- owns(C, B, T), not involved(B, T), time(T), T < max_time.

% Trade 1
owns(C2, B1, T+1) :- trade1(C1, B1, C2, B2, T).
owns(C1, B2, T+1) :- trade1(C1, B1, C2, B2, T).

% Trade 2
owns(C2, B1, T+1) :- trade2(C1, B1, C2, B2, B3, T).
owns(C1, B2, T+1) :- trade2(C1, B1, C2, B2, B3, T).
owns(C1, B3, T+1) :- trade2(C1, B1, C2, B2, B3, T).

% Trade 3
owns(C2, B1, T+1) :- trade3(C1, B1, C2, B2, B3, T).
owns(C1, B2, T+1) :- trade3(C1, B1, C2, B2, B3, T).
owns(C1, B3, T+1) :- trade3(C1, B1, C2, B2, B3, T).

% Options
% A: RealProp owns exactly Flores and Garza
option_a(T) :- time(T), owns(rp, flores, T), owns(rp, garza, T), 
               not owns(rp, B, T) : building(B), B != flores, B != garza.
% B: Southco owns exactly Flores and Meyer
option_b(T) :- time(T), owns(sc, flores, T), owns(sc, meyer, T), 
               not owns(sc, B, T) : building(B), B != flores, B != meyer.
% C: Southco owns exactly Garza and Lynch
option_c(T) :- time(T), owns(sc, garza, T), owns(sc, lynch, T), 
               not owns(sc, B, T) : building(B), B != garza, B != lynch.
% D: Trustcorp owns exactly Flores and Ortiz
option_d(T) :- time(T), owns(tc, flores, T), owns(tc, ortiz, T), 
               not owns(tc, B, T) : building(B), B != flores, B != ortiz.
% E: Trustcorp owns exactly Garza and Meyer
option_e(T) :- time(T), owns(tc, garza, T), owns(tc, meyer, T), 
               not owns(tc, B, T) : building(B), B != garza, B != meyer.

possible(a) :- option_a(T), time(T).
possible(b) :- option_b(T), time(T).
possible(c) :- option_c(T), time(T).
possible(d) :- option_d(T), time(T).
possible(e) :- option_e(T), time(T).

option(a) :- not possible(a).
option(b) :- not possible(b).
option(c) :- not possible(c).
option(d) :- not possible(d).
option(e) :- not possible(e).
#show option/1.