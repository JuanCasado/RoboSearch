(define (problem probPlanetary) (:domain planetary) (:objects
 ROBOT1 ROBOT2 - robot
 LOCATION0 LOCATION1 LOCATION2 LOCATION3 LOCATION4 LOCATION5 - location
 SLOW FAST - speedType
 DRILL PHOTO - taskType
)
(:init (= (totalTime) 0) (= (totalBattery) 0) (= (totalDistance) 0) (= (recharges) 0)
 (at ROBOT1 LOCATION3)
(= (speed ROBOT1 FAST) 40)(= (moveBurn ROBOT1 FAST) 4)
 (= (speed ROBOT1 SLOW) 20)(= (moveBurn ROBOT1 SLOW) 3)
(= (battery ROBOT1) 20) (= (maxBattery ROBOT1) 400) (= (rechargeRate ROBOT1) 0.001)
(= (taskDuration ROBOT1 DRILL) 40) (= (taskBurn ROBOT1 DRILL) 1)
 (= (taskDuration ROBOT1 PHOTO) 30) (= (taskBurn ROBOT1 PHOTO) 1)

 (at ROBOT2 LOCATION2)
(= (speed ROBOT2 FAST) 40)(= (moveBurn ROBOT2 FAST) 4)
 (= (speed ROBOT2 SLOW) 20)(= (moveBurn ROBOT2 SLOW) 3)
(= (battery ROBOT2) 20) (= (maxBattery ROBOT2) 400) (= (rechargeRate ROBOT2) 0.001)
(= (taskDuration ROBOT2 DRILL) 40) (= (taskBurn ROBOT2 DRILL) 1)
 (= (taskDuration ROBOT2 PHOTO) 30) (= (taskBurn ROBOT2 PHOTO) 1)


 (= (tasks LOCATION0 DRILL) 0)(= (tasks LOCATION1 DRILL) 0)(= (tasks LOCATION2 DRILL) 0)(= (tasks LOCATION3 DRILL) 0)(= (tasks LOCATION4 DRILL) 0)(= (tasks LOCATION5 DRILL) 0)(= (tasks LOCATION0 PHOTO) 0)(= (tasks LOCATION1 PHOTO) 0)(= (tasks LOCATION2 PHOTO) 0)(= (tasks LOCATION3 PHOTO) 0)(= (tasks LOCATION4 PHOTO) 0)(= (tasks LOCATION5 PHOTO) 0)

  (= (distance LOCATION0 LOCATION1) 350) (= (distance LOCATION0 LOCATION2) 286) (= (distance LOCATION0 LOCATION3) 234) (= (distance LOCATION0 LOCATION4) 133) (= (distance LOCATION0 LOCATION5) 251) (= (distance LOCATION1 LOCATION0) 350)  (= (distance LOCATION1 LOCATION2) 129) (= (distance LOCATION1 LOCATION3) 250) (= (distance LOCATION1 LOCATION4) 243) (= (distance LOCATION1 LOCATION5) 99) (= (distance LOCATION2 LOCATION0) 286) (= (distance LOCATION2 LOCATION1) 129)   (= (distance LOCATION2 LOCATION4) 226) (= (distance LOCATION2 LOCATION5) 101) (= (distance LOCATION3 LOCATION0) 234) (= (distance LOCATION3 LOCATION1) 250)   (= (distance LOCATION3 LOCATION4) 111) (= (distance LOCATION3 LOCATION5) 188) (= (distance LOCATION4 LOCATION0) 133) (= (distance LOCATION4 LOCATION1) 243) (= (distance LOCATION4 LOCATION2) 226) (= (distance LOCATION4 LOCATION3) 111)  (= (distance LOCATION4 LOCATION5) 150) (= (distance LOCATION5 LOCATION0) 251) (= (distance LOCATION5 LOCATION1) 99) (= (distance LOCATION5 LOCATION2) 101) (= (distance LOCATION5 LOCATION3) 188) (= (distance LOCATION5 LOCATION4) 150) 

 (connected LOCATION1 LOCATION4) (connected LOCATION1 LOCATION2) (connected LOCATION2 LOCATION5) (connected LOCATION0 LOCATION1) (connected LOCATION5 LOCATION4) (connected LOCATION3 LOCATION0) (connected LOCATION2 LOCATION4) (connected LOCATION4 LOCATION0) (connected LOCATION4 LOCATION3) (connected LOCATION5 LOCATION2) (connected LOCATION1 LOCATION3) (connected LOCATION1 LOCATION0) (connected LOCATION2 LOCATION0) (connected LOCATION5 LOCATION3) (connected LOCATION0 LOCATION5) (connected LOCATION5 LOCATION0) (connected LOCATION0 LOCATION4) (connected LOCATION0 LOCATION2) (connected LOCATION3 LOCATION1) (connected LOCATION4 LOCATION1) (connected LOCATION0 LOCATION3) (connected LOCATION5 LOCATION1) (connected LOCATION2 LOCATION1) (connected LOCATION3 LOCATION5) (connected LOCATION4 LOCATION5) (connected LOCATION3 LOCATION4) (connected LOCATION1 LOCATION5) (connected LOCATION4 LOCATION2)

)(:goal (and
 (= (tasks LOCATION4 DRILL) 3)
 (= (tasks LOCATION0 PHOTO) 2)
 (= (tasks LOCATION0 DRILL) 4)
 (= (tasks LOCATION5 DRILL) 2)
 (= (tasks LOCATION1 PHOTO) 6)
))
 (:metric minimize (totalTime))
)
