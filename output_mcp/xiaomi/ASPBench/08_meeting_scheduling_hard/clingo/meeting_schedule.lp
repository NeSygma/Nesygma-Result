% ==========================================
% Meeting Scheduling Problem
% Schedule 20 meetings across 4 rooms and 5 days
% ==========================================

% ============ DOMAINS ============
% Rooms
room(r1). room(r2). room(r3). room(r4).

% Meetings
meeting(m1). meeting(m2). meeting(m3). meeting(m4). meeting(m5).
meeting(m6). meeting(m7). meeting(m8). meeting(m9). meeting(m10).
meeting(m11). meeting(m12). meeting(m13). meeting(m14). meeting(m15).
meeting(m16). meeting(m17). meeting(m18). meeting(m19). meeting(m20).

% People
person(p1). person(p2). person(p3). person(p4). person(p5).
person(p6). person(p7). person(p8). person(p9). person(p10).
person(p11). person(p12). person(p13). person(p14). person(p15).
person(p16). person(p17). person(p18). person(p19). person(p20).

% Days and Time Slots
day(1). day(2). day(3). day(4). day(5).
slot(1). slot(2). slot(3). slot(4).

% ============ ROOM EQUIPMENT ============
% r1: projector, whiteboard, video, confcall
has_equipment(r1, projector). has_equipment(r1, whiteboard).
has_equipment(r1, video). has_equipment(r1, confcall).

% r2: projector, whiteboard, confcall
has_equipment(r2, projector). has_equipment(r2, whiteboard).
has_equipment(r2, confcall).

% r3: whiteboard, confcall
has_equipment(r3, whiteboard). has_equipment(r3, confcall).

% r4: projector, video
has_equipment(r4, projector). has_equipment(r4, video).

% ============ MEETING EQUIPMENT REQUIREMENTS ============
% m1, m11: projector
requires(m1, projector). requires(m11, projector).

% m2, m12: whiteboard
requires(m2, whiteboard). requires(m12, whiteboard).

% m3, m13: confcall
requires(m3, confcall). requires(m13, confcall).

% m4, m14: video, projector
requires(m4, video). requires(m4, projector).
requires(m14, video). requires(m14, projector).

% m5, m15: projector, confcall
requires(m5, projector). requires(m5, confcall).
requires(m15, projector). requires(m15, confcall).

% m6, m16: whiteboard, confcall
requires(m6, whiteboard). requires(m6, confcall).
requires(m16, whiteboard). requires(m16, confcall).

% m7, m17: projector, whiteboard, confcall
requires(m7, projector). requires(m7, whiteboard). requires(m7, confcall).
requires(m17, projector). requires(m17, whiteboard). requires(m17, confcall).

% m8, m18: video, confcall
requires(m8, video). requires(m8, confcall).
requires(m18, video). requires(m18, confcall).

% m9, m19: projector, video
requires(m9, projector). requires(m9, video).
requires(m19, projector). requires(m19, video).

% m10, m20: projector, whiteboard
requires(m10, projector). requires(m10, whiteboard).
requires(m20, projector). requires(m20, whiteboard).

% ============ MEETING ATTENDEES ============
% m1: p1, p3, p6, p8
attendee(m1, p1). attendee(m1, p3). attendee(m1, p6). attendee(m1, p8).

% m2: p2, p4, p7, p9
attendee(m2, p2). attendee(m2, p4). attendee(m2, p7). attendee(m2, p9).

% m3: p3, p5, p8, p10
attendee(m3, p3). attendee(m3, p5). attendee(m3, p8). attendee(m3, p10).

% m4: p4, p6, p9, p11
attendee(m4, p4). attendee(m4, p6). attendee(m4, p9). attendee(m4, p11).

% m5: p5, p7, p10, p12
attendee(m5, p5). attendee(m5, p7). attendee(m5, p10). attendee(m5, p12).

% m6: p6, p8, p11, p13
attendee(m6, p6). attendee(m6, p8). attendee(m6, p11). attendee(m6, p13).

% m7: p7, p9, p12, p14
attendee(m7, p7). attendee(m7, p9). attendee(m7, p12). attendee(m7, p14).

% m8: p8, p10, p13, p15
attendee(m8, p8). attendee(m8, p10). attendee(m8, p13). attendee(m8, p15).

% m9: p9, p11, p14, p16
attendee(m9, p9). attendee(m9, p11). attendee(m9, p14). attendee(m9, p16).

% m10: p10, p12, p15, p17
attendee(m10, p10). attendee(m10, p12). attendee(m10, p15). attendee(m10, p17).

% m11: p11, p13, p16, p18
attendee(m11, p11). attendee(m11, p13). attendee(m11, p16). attendee(m11, p18).

% m12: p12, p14, p17, p19
attendee(m12, p12). attendee(m12, p14). attendee(m12, p17). attendee(m12, p19).

% m13: p13, p15, p18, p20
attendee(m13, p13). attendee(m13, p15). attendee(m13, p18). attendee(m13, p20).

% m14: p14, p16, p19, p1
attendee(m14, p14). attendee(m14, p16). attendee(m14, p19). attendee(m14, p1).

% m15: p15, p17, p20, p2
attendee(m15, p15). attendee(m15, p17). attendee(m15, p20). attendee(m15, p2).

% m16: p16, p18, p1, p3
attendee(m16, p16). attendee(m16, p18). attendee(m16, p1). attendee(m16, p3).

% m17: p17, p19, p2, p4
attendee(m17, p17). attendee(m17, p19). attendee(m17, p2). attendee(m17, p4).

% m18: p18, p20, p3, p5
attendee(m18, p18). attendee(m18, p20). attendee(m18, p3). attendee(m18, p5).

% m19: p19, p1, p4, p6
attendee(m19, p19). attendee(m19, p1). attendee(m19, p4). attendee(m19, p6).

% m20: p20, p2, p5, p7
attendee(m20, p20). attendee(m20, p2). attendee(m20, p5). attendee(m20, p7).

% ============ DECISION VARIABLES ============
% Each meeting is assigned to exactly one (day, slot, room)
1 { assigned(M, D, S, R) : day(D), slot(S), room(R) } 1 :- meeting(M).

% ============ CONSTRAINTS ============

% Constraint 1: Equipment Requirements
% A meeting can only be assigned to a room that has all required equipment
:- assigned(M, D, S, R), requires(M, E), not has_equipment(R, E).

% Constraint 2: Room Occupancy
% Each room can host at most one meeting per (day, slot)
:- assigned(M1, D, S, R), assigned(M2, D, S, R), M1 != M2.

% Constraint 3: Person Availability
% No person can attend two meetings at the same (day, slot)
:- assigned(M1, D, S, R1), assigned(M2, D, S, R2), M1 != M2, attendee(M1, P), attendee(M2, P).

% ============ OUTPUT ============
#show assigned/4.