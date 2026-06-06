% --- Domain Facts ---
room(r1; r2; r3; r4).
meeting(m1; m2; m3; m4; m5; m6; m7; m8; m9; m10; m11; m12; m13; m14; m15; m16; m17; m18; m19; m20).
day(1..5).
slot(1..4).
person(p1; p2; p3; p4; p5; p6; p7; p8; p9; p10; p11; p12; p13; p14; p15; p16; p17; p18; p19; p20).

time(D, S) :- day(D), slot(S).

% --- Room Equipment ---
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

equipment(projector; whiteboard; video; confcall).

% --- Meeting Equipment Requirements ---
% m1, m11: projector
% m2, m12: whiteboard
% m3, m13: confcall
% m4, m14: video, projector
% m5, m15: projector, confcall
% m6, m16: whiteboard, confcall
% m7, m17: projector, whiteboard, confcall
% m8, m18: video, confcall
% m9, m19: projector, video
% m10, m20: projector, whiteboard

% m1, m11
requires_equip(m1, projector).
requires_equip(m11, projector).

% m2, m12
requires_equip(m2, whiteboard).
requires_equip(m12, whiteboard).

% m3, m13
requires_equip(m3, confcall).
requires_equip(m13, confcall).

% m4, m14
requires_equip(m4, video).
requires_equip(m4, projector).
requires_equip(m14, video).
requires_equip(m14, projector).

% m5, m15
requires_equip(m5, projector).
requires_equip(m5, confcall).
requires_equip(m15, projector).
requires_equip(m15, confcall).

% m6, m16
requires_equip(m6, whiteboard).
requires_equip(m6, confcall).
requires_equip(m16, whiteboard).
requires_equip(m16, confcall).

% m7, m17
requires_equip(m7, projector).
requires_equip(m7, whiteboard).
requires_equip(m7, confcall).
requires_equip(m17, projector).
requires_equip(m17, whiteboard).
requires_equip(m17, confcall).

% m8, m18
requires_equip(m8, video).
requires_equip(m8, confcall).
requires_equip(m18, video).
requires_equip(m18, confcall).

% m9, m19
requires_equip(m9, projector).
requires_equip(m9, video).
requires_equip(m19, projector).
requires_equip(m19, video).

% m10, m20
requires_equip(m10, projector).
requires_equip(m10, whiteboard).
requires_equip(m20, projector).
requires_equip(m20, whiteboard).

% --- Meeting Attendees ---
attends(m1, p1; p3; p6; p8).
attends(m2, p2; p4; p7; p9).
attends(m3, p3; p5; p8; p10).
attends(m4, p4; p6; p9; p11).
attends(m5, p5; p7; p10; p12).
attends(m6, p6; p8; p11; p13).
attends(m7, p7; p9; p12; p14).
attends(m8, p8; p10; p13; p15).
attends(m9, p9; p11; p14; p16).
attends(m10, p10; p12; p15; p17).
attends(m11, p11; p13; p16; p18).
attends(m12, p12; p14; p17; p19).
attends(m13, p13; p15; p18; p20).
attends(m14, p14; p16; p19; p1).
attends(m15, p15; p17; p20; p2).
attends(m16, p16; p18; p1; p3).
attends(m17, p17; p19; p2; p4).
attends(m18, p18; p20; p3; p5).
attends(m19, p19; p1; p4; p6).
attends(m20, p20; p2; p5; p7).

% --- Constraint 1: Assignment ---
% Each meeting assigned to exactly one (day, slot, room)
1 { assigned(M, D, S, R) : day(D), slot(S), room(R) } 1 :- meeting(M).

% --- Constraint 2: Person Availability ---
% No person attends two meetings at the same (day, slot)
:- assigned(M1, D, S, _), assigned(M2, D, S, _), M1 != M2,
   attends(M1, P), attends(M2, P).

% --- Constraint 3: Room Occupancy ---
% Each room can host at most one meeting per (day, slot)
:- assigned(M1, D, S, R), assigned(M2, D, S, R), M1 != M2.

% --- Constraint 4: Equipment Requirements ---
% Meeting must be assigned to a room that has all required equipment
:- assigned(M, _, _, R), requires_equip(M, E), not has_equipment(R, E).

% --- Show Results ---
#show assigned/4.
#show feasible/1.

% Feasibility indicator
feasible(true) :- #count { M : meeting(M) } = 20.