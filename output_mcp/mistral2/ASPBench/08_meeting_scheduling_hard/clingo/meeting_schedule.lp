% --- Domains ---
room(r1; r2; r3; r4).
meeting(m1; m2; m3; m4; m5; m6; m7; m8; m9; m10;
         m11; m12; m13; m14; m15; m16; m17; m18; m19; m20).
person(p1; p2; p3; p4; p5; p6; p7; p8; p9; p10;
       p11; p12; p13; p14; p15; p16; p17; p18; p19; p20).
day(1; 2; 3; 4; 5).
slot(1; 2; 3; 4).

% --- Equipment ---
equipment(projector; whiteboard; video; confcall).

% --- Room Equipment ---
room_equipment(r1, projector).
room_equipment(r1, whiteboard).
room_equipment(r1, video).
room_equipment(r1, confcall).

room_equipment(r2, projector).
room_equipment(r2, whiteboard).
room_equipment(r2, confcall).

room_equipment(r3, whiteboard).
room_equipment(r3, confcall).

room_equipment(r4, projector).
room_equipment(r4, video).

% --- Meeting Equipment Requirements ----
% m1, m11: projector
meeting_equipment(m1, projector).
meeting_equipment(m11, projector).

% m2, m12: whiteboard
meeting_equipment(m2, whiteboard).
meeting_equipment(m12, whiteboard).

% m3, m13: confcall
meeting_equipment(m3, confcall).
meeting_equipment(m13, confcall).

% m4, m14: video, projector
meeting_equipment(m4, video).
meeting_equipment(m4, projector).
meeting_equipment(m14, video).
meeting_equipment(m14, projector).

% m5, m15: projector, confcall
meeting_equipment(m5, projector).
meeting_equipment(m5, confcall).
meeting_equipment(m15, projector).
meeting_equipment(m15, confcall).

% m6, m16: whiteboard, confcall
meeting_equipment(m6, whiteboard).
meeting_equipment(m6, confcall).
meeting_equipment(m16, whiteboard).
meeting_equipment(m16, confcall).

% m7, m17: projector, whiteboard, confcall
meeting_equipment(m7, projector).
meeting_equipment(m7, whiteboard).
meeting_equipment(m7, confcall).
meeting_equipment(m17, projector).
meeting_equipment(m17, whiteboard).
meeting_equipment(m17, confcall).

% m8, m18: video, confcall
meeting_equipment(m8, video).
meeting_equipment(m8, confcall).
meeting_equipment(m18, video).
meeting_equipment(m18, confcall).

% m9, m19: projector, video
meeting_equipment(m9, projector).
meeting_equipment(m9, video).
meeting_equipment(m19, projector).
meeting_equipment(m19, video).

% m10, m20: projector, whiteboard
meeting_equipment(m10, projector).
meeting_equipment(m10, whiteboard).
meeting_equipment(m20, projector).
meeting_equipment(m20, whiteboard).

% --- Meeting Attendees ---
attends(m1, p1). attends(m1, p3). attends(m1, p6). attends(m1, p8).
attends(m2, p2). attends(m2, p4). attends(m2, p7). attends(m2, p9).
attends(m3, p3). attends(m3, p5). attends(m3, p8). attends(m3, p10).
attends(m4, p4). attends(m4, p6). attends(m4, p9). attends(m4, p11).
attends(m5, p5). attends(m5, p7). attends(m5, p10). attends(m5, p12).
attends(m6, p6). attends(m6, p8). attends(m6, p11). attends(m6, p13).
attends(m7, p7). attends(m7, p9). attends(m7, p12). attends(m7, p14).
attends(m8, p8). attends(m8, p10). attends(m8, p13). attends(m8, p15).
attends(m9, p9). attends(m9, p11). attends(m9, p14). attends(m9, p16).
attends(m10, p10). attends(m10, p12). attends(m10, p15). attends(m10, p17).
attends(m11, p11). attends(m11, p13). attends(m11, p16). attends(m11, p18).
attends(m12, p12). attends(m12, p14). attends(m12, p17). attends(m12, p19).
attends(m13, p13). attends(m13, p15). attends(m13, p18). attends(m13, p20).
attends(m14, p14). attends(m14, p16). attends(m14, p19). attends(m14, p1).
attends(m15, p15). attends(m15, p17). attends(m15, p20). attends(m15, p2).
attends(m16, p16). attends(m16, p18). attends(m16, p1). attends(m16, p3).
attends(m17, p17). attends(m17, p19). attends(m17, p2). attends(m17, p4).
attends(m18, p18). attends(m18, p20). attends(m18, p3). attends(m18, p5).
attends(m19, p19). attends(m19, p1). attends(m19, p4). attends(m19, p6).
attends(m20, p20). attends(m20, p2). attends(m20, p5). attends(m20, p7).

% --- Choice Rule: Assign each meeting to a (day, slot, room) ---
1 { assigned(M, D, S, R) : day(D), slot(S), room(R) } 1 :- meeting(M).

% --- Constraints ---

% 1. Person Availability: No person attends two meetings at the same (day, slot)
:- attends(M1, P), attends(M2, P), M1 != M2,
   assigned(M1, D, S, _), assigned(M2, D, S, _).

% 2. Room Occupancy: No room hosts two meetings at the same (day, slot)
:- assigned(M1, D, S, R), assigned(M2, D, S, R), M1 != M2.

% 3. Equipment Requirements: Room must have all equipment required by meeting
:- assigned(M, D, S, R),
   meeting_equipment(M, E),
   not room_equipment(R, E).

% --- Show the schedule ---
#show assigned/4.