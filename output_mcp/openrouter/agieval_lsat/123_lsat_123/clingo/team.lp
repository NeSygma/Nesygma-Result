% Options selection
1 { option(a); option(b); option(c); option(d); option(e) } 1.

% Selected employees per option
selected(myers) :- option(a).
selected(paine) :- option(a).
selected(schmidt) :- option(a).
selected(thomson) :- option(a).

selected(ortega) :- option(b).
selected(paine) :- option(b).
selected(thomson) :- option(b).
selected(zayre) :- option(b).

selected(paine) :- option(c).
selected(schmidt) :- option(c).
selected(yoder) :- option(c).
selected(zayre) :- option(c).

selected(schmidt) :- option(d).
selected(thomson) :- option(d).
selected(yoder) :- option(d).
selected(zayre) :- option(d).

selected(thomson) :- option(e).
selected(wong) :- option(e).
selected(yoder) :- option(e).
selected(zayre) :- option(e).

% Constraints
:- selected(myers), selected(ortega).
:- selected(myers), selected(paine).

:- selected(schmidt), not selected(paine).
:- selected(schmidt), not selected(thomson).

:- selected(wong), not selected(myers).
:- selected(wong), not selected(yoder).

% At least 4 employees
:- N = #count { E : selected(E) }, N < 4.

#show option/1.