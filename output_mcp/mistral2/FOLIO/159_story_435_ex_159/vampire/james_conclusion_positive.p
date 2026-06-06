fof(works_in_library_implies_not_cs, axiom,
    ! [S] : (works_in_library(S) => ~from_department(S, computer_science))).

fof(part_time_job_implies_library, axiom,
    ! [S] : (has_part_time_job(S) => works_in_library(S))).

fof(database_course_implies_cs, axiom,
    ! [S] : (taking_database_course(S) => from_department(S, computer_science))).

fof(class_with_professor_david_implies_database, axiom,
    ! [S] : (taking_class_with_professor_david(S) => taking_database_course(S))).

fof(works_in_lab_implies_class_with_professor_david, axiom,
    ! [S] : (works_in_lab(S) => taking_class_with_professor_david(S))).

fof(james_works_in_lab, axiom,
    works_in_lab(james)).

fof(james_no_lab_or_part_time, axiom,
    ~works_in_lab(james) | ~has_part_time_job(james)).

fof(conclusion, conjecture,
    taking_database_course(james) | has_part_time_job(james)).