% Domain choice rule
{ sel_myers, sel_ortega, sel_paine, sel_schmidt, sel_thomson, sel_wong, sel_yoder, sel_zayre }.

% Constraints
:- sel_myers, sel_ortega.
:- sel_myers, sel_paine.
:- sel_schmidt, not sel_paine.
:- sel_schmidt, not sel_thomson.
:- sel_wong, not sel_myers.
:- sel_wong, not sel_yoder.
:- sel_paine.
4 { sel_myers, sel_ortega, sel_paine, sel_schmidt, sel_thomson, sel_wong, sel_yoder, sel_zayre }.

% Option conditions
option(a) :- not sel_myers, not sel_ortega.
option(b) :- not sel_myers, not sel_thomson.
option(c) :- not sel_myers, not sel_zayre.
option(d) :- not sel_ortega, not sel_thomson.
option(e) :- not sel_ortega, not sel_yoder.

#show option/1.