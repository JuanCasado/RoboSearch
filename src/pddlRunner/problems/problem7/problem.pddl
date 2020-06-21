(define (problem probPlanetary) (:domain planetary) (:objects
 robot1 robot2 - robot
 LOCATION0 LOCATION1 LOCATION2 LOCATION3 LOCATION4 LOCATION5 - location
 FAST - speedType
 task2 task1 - taskType
)
(:init (= (totalTime) 0) (= (totalBattery) 0) (= (totalDistance) 0) (= (recharges) 0)
 (at robot1 LOCATION0)
(= (speed robot1 FAST) 40)(= (moveBurn robot1 FAST) 1)
(= (battery robot1) 200) (= (maxBattery robot1) 400) (= (rechargeRate robot1) 1)
(= (taskDuration robot1 task1) 20) (= (taskBurn robot1 task1) 1)

 (at robot2 LOCATION5)
(= (speed robot2 FAST) 45)(= (moveBurn robot2 FAST) 1)
(= (battery robot2) 100) (= (maxBattery robot2) 500) (= (rechargeRate robot2) 1)
(= (taskDuration robot2 task2) 2) (= (taskBurn robot2 task2) 10)


 (= (tasks LOCATION0 task2) 0)(= (tasks LOCATION1 task2) 0)(= (tasks LOCATION2 task2) 0)(= (tasks LOCATION3 task2) 0)(= (tasks LOCATION4 task2) 0)(= (tasks LOCATION5 task2) 0)(= (tasks LOCATION0 task1) 0)(= (tasks LOCATION1 task1) 0)(= (tasks LOCATION2 task1) 0)(= (tasks LOCATION3 task1) 0)(= (tasks LOCATION4 task1) 0)(= (tasks LOCATION5 task1) 0)

  (= (distance LOCATION0 LOCATION1) 346) (= (distance LOCATION0 LOCATION2) 281) (= (distance LOCATION0 LOCATION3) 327) (= (distance LOCATION0 LOCATION4) 334)  (= (distance LOCATION1 LOCATION0) 346)  (= (distance LOCATION1 LOCATION2) 411) (= (distance LOCATION1 LOCATION3) 451) (= (distance LOCATION1 LOCATION4) 25) (= (distance LOCATION1 LOCATION5) 315) (= (distance LOCATION2 LOCATION0) 281) (= (distance LOCATION2 LOCATION1) 411)  (= (distance LOCATION2 LOCATION3) 48) (= (distance LOCATION2 LOCATION4) 417) (= (distance LOCATION2 LOCATION5) 327) (= (distance LOCATION3 LOCATION0) 327) (= (distance LOCATION3 LOCATION1) 451) (= (distance LOCATION3 LOCATION2) 48)  (= (distance LOCATION3 LOCATION4) 458) (= (distance LOCATION3 LOCATION5) 334) (= (distance LOCATION4 LOCATION0) 334) (= (distance LOCATION4 LOCATION1) 25) (= (distance LOCATION4 LOCATION2) 417) (= (distance LOCATION4 LOCATION3) 458)  (= (distance LOCATION4 LOCATION5) 338)  (= (distance LOCATION5 LOCATION1) 315) (= (distance LOCATION5 LOCATION2) 327) (= (distance LOCATION5 LOCATION3) 334) (= (distance LOCATION5 LOCATION4) 338) 

 (connected LOCATION3 LOCATION2) (connected LOCATION1 LOCATION3) (connected LOCATION1 LOCATION5) (connected LOCATION5 LOCATION2) (connected LOCATION2 LOCATION3) (connected LOCATION3 LOCATION5) (connected LOCATION2 LOCATION5) (connected LOCATION0 LOCATION1) (connected LOCATION5 LOCATION3) (connected LOCATION0 LOCATION4) (connected LOCATION4 LOCATION1) (connected LOCATION4 LOCATION0) (connected LOCATION1 LOCATION4) (connected LOCATION0 LOCATION2) (connected LOCATION4 LOCATION2) (connected LOCATION2 LOCATION1) (connected LOCATION2 LOCATION4) (connected LOCATION3 LOCATION1) (connected LOCATION3 LOCATION4) (connected LOCATION1 LOCATION0) (connected LOCATION0 LOCATION3) (connected LOCATION2 LOCATION0) (connected LOCATION5 LOCATION1) (connected LOCATION3 LOCATION0) (connected LOCATION4 LOCATION3) (connected LOCATION5 LOCATION4) (connected LOCATION4 LOCATION5) (connected LOCATION1 LOCATION2)

)(:goal (and
 (= (tasks LOCATION4 task1) 2)
 (= (tasks LOCATION3 task1) 3)
 (= (tasks LOCATION1 task2) 2)
 (= (tasks LOCATION2 task2) 1)
))
 (:metric minimize (totalTime))
)
