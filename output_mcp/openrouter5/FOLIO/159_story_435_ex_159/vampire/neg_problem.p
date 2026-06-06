% Negative version: negated conclusion as conjecture
% Negated: James does NOT take the database course AND does NOT have a part-time job offered by the university.

% I need to re-read the premises more carefully.
% "James is a student working in the lab." - This says lab_worker(james)
% "James doesn't work in the lab or have a part-time job offered by the university."
% This could mean: James doesn't work in the lab, OR James doesn't have a part-time job.
% Actually "doesn't work in the lab or have a part-time job" = ~(works in the lab) AND ~(has a part-time job)
% So: ~lab_worker(james) & ~pt_job_uni(james)
% But premise says lab_worker(james). This is contradictory.

% Let me re-read more carefully. Maybe "James doesn't work in the lab" is a separate statement
% that contradicts "James is a student working in the lab"? That would make the premises inconsistent.
% Let me check if there's another interpretation.

% Actually, maybe the premise "James is a student working in the lab" is separate from
% "James doesn't work in the lab or have a part-time job offered by the university."
% These are contradictory. So the premises are inconsistent.

% Let me try removing the contradictory premise and see what happens.
% Actually wait - maybe "James doesn't work in the lab or have a part-time job" means
% James doesn't have (work in the lab or have a part-time job) = ~(lab_worker(james) | pt_job_uni(james))
% = ~lab_worker(james) & ~pt_job_uni(james)

% The premises are contradictory. Let me just proceed with the encoding and see.

fof(premise1, axiom, ! [X] : ((student(X) & library_worker(X)) => ~cs_dept(X))).
fof(premise2, axiom, ! [X] : ((student(X) & pt_job_uni(X)) => library_worker(X))).
fof(premise3, axiom, ! [X] : ((student(X) & takes_db_course(X)) => cs_dept(X))).
fof(premise4, axiom, ! [X] : ((student(X) & takes_class_with_david(X)) => takes_db_course(X))).
fof(premise5, axiom, ! [X] : ((student(X) & lab_worker(X)) => takes_class_with_david(X))).
fof(premise6, axiom, student(james)).
fof(premise7, axiom, lab_worker(james)).
fof(premise8, axiom, ~lab_worker(james)).
fof(premise9, axiom, ~pt_job_uni(james)).

% Negated conclusion: James does NOT take the database course AND does NOT have a part-time job
fof(neg_conclusion, conjecture, ~takes_db_course(james) & ~pt_job_uni(james)).