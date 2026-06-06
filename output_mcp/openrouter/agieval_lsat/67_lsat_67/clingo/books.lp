% Books and shelves
book(f). book(g). book(h). book(i). book(k). book(l). book(m). book(o).

shelf(top). shelf(middle). shelf(bottom).

% higher relation between shelves (higher shelf means physically above)
higher(top,middle). higher(middle,bottom). higher(top,bottom).

% ---------- Option A ----------
% Two independent placements to test determinacy under extra condition (I and M same shelf)
1 { shelfA1(B, top); shelfA1(B, middle); shelfA1(B, bottom) } 1 :- book(B).
1 { shelfA2(B, top); shelfA2(B, middle); shelfA2(B, bottom) } 1 :- book(B).

% Base constraints for copy1
:- not #count{B : shelfA1(B, top)} >= 2.
:- not #count{B : shelfA1(B, middle)} >= 2.
:- not #count{B : shelfA1(B, bottom)} >= 2.
:- not #count{B : shelfA1(B, bottom)} > #count{B : shelfA1(B, top)}.
% I on middle
:- shelfA1(i, S), S != middle.
% K higher than F
:- shelfA1(k, Sk), shelfA1(f, Sf), not higher(Sk, Sf).
% O higher than L
:- shelfA1(o, So), shelfA1(l, Sl), not higher(So, Sl).
% F same as M
:- shelfA1(f, Sf), shelfA1(m, Sm), Sf != Sm.
% Extra condition for option A: I and M same shelf
:- shelfA1(i, Si), shelfA1(m, Sm), Si != Sm.

% Base constraints for copy2 (same as copy1)
:- not #count{B : shelfA2(B, top)} >= 2.
:- not #count{B : shelfA2(B, middle)} >= 2.
:- not #count{B : shelfA2(B, bottom)} >= 2.
:- not #count{B : shelfA2(B, bottom)} > #count{B : shelfA2(B, top)}.
:- shelfA2(i, S), S != middle.
:- shelfA2(k, Sk), shelfA2(f, Sf), not higher(Sk, Sf).
:- shelfA2(o, So), shelfA2(l, Sl), not higher(So, Sl).
:- shelfA2(f, Sf), shelfA2(m, Sm), Sf != Sm.
:- shelfA2(i, Si), shelfA2(m, Sm), Si != Sm.

% Detect difference between the two placements
diffA :- shelfA1(B, S1), shelfA2(B, S2), S1 != S2.
option(a) :- not diffA.

% ---------- Option B ----------
1 { shelfB1(B, top); shelfB1(B, middle); shelfB1(B, bottom) } 1 :- book(B).
1 { shelfB2(B, top); shelfB2(B, middle); shelfB2(B, bottom) } 1 :- book(B).
% copy1 constraints
:- not #count{B : shelfB1(B, top)} >= 2.
:- not #count{B : shelfB1(B, middle)} >= 2.
:- not #count{B : shelfB1(B, bottom)} >= 2.
:- not #count{B : shelfB1(B, bottom)} > #count{B : shelfB1(B, top)}.
:- shelfB1(i, S), S != middle.
:- shelfB1(k, Sk), shelfB1(f, Sf), not higher(Sk, Sf).
:- shelfB1(o, So), shelfB1(l, Sl), not higher(So, Sl).
:- shelfB1(f, Sf), shelfB1(m, Sm), Sf != Sm.
% copy2 constraints
:- not #count{B : shelfB2(B, top)} >= 2.
:- not #count{B : shelfB2(B, middle)} >= 2.
:- not #count{B : shelfB2(B, bottom)} >= 2.
:- not #count{B : shelfB2(B, bottom)} > #count{B : shelfB2(B, top)}.
:- shelfB2(i, S), S != middle.
:- shelfB2(k, Sk), shelfB2(f, Sf), not higher(Sk, Sf).
:- shelfB2(o, So), shelfB2(l, Sl), not higher(So, Sl).
:- shelfB2(f, Sf), shelfB2(m, Sm), Sf != Sm.
% Extra condition for option B: K and G same shelf
:- shelfB1(k, Sk), shelfB1(g, Sg), Sk != Sg.
:- shelfB2(k, Sk), shelfB2(g, Sg), Sk != Sg.
% diff detection
diffB :- shelfB1(B, S1), shelfB2(B, S2), S1 != S2.
option(b) :- not diffB.

% ---------- Option C ----------
1 { shelfC1(B, top); shelfC1(B, middle); shelfC1(B, bottom) } 1 :- book(B).
1 { shelfC2(B, top); shelfC2(B, middle); shelfC2(B, bottom) } 1 :- book(B).
% copy1 constraints
:- not #count{B : shelfC1(B, top)} >= 2.
:- not #count{B : shelfC1(B, middle)} >= 2.
:- not #count{B : shelfC1(B, bottom)} >= 2.
:- not #count{B : shelfC1(B, bottom)} > #count{B : shelfC1(B, top)}.
:- shelfC1(i, S), S != middle.
:- shelfC1(k, Sk), shelfC1(f, Sf), not higher(Sk, Sf).
:- shelfC1(o, So), shelfC1(l, Sl), not higher(So, Sl).
:- shelfC1(f, Sf), shelfC1(m, Sm), Sf != Sm.
% copy2 constraints
:- not #count{B : shelfC2(B, top)} >= 2.
:- not #count{B : shelfC2(B, middle)} >= 2.
:- not #count{B : shelfC2(B, bottom)} >= 2.
:- not #count{B : shelfC2(B, bottom)} > #count{B : shelfC2(B, top)}.
:- shelfC2(i, S), S != middle.
:- shelfC2(k, Sk), shelfC2(f, Sf), not higher(Sk, Sf).
:- shelfC2(o, So), shelfC2(l, Sl), not higher(So, Sl).
:- shelfC2(f, Sf), shelfC2(m, Sm), Sf != Sm.
% Extra condition for option C: L and F same shelf
:- shelfC1(l, Sl), shelfC1(f, Sf), Sl != Sf.
:- shelfC2(l, Sl), shelfC2(f, Sf), Sl != Sf.
% diff detection
diffC :- shelfC1(B, S1), shelfC2(B, S2), S1 != S2.
option(c) :- not diffC.

% ---------- Option D ----------
1 { shelfD1(B, top); shelfD1(B, middle); shelfD1(B, bottom) } 1 :- book(B).
1 { shelfD2(B, top); shelfD2(B, middle); shelfD2(B, bottom) } 1 :- book(B).
% copy1 constraints
:- not #count{B : shelfD1(B, top)} >= 2.
:- not #count{B : shelfD1(B, middle)} >= 2.
:- not #count{B : shelfD1(B, bottom)} >= 2.
:- not #count{B : shelfD1(B, bottom)} > #count{B : shelfD1(B, top)}.
:- shelfD1(i, S), S != middle.
:- shelfD1(k, Sk), shelfD1(f, Sf), not higher(Sk, Sf).
:- shelfD1(o, So), shelfD1(l, Sl), not higher(So, Sl).
:- shelfD1(f, Sf), shelfD1(m, Sm), Sf != Sm.
% copy2 constraints
:- not #count{B : shelfD2(B, top)} >= 2.
:- not #count{B : shelfD2(B, middle)} >= 2.
:- not #count{B : shelfD2(B, bottom)} >= 2.
:- not #count{B : shelfD2(B, bottom)} > #count{B : shelfD2(B, top)}.
:- shelfD2(i, S), S != middle.
:- shelfD2(k, Sk), shelfD2(f, Sf), not higher(Sk, Sf).
:- shelfD2(o, So), shelfD2(l, Sl), not higher(So, Sl).
:- shelfD2(f, Sf), shelfD2(m, Sm), Sf != Sm.
% Extra condition for option D: M and H same shelf
:- shelfD1(m, Sm), shelfD1(h, Sh), Sm != Sh.
:- shelfD2(m, Sm), shelfD2(h, Sh), Sm != Sh.
% diff detection
diffD :- shelfD1(B, S1), shelfD2(B, S2), S1 != S2.
option(d) :- not diffD.

% ---------- Option E ----------
1 { shelfE1(B, top); shelfE1(B, middle); shelfE1(B, bottom) } 1 :- book(B).
1 { shelfE2(B, top); shelfE2(B, middle); shelfE2(B, bottom) } 1 :- book(B).
% copy1 constraints
:- not #count{B : shelfE1(B, top)} >= 2.
:- not #count{B : shelfE1(B, middle)} >= 2.
:- not #count{B : shelfE1(B, bottom)} >= 2.
:- not #count{B : shelfE1(B, bottom)} > #count{B : shelfE1(B, top)}.
:- shelfE1(i, S), S != middle.
:- shelfE1(k, Sk), shelfE1(f, Sf), not higher(Sk, Sf).
:- shelfE1(o, So), shelfE1(l, Sl), not higher(So, Sl).
:- shelfE1(f, Sf), shelfE1(m, Sm), Sf != Sm.
% copy2 constraints
:- not #count{B : shelfE2(B, top)} >= 2.
:- not #count{B : shelfE2(B, middle)} >= 2.
:- not #count{B : shelfE2(B, bottom)} >= 2.
:- not #count{B : shelfE2(B, bottom)} > #count{B : shelfE2(B, top)}.
:- shelfE2(i, S), S != middle.
:- shelfE2(k, Sk), shelfE2(f, Sf), not higher(Sk, Sf).
:- shelfE2(o, So), shelfE2(l, Sl), not higher(So, Sl).
:- shelfE2(f, Sf), shelfE2(m, Sm), Sf != Sm.
% Extra condition for option E: H and O same shelf
:- shelfE1(h, Sh), shelfE1(o, So), Sh != So.
:- shelfE2(h, Sh), shelfE2(o, So), Sh != So.
% diff detection
diffE :- shelfE1(B, S1), shelfE2(B, S2), S1 != S2.
option(e) :- not diffE.

#show option/1.