:- (dynamic[visited/2, wumpus/2, confundus/2, tingle/2, glitter/2, stench/2, safe/2, wall/2]).
:- (dynamic[confounded/0, stench/0, tingle/0, glitter/0, bump/0, scream/0]).
:- (dynamic[hasarrow/0]).
:- (dynamic[current/3]).
:- (dynamic[tempcurrent/3]).
:- retractall(current(_, _, _)).
:- retractall(hasarrow).
:- assertz(current(0, 0, rnorth)).
:- assertz(hasarrow).
% :- assertz(visited(0, 0)).
:- assertz(safe(0, 0)).
:- assertz(confounded).

reborn :-
    reposition([on, off, off, off, off, off]),
    retractall(hasarrow),
    assertz(hasarrow).

same([], []).

same([H1|R1], [H2|R2]) :-
    H1=H2,
    same(R1, R2).

upto(Low,High,_Step,Low) :- Low =< High.
upto(Low,High,Step,Var) :-
    Inc is Low+Step,
    Inc =< High,
    upto(Inc, High, Step, Var).

downto(Low,High,_Step,High) :- Low =< High.
downto(Low,High,Step,Var) :-
    Dec is High-Step,
    Dec >= Low,
    downto(Low, Dec, Step, Var).

switch(X, [Val:Goal|Cases]) :-
    ( X=Val ->
        call(Goal)
    ;
        switch(X, Cases)
    ).

test3 :-
    X1 is 1,
    X2 is 0,
    X is X2-X1,
    writeln(X),
    switch(X, [
        -1 : writeln(case1),
        b : writeln(case2),
        c : writeln(case3)
    ]).

test :-
    checkunvisitedsafecell,
    nb_getval(unvisitedlist, L),
    write(L),
    test2(L).

test2([H|_]) :-
    current(X, Y, _),
    H=(X, Y).
    
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

removeunsafe(X, Y) :-
    (   wumpus(X, Y)
    ->  retract(wumpus(X, Y))
    ;    !
    ),
    (   confundus(X, Y)
    ->  retract(confundus(X, Y))
    ;    !
    ).

removewrongsafe(X, Y) :-
    (   safe(X, Y)
    ->  retract(safe(X, Y))
    ;    !
    ).

addsafe(X, Y) :-
    (   not(safe(X, Y))
    ->  assertz(safe(X, Y))
    ;    !
    ).

addvisited(X, Y) :-
    (   not(visited(X, Y))
    ->  assertz(visited(X, Y))
    ;    !
    ).

forward :-
    current(X, Y, D),
    (   D=rnorth
    ->  Y1 is Y+1,
        (   bump
        ->  (   not(wall(X, Y1))
            ->  assertz(wall(X, Y1)),
                removewrongsafe(X, Y1),
                removeunsafe(X, Y1)
            ;    !
            )
        ;   retractall(current(_, _, _)),
            addsafe(X, Y1),
            addvisited(X, Y),
            removeunsafe(X, Y1),
            assertz(current(X, Y1, D))
        )
    ;   D=rwest
    ->  X1 is X-1,
        (   bump
        ->  (   not(wall(X1, Y))
            ->  assertz(wall(X1, Y)),
                removewrongsafe(X1, Y),
                removeunsafe(X1, Y)
            ;    !
            )
        ;   retractall(current(_, _, _)),
            addsafe(X1, Y),
            addvisited(X, Y),
            removeunsafe(X1, Y),
            assertz(current(X1, Y, D))
        )
    ;   D=reast
    ->  X1 is X+1,
        (   bump
        ->  (   not(wall(X1, Y))
            ->  assertz(wall(X1, Y)),
                removewrongsafe(X1, Y),
                removeunsafe(X1, Y)
            ;    !
            )
        ;   retractall(current(_, _, _)),
            addsafe(X1, Y),
            addvisited(X, Y),
            removeunsafe(X1, Y),
            assertz(current(X1, Y, D))
        )
    ;   D=rsouth
    ->  Y1 is Y-1,
        (   bump
        ->  (   not(wall(X, Y1))
            ->  assertz(wall(X, Y1)),
                removewrongsafe(X, Y1),
                removeunsafe(X, Y1)
            ;    !
            )
        ;   retractall(current(_, _, _)),
            addsafe(X, Y1),
            addvisited(X, Y),
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

addwumpus :-
    current(X, Y, _),
    X1 is X+1,
    X2 is X-1,
    Y1 is Y+1,
    Y2 is Y-1,
    (   not(wall(X1, Y)),
        not(visited(X1, Y)),
        not(safe(X1,Y)),
        not(confundus(X1,Y))
    ->  addwumpus(X1, Y)
    ;    !
    ),
    (   not(wall(X2, Y)),
        not(visited(X2, Y)),
        not(safe(X2,Y)),
        not(confundus(X2,Y))
    ->  addwumpus(X2, Y)
    ;    !
    ),
    (   not(wall(X, Y1)),
        not(visited(X, Y1)),
        not(safe(X,Y1)),
        not(confundus(X,Y1))
    ->  addwumpus(X, Y1)
    ;    !
    ),
    (   not(wall(X, Y2)),
        not(visited(X, Y2)),
        not(safe(X,Y2)),
        not(confundus(X,Y2))
    ->  addwumpus(X, Y2)
    ;    !
    ).

addwumpus(X, Y) :-
    (   not(wumpus(X, Y))
    ->  assertz(wumpus(X, Y))
    ;    !
    ).

addstench(X, Y) :-
    (   not(stench(X, Y))
    ->  assertz(stench(X, Y))
    ;    !
    ).

% if stench the cell infront might have wumpus
stench(A) :-
    (   A=on,
        current(X, Y, _),
        addwumpus,
        addstench(X, Y),
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

addtingle(X, Y) :-
    (   not(tingle(X, Y))
    ->  assertz(tingle(X, Y))
    ;    !
    ).

addconfundus :-
    current(X, Y, _),
    X1 is X+1,
    X2 is X-1,
    Y1 is Y+1,
    Y2 is Y-1,
    (   not(wall(X1, Y)),
        not(visited(X1, Y)),
        not(safe(X1,Y)),
        not(wumpus(X1,Y))
    ->  addconfundus(X1, Y)
    ;    !
    ),
    (   not(wall(X2, Y)),
        not(visited(X2, Y)),
        not(safe(X2,Y)),
        not(wumpus(X2,Y))
    ->  addconfundus(X2, Y)
    ;    !
    ),
    (   not(wall(X, Y1)),
        not(visited(X, Y1)),
        not(safe(X,Y1)),
        not(wumpus(X,Y1))
    ->  addconfundus(X, Y1)
    ;    !
    ),
    (   not(wall(X, Y2)),
        not(visited(X, Y2)),
        not(safe(X,Y2)),
        not(wumpus(X,Y2))
    ->  addconfundus(X, Y2)
    ;    !
    ).

addconfundus(X, Y) :-
    (   not(confundus(X, Y))
    ->  assertz(confundus(X, Y))
    ;    !
    ).

tingle(A) :-
    (   A=on
    ->  current(X, Y, _),
        addconfundus,
        addtingle(X, Y),
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

checksurroundsafe :-
    (   current(X, Y, _),
        X1 is X+1,
        X2 is X-1,
        Y1 is Y+1,
        Y2 is Y-1,
        not(tingle),
        not(stench)
    ->  (   not(wall(X1, Y))
        ->  removeunsafe(X1,Y),
            addsafe(X1, Y)
        ;    !
        ),
        (   not(wall(X2, Y))
        ->  removeunsafe(X2,Y),
            addsafe(X2, Y)
        ;    !
        ),
        (   not(wall(X, Y1))
        ->  removeunsafe(X,Y1),
            addsafe(X, Y1)
        ;    !
        ),
        (   not(wall(X, Y2))
        ->  removeunsafe(X,Y2),
            addsafe(X, Y2)
        ;    !
        )
    ;    !
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
    % assertz(visited(0, 0)),
    assertz(safe(0, 0)),
    confounded(LA),
    stench(LB),
    tingle(LC),
    glitter(LD),
    bump(LE),
    scream(LF).

move(A, [LA, LB, LC, LD, LE, LF]) :-
    bump(LE),
    scream(LF),
    move(A),
    confounded(LA),
    stench(LB),
    tingle(LC),
    glitter(LD),
    checksurroundsafe,
    removewrongprediction.

removewrongprediction:-
    current(X, Y, _),
        X1 is X+1,
        X2 is X-1,
        Y1 is Y+1,
        Y2 is Y-1,
        stench ->
        (   not(wall(X1, Y)),
    confundus(X1,Y)
        ->  retract(confundus(X1,Y)),
            addsafe(X1, Y)
        ;    !
        ),
        (   not(wall(X2, Y)),
    confundus(X2,Y)
        ->  retract(confundus(X2,Y)),
            addsafe(X2, Y)
        ;    !
        ),
        (   not(wall(X, Y1)),
    confundus(X,Y1)
        ->  retract(confundus(X,Y1)),
            addsafe(X, Y1)
        ;    !
        ),
        (   not(wall(X, Y2)),
    confundus(X,Y2)
        ->  retract(confundus(X,Y2)),
            addsafe(X, Y2)
        ;    !
        )   ,
tingle ->
(   not(wall(X1, Y)),
    wumpus(X1,Y)
->  retract(wumpus(X1,Y)),
    addsafe(X1, Y)
;    !
),
(   not(wall(X2, Y)),
wumpus(X2,Y)
->  retract(wumpus(X2,Y)),
    addsafe(X2, Y)
;    !
),
(   not(wall(X, Y1)),
wumpus(X,Y1)
->  retract(wumpus(X,Y1)),
    addsafe(X, Y1)
;    !
),
(   not(wall(X, Y2)),
wumpus(X,Y2)
->  retract(wumpus(X,Y2)),
    addsafe(X, Y2)
;    !
).

addtoglitterlist(X) :-
    nb_getval(glitterlist, L),
    append(L, X, NL),
    nb_setval(glitterlist, NL).

addtosafelist(X) :-
    nb_getval(safelist, L),
    append(L, X, NL),
    nb_setval(safelist, NL).

addtovisitedlist(X) :-
    nb_getval(visitedlist, L),
    append(L, X, NL),
    nb_setval(visitedlist, NL).

checkunvisitedsafecell :-
    (   
        nb_delete(safelist),
        nb_delete(visitedlist),
        nb_delete(unvisitedlist),
        nb_setval(safelist, []),
        nb_setval(visitedlist, []),
        nb_setval(unvisitedlist, []),
        forall(safe(X, Y),
               addtosafelist([[X,Y]])),
        forall(visited(X, Y),
               addtovisitedlist([[X,Y]])),
        nb_getval(safelist, SL),
        nb_getval(visitedlist, VL),
        not(same(SL, VL))
    ->  nb_getval(safelist, SL),
        nb_getval(visitedlist, VL),
        subtract(SL, VL, L),
        nb_setval(unvisitedlist, L)
    ).

getglitterlist :-
    nb_delete(glitterlist),
    nb_setval(glitterlist, []),
    forall(glitter(X, Y), addtoglitterlist([[X,Y]])).
    

explore(L) :-
    ((confounded) 
    ->  L=[moveforward]
    ;   
        current(X,Y,D),
        addvisited(X, Y),
        retractall(tempcurrent(_, _, _)),
        assertz(tempcurrent(X,Y,D)),
        nb_setval(movelist, []),
        checkunvisitedsafecell,
        nb_getval(unvisitedlist, UVL),
        % writeln('UVL:'),
        % writeln(UVL),
        length(UVL, Length),
        (Length=0
        ->  
            getglitterlist,
            nb_getval(glitterlist, GL),
            % writeln('GL:'),
            % writeln(GL),
            length(GL, GLength),
            (GLength \= 0 
            -> getpickuplist(GL)
            ;  !
            ),
            getmovelistYX([[0,0]])
        ;   getmovelistYX(UVL)
        ),
        nb_getval(movelist, ML),
        length(ML, Length2),
        ( (Length2=0, Length \=0)
        ->  
            getmovelistXY(UVL)
        ;   getmovelistYX([[0,0]])
        ),
        nb_getval(movelist, L)
    ).

getpickuplist([H|T]) :-
    movetolocationYX(H),
    nb_getval(movelist, List),
    append(List, [pickup], NL),
    nb_setval(movelist, NL),
    length(T, L),
    L\=0
    ->  getpickuplist(T); !.   

getmovelistXY([H|_]) :-
        movetolocationXY(H).
        % length(T, L),
        % L\=0
        % ->  getmovelistXY(T); !.
    
gototargetXY(StartX, EndX, StartY, EndY):-
    ((StartX \= EndX; StartY \= EndY) ->
        moveX(StartY, EndY),
        moveY(StartX, EndX),
        tempcurrent(NStartX,NStartY,_),
        gototargetXY(NStartX, EndX, NStartY, EndY)
    ;   !
    ). 

movetolocationXY([EndX,EndY]):-
    tempcurrent(StartX,StartY,_),
    gototargetXY(StartX, EndX, StartY, EndY).

getmovelistYX([H|_]) :-
    movetolocationYX(H).
    % length(T, L),
    % L\=0
    % ->  getmovelistYX(T); !.

gototargetYX(StartX, EndX, StartY, EndY):-
    ((StartX \= EndX; StartY \= EndY) ->
        moveY(StartY, EndY),
        moveX(StartX, EndX),
        tempcurrent(NStartX,NStartY,_),
        gototargetYX(NStartX, EndX, NStartY, EndY)
    ;   !
    ).

movetolocationYX([EndX,EndY]):-
    tempcurrent(StartX,StartY,_),
    gototargetYX(StartX, EndX, StartY, EndY).

changedirection(G):-
    tempcurrent(X,Y,D),
    nb_getval(movelist, L),
    D \= G ->
    (   D=rnorth
        ->  append(L, [turnright], NL),
            nb_setval(movelist, NL),
            retractall(tempcurrent(_, _, _)),
            assertz(tempcurrent(X, Y, reast)),
            changedirection(G)
        ;   D=rwest
        ->  append(L, [turnright], NL),
            nb_setval(movelist, NL),
            retractall(tempcurrent(_, _, _)),
            assertz(tempcurrent(X, Y, rnorth)),
            changedirection(G)
        ;   D=reast
        ->  append(L, [turnright], NL),
            nb_setval(movelist, NL),
            retractall(tempcurrent(_, _, _)),
            assertz(tempcurrent(X, Y, rsouth)),
            changedirection(G)
        ;   D=rsouth
        ->  append(L, [turnright], NL),
            nb_setval(movelist, NL),
            retractall(tempcurrent(_, _, _)),
            assertz(tempcurrent(X, Y, rwest)),
            changedirection(G)
    ); !.

addmoveforwardX(X) :-
    tempcurrent(_,Y,D),
    nb_getval(stop, S),
    % write('stop: '),
    % writeln(S),
    ((safe(X,Y), S=0)
    ->  retractall(tempcurrent(_, _, _)),
        assertz(tempcurrent(X, Y, D)),
        nb_getval(movelist, L),
        append(L, [moveforward], NL),
        nb_setval(movelist, NL)
    ;  nb_setval(stop, 1)
    ).

addmoveforwardY(Y) :-
    tempcurrent(X,_,D),
    nb_getval(stop, S),
    % write('stop: '),
    % writeln(S),
    ((safe(X,Y), S=0)
    ->  retractall(tempcurrent(_, _, _)),
        assertz(tempcurrent(X, Y, D)),
        nb_getval(movelist, L),
        append(L, [moveforward], NL),
        nb_setval(movelist, NL)
     ;  nb_setval(stop, 1)
     ).

moveX(S,E):-
    nb_delete(stop),
    nb_setval(stop, 0),
    (   S<E
    ->  changedirection(reast),
        S1 is S+1,
        forall(upto(S1,E,1,X1),addmoveforwardX(X1))
    ;   S>E 
    ->  changedirection(rwest),
        S1 is S-1,
        forall(downto(E,S1,1,X1),addmoveforwardX(X1))
    ;   !
    ).

moveY(S,E):-
    nb_delete(stop),
    nb_setval(stop, 0),
    (   S<E
    ->  changedirection(rnorth),
        S1 is S+1,
        forall(upto(S1,E,1,Y1),addmoveforwardY(Y1))
    ;   S>E
    ->  changedirection(rsouth),
        S1 is S-1,
        forall(downto(E,S1,1,Y1),addmoveforwardY(Y1))
    ;   !
    ).