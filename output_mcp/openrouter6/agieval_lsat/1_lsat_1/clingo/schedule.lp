% Domain definitions
day(mon; tue; wed).
time(morning; afternoon).
student(george; helen; irving; kyle; lenore; nina; olivia; robert).

% Option A assignments
assign_a(mon, morning, helen).
assign_a(mon, afternoon, robert).
assign_a(tue, morning, olivia).
assign_a(tue, afternoon, irving).
assign_a(wed, morning, lenore).
assign_a(wed, afternoon, kyle).

% Option B assignments
assign_b(mon, morning, irving).
assign_b(mon, afternoon, olivia).
assign_b(tue, morning, helen).
assign_b(tue, afternoon, kyle).
assign_b(wed, morning, nina).
assign_b(wed, afternoon, lenore).

% Option C assignments
assign_c(mon, morning, lenore).
assign_c(mon, afternoon, helen).
assign_c(tue, morning, george).
assign_c(tue, afternoon, kyle).
assign_c(wed, morning, robert).
assign_c(wed, afternoon, irving).

% Option D assignments
assign_d(mon, morning, nina).
assign_d(mon, afternoon, helen).
assign_d(tue, morning, robert).
assign_d(tue, afternoon, irving).
assign_d(wed, morning, olivia).
assign_d(wed, afternoon, lenore).

% Option E assignments
assign_e(mon, morning, olivia).
assign_e(mon, afternoon, nina).
assign_e(tue, morning, irving).
assign_e(tue, afternoon, helen).
assign_e(wed, morning, kyle).
assign_e(wed, afternoon, george).

% Helper predicates for Option A
has_student_a(D, S) :- assign_a(D, _, S).
has_helen_tue_a :- has_student_a(tue, helen).
has_irving_tue_a :- has_student_a(tue, irving).
has_helen_wed_a :- has_student_a(wed, helen).
has_irving_wed_a :- has_student_a(wed, irving).

% Helper predicates for Option B
has_student_b(D, S) :- assign_b(D, _, S).
has_helen_tue_b :- has_student_b(tue, helen).
has_irving_tue_b :- has_student_b(tue, irving).
has_helen_wed_b :- has_student_b(wed, helen).
has_irving_wed_b :- has_student_b(wed, irving).

% Helper predicates for Option C
has_student_c(D, S) :- assign_c(D, _, S).
has_helen_tue_c :- has_student_c(tue, helen).
has_irving_tue_c :- has_student_c(tue, irving).
has_helen_wed_c :- has_student_c(wed, helen).
has_irving_wed_c :- has_student_c(wed, irving).

% Helper predicates for Option D
has_student_d(D, S) :- assign_d(D, _, S).
has_helen_tue_d :- has_student_d(tue, helen).
has_irving_tue_d :- has_student_d(tue, irving).
has_helen_wed_d :- has_student_d(wed, helen).
has_irving_wed_d :- has_student_d(wed, irving).

% Helper predicates for Option E
has_student_e(D, S) :- assign_e(D, _, S).
has_helen_tue_e :- has_student_e(tue, helen).
has_irving_tue_e :- has_student_e(tue, irving).
has_helen_wed_e :- has_student_e(wed, helen).
has_irving_wed_e :- has_student_e(wed, irving).

% Option A validity
option(a) :-
    % Exactly six distinct students
    #count{S : assign_a(_, _, S)} = 6,
    % George only on Tuesday
    not (assign_a(D, T, george), D != tue),
    % Olivia and Robert not in afternoon
    not assign_a(_, afternoon, olivia),
    not assign_a(_, afternoon, robert),
    % Nina Monday constraint
    ( not assign_a(mon, _, nina) or (has_helen_tue_a and has_irving_tue_a) ),
    % Nina Tuesday constraint
    ( not assign_a(tue, _, nina) or (has_helen_wed_a and has_irving_wed_a) ).

% Option B validity
option(b) :-
    #count{S : assign_b(_, _, S)} = 6,
    not (assign_b(D, T, george), D != tue),
    not assign_b(_, afternoon, olivia),
    not assign_b(_, afternoon, robert),
    ( not assign_b(mon, _, nina) or (has_helen_tue_b and has_irving_tue_b) ),
    ( not assign_b(tue, _, nina) or (has_helen_wed_b and has_irving_wed_b) ).

% Option C validity
option(c) :-
    #count{S : assign_c(_, _, S)} = 6,
    not (assign_c(D, T, george), D != tue),
    not assign_c(_, afternoon, olivia),
    not assign_c(_, afternoon, robert),
    ( not assign_c(mon, _, nina) or (has_helen_tue_c and has_irving_tue_c) ),
    ( not assign_c(tue, _, nina) or (has_helen_wed_c and has_irving_wed_c) ).

% Option D validity
option(d) :-
    #count{S : assign_d(_, _, S)} = 6,
    not (assign_d(D, T, george), D != tue),
    not assign_d(_, afternoon, olivia),
    not assign_d(_, afternoon, robert),
    ( not assign_d(mon, _, nina) or (has_helen_tue_d and has_irving_tue_d) ),
    ( not assign_d(tue, _, nina) or (has_helen_wed_d and has_irving_wed_d) ).

% Option E validity
option(e) :-
    #count{S : assign_e(_, _, S)} = 6,
    not (assign_e(D, T, george), D != tue),
    not assign_e(_, afternoon, olivia),
    not assign_e(_, afternoon, robert),
    ( not assign_e(mon, _, nina) or (has_helen_tue_e and has_irving_tue_e) ),
    ( not assign_e(tue, _, nina) or (has_helen_wed_e and has_irving_wed_e) ).

#show option/1.