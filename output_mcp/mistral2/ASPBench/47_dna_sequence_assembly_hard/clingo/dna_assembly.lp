% --- Fragment Data ---
% Fragments are represented as sequences of bases.
% Each base is represented as a fact: base(FragmentId, Position, Base).

base(0, 1, "A"). base(0, 2, "T"). base(0, 3, "G"). base(0, 4, "G"). base(0, 5, "G"). base(0, 6, "C"). base(0, 7, "G"). base(0, 8, "C").
base(1, 1, "G"). base(1, 2, "G"). base(1, 3, "C"). base(1, 4, "G"). base(1, 5, "C"). base(1, 6, "C"). base(1, 7, "A"). base(1, 8, "T").
base(2, 1, "G"). base(2, 2, "C"). base(2, 3, "C"). base(2, 4, "A"). base(2, 5, "T"). base(2, 6, "T").
base(3, 1, "A"). base(3, 2, "T"). base(3, 3, "T"). base(3, 4, "T"). base(3, 5, "A"). base(3, 6, "A").
base(4, 1, "A"). base(4, 2, "T"). base(4, 3, "G"). base(4, 4, "C"). base(4, 5, "C"). base(4, 6, "T"). base(4, 7, "C"). base(4, 8, "G").
base(5, 1, "G"). base(5, 2, "C"). base(5, 3, "T"). base(5, 4, "C"). base(5, 5, "G"). base(5, 6, "A"). base(5, 7, "G"). base(5, 8, "G").
base(6, 1, "T"). base(6, 2, "C"). base(6, 3, "G"). base(6, 4, "A"). base(6, 5, "G"). base(6, 6, "C"). base(6, 7, "T"). base(6, 8, "G").
base(7, 1, "A"). base(7, 2, "G"). base(7, 3, "C"). base(7, 4, "T"). base(7, 5, "G"). base(7, 6, "A").
base(8, 1, "A"). base(8, 2, "T"). base(8, 3, "T"). base(8, 4, "C"). base(8, 5, "G").

% --- Fragment length ---
fragment_length(Id, Len) :- fragment_length(Id, 1, Len).
fragment_length(Id, Pos, Len) :- base(Id, Pos, _), Pos1 = Pos + 1, fragment_length(Id, Pos1, Len1), Len = Len1 + 1.
fragment_length(Id, Pos, 1) :- base(Id, Pos, _), not base(Id, Pos+1, _).

% --- GC-content calculation ---
gc_content(Id, GC) :-
    fragment_length(Id, Len),
    gc_count(Id, GC_C, GC_G),
    GC = GC_C + GC_G.

gc_count(Id, GC_C, GC_G) :- gc_count(Id, 1, GC_C, GC_G).
gc_count(Id, Pos, GC_C, GC_G) :- base(Id, Pos, "C"), Pos1 = Pos + 1, gc_count(Id, Pos1, GC_C1, GC_G), GC_C = GC_C1 + 1.
gc_count(Id, Pos, GC_C, GC_G) :- base(Id, Pos, "G"), Pos1 = Pos + 1, gc_count(Id, Pos1, GC_C, GC_G1), GC_G = GC_G1 + 1.
gc_count(Id, Pos, 0, 0) :- base(Id, Pos, _), not base(Id, Pos, "C"), not base(Id, Pos, "G"), Pos1 = Pos + 1, gc_count(Id, Pos1, GC_C, GC_G).
gc_count(Id, Pos, 0, 0) :- base(Id, Pos, _), not base(Id, Pos+1, _).

% --- Complementary bases ---
complement("A", "T").
complement("T", "A").
complement("C", "G").
complement("G", "C").

% --- Fragment definition ---
fragment(Id) :- base(Id, 1, _).

% --- Orientation choice ---
{ orientation(Id, "forward") ; orientation(Id, "reverse") } = 1 :- fragment(Id).

% --- Reverse complement fragment ID assignment ---
revcomp_id(Id, RevId) :- fragment(Id), RevId = Id + 9.

% --- Base for reverse complement fragments ---
base(RevId, Pos, Base) :-
    revcomp_id(Id, RevId),
    base(Id, Pos, B),
    complement(B, Base).

% --- Contig structure ---
contig(1..9).
position(1..9).

% --- Fragment in contig ---
1 { fragment_in_contig(C, Id, Pos) : position(Pos) } 1 :- fragment(Id), contig(C).

% --- Overlap validation ---
suffix_matches_prefix(Id1, Id2, MinOverlap) :-
    fragment(Id1),
    fragment(Id2),
    MinOverlap = 3,
    base(Id1, L1, B1),
    base(Id2, L2, B2),
    L1 >= fragment_length(Id1, _) - MinOverlap + 1,
    L2 =< MinOverlap,
    base(Id1, L1, B1),
    base(Id2, L2, B2),
    B1 = B2.

% --- Adjacency and overlap constraints ---
:- fragment_in_contig(C, Id1, Pos1),
   fragment_in_contig(C, Pos2, Id2),
   Pos2 = Pos1 + 1,
   not suffix_matches_prefix(Id1, Id2, MinOverlap),
   gc_content(Id1, GC1),
   gc_content(Id2, GC2),
   MinOverlap = (GC1 > 4 and GC2 > 4) ? 4 : 3.

% --- Start and stop codon validation ---
starts_with_atg(C) :-
    fragment_in_contig(C, Id, 1),
    orientation(Id, "forward"),
    base(Id, 1, "A"), base(Id, 2, "T"), base(Id, 3, "G").

starts_with_atg(C) :-
    fragment_in_contig(C, Id, 1),
    orientation(Id, "reverse"),
    revcomp_id(Id, RevId),
    base(RevId, 1, "A"), base(RevId, 2, "T"), base(RevId, 3, "G").

ends_with_stop(C) :-
    fragment_in_contig(C, Id, Pos),
    orientation(Id, "forward"),
    base(Id, Pos, "T"), base(Id, Pos+1, "A"), base(Id, Pos+2, "A").

ends_with_stop(C) :-
    fragment_in_contig(C, Id, Pos),
    orientation(Id, "forward"),
    base(Id, Pos, "T"), base(Id, Pos+1, "A"), base(Id, Pos+2, "G").

ends_with_stop(C) :-
    fragment_in_contig(C, Id, Pos),
    orientation(Id, "forward"),
    base(Id, Pos, "T"), base(Id, Pos+1, "G"), base(Id, Pos+2, "A").

ends_with_stop(C) :-
    fragment_in_contig(C, Id, Pos),
    orientation(Id, "reverse"),
    revcomp_id(Id, RevId),
    base(RevId, Pos, "T"), base(RevId, Pos+1, "A"), base(RevId, Pos+2, "A").

ends_with_stop(C) :-
    fragment_in_contig(C, Id, Pos),
    orientation(Id, "reverse"),
    revcomp_id(Id, RevId),
    base(RevId, Pos, "T"), base(RevId, Pos+1, "A"), base(RevId, Pos+2, "G").

ends_with_stop(C) :-
    fragment_in_contig(C, Id, Pos),
    orientation(Id, "reverse"),
    revcomp_id(Id, RevId),
    base(RevId, Pos, "T"), base(RevId, Pos+1, "G"), base(RevId, Pos+2, "A").

% --- Exclusion ---
excluded_chimeric(Id) :- fragment(Id), not fragment_in_contig(_, Id, _).

% --- Valid contig ---
valid_contig(C) :-
    contig(C),
    starts_with_atg(C),
    ends_with_stop(C).

% --- Objective: Minimize the number of contigs ---
#minimize { 1@1,C : contig(C), not valid_contig(C) }.

% --- Show directives ---
#show fragment_in_contig/3.
#show orientation/2.
#show excluded_chimeric/1.

% --- Ensure all fragments are either in a contig or marked as chimeric ---
:- fragment(Id), not excluded_chimeric(Id), not fragment_in_contig(_, Id, _).