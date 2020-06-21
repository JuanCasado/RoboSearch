(define (problem probPlanetary) (:domain planetary) (:objects
 robot1 robot2 - robot
 LOCATION0 LOCATION1 LOCATION2 LOCATION3 LOCATION4 - location
 FAST - speedType
 task1 - taskType
)
(:init (= (totalTime) 0) (= (totalBattery) 0) (= (totalDistance) 0) (= (recharges) 0)
 (at robot1 LOCATION4)
(= (speed robot1 FAST) 80)(= (moveBurn robot1 FAST) 0.1)
(= (battery robot1) 5000) (= (maxBattery robot1) 5000) (= (rechargeRate robot1) 1)
(= (taskDuration robot1 task1) 20) (= (taskBurn robot1 task1) 1)

 (at robot2 LOCATION3)
(= (speed robot2 FAST) 80)(= (moveBurn robot2 FAST) 0.1)
(= (battery robot2) 5000) (= (maxBattery robot2) 5000) (= (rechargeRate robot2) 1)
(= (taskDuration robot2 task1) 20) (= (taskBurn robot2 task1) 1)


 (= (tasks LOCATION0 task1) 0)(= (tasks LOCATION1 task1) 0)(= (tasks LOCATION2 task1) 0)(= (tasks LOCATION3 task1) 0)(= (tasks LOCATION4 task1) 0)

  (= (distance LOCATION0 LOCATION1) 234) (= (distance LOCATION0 LOCATION2) 200) (= (distance LOCATION0 LOCATION3) 229) (= (distance LOCATION0 LOCATION4) 241) (= (distance LOCATION1 LOCATION0) 234)  (= (distance LOCATION1 LOCATION2) 434) (= (distance LOCATION1 LOCATION3) 280) (= (distance LOCATION1 LOCATION4) 346) (= (distance LOCATION2 LOCATION0) 200) (= (distance LOCATION2 LOCATION1) 434)  (= (distance LOCATION2 LOCATION3) 334) (= (distance LOCATION2 LOCATION4) 315) (= (distance LOCATION3 LOCATION0) 229) (= (distance LOCATION3 LOCATION1) 280) (= (distance LOCATION3 LOCATION2) 334)   (= (distance LOCATION4 LOCATION0) 241) (= (distance LOCATION4 LOCATION1) 346) (= (distance LOCATION4 LOCATION2) 315)  

 (connected LOCATION4 LOCATION2) (connected LOCATION4 LOCATION1) (connected LOCATION1 LOCATION0) (connected LOCATION4 LOCATION0) (connected LOCATION3 LOCATION1) (connected LOCATION2 LOCATION1) (connected LOCATION2 LOCATION4) (connected LOCATION1 LOCATION2) (connected LOCATION0 LOCATION3) (connected LOCATION1 LOCATION4) (connected LOCATION2 LOCATION3) (connected LOCATION0 LOCATION2) (connected LOCATION0 LOCATION1) (connected LOCATION2 LOCATION0) (connected LOCATION1 LOCATION3) (connected LOCATION3 LOCATION2) (connected LOCATION0 LOCATION4) (connected LOCATION3 LOCATION0)

)(:goal (and
 (= (tasks LOCATION2 task1) 1)
 (= (tasks LOCATION1 task1) 1)
 (= (tasks LOCATION0 task1) 5)
))
 (:metric minimize (totalTime))
)
