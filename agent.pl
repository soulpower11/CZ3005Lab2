- (dynamic[visited/2, wumpus/2, confundus/2, tingle/2, glitter/2, stench/2, safe/2, wall/2]).
:- (dynamic[confounded/0, stench/0, tingle/0, glitter/0, bump/0, scream/0]).
:- (dynamic[hasarrow/0]).
:- (dynamic[current/3]).
:- retractall(current(_, _, _)).
:- retractall(hasarrow).
:- assertz(current(0, 0, rnorth)).
:- assertz(hasarrow).
:- assertz(visited(0, 0)).
:- assertz(confounded).

reborn :-
    reposition([on, off, off, off, off, off]),
    retractall(hasarrow),
    assertz(hasarrow).

test :-
    assertz(explore([moveforward])).

move(A) :-
    (   A=shoot
    ->  shoot
    ;   A=moveforward
    ->  forward
    ;   A=turnleft
    ->  turnleft
    ;   A=turnright
    ->  turnright
    ;   A=pickup
    ->  pickup
    ).

shoot :-
    retract(hasarrow),
    retract(wumpus(_, _)),
    write(shoot).

forward :-
    current(X, Y, D),
    (   D=rnorth
    ->  Y1 is Y+1,
        (   bump
        ->  assertz(wall(X, Y1))
        ;   retractall(current(_, _, _)),
            assertz(visited(X, Y1)),
            assertz(current(X, Y1, D))
        )
    ;   D=rwest
    ->  X1 is X-1,
        (   bump
        ->  assertz(wall(X1, Y))
        ;   retractall(current(_, _, _)),
            assertz(visited(X1, Y)),
            assertz(current(X1, Y, D))
        )
    ;   D=reast
    ->  X1 is X+1,
        (   bump
        ->  assertz(wall(X1, Y))
        ;   retractall(current(_, _, _)),
            assertz(visited(X1, Y)),
            assertz(current(X1, Y, D))
        )
    ;   D=rsouth
    ->  Y1 is Y-1,
        (   bump
        ->  assertz(wall(X, Y1))
        ;   retractall(current(_, _, _)),
            assertz(visited(X, Y1)),
            assertz(current(X, Y1, D))
        )
    ).

turnleft :-
    current(X, Y, D),
    (   D=rnorth
    ->  retractall(current(_, _, _)),
        assertz(current(X, Y, rwest))
    ;   D=rwest
    ->  retractall(current(_, _, _)),
        assertz(current(X, Y, rsouth))
    ;   D=reast
    ->  retractall(current(_, _, _)),
        assertz(current(X, Y, rnorth))
    ;   D=rsouth
    ->  retractall(current(_, _, _)),
        assertz(current(X, Y, reast))
    ).

turnright :-
    current(X, Y, D),
    (   D=rnorth
    ->  retractall(current(_, _, _)),
        assertz(current(X, Y, reast))
    ;   D=rwest
    ->  retractall(current(_, _, _)),
        assertz(current(X, Y, rnorth))
    ;   D=reast
    ->  retractall(current(_, _, _)),
        assertz(current(X, Y, rsouth))
    ;   D=rsouth
    ->  retractall(current(_, _, _)),
        assertz(current(X, Y, rwest))
    ).

pickup :-
    current(X, Y, _),
    (   glitter(X, Y)
    ->  retract(glitter(X, Y)),
        retract(glitter)
    ).

confounded(A) :-
    (   A=on
    ->  (   not(confounded)
        ->  assertz(confounded)
        ;    !
        )
    ;   A=off
    ->  (   confounded
        ->  retract(confounded)
        ;    !
        )
    ).

stench(A) :-
    (   A=on
    ->  current(X, Y, _),
        assertz(stench(X, Y)),
        (   not(stench)
        ->  assertz(stench)
        ;    !
        )
    ;   A=off
    ->  (   stench
        ->  retract(stench)
        ;    !
        )
    ).

tingle(A) :-
    (   A=on
    ->  current(X, Y, _),
        assertz(tingle(X, Y)),
        (   not(tingle)
        ->  assertz(tingle)
        ;    !
        )
    ;   A=off
    ->  (   tingle
        ->  retract(tingle)
        ;    !
        )
    ).

glitter(A) :-
    (   A=on
    ->  current(X, Y, _),
        assertz(glitter(X, Y)),
        (   not(glitter)
        ->  assertz(glitter)
        ;    !
        )
    ;   A=off
    ->  (   glitter
        ->  retract(glitter)
        ;    !
        )
    ).

bump(A) :-
    (   A=on
    ->  (   not(bump)
        ->  assertz(bump)
        ;    !
        )
    ;   A=off
    ->  (   bump
        ->  retract(bump)
        ;    !
        )
    ).

scream(A) :-
    (   A=on
    ->  (   not(scream)
        ->  assertz(scream)
        ;    !
        )
    ;   A=off
    ->  (   scream
        ->  retract(scream)
        ;    !
        )
    ).

reposition([LA, LB, LC, LD, LE, LF]) :-
    retractall(visited(_, _)),
    retractall(wumpus(_, _)),
    retractall(confundus(_, _)),
    retractall(tingle(_, _)),
    retractall(glitter(_, _)),
    retractall(stench(_, _)),
    retractall(safe(_, _)),
    retractall(wall(_, _)),
    retractall(current(_, _, _)),
    assertz(current(0, 0, rnorth)),
    assertz(visited(0, 0)),
    confounded(LA),
    stench(LB),
    tingle(LC),
    glitter(LD),
    bump(LE),
    scream(LF).

move(A, [LA, LB, LC, LD, LE, LF]) :-
    confounded(LA),
    stench(LB),
    tingle(LC),
    glitter(LD),
    bump(LE),
    scream(LF),
    move(A).

explore([H|T]) :-
    (   write(H),
        H=moveforward
    ->  checksafe
    ;    !,
        length(T, L),
        L\=0
    ->  explore(T)
    ;    !
    ).

checksafe :-
    current(X, Y, D),
    (   D=rnorth
    ->  Y1 is Y+1,
        safe(X, Y1)
    ;   D=rwest
    ->  X1 is X-1,
        safe(X1, Y)
    ;   D=reast
    ->  X1 is X+1,
        safe(X1, Y)
    ;   D=rsouth
    ->  Y1 is Y-1,
        safe(X, Y1)
    ).