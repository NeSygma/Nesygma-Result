% Members
member(guitarist; keyboard_player; percussionist; saxophonist; trumpeter; violinist).

% Positions 1-6
position(1..6).

% Each member gets exactly one position (solo order)
1 { assigned(M, P) : position(P) } 1 :- member(M).

% Each position has exactly one member
1 { assigned(M, P) : member(M) } 1 :- position(P).

% Rule 1: The guitarist does not perform the fourth solo.
:- assigned(guitarist, 4).

% Define "before" relation
before(M1, M2) :- assigned(M1, P1), assigned(M2, P2), P1 < P2.

% Rule 2: The percussionist performs a solo at some time before the keyboard player does.
:- not before(percussionist, keyboard_player).

% Rule 3: The keyboard player performs a solo at some time after the violinist does AND at some time before the guitarist does.
:- not before(violinist, keyboard_player).
:- not before(keyboard_player, guitarist).

% Rule 4: The saxophonist performs a solo at some time after either the percussionist does or the trumpeter does, but not both.
% Define: sax is after perc?
sax_after_perc :- before(percussionist, saxophonist).
% Define: sax is after trumpeter?
sax_after_trump :- before(trumpeter, saxophonist).

% Exactly one of these holds.
:- not sax_after_perc, not sax_after_trump.
:- sax_after_perc, sax_after_trump.

% Additional condition from the question: percussionist performs a solo at some time before the saxophonist does.
:- not before(percussionist, saxophonist).

% --- Now evaluate the options ---

% Option (A): The percussionist performs the first solo.
perc_first :- assigned(percussionist, 1).

% Option (B): The percussionist performs the second solo.
perc_second :- assigned(percussionist, 2).

% Option (C): The violinist performs a solo at some time before the saxophonist does.
violin_before_sax :- before(violinist, saxophonist).

% Option (D): The percussionist performs a solo at some time before the trumpeter does.
perc_before_trump :- before(percussionist, trumpeter).

% Option (E): The saxophonist performs a solo at some time before the keyboard player does.
sax_before_keyboard :- before(saxophonist, keyboard_player).

% Now derive which option must be true in ALL valid scenarios.
% In ASP, we can check this by seeing which option atom holds in EVERY answer set.
% One way: add constraints to force each option to be false, and see if the problem becomes UNSAT.
% If forcing option X to be false leads to UNSAT, then X must be true.

% So we create a scenario where we test each option:
% We'll use a choice to "select" an option to test.

% Let's do it differently: use #show to see what holds in all models.
#show assigned/2.
#show perc_first/0.
#show perc_second/0.
#show violin_before_sax/0.
#show perc_before_trump/0.
#show sax_before_keyboard/0.