:- (dynamic[visited/2, wumpus/2, confundus/2, tingle/2, glitter/2, stench/2, safe/2, wall/2]).
:- (dynamic[confounded/0, stench/0, tingle/0, glitter/0, bump/0, scream/0]).
:- (dynamic[hasarrow/0]).
:- (dynamic[current/3]).
:- (dynamic[explore/1]).
:- retractall(current(_, _, _)).
:- retractall(hasarrow).
:- assertz(current(0, 0, rnorth)).
:- assertz(hasarrow).
:- assertz(visited(0, 0)).
:- assertz(safe(0, 0)).
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
    (   hasarrow
    ->  retractall(hasarrow),
        scream
    ->  retractall(wumpus(_, _)),
        retractall(stench(_, _))
    ).

% addwall(X, Y) :-
%     (   bump
%     ->  (   not(wall(X, Y))
%         ->  assertz(wall(X, Y))
%         ;    !
%         )
%     ;   write(hello),
%         write(more)
%     ).

% forward :-
%     current(X, Y, D),
%     (   D=rnorth
%     ->  Y1 is Y+1,
%         (   bump
%         ->  assertz(wall(X, Y1))
%         ;   retractall(current(_, _, _)),
%             assertz(visited(X, Y1)),
%             assertz(safe(X, Y1)),
%             removeunsafe(X, Y1),
%             assertz(current(X, Y1, D))
%         )
%     ;   D=rwest
%     ->  X1 is X-1,
%         (   bump
%         ->  assertz(wall(X1, Y))
%         ;   retractall(current(_, _, _)),
%             assertz(visited(X1, Y)),
%             assertz(safe(X1, Y)),
%             removeunsafe(X1, Y),
%             assertz(current(X1, Y, D))
%         )
%     ;   D=reast
%     ->  X1 is X+1,
%         (   bump
%         ->  assertz(wall(X1, Y))
%         ;   retractall(current(_, _, _)),
%             assertz(visited(X1, Y)),
%             assertz(safe(X1, Y)),
%             removeunsafe(X1, Y),
%             assertz(current(X1, Y, D))
%         )
%     ;   D=rsouth
%     ->  Y1 is Y-1,
%         (   bump
%         ->  assertz(wall(X, Y1))
%         ;   retractall(current(_, _, _)),
%             assertz(visited(X, Y1)),
%             assertz(safe(X, Y1)),
%             removeunsafe(X, Y1),
%             assertz(current(X, Y1, D))
%         )
%     ).
removeunsafe(X, Y) :-
    (   wumpus(X, Y)
    ->  retract(wumpus(X, Y))
    ;    !
    ),
    (   confundus(X, Y)
    ->  retract(confundus(X, Y))
    ;    !
    ).

addsafe(X, Y) :-
    (   not(visited(X, Y))
    ->  assertz(visited(X, Y))
    ;    !
    ),
    (   not(safe(X, Y))
    ->  assertz(safe(X, Y))
    ;    !
    ).

forward :-
    current(X, Y, D),
    (   D=rnorth
    ->  Y1 is Y+1,
        (   bump
        ->  (   not(wall(X, Y1))
            ->  assertz(wall(X, Y1)),
                removeunsafe(X, Y1)
            ;    !
            )
        ;   retractall(current(_, _, _)),
            addsafe(X, Y1),
            removeunsafe(X, Y1),
            assertz(current(X, Y1, D))
        )
    ;   D=rwest
    ->  X1 is X-1,
        (   bump
        ->  (   not(wall(X1, Y))
            ->  assertz(wall(X1, Y)),
                removeunsafe(X1, Y)
            ;    !
            )
        ;   retractall(current(_, _, _)),
            addsafe(X1, Y),
            removeunsafe(X1, Y),
            assertz(current(X1, Y, D))
        )
    ;   D=reast
    ->  X1 is X+1,
        (   bump
        ->  (   not(wall(X1, Y))
            ->  assertz(wall(X1, Y)),
                removeunsafe(X1, Y)
            ;    !
            )
        ;   retractall(current(_, _, _)),
            addsafe(X1, Y),
            removeunsafe(X1, Y),
            assertz(current(X1, Y, D))
        )
    ;   D=rsouth
    ->  Y1 is Y-1,
        (   bump
        ->  (   not(wall(X, Y1))
            ->  assertz(wall(X, Y1)),
                removeunsafe(X, Y1)
            ;    !
            )
        ;   retractall(current(_, _, _)),
            addsafe(X, Y1),
            removeunsafe(X, Y1),
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

addwumpus(X, Y) :-
    (   (   not(wall(X, Y))
        ->  (   not(visited(X, Y))
            ->  (   not(wumpus(X, Y))
                ->  assertz(wumpus(X, Y))
                ;    !
                )
            )
        ;    !
        )
    ;    !
    ).


addstench(X, Y) :-
    (   not(stench(X, Y))
    ->  assertz(stench(X, Y))
    ;    !
    ).

% if stench the cell infront might have wumpus
stench(A) :-
    (   A=on
    ->  current(X, Y, D),
        (   D=rnorth
        ->  Y1 is Y+1,
            addwumpus(X, Y1),
            addstench(X, Y)
        ;   D=rwest
        ->  X1 is X-1,
            addwumpus(X1, Y),
            addstench(X, Y)
        ;   D=reast
        ->  X1 is X+1,
            addwumpus(X1, Y),
            addstench(X, Y)
        ;   D=rsouth
        ->  Y1 is Y-1,
            addwumpus(X, Y1),
            addstench(X, Y)
        ),
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

% stench(A) :-
%     (   A=on
%     ->  current(X, Y, D),
%         (   D=rnorth
%         ->  Y1 is Y+1,
%             Y2 is Y+2,
%             addwumpus(X, Y2),
%             addstench(X, Y1)
%         ;   D=rwest
%         ->  X1 is X-1,
%             X2 is X-2,
%             addwumpus(X2, Y),
%             addstench(X1, Y)
%         ;   D=reast
%         ->  X1 is X+1,
%             X2 is X+2,
%             addwumpus(X2, Y),
%             addstench(X1, Y)
%         ;   D=rsouth
%         ->  Y1 is Y-1,
%             Y2 is Y-2,
%             addwumpus(X, Y2),
%             addstench(X, Y1)
%         ),
%         (   not(stench)
%         ->  assertz(stench)
%         ;    !
%         )
%     ;   A=off
%     ->  (   stench
%         ->  retract(stench)
%         ;    !
%         )
%     ).
addtingle(X, Y) :-
    (   not(tingle(X, Y))
    ->  assertz(tingle(X, Y))
    ;    !
    ).

addconfundus(X, Y) :-
    (   (   not(wall(X, Y))
        ->  (   not(visited(X, Y))
            ->  (   not(confundus(X, Y))
                ->  assertz(confundus(X, Y))
                ;    !
                )
            )
        ;    !
        )
    ;    !
    ).


tingle(A) :-
    (   A=on
    ->  current(X, Y, D),
        (   D=rnorth
        ->  Y1 is Y+1,
            addconfundus(X, Y1),
            addtingle(X, Y)
        ;   D=rwest
        ->  X1 is X-1,
            addconfundus(X1, Y),
            addtingle(X, Y)
        ;   D=reast
        ->  X1 is X+1,
            addconfundus(X1, Y),
            addtingle(X, Y)
        ;   D=rsouth
        ->  Y1 is Y-1,
            addconfundus(X, Y1),
            addtingle(X, Y)
        ),
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

% tingle(A) :-
%     (   A=on
%     ->  current(X, Y, D),
%         (   D=rnorth
%         ->  Y1 is Y+1,
%             Y2 is Y+2,
%             addconfundus(X, Y2),
%             addtingle(X, Y1)
%         ;   D=rwest
%         ->  X1 is X-1,
%             X2 is X-2,
%             addconfundus(X2, Y),
%             addtingle(X1, Y)
%         ;   D=reast
%         ->  X1 is X+1,
%             X2 is X+2,
%             addconfundus(X2, Y),
%             addtingle(X1, Y)
%         ;   D=rsouth
%         ->  Y1 is Y-1,
%             Y2 is Y-2,
%             addconfundus(X, Y2),
%             addtingle(X, Y1)
%         ),
%         (   not(tingle)
%         ->  assertz(tingle)
%         ;    !
%         )
%     ;   A=off
%     ->  (   tingle
%         ->  retract(tingle)
%         ;    !
%         )
%     ).
addglitter(X, Y) :-
    (   not(glitter(X, Y))
    ->  assertz(glitter(X, Y))
    ;    !
    ).

glitter(A) :-
    (   A=on
    ->  current(X, Y, _),
        addglitter(X, Y),
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

% glitter(A) :-
%     (   A=on
%     ->  current(X, Y, D),
%         (   D=rnorth
%         ->  Y1 is Y+1,
%             addglitter(X, Y1)
%         ;   D=rwest
%         ->  X1 is X-1,
%             addglitter(X1, Y)
%         ;   D=reast
%         ->  X1 is X+1,
%             addglitter(X1, Y)
%         ;   D=rsouth
%         ->  Y1 is Y-1,
%             addglitter(X, Y1)
%         ),
%         (   not(glitter)
%         ->  assertz(glitter)
%         ;    !
%         )
%     ;   A=off
%     ->  (   glitter
%         ->  retract(glitter)
%         ;    !
%         )
%     ).
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
    assertz(safe(0, 0)),
    confounded(LA),
    stench(LB),
    tingle(LC),
    glitter(LD),
    bump(LE),
    scream(LF).

% move(A, [LA, LB, LC, LD, LE, LF]) :-
%     confounded(LA),
%     stench(LB),
%     tingle(LC),
%     glitter(LD),
%     bump(LE),
%     scream(LF),
%     move(A).
move(A, [LA, LB, LC, LD, LE, LF]) :-
    bump(LE),
    scream(LF),
    move(A),
    confounded(LA),
    stench(LB),
    tingle(LC),
    glitter(LD).

explore(L) :-
    (   checksafe
    ->  (   checkvisited
        ->  append([], [turnleft], L)
        ;   append([], [moveforward], L)
        )
    ;   append([], [turnleft], L)
    ).

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
        not(confundus(X, Y1)),
        not(wumpus(X, Y1)),
        not(wall(X, Y1))
    ;   D=rwest
    ->  X1 is X-1,
        not(confundus(X1, Y)),
        not(wumpus(X1, Y)),
        not(wall(X1, Y))
    ;   D=reast
    ->  X1 is X+1,
        not(confundus(X1, Y)),
        not(wumpus(X1, Y)),
        not(wall(X1, Y))
    ;   D=rsouth
    ->  Y1 is Y-1,
        not(confundus(X, Y1)),
        not(wumpus(X, Y1)),
        not(wall(X, Y1))
    ).

checkvisited :-
    current(X, Y, D),
    (   D=rnorth
    ->  Y1 is Y+1,
        visited(X, Y1)
    ;   D=rwest
    ->  X1 is X-1,
        visited(X1, Y)
    ;   D=reast
    ->  X1 is X+1,
        visited(X1, Y)
    ;   D=rsouth
    ->  Y1 is Y-1,
        visited(X, Y1)
    ).