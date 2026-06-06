% DNA Assembly Problem - ASP Model
% Goal: Minimize number of contigs, mark chimeric fragments

% ============ FRAGMENT DATA ============
% Fragments
fragment(f0). fragment(f1). fragment(f2). fragment(f3). fragment(f4).
fragment(f5). fragment(f6). fragment(f7). fragment(f8).

% Forward sequences as character lists
% F0: ATGGGCGC
base(f0,1,a). base(f0,2,t). base(f0,3,g). base(f0,4,g). 
base(f0,5,g). base(f0,6,c). base(f0,7,g). base(f0,8,c).

% F1: GGCGCCAT
base(f1,1,g). base(f1,2,g). base(f1,3,c). base(f1,4,g). 
base(f1,5,c). base(f1,6,c). base(f1,7,a). base(f1,8,t).

% F2: GCCATT
base(f2,1,g). base(f2,2,c). base(f2,3,c). base(f2,4,a). 
base(f2,5,t). base(f2,6,t).

% F3: ATTTAA
base(f3,1,a). base(f3,2,t). base(f3,3,t). base(f3,4,t). 
base(f3,5,a). base(f3,6,a).

% F4: ATGCCTCG
base(f4,1,a). base(f4,2,t). base(f4,3,g). base(f4,4,c). 
base(f4,5,c). base(f4,6,t). base(f4,7,c). base(f4,8,g).

% F5: GCTCGAGG
base(f5,1,g). base(f5,2,c). base(f5,3,t). base(f5,4,c). 
base(f5,5,g). base(f5,6,a). base(f5,7,g). base(f5,8,g).

% F6: TCGAGCTG
base(f6,1,t). base(f6,2,c). base(f6,3,g). base(f6,4,a). 
base(f6,5,g). base(f6,6,c). base(f6,7,t). base(f6,8,g).

% F7: AGCTGA
base(f7,1,a). base(f7,2,g). base(f7,3,c). base(f7,4,t). 
base(f7,5,g). base(f7,6,a).

% F8: ATTCG
base(f8,1,a). base(f8,2,t). base(f8,3,t). base(f8,4,c). 
base(f8,5,g).

% Fragment lengths
flen(f0,8). flen(f1,8). flen(f2,6). flen(f3,6). flen(f4,8).
flen(f5,8). flen(f6,8). flen(f7,6). flen(f8,5).

% Complement mapping
comp(a,t). comp(t,a). comp(c,g). comp(g,c).

% Reverse complement: base(F, I, B) -> rc_base(F, J, comp(B)) where J = len+1-I
rc_base(F, J, CB) :- fragment(F), flen(F, L), base(F, I, B), comp(B, CB), J = L + 1 - I.

% GC content (count of g or c in forward)
gc_count(F, N) :- fragment(F), N = #count{I : base(F, I, B), B = g}.
gc_count2(F, N) :- fragment(F), N = #count{I : base(F, I, B), B = c}.
total_gc(F, N) :- gc_count(F, N1), gc_count2(F, N2), N = N1 + N2.

% High GC (>50%)
high_gc(F) :- fragment(F), flen(F, L), total_gc(F, N), N * 2 > L.

% ============ CONTIG STRUCTURE ============
% Maximum number of contigs (we want to minimize, but need an upper bound)
max_contigs(5).
contig(1..5).

% Maximum fragments per contig
max_frag_pos(9).
frag_pos(1..9).

% Orientation domain
orient(fwd). orient(rc).

% ============ DECISION VARIABLES ============
% Each fragment is either used in exactly one contig at one position with one orientation, or chimeric
{ used(F, C, P, O) : contig(C), frag_pos(P), orient(O) } 1 :- fragment(F).
chimeric(F) :- fragment(F), not used(F, _, _, _).

% Each contig position has at most one fragment
{ assigned(C, P, F, O) : fragment(F), orient(O) } 1 :- contig(C), frag_pos(P).

% Link used and assigned
used(F, C, P, O) :- assigned(C, P, F, O).
assigned(C, P, F, O) :- used(F, C, P, O).

% Contiguous fragments (no gaps within a contig)
has_frag(C, P) :- assigned(C, P, F, O).
:- frag_pos(P), P > 1, has_frag(C, P), not has_frag(C, P-1), contig(C).

% ============ SEQUENCE RECONSTRUCTION ============
% Get the effective base for a fragment at position I based on orientation
eff_base(F, I, B) :- used(F, _, _, fwd), base(F, I, B).
eff_base(F, I, B) :- used(F, _, _, rc), rc_base(F, I, B).

% ============ OVERLAP REQUIREMENTS ============
% For adjacent fragments in a contig, compute overlap
% Overlap means: suffix of fragment at position P matches prefix of fragment at position P+1
% We need to check overlaps of length 3 or 4

% Required overlap between two fragments
req_overlap(F1, F2, 4) :- high_gc(F1), high_gc(F2).
req_overlap(F1, F2, 3) :- fragment(F1), fragment(F2), not high_gc(F1).
req_overlap(F1, F2, 3) :- fragment(F1), fragment(F2), not high_gc(F2).

% Check if two fragments can overlap with required length (considering orientations)
% For fwd-fwd: last K of F1 fwd must match first K of F2 fwd
overlap_ok(F1, fwd, F2, fwd, K) :- 
    req_overlap(F1, F2, K), flen(F1, L1),
    J = 1..K,
    base(F1, L1-K+J, B1),
    base(F2, J, B2),
    B1 = B2.

% For fwd-rc: last K of F1 fwd must match first K of F2 rc
overlap_ok(F1, fwd, F2, rc, K) :- 
    req_overlap(F1, F2, K), flen(F1, L1), flen(F2, L2),
    J = 1..K,
    base(F1, L1-K+J, B1),
    rc_base(F2, J, B2),
    B1 = B2.

% For rc-fwd: last K of F1 rc must match first K of F2 fwd
overlap_ok(F1, rc, F2, fwd, K) :- 
    req_overlap(F1, F2, K), flen(F1, L1), flen(F2, L2),
    J = 1..K,
    rc_base(F1, L1-K+J, B1),
    base(F2, J, B2),
    B1 = B2.

% For rc-rc: last K of F1 rc must match first K of F2 rc
overlap_ok(F1, rc, F2, rc, K) :- 
    req_overlap(F1, F2, K), flen(F1, L1), flen(F2, L2),
    J = 1..K,
    rc_base(F1, L1-K+J, B1),
    rc_base(F2, J, B2),
    B1 = B2.

% Adjacent fragments in contig must have valid overlap
:- assigned(C, P, F1, O1), assigned(C, P+1, F2, O2), 
   req_overlap(F1, F2, K), not overlap_ok(F1, O1, F2, O2, K).

% ============ START AND STOP CODONS ============
% First fragment of contig must start with ATG (in its effective orientation)
% eff_base of first position must be a, t, g
start_ok(C) :- assigned(C, 1, F, O), eff_base(F, 1, a), eff_base(F, 2, t), eff_base(F, 3, g).

% Last fragment of contig must end with stop codon (TAA, TAG, or TGA)
last_pos(C, P) :- assigned(C, P, F, O), not assigned(C, P+1, _, _).

stop_ok(C) :- last_pos(C, P), assigned(C, P, F, O), flen(F, L),
              eff_base(F, L-2, t), eff_base(F, L-1, a), eff_base(F, L, a).
stop_ok(C) :- last_pos(C, P), assigned(C, P, F, O), flen(F, L),
              eff_base(F, L-2, t), eff_base(F, L-1, a), eff_base(F, L, g).
stop_ok(C) :- last_pos(C, P), assigned(C, P, F, O), flen(F, L),
              eff_base(F, L-2, t), eff_base(F, L-1, g), eff_base(F, L, a).

% Contig must have valid start and stop
:- has_frag(C, _), not start_ok(C).
:- has_frag(C, _), not stop_ok(C).

% ============ OPTIMIZATION ============
% Minimize number of contigs used
contig_used(C) :- has_frag(C, _).
#minimize { 1, C : contig_used(C) }.

% ============ OUTPUT ============
#show assigned/4.
#show chimeric/1.
#show contig_used/1.