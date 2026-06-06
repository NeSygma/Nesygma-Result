% Yale University Endowment Evaluation
% Based strictly on given premises

% --- Facts from premises ---
% Premise 1: Yale University is a private Ivy League research university
university(yale).
type(yale, "private").
type(yale, "ivy_league").
type(yale, "research").

% Premise 2: Yale University moved to New Haven in 1716
moved_to(yale, "new_haven", 1716).

% Premise 3: Yale University's endowment was valued at $42.3 billion
endowment(yale, 42300000000).  % $42.3 billion in dollars

% Premise 4: List of residential colleges at Yale
residential_college("benjamin_franklin").
residential_college("berkeley").
residential_college("branford").
residential_college("davenport").
residential_college("ezra_stiles").
residential_college("grace_hopper").
residential_college("jonathan_edwards").
residential_college("morse").
residential_college("pauli_murray").
residential_college("pierson").
residential_college("saybrook").
residential_college("silliman").
residential_college("timothy_dwight").
residential_college("trumbull").

% --- Domain: Educational institutions ---
% We only know about Yale from the premises
educational_institution(yale).

% --- Conclusion evaluation ---
% To prove TRUE: Yale's endowment must be larger than ALL other institutions
% To prove FALSE: Some other institution must have a larger endowment than Yale
% Since we have NO information about other institutions' endowments, we cannot determine

% Positive logic for True: Yale has largest endowment
% This would require: endowment(yale, E) AND for all other institutions I, endowment(I, E2) where E2 < E
% We cannot derive this because we don't know other institutions' endowments

% Positive logic for False: Some other institution has larger endowment
% This would require: endowment(other_institution, E2) where E2 > 42300000000
% We cannot derive this because we don't know other institutions' endowments

% --- Final Answer Mapping ---
% Since we cannot derive either conclusion_true or conclusion_false from premises,
% the answer must be UNCERTAIN

answer(true) :- false.  % Cannot derive true
answer(false) :- false. % Cannot derive false
answer(uncertain) :- not answer(true), not answer(false).

% Show the answer
#show answer/1.
#show endowment/2.
#show educational_institution/1.