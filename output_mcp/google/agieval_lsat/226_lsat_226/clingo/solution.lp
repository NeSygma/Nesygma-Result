% --- Initial State ---
company(realprop; southco; trustcorp).
building(garza; yates; zimmer; flores; lynch; king; meyer; ortiz).

class(garza, 1).
class(yates, 3).
class(zimmer, 3).
class(flores, 1).
class(lynch, 2).
class(king, 2).
class(meyer, 2).
class(ortiz, 2).

initial_owns(realprop, garza).
initial_owns(realprop, yates).
initial_owns(realprop, zimmer).
initial_owns(southco, flores).
initial_owns(southco, lynch).
initial_owns(trustcorp, king).
initial_owns(trustcorp, meyer).
initial_owns(trustcorp, ortiz).

% --- Option Definitions ---
option(a;b;c;d;e).
option_owns(a, realprop, flores). option_owns(a, realprop, garza).
option_owns(a, southco, lynch). option_owns(a, southco, yates). option_owns(a, southco, zimmer).
option_owns(a, trustcorp, king). option_owns(a, trustcorp, meyer). option_owns(a, trustcorp, ortiz).

option_owns(b, realprop, garza). option_owns(b, realprop, king). option_owns(b, realprop, ortiz).
option_owns(b, southco, flores). option_owns(b, southco, lynch).
option_owns(b, trustcorp, meyer). option_owns(b, trustcorp, yates). option_owns(b, trustcorp, zimmer).

option_owns(c, realprop, garza). option_owns(c, realprop, lynch).
option_owns(c, southco, flores). option_owns(c, southco, yates). option_owns(c, southco, zimmer).
option_owns(c, trustcorp, king). option_owns(c, trustcorp, meyer). option_owns(c, trustcorp, ortiz).

option_owns(d, realprop, garza). option_owns(d, realprop, meyer). option_owns(d, realprop, yates).
option_owns(d, southco, flores). option_owns(d, southco, lynch).
option_owns(d, trustcorp, king). option_owns(d, trustcorp, ortiz). option_owns(d, trustcorp, zimmer).

option_owns(e, realprop, garza). option_owns(e, realprop, yates). option_owns(e, realprop, zimmer).
option_owns(e, southco, lynch). option_owns(e, southco, ortiz).
option_owns(e, trustcorp, flores). option_owns(e, trustcorp, king). option_owns(e, trustcorp, meyer).

% --- Trade Logic ---
% A trade involves C1 giving S1 and C2 giving S2.
% S1 and S2 are sets of buildings.
{ trade_gives(C, B) : initial_owns(C, B) } :- company(C).

% Exactly two companies involved
1 { involved(C) : company(C) } 2.
:- trade_gives(C, _), not involved(C).
:- involved(C), not trade_gives(C, _).
:- involved(C1), involved(C2), involved(C3), C1 != C2, C2 != C3, C1 != C3.

% Trade validity
num_given(C, N) :- company(C), N = #count { B : trade_gives(C, B) }.

% Type 1: 1 for 1 (same class)
is_type1 :- involved(C1), involved(C2), C1 != C2,
            num_given(C1, 1), num_given(C2, 1),
            trade_gives(C1, B1), trade_gives(C2, B2),
            class(B1, C), class(B2, C).

% Type 2: 1 (class 1) for 2 (class 2)
is_type2 :- involved(C1), involved(C2), C1 != C2,
            num_given(C1, 1), num_given(C2, 2),
            trade_gives(C1, B1), class(B1, 1),
            trade_gives(C2, B2a), trade_gives(C2, B2b), B2a != B2b,
            class(B2a, 2), class(B2b, 2).
is_type2 :- involved(C1), involved(C2), C1 != C2,
            num_given(C1, 2), num_given(C2, 1),
            trade_gives(C1, B2a), trade_gives(C1, B2b), B2a != B2b,
            class(B2a, 2), class(B2b, 2),
            trade_gives(C2, B1), class(B1, 1).

% Type 3: 1 (class 2) for 2 (class 3)
is_type3 :- involved(C1), involved(C2), C1 != C2,
            num_given(C1, 1), num_given(C2, 2),
            trade_gives(C1, B1), class(B1, 2),
            trade_gives(C2, B2a), trade_gives(C2, B2b), B2a != B2b,
            class(B2a, 3), class(B2b, 3).
is_type3 :- involved(C1), involved(C2), C1 != C2,
            num_given(C1, 2), num_given(C2, 1),
            trade_gives(C1, B2a), trade_gives(C1, B2b), B2a != B2b,
            class(B2a, 3), class(B2b, 3),
            trade_gives(C2, B1), class(B1, 2).

:- not is_type1, not is_type2, not is_type3.

% Final state
final_owns(Comp, B) :- company(Comp), initial_owns(Comp, B), not trade_gives(Comp, B).
final_owns(Comp, B) :- company(Comp), involved(C1), involved(C2), C1 != C2,
                       trade_gives(C1, B), Comp == C2.
final_owns(Comp, B) :- company(Comp), involved(C1), involved(C2), C1 != C2,
                       trade_gives(C2, B), Comp == C1.

% Check option
is_option(Opt) :- option(Opt),
    #count { Comp, B : final_owns(Comp, B), not option_owns(Opt, Comp, B) } = 0,
    #count { Comp, B : option_owns(Opt, Comp, B), not final_owns(Comp, B) } = 0.

#show is_option/1.