% Domains
meeting(m1..m20).
room(r1; r2; r3; r4).
day(1..5).
slot(1..4).
person(p1..p20).
equipment(projector; whiteboard; video; confcall).

% Room Equipment
room_has(r1, projector). room_has(r1, whiteboard). room_has(r1, video). room_has(r1, confcall).
room_has(r2, projector). room_has(r2, whiteboard). room_has(r2, confcall).
room_has(r3, whiteboard). room_has(r3, confcall).
room_has(r4, projector). room_has(r4, video).

% Meeting Equipment Requirements
meeting_needs(m1, projector). meeting_needs(m11, projector).
meeting_needs(m2, whiteboard). meeting_needs(m12, whiteboard).
meeting_needs(m3, confcall). meeting_needs(m13, confcall).
meeting_needs(m4, video). meeting_needs(m4, projector). meeting_needs(m14, video). meeting_needs(m14, projector).
meeting_needs(m5, projector). meeting_needs(m5, confcall). meeting_needs(m15, projector). meeting_needs(m15, confcall).
meeting_needs(m6, whiteboard). meeting_needs(m6, confcall). meeting_needs(m16, whiteboard). meeting_needs(m16, confcall).
meeting_needs(m7, projector). meeting_needs(m7, whiteboard). meeting_needs(m7, confcall). meeting_needs(m17, projector). meeting_needs(m17, whiteboard). meeting_needs(m17, confcall).
meeting_needs(m8, video). meeting_needs(m8, confcall). meeting_needs(m18, video). meeting_needs(m18, confcall).
meeting_needs(m9, projector). meeting_needs(m9, video). meeting_needs(m19, projector). meeting_needs(m19, video).
meeting_needs(m10, projector). meeting_needs(m10, whiteboard). meeting_needs(m20, projector). meeting_needs(m20, whiteboard).

% Meeting Attendees
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

% 1. Assignment: Each meeting must be assigned to exactly one (day, slot, room)
1 { assigned(M, D, S, R) : day(D), slot(S), room(R) } 1 :- meeting(M).

% 2. Person Availability: No person can attend two meetings at the same (day, slot)
:- assigned(M1, D, S, R1), assigned(M2, D, S, R2), M1 != M2, attends(M1, P), attends(M2, P).

% 3. Room Occupancy: Each room can host at most one meeting per (day, slot)
:- assigned(M1, D, S, R), assigned(M2, D, S, R), M1 != M2.

% 4. Equipment Requirements: Each meeting must be assigned to a room that has all required equipment
:- assigned(M, D, S, R), meeting_needs(M, E), not room_has(R, E).

#show assigned/4.