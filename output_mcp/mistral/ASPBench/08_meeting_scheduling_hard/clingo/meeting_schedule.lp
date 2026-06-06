% Domains
room(r1; r2; r3; r4).
meeting(m1; m2; m3; m4; m5; m6; m7; m8; m9; m10;
        m11; m12; m13; m14; m15; m16; m17; m18; m19; m20).
person(p1; p2; p3; p4; p5; p6; p7; p8; p9; p10;
       p11; p12; p13; p14; p15; p16; p17; p18; p19; p20).
day(1; 2; 3; 4; 5).
slot(1; 2; 3; 4).

% Room equipment facts
% r1: projector, whiteboard, video, confcall
has_equipment(r1, projector).
has_equipment(r1, whiteboard).
has_equipment(r1, video).
has_equipment(r1, confcall).

% r2: projector, whiteboard, confcall
has_equipment(r2, projector).
has_equipment(r2, whiteboard).
has_equipment(r2, confcall).

% r3: whiteboard, confcall
has_equipment(r3, whiteboard).
has_equipment(r3, confcall).

% r4: projector, video
has_equipment(r4, projector).
has_equipment(r4, video).

% Meeting equipment requirements (based on meeting number mod 10)
% m1, m11: projector
requires_equipment(m1, projector).
requires_equipment(m11, projector).

% m2, m12: whiteboard
requires_equipment(m2, whiteboard).
requires_equipment(m12, whiteboard).

% m3, m13: confcall
requires_equipment(m3, confcall).
requires_equipment(m13, confcall).

% m4, m14: video, projector
requires_equipment(m4, video).
requires_equipment(m4, projector).
requires_equipment(m14, video).
requires_equipment(m14, projector).

% m5, m15: projector, confcall
requires_equipment(m5, projector).
requires_equipment(m5, confcall).
requires_equipment(m15, projector).
requires_equipment(m15, confcall).

% m6, m16: whiteboard, confcall
requires_equipment(m6, whiteboard).
requires_equipment(m6, confcall).
requires_equipment(m16, whiteboard).
requires_equipment(m16, confcall).

% m7, m17: projector, whiteboard, confcall
requires_equipment(m7, projector).
requires_equipment(m7, whiteboard).
requires_equipment(m7, confcall).
requires_equipment(m17, projector).
requires_equipment(m17, whiteboard).
requires_equipment(m17, confcall).

% m8, m18: video, confcall
requires_equipment(m8, video).
requires_equipment(m8, confcall).
requires_equipment(m18, video).
requires_equipment(m18, confcall).

% m9, m19: projector, video
requires_equipment(m9, projector).
requires_equipment(m9, video).
requires_equipment(m19, projector).
requires_equipment(m19, video).

% m10, m20: projector, whiteboard
requires_equipment(m10, projector).
requires_equipment(m10, whiteboard).
requires_equipment(m20, projector).
requires_equipment(m20, whiteboard).

% Meeting attendees
attends(p1, m1).  attends(p3, m1).  attends(p6, m1).  attends(p8, m1).
attends(p2, m2).  attends(p4, m2).  attends(p7, m2).  attends(p9, m2).
attends(p3, m3).  attends(p5, m3).  attends(p8, m3).  attends(p10, m3).
attends(p4, m4).  attends(p6, m4).  attends(p9, m4).  attends(p11, m4).
attends(p5, m5).  attends(p7, m5).  attends(p10, m5).  attends(p12, m5).
attends(p6, m6).  attends(p8, m6).  attends(p11, m6).  attends(p13, m6).
attends(p7, m7).  attends(p9, m7).  attends(p12, m7).  attends(p14, m7).
attends(p8, m8).  attends(p10, m8).  attends(p13, m8).  attends(p15, m8).
attends(p9, m9).  attends(p11, m9).  attends(p14, m9).  attends(p16, m9).
attends(p10, m10). attends(p12, m10). attends(p15, m10). attends(p17, m10).
attends(p11, m11). attends(p13, m11). attends(p16, m11). attends(p18, m11).
attends(p12, m12). attends(p14, m12). attends(p17, m12). attends(p19, m12).
attends(p13, m13). attends(p15, m13). attends(p18, m13). attends(p20, m13).
attends(p14, m14). attends(p16, m14). attends(p19, m14). attends(p1, m14).
attends(p15, m15). attends(p17, m15). attends(p20, m15). attends(p2, m15).
attends(p16, m16). attends(p18, m16). attends(p1, m16).  attends(p3, m16).
attends(p17, m17). attends(p19, m17). attends(p2, m17).  attends(p4, m17).
attends(p18, m18). attends(p20, m18). attends(p3, m18).  attends(p5, m18).
attends(p19, m19). attends(p1, m19).  attends(p4, m19).  attends(p6, m19).
attends(p20, m20). attends(p2, m20).  attends(p5, m20).  attends(p7, m20).

% Assignment choice rule: each meeting assigned to exactly one (day, slot, room)
1 { assigned(M, D, S, R) : day(D), slot(S), room(R) } 1 :- meeting(M).

% Constraint 1: No person can attend two meetings at the same (day, slot)
:- attends(P, M1), attends(P, M2), M1 != M2, 
   assigned(M1, D, S, _), assigned(M2, D, S, _).

% Constraint 2: Each room can host at most one meeting per (day, slot)
:- assigned(M1, D, S, R), assigned(M2, D, S, R), M1 != M2.

% Constraint 3: Each meeting must be assigned to a room with all required equipment
:- meeting(M), assigned(M, D, S, R), 
   requires_equipment(M, E), not has_equipment(R, E).

% Indicate feasibility
feasible :- meeting(M), assigned(M, D, S, R).

% Show the schedule
#show assigned/4.
#show feasible/0.