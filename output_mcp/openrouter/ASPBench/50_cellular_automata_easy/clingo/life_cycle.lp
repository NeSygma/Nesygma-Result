% Domains
row(1..5).
col(1..5).
cell(R,C) :- row(R), col(C).

time(0..10).

% Offsets for neighbor positions (excluding (0,0))
offset(-1,-1).
offset(-1,0).
offset(-1,1).
offset(0,-1).
offset(0,1).
offset(1,-1).
offset(1,0).
offset(1,1).

% Neighbor relation
neighbor(R,C,R1,C1) :- cell(R,C), offset(DR,DC), R1 = R + DR, C1 = C + DC, row(R1), col(C1).

% Initial configuration (time 0)
alive(0,1,2). alive(0,1,4).
alive(0,2,1). alive(0,2,3). alive(0,2,5).
alive(0,3,2). alive(0,3,4).
alive(0,4,1). alive(0,4,3). alive(0,4,5).
alive(0,5,2). alive(0,5,4).

% Define dead cells (open world)
dead(T,R,C) :- cell(R,C), time(T), not alive(T,R,C).

% Evolution rules for next generation (T -> T+1) up to step 9 (so T+1 <=10)
% Survival with 2 neighbors
alive(T+1,R,C) :- time(T), T < 10, cell(R,C), alive(T,R,C), N = #count { (R1,C1) : neighbor(R,C,R1,C1), alive(T,R1,C1) }, N = 2.
% Survival with 3 neighbors
alive(T+1,R,C) :- time(T), T < 10, cell(R,C), alive(T,R,C), N = #count { (R1,C1) : neighbor(R,C,R1,C1), alive(T,R1,C1) }, N = 3.
% Birth with exactly 3 neighbors
alive(T+1,R,C) :- time(T), T < 10, cell(R,C), dead(T,R,C), N = #count { (R1,C1) : neighbor(R,C,R1,C1), alive(T,R1,C1) }, N = 3.

% Detect difference between two time steps
diff(T1,T2) :- time(T1), time(T2), cell(R,C), alive(T1,R,C), not alive(T2,R,C).
diff(T1,T2) :- time(T1), time(T2), cell(R,C), alive(T2,R,C), not alive(T1,R,C).

% Equality when no difference
equal(T1,T2) :- time(T1), time(T2), T1 < T2, not diff(T1,T2).

% Repeat when equal
repeat(T1,T2) :- equal(T1,T2).

% Choose earliest repeat (minimal T2, then minimal T1)
earliest_repeat(T1,T2) :- repeat(T1,T2), not earlier_t2(T2).
earlier_t2(T2) :- repeat(_,T2p), time(T2p), T2p < T2, time(T2).
% If multiple T1 for same minimal T2, pick minimal T1
earliest_repeat(T1,T2) :- repeat(T1,T2), not earlier_t2(T2), not earlier_t1(T1,T2).
earlier_t1(T1,T2) :- repeat(T1p,T2), time(T1p), T1p < T1, time(T1), time(T2).

% Period of the cycle
period(P) :- earliest_repeat(T1,T2), P = T2 - T1.

% Pattern identifier (first pattern)
pattern(1,P) :- period(P).

% Times that belong to the cycle
in_cycle(T) :- earliest_repeat(T1,T2), time(T), T >= T1, T < T2.

% Record cell states within the cycle (1 = alive, 0 = dead)
cell_state(T,R,C,1) :- in_cycle(T), alive(T,R,C).
cell_state(T,R,C,0) :- in_cycle(T), cell(R,C), not alive(T,R,C).

#show pattern/2.
#show cell_state/4.