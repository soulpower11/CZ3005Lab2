%% returns true if the Agent has already visited position(X,Y), else returns false
:- dynamic visited/2.

%% returns true if the Agent has reasoned that the Wumpus is or possibly can be at position(X,Y), else returns false
:- dynamic wumpus/2.

%% returns true if the Agent has reasoned that a Confundus portal is or possibly can be at position(X,Y), else returns false
:- dynamic confundus/2.

%% returns true if the Agent knows that a there is a Tingle at position(X,Y), else returns false
:- dynamic tingle/2.

%% returns true if the Agent knows that a there is a Glitter at position(X,Y), else returns false
:- dynamic glitter/2.

%% returns true if the Agent knows that a there is a Stench at position(X,Y), else returns false
:- dynamic stench/2.

%% returns true if the Agent has reasoned that there is a wall at position(X,Y), else returns false
:- dynamic wall/2.

%% returns true if the Agent has an arrow
:- dynamic arrow/1.

%% keeps track of the number of coins Agent currently holds
:- dynamic num_of_coins/1.

%% keeps track of whether the wumpus is alive or not
:- dynamic wumpus_alive/1.

:- dynamic certified_no_confundus/2.
:- dynamic certified_no_wumpus/2.

%% returns true if the Agent has reasoned that position(X,Y) is safe i.e. does not contain a Wumpus or a Confundus portal
safe(X,Y):-
  (
		\+ wumpus(X,Y), \+ confundus(X,Y)
	) ;
	visited(X,Y);
	certified_safe(X,Y).

%% returns true if (X,Y) is the current relative position and D is the current relative orientation of the Agent
:- dynamic current/3.

%% implements Agent's reset due to arriving into a cell
%% removes memory of all previous steps and sensory readings
%% reset relative position and return arrow to Agent
reborn:-
	retractall(visited(_,_)), retractall(wumpus(_,_)), retractall(confundus(_,_)), 
	retractall(tingle(_,_)), retractall(glitter(_,_)), retractall(stench(_,_)),
	retractall(arrow(_)), retractall(wumpus_alive(_)), retractall(current(_,_,_)),
	assert(current(0,0,rnorth)), assert(arrow(1)), assert(wumpus_alive(1)),
	assert(num_of_coins(0)), assert(visited(0,0)).

%% implements Agent's reset due to game start or arrival to a cell inhabited by a Confundus Portal
%% initial sensory information of the new cell given
reposition([Confunded|[Stench|[Tingle|[Glitter|[Bump|[Scream]]]]]]):-
	retractall(visited(_,_)), retractall(wumpus(_,_)), retractall(confundus(_,_)),
	retractall(tingle(_,_)), retractall(glitter(_,_)), retractall(stench(_,_)),
	retractall(current(_,_,_)), assert(current(0,0,rnorth)).
	%% assert(confundus(0,0)),	%% indicate relative origin
  %% check_stench_indicator(Stench).

%% update relative direction when turnleft action given
change_relative_direction(Dir):-
	Dir == turnleft, current(X,Y,D),
	(
		( 
			D == rnorth, NewDir = rwest,		%% facing north turn left is west
			retract(current(X,Y,D)), assert(current(X,Y,NewDir))
		);
		(
			D == rwest, NewDir = rsouth,	%% facing west turn left is south
			retract(current(X,Y,D)), assert(current(X,Y,NewDir))
		);
		(
			D == reast, NewDir = rnorth,	%% facing east turn left is north
			retract(current(X,Y,D)), assert(current(X,Y,NewDir))
		);
		(
			D == rsouth, NewDir = reast,		%% facing south turn left is east
			retract(current(X,Y,D)), assert(current(X,Y,NewDir))
		)
	).

%% update relative direction when turnright action given
change_relative_direction(Dir):-
	Dir == turnright, current(X,Y,D),
	(
		( D == rnorth, NewDir = reast, retract(current(X,Y,D)), assert(current(X,Y,NewDir)) );
		( D == rwest, NewDir = rnorth, retract(current(X,Y,D)), assert(current(X,Y,NewDir)) );
		( D == reast, NewDir = rsouth, retract(current(X,Y,D)), assert(current(X,Y,NewDir)) );
		( D == rsouth, NewDir = rwest, retract(current(X,Y,D)), assert(current(X,Y,NewDir)) )
	).

%% update current position if Agent took one step forward in the Relative North direction
update_current_pos:-
	current(X,Y,D), D == rnorth, Ynew is Y + 1,
	retract(current(X,Y,D)), assert(current(X,Ynew,D)), assert(visited(X,Ynew)).

%% update current position if Agent took one step forward in the Relative West direction
update_current_pos:-
	current(X,Y,D), D == rwest, Xnew is X - 1,
	retract(current(X,Y,D)), assert(current(Xnew,Y,D)), assert(visited(Xnew,Y)).

%% update current position if Agent took one step forward in the Relative East direction
update_current_pos:-
	current(X,Y,D), D == reast, Xnew is X + 1,
	retract(current(X,Y,D)), assert(current(Xnew,Y,D)), assert(visited(Xnew,Y)).

%% update current position if Agent took one step forward in the Relative South direction
update_current_pos:-
	current(X,Y,D), D == rsouth, Ynew is Y - 1,
	retract(current(X,Y,D)), assert(current(X,Ynew,D)), assert(visited(X,Ynew)).

%% assert wumpus if not already present in the database
assert_wumpus_if_not_present(X,Y):-
	(
		\+ wumpus(X,Y), \+ visited(X,Y), \+ certified_no_wumpus(X,Y),
		\+ tingle(X,Y), assert(wumpus(X,Y))
	);
	true.

%% check that stench indicator is on
%% if stench is on, add to the possible wumpus positions
check_stench_indicator(A):-
	A == off ;
	( 
		A == on, current(X,Y,D), assert(stench(X,Y)),
		Ynorth is Y + 1, XEast is X + 1, XWest is X - 1, Ysouth is Y - 1,
		assert_wumpus_if_not_present(X,Ynorth), assert_wumpus_if_not_present(XEast,Y),
		assert_wumpus_if_not_present(XWest,Y), assert_wumpus_if_not_present(X,Ysouth)
	).

%% assert confundus if not already present in the database
assert_confundus_if_not_present(X,Y):-
  (
		\+ confundus(X,Y), \+ visited(X,Y), \+ certified_no_confundus(X,Y),
		\+ stench(X,Y), assert(confundus(X,Y))
	);
	true.

%% check that tingle indicator is on
%% if tingle is on, add to the possible confundus positions
check_tingle_indicator(A):-
	A == off ;
	( 
		A == on, current(X,Y,D), assert(tingle(X,Y)),
		Ynorth is Y + 1, XEast is X + 1, XWest is X - 1, Ysouth is Y - 1,
		assert_confundus_if_not_present(X,Ynorth), assert_confundus_if_not_present(XEast,Y),
		assert_confundus_if_not_present(XWest,Y), assert_confundus_if_not_present(X,Ysouth)
	).

%% assert glitter if not already present in the database
assert_glitter_if_not_present(X,Y):-
 (
		\+ glitter(X,Y), assert(glitter(X,Y))
 );
 true.

%% increment the number of coins
increment_coins(N):-
	AddCoin is N + 1,
	retractall(num_of_coins(_)),
	assert(num_of_coins(AddCoin)).

%% check that glitter indicator is on
check_glitter_indicator(A):-
	A == off ;
	( 
		A == on, current(X,Y,D),
		assert_glitter_if_not_present(X,Y)
	).

%% if any of the wall cells have been reasoned as possible confundus or wumpus previously, remove those reasonings
remove_any_confundus_wumpus_from_wall(X,Y):-
	(
		(confundus(X,Y), wumpus(X,Y), retract(confundus(X,Y), retract(wumpus(X,Y))));
		(wumpus(X,Y), retract(wumpus(X,Y)));
		(confundus(X,Y), retract(confundus(X,Y)));
		true
	).

%% Agent moves forward and encounters a Confundus portal
move(Action,[Confunded|[Stench|[Tingle|[Glitter|[Bump|[Scream]]]]]]):-
	Confunded == on, Action == moveforward,
	reposition([on,off,off,off,off,off]).

%% Agent moves forward and encounters a Wall
move(Action,[Confunded|[Stench|[Tingle|[Glitter|[Bump|[Scream]]]]]]):-
	Action == moveforward, Bump == on, current(X,Y,D),
	(
		( D == rnorth, Ynew is Y + 1, remove_any_confundus_wumpus_from_wall(X,Ynew), assert(wall(X,Ynew)) );
		( D == rsouth, Ynew is Y - 1, remove_any_confundus_wumpus_from_wall(X,Ynew), assert(wall(X,Ynew)) );
		( D == rwest, Xnew is X - 1, remove_any_confundus_wumpus_from_wall(Xnew,Y), assert(wall(Xnew,Y)) );
		( D == reast, Xnew is X + 1, remove_any_confundus_wumpus_from_wall(Xnew,Y), assert(wall(Xnew,Y)) )
	).

%% Agent turns left
move(Action,[Confunded|[Stench|[Tingle|[Glitter|[Bump|[Scream]]]]]]):-
	Action == turnleft,
	change_relative_direction(Action).

%% Agent turns right
move(Action,[Confunded|[Stench|[Tingle|[Glitter|[Bump|[Scream]]]]]]):-
	Action == turnright,
	change_relative_direction(turnright).

%% Agent moves forward and encounter either a Stench, Tingle and/or Glitter
move(Action,[Confunded|[Stench|[Tingle|[Glitter|[Bump|[Scream]]]]]]):-
	Action == moveforward, update_current_pos,
	check_stench_indicator(Stench), check_tingle_indicator(Tingle), check_glitter_indicator(Glitter).

%% Agent asked to pick up a coin
move(Action, [Confunded|[Stench|[Tingle|[Glitter|[Bump|[Scream]]]]]]):-
	Action == pickup, current(X,Y,D), glitter(X,Y),
	num_of_coins(N), increment_coins(N),
	retract(glitter(X,Y)).

%% Agent shoots its arrow
move(Action, [Confunded|[Stench|[Tingle|[Glitter|[Bump|[Scream]]]]]]):-
	Action == shoot,
	(
		(
			arrow(1), retract(arrow(1)), assert(arrow(0)),
			(
				( Scream == on, retract(wumpus_alive(1)), assert(wumpus_alive(0)), retractall(stench(_,_)), retractall(wumpus(_,_)) );
				( Scream == off )
			)
		);
		true
	).

%% when inside a cell with only a tingle, we check the cell above, below, to the left and to the right of the current cell for wumpus
%% Since we are inside a cell with only a tingle, a wumpus cannot exist in those four locations since the current cell does not have a stench
%% we remove the wumpus markings from these cells and certify that these cells do not contain a wumpus
check_for_possible_wumpus(X,Y,Xtop,Ytop,Xleft,Yleft,Xright,Yright,Xbot,Ybot):-
	(
		(wumpus(Xtop, Ytop), retract(wumpus(Xtop, Ytop)), assert(certified_no_wumpus(Xtop, Ytop))); true
	),
	(
		(wumpus(Xleft, Yleft), retract(wumpus(Xleft, Yleft)), assert(certified_no_wumpus(Xleft, Yleft))); true
	),
	(
		(wumpus(Xright, Yright), retract(wumpus(Xright, Yright)), assert(certified_no_wumpus(Xright, Yright))); true
	),
	(
		(wumpus(Xbot, Ybot), retract(wumpus(Xbot, Ybot)), assert(certified_no_wumpus(Xbot, Ybot))); true
	).


%% Decide what action to take when in a cell with only a tingle
%% Check for possible wumpus in the surrounding cells to remove any wumpus
%% Look for a cell in the surrounding cells that we can safely navigate to e.g. a visited cell or a cell certified not to contain a confundus,
decide_next_step_when_tingle(X,Y,D,L):-
	Xtop is X, Ytop is Y+1,
	Xleft is X-1, Yleft is Y,
	Xright is X+1, Yright is Y,
	Xbot is X, Ybot is Y-1,
	check_for_possible_wumpus(X,Y,Xtop,Ytop,Xleft,Yleft,Xright,Yright,Xbot,Ybot),
	(
		(
			\+ confundus(Xtop,Ytop),
			(
				( (D == rsouth; D == rwest), L = turnright );
				( D == reast, L = turnleft );
				( D == rnorth, L = moveforward )
			)
		);
		(
			\+ confundus(Xleft,Yleft),
			(
				( (D == rsouth; D == reast), L = turnright );
				( D == rnorth, L = turnleft	);
				( D == rwest, L = moveforward )
			)
		);
		(
			\+ confundus(Xright,Yright),
			(
				( (D == rsouth; D == rwest), L = turnleft );
				( D == rnorth, L = turnright );
				( D == reast, L = moveforward )
			)
		);
		(
			\+ confundus(Xbot,Ybot),
			(
				( D == rsouth, L = moveforward );
				( (D == rnorth; D == reast), L = turnright );
				( D == rwest, L = turnleft )
			)
		)
	).

%% when inside a cell with only a stench, we check the cell above, below, to the left and to the right of the current cell for confundus
%% Since we are inside a cell with only a stench, a confundus cannot exist in those four locations since the current cell does not have a tingle
%% we remove the confundus markings from these cells and certify that these cells do not contain a confundus
check_for_possible_confundus(X,Y,Xtop,Ytop,Xleft,Yleft,Xright,Yright,Xbot,Ybot):-
	(
		(confundus(Xtop, Ytop), retract(confundus(Xtop, Ytop)), assert(certified_no_confundus(Xtop, Ytop))); true
	),
	(
		(confundus(Xleft, Yleft), retract(confundus(Xleft, Yleft)), assert(certified_no_confundus(Xleft, Yleft))); true
	),
	(
		(confundus(Xright, Yright), retract(confundus(Xright, Yright)), assert(certified_no_confundus(Xright, Yright))); true
	),
	(
		(confundus(Xbot, Ybot), retract(confundus(Xbot, Ybot)), assert(certified_no_confundus(Xbot, Ybot))); true
	).

%% When we have found 3 stenches on the map we can kill the wumpus, this is because we either have two vertical stenches and one horizontal stench surrounding the wumpus
%% or two horizontal stenches and one vertical stenches surrounding the wumpus
%% In this case we have two vertical stenches and one horizontal stench surrounding the wumpus
%% to find the two vertical stenches, we just need to compare the coordinates and find the two coordinates with the same x-coordinate
find_index_of_stench_vertical_coordinates(A,B,List):-
	(
		(
			nth0(0, List, First),
			nth0(1, List, Second),
			nth0(0, First, FirstElemOfFirstCoord),
			nth0(0, Second, FirstElemOfSecondCoord),
			FirstElemOfFirstCoord == FirstElemOfSecondCoord,
			A is 0, B is 1
		);
		(
			nth0(0, List, First),
			nth0(2, List, Third),
			nth0(0, First, FirstElemOfFirstCoord),
			nth0(0, Third, FirstElemOfThirdCoord),
			FirstElemOfFirstCoord == FirstElemOfThirdCoord,
			A is 0, B is 2
		);
		(
			nth0(1, List, Second),
			nth0(2, List, Third),
			nth0(0, Second, FirstElemOfSecondCoord),
			nth0(0, Third, FirstElemOfThirdCoord),
			FirstElemOfSecondCoord == FirstElemOfThirdCoord,
			A is 1, B is 2
		)
	).

%% When we have found 3 stenches on the map we can kill the wumpus, this is because we either have two vertical stenches and one horizontal stench surrounding the wumpus
%% or two horizontal stenches and one vertical stenches surrounding the wumpus
%% In this case we have two horizontal stenches and one vertical stench surrounding the wumpus
%% to find the two horizontal stenches, we just need to compare the coordinates and find the two coordinates with the same y-coordinate
find_index_of_stench_horizontal_coordinates(A,B,List):-
	(
		(
			nth0(0, List, First),
			nth0(1, List, Second),
			nth0(1, First, SecondElemOfFirstCoord),
			nth0(1, Second, SecondElemOfSecondCoord),
			SecondElemOfFirstCoord == SecondElemOfSecondCoord,
			A is 0, B is 1
		);
		(
			nth0(0, List, First),
			nth0(2, List, Third),
			nth0(1, First, SecondElemOfFirstCoord),
			nth0(1, Third, SecondElemOfThirdCoord),
			SecondElemOfFirstCoord == SecondElemOfThirdCoord,
			A is 0, B is 2
		);
		(
			nth0(1, List, Second),
			nth0(2, List, Third),
			nth0(1, Second, SecondElemOfSecondCoord),
			nth0(1, Third, SecondElemOfThirdCoord),
			SecondElemOfSecondCoord == SecondElemOfThirdCoord,
			A is 1, B is 2
		)
	).

%% Once we have found the two coordinate of the vertical stenches, we know that the x-coordinate of the wumpus is the same as the x-coordinates of the vertical stenches
%% To find the y-coordinate of the wumpus, we take the sum of the y-coordinates of the vertical stenches and divide it by two
find_wumpus_coordinates_from_vertical_stench_coord(Coord1, Coord2, Xcoord, Ycoord):-
	nth0(0, Coord1, Xcoord),
	nth0(1, Coord1, Ycoord1),
	nth0(1, Coord2, Ycoord2),
	Ycoord is (Ycoord1 + Ycoord2)/2.

%% Once we have found the two coordinate of the horizontal stenches, we know that the y-coordinate of the wumpus is the same as the y-coordinates of the horizontal stenches
%% To find the x-coordinate of the wumpus, we take the sum of the x-coordinates of the horizontal stenches and divide it by two
find_wumpus_coordinates_from_horizontal_stench_coord(Coord1, Coord2, Xcoord, Ycoord):-
	nth0(1, Coord1, Ycoord),
	nth0(0, Coord1, Xcoord1),
	nth0(0, Coord2, Xcoord2),
	Xcoord is (Xcoord1 + Xcoord2)/2.

%% We check for wumpus using the vertical stenches and derive the wumpus exact coordinates
%% We then choose the appropriate action for the agent
%% If agent is directly faceing the wumpus, our next action is to shoot an arrow
%% if agent is facing away from the wumpus, we either turnleft or turnright depending on where Agent is facing to face the wumpus
%% return false if we cannot find wumpus coordinates
check_for_vertical_stenches(L,CurX,CurY,D):-
	(
		findall([X,Y],stench(X,Y),List),
		find_index_of_stench_vertical_coordinates(A,B,List),
		nth0(A, List, Coord1),
		nth0(B, List, Coord2),
		find_wumpus_coordinates_from_vertical_stench_coord(Coord1, Coord2, Xcoord, Ycoord),
		(
			(
				CurX==Xcoord, CurY<Ycoord,
				(
					(D == rnorth, L = shoot);
					((D == rwest; D == rsouth), L = turnright);
					(D == reast, L = turnleft)
				)
			);
			(
				CurX==Xcoord, CurY>Ycoord,
				(
					(D == rsouth, L = shoot);
					((D == rnorth; D == rwest), L = turnleft);
					(D == reast, L = turnright)
				)
			);
			(
				CurX<Xcoord, CurY==Ycoord,
				(
					(D == reast, L = shoot);
					((D == rsouth; D == rwest), L = turnleft);
					(D == rnorth, L = turnright)
				)
			);
			(
				CurX>Xcoord, CurY==Ycoord,
				(
					(D == rwest, L = shoot);
					((D == rnorth; D == reast), L = turnleft);
					(D == rsouth, L = turnright)
				)
			)
		)
	);
	false.

%% We check for wumpus using the horizontal stenches and derive the wumpus exact coordinates
%% We then choose the appropriate action for the agent
%% If agent is directly faceing the wumpus, our next action is to shoot an arrow
%% if agent is facing away from the wumpus, we either turnleft or turnright depending on where Agent is facing to face the wumpus
%% return false if we cannot find wumpus coordinates
check_for_horizontal_stenches(L,CurX,CurY,D):-
	(
		findall([X,Y],stench(X,Y),List),
		find_index_of_stench_horizontal_coordinates(A,B,List),
		nth0(A, List, Coord1),
		nth0(B, List, Coord2),
		find_wumpus_coordinates_from_horizontal_stench_coord(Coord1, Coord2, Xcoord, Ycoord),
		(
			(
				CurX==Xcoord, CurY<Ycoord,
				(
					(D == rnorth, L = shoot);
					((D == rwest; D == rsouth), L = turnright);
					(D == reast, L = turnleft)
				)
			);
			(
				CurX==Xcoord, CurY>Ycoord,
				(
					(D == rsouth, L = shoot);
					((D == rnorth; D == rwest), L = turnleft);
					(D == reast, L = turnright)
				)
			);
			(
				CurX<Xcoord, CurY==Ycoord,
				(
					(D == reast, L = shoot);
					((D == rsouth; D == rwest), L = turnleft);
					(D == rnorth, L = turnright)
				)
			);
			(
				CurX>Xcoord, CurY==Ycoord,
				(
					(D == rwest, L = shoot);
					((D == rnorth; D == reast), L = turnleft);
					(D == rsouth, L = turnright)
				)
			)
		)
	);
	false.

%% Action to take when Agent is on a cell with a stench
%% Check and remove Confundus that cannot exist in the surrounding cells
%% If stench count is 3, take action to kill wumpus
%% else navigate to a safe location
decide_next_step_when_stench(X,Y,D,L):-
	Xtop is X, Ytop is Y+1,
	Xleft is X-1, Yleft is Y,
	Xright is X+1, Yright is Y,
	Xbot is X, Ybot is Y-1,
	check_for_possible_confundus(X,Y,Xtop,Ytop,Xleft,Yleft,Xright,Yright,Xbot,Ybot),
	(
		(
			aggregate_all(count, stench(X1,Y1), StenchCount),
			StenchCount == 3,
			(
				check_for_vertical_stenches(L,X,Y,D);
				check_for_horizontal_stenches(L,X,Y,D)
			)
		);
		(
			(
				\+ wumpus(Xtop,Ytop),
				(
					( (D == rsouth; D == rwest), L = turnright );
					( D == reast, L = turnleft );
					( D == rnorth, L = moveforward )
				)
			);
			(
				\+ wumpus(Xright,Yright),
				(
					( (D == rsouth; D == rwest), L = turnleft );
					( D == rnorth; L = turnright );
					( D == reast, L = moveforward )
				)
			);
			(
				\+ wumpus(Xleft,Yleft),
				(
					( (D == rsouth; D == reast ), L = turnright );
					( D == rnorth; L = turnleft );
					( D == rwest, L = moveforward )
				)	
			);
			(
				\+ wumpus(Xbot,Ybot),
				(
					( D == rsouth, L = moveforward );
					( (D == rnorth; D == reast), L = turnright );
					( D == rwest, L = turnleft )
				)
			)
		)
	).

%% Action to take when Agent is on a cell with both a stench and a tingle
%% If stench count is 3, take action to kill wumpus
%% else navigate to a safe location
decide_next_step_when_stench_and_tingle(X,Y,D,L):-
	Xtop is X, Ytop is Y+1,
	Xleft is X-1, Yleft is Y,
	Xright is X+1, Yright is Y,
	Xbot is X, Ybot is Y-1,
	(
		(
			aggregate_all(count, stench(X1,Y1), StenchCount),
			StenchCount == 3,
			(
				check_for_vertical_stenches(L,X,Y,D);
				check_for_horizontal_stenches(L,X,Y,D)
			)
		);
		(
			\+ wumpus(Xtop,Ytop), \+ confundus(Xtop,Ytop),
			(
				( (D == rsouth; D == rwest), L = turnright );
				( D == reast, L = turnleft );
				( D == rnorth, L = moveforward )
			)
		);
		(
			\+ wumpus(Xleft,Yleft), \+ confundus(Xleft,Yleft),
			(
				( (D == rsouth; D == reast), L = turnright );
				( D == rnorth, L = turnleft	);
				( D == rwest, L = moveforward )
			)
		);
		(
			\+ wumpus(Xright,Yright), \+ confundus(Xright,Yright),
			(
				( (D == rsouth; D == rwest), L = turnleft );
				( D == rnorth, L = turnright );
				( D == reast, L = moveforward )
			)
		);
		(
			\+ wumpus(Xbot,Ybot), \+confundus(Xbot,Ybot),
			(
				( D == rsouth, L = moveforward );
				( (D == rnorth; D == reast), L = turnright );
				( D == rwest, L = turnleft )
			)
		)
	).

%% When all four surrounding cells have been visited before, we sort and check for the cell with the least visits
%% return the direction of the cell with least visits e.g. if the least visited cell is the top cell, we return rnorth
check_visited_count(X,Y,Dir):-
	Xtop is X, Ytop is Y+1,
	Xleft is X-1, Yleft is Y,
	Xright is X+1, Yright is Y,
	Xbot is X, Ybot is Y-1,
	( 
		((wall(Xtop,Ytop); confundus(Xtop,Ytop); wumpus(Xtop,Ytop)), TopCount is 1000000);
		aggregate_all(count, visited(Xtop,Ytop), TopCount)
	),
	( 
		((wall(Xleft,Yleft); confundus(Xleft,Yleft); wumpus(Xleft,Yleft)), LeftCount is 1000000);
		aggregate_all(count, visited(Xleft,Yleft), LeftCount)
	),
	( 
		((wall(Xright,Yright); confundus(Xright,Yright); wumpus(Xright,Yright)), RightCount is 1000000);
		aggregate_all(count, visited(Xright,Yright), RightCount)
	),
	( 
		((wall(Xbot,Ybot); confundus(Xbot,Ybot); wumpus(Xbot,Ybot)), BotCount is 1000000);
		aggregate_all(count, visited(Xbot,Ybot), BotCount)
	),
	sort([TopCount, LeftCount, RightCount, BotCount], A),
	nth0(0, A, First),
	(
		(First is TopCount, Dir = rnorth);
		(First is LeftCount, Dir = rwest);
		(First is RightCount, Dir = reast);
		(First is BotCount, Dir = rsouth)
	).

%% decide what action to take when we are in a safe cell, no stench and/or tingle
%% Check the surrounding cells for wumpus and/or confundus markings, since this cell does not have both stench and tingle,
%% there is no reason for surrounding cells to have wumpus and/or confundus
%% then look for a safe spot to move to
decide_next_step_when_safe(X,Y,D,L):-
	Xtop is X, Ytop is Y+1,
	Xleft is X-1, Yleft is Y,
	Xright is X+1, Yright is Y,
	Xbot is X, Ybot is Y-1,
	check_for_possible_wumpus(X,Y,Xtop,Ytop,Xleft,Yleft,Xright,Yright,Xbot,Ybot),
	check_for_possible_confundus(X,Y,Xtop,Ytop,Xleft,Yleft,Xright,Yright,Xbot,Ybot),
	(
		(
			\+ visited(Xtop,Ytop), \+ wall(Xtop,Ytop), \+ confundus(Xtop,Ytop), \+ wumpus(Xtop,Ytop),
			(
				( (D == rsouth; D == rwest), L = turnright );
				( D == reast, L = turnleft );
				( D == rnorth, L = moveforward )
			)
		);
		(
			\+ visited(Xleft,Yleft), \+ wall(Xleft, Yleft), \+ confundus(Xleft,Yleft), \+ wumpus(Xleft,Yleft),
			(
				( (D == rsouth; D == reast), L = turnright );
				( D == rnorth, L = turnleft	);
				( D == rwest, L = moveforward )
			)
		);
		(
			\+ visited(Xbot,Ybot), \+ wall(Xbot, Ybot), \+ confundus(Xbot,Ybot), \+ wumpus(Xbot,Ybot),
			(
				( D == rsouth, L = moveforward );
				( (D == rnorth; D == reast), L = turnright );
				( D == rwest, L = turnleft )
			)		
		);
		(
			\+ visited(Xright,Yright), \+ wall(Xright, Yright), \+ confundus(Xright,Yright), \+ wumpus(Xright,Yright),
			(
				( (D == rsouth; D == rwest), L = turnleft );
				( D == rnorth, L = turnright );
				( D == reast, L = moveforward )
			)
		);
		(
			check_visited_count(X,Y,Dir),
			(
				(
					Dir == rnorth,
					(
						( (D == rsouth; D == rwest), L = turnright );
						( D == rnorth, L = moveforward );
						( D == reast, L = turnleft )
					)
				);
				(
					Dir == rwest,
					(
						( (D == rnorth; D == reast), L = turnleft );
						( D == rsouth, L = turnright );
						( D == rwest, L = moveforward)
					)
				);
				(
					Dir == rsouth,
					(
						( (D == rnorth; D == rwest), L = turnleft );
						( D == reast, L = turnright );
						( D == rsouth, L = moveforward)
					)
				);
				(
					Dir == reast,
					(
						( (D == rnorth; D == rwest), L = turnright );
						( D == rsouth, L = turnleft );
						( D == reast, L = moveforward)
					)
				)
			)
		)
	).

%% explore function
%% either Agent is provided with an action to determine if it is a safe action to take
%% or the function returns an action that leads to a safe path
explore(L):-
	current(X,Y,D),CurrentX = X, CurrentY = Y,
	(
		( glitter(CurrentX,CurrentY), L = pickup );
		( tingle(CurrentX,CurrentY), stench(CurrentX, CurrentY), decide_next_step_when_stench_and_tingle(X,Y,D,L) );
		( tingle(X,Y), decide_next_step_when_tingle(X,Y,D,L) );
		( stench(X,Y), decide_next_step_when_stench(X,Y,D,L) );
		decide_next_step_when_safe(X,Y,D,L)
	).