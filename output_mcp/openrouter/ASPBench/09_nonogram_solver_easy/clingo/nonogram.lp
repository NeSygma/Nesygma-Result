% Domains
row(1..5). col(1..5).

% Row group definitions: group(Row, Index, Length)
group(1,1,2).
group(2,1,1).
group(3,1,3).
group(4,1,1). group(4,2,1).
group(5,1,2).

% Column group definitions: col_group(Col, Index, Length)
col_group(1,1,1). col_group(1,2,1).
col_group(2,1,1). col_group(2,2,3).
col_group(3,1,2).
col_group(4,1,1).
col_group(5,1,1).

% Cell domain
cell(R,C) :- row(R), col(C).

% Exactly one start position for each row group
1 { row_start(R,I,S) : col(S) } 1 :- group(R,I,_).
% Bounds for row starts (group fits in row)
:- row_start(R,I,S), group(R,I,Len), S + Len - 1 > 5.
% Separation between consecutive row groups
:- row_start(R,I,S1), group(R,I,Len1), row_start(R,I+1,S2), S2 < S1 + Len1 + 1.

% Exactly one start position for each column group
1 { col_start(C,J,R0) : row(R0) } 1 :- col_group(C,J,_).
% Bounds for column starts (group fits in column)
:- col_start(C,J,R0), col_group(C,J,Len), R0 + Len - 1 > 5.
% Separation between consecutive column groups
:- col_start(C,J,R0), col_group(C,J,Len), col_start(C,J+1,R1), R1 < R0 + Len + 1.

% Define black cells from row groups (safe variables)
cell_black(R,C) :- cell(R,C), row_start(R,I,S), group(R,I,Len), C >= S, C < S + Len.
% Define black cells from column groups (safe variables)
col_black(R,C) :- cell(R,C), col_start(C,J,R0), col_group(C,J,Len), R >= R0, R < R0 + Len.

% Consistency between row and column perspectives
:- cell_black(R,C), not col_black(R,C).
:- col_black(R,C), not cell_black(R,C).

% Define white cells (optional)
cell_white(R,C) :- cell(R,C), not cell_black(R,C).

#show cell_black/2.