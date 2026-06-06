% Domain
book(f;g;h;i;k;l;m;o).
shelf(1..3).  % 1=top, 2=middle, 3=bottom

% Each book on exactly one shelf
1 { on(B, S) : shelf(S) } 1 :- book(B).

% At least 2 books per shelf
:- shelf(S), #count { B : on(B, S) } < 2.

% More on bottom than top
bottom_count(N) :- N = #count { B : on(B, 3) }.
top_count(N) :- N = #count { B : on(B, 1) }.
:- bottom_count(B), top_count(T), B <= T.

% I on middle
on(i, 2).

% K higher than F (smaller number = higher)
:- on(K, SK), on(F, SF), SK >= SF.

% O higher than L
:- on(O, SO), on(L, SL), SO >= SL.

% F and M same shelf
:- on(F, SF), on(M, SM), SF != SM.

% G on top (given condition)
on(g, 1).

% Define what each option claims about middle shelf
mid_books(a, h). mid_books(a, i).      % A: H, I
mid_books(b, i). mid_books(b, l).      % B: I, L
mid_books(c, h). mid_books(c, i). mid_books(c, l).  % C: H, I, L
mid_books(d, i). mid_books(d, k). mid_books(d, l).  % D: I, K, L
mid_books(e, f). mid_books(e, i). mid_books(e, m).  % E: F, I, M

option(a;b;c;d;e).

% All listed books must be on middle
:- option(O), mid_books(O, B), not on(B, 2).

% No extra books on middle
:- option(O), book(B), on(B, 2), not mid_books(O, B).

% An option is possible if both above constraints hold
possible(O) :- option(O), 
               not any_missing(O),
               not any_extra(O).

any_missing(O) :- mid_books(O, B), not on(B, 2).
any_extra(O) :- book(B), on(B, 2), not mid_books(O, B).

% The answer is the possible option(s)
answer(O) :- possible(O).

#show answer/1.