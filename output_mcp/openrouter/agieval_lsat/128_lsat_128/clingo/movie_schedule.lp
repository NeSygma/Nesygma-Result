% Define schedules for each option
show_a(romance,1,7).
show_a(horror,1,9).
show_a(western,2,7).
show_a(scifi,2,9).
show_a(mystery,3,8).

show_b(mystery,1,7).
show_b(romance,1,9).
show_b(horror,2,7).
show_b(scifi,2,9).
show_b(western,3,8).

show_c(western,1,7).
show_c(scifi,1,9).
show_c(mystery,2,7).
show_c(horror,2,9).
show_c(romance,3,8).

show_d(romance,1,7).
show_d(mystery,1,9).
show_d(western,2,7).
show_d(horror,2,9).
show_d(scifi,3,8).

show_e(western,1,7).
show_e(mystery,1,9).
show_e(scifi,2,7).
show_e(romance,2,9).
show_e(horror,3,8).

% Helper to test each option against the problem constraints
option(a) :-
    % western before horror
    show_a(western,_,TW), show_a(horror,_,TH), TW < TH,
    % scifi not on screen 3
    not show_a(scifi,3,_),
    % romance not on screen 2
    not show_a(romance,2,_),
    % horror and mystery on different screens
    show_a(horror,SH,_), show_a(mystery,SM,_), SH != SM,
    % screen capacities
    2 = #count{M,T : show_a(M,1,T)},
    2 = #count{M,T : show_a(M,2,T)},
    1 = #count{M : show_a(M,3,8)},
    % each of screens 1 and 2 must have times 7 and 9
    show_a(_,1,7), show_a(_,1,9),
    show_a(_,2,7), show_a(_,2,9).

option(b) :-
    show_b(western,_,TW), show_b(horror,_,TH), TW < TH,
    not show_b(scifi,3,_),
    not show_b(romance,2,_),
    show_b(horror,SH,_), show_b(mystery,SM,_), SH != SM,
    2 = #count{M,T : show_b(M,1,T)},
    2 = #count{M,T : show_b(M,2,T)},
    1 = #count{M : show_b(M,3,8)},
    show_b(_,1,7), show_b(_,1,9),
    show_b(_,2,7), show_b(_,2,9).

option(c) :-
    show_c(western,_,TW), show_c(horror,_,TH), TW < TH,
    not show_c(scifi,3,_),
    not show_c(romance,2,_),
    show_c(horror,SH,_), show_c(mystery,SM,_), SH != SM,
    2 = #count{M,T : show_c(M,1,T)},
    2 = #count{M,T : show_c(M,2,T)},
    1 = #count{M : show_c(M,3,8)},
    show_c(_,1,7), show_c(_,1,9),
    show_c(_,2,7), show_c(_,2,9).

option(d) :-
    show_d(western,_,TW), show_d(horror,_,TH), TW < TH,
    not show_d(scifi,3,_),
    not show_d(romance,2,_),
    show_d(horror,SH,_), show_d(mystery,SM,_), SH != SM,
    2 = #count{M,T : show_d(M,1,T)},
    2 = #count{M,T : show_d(M,2,T)},
    1 = #count{M : show_d(M,3,8)},
    show_d(_,1,7), show_d(_,1,9),
    show_d(_,2,7), show_d(_,2,9).

option(e) :-
    show_e(western,_,TW), show_e(horror,_,TH), TW < TH,
    not show_e(scifi,3,_),
    not show_e(romance,2,_),
    show_e(horror,SH,_), show_e(mystery,SM,_), SH != SM,
    2 = #count{M,T : show_e(M,1,T)},
    2 = #count{M,T : show_e(M,2,T)},
    1 = #count{M : show_e(M,3,8)},
    show_e(_,1,7), show_e(_,1,9),
    show_e(_,2,7), show_e(_,2,9).

#show option/1.