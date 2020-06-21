(define (problem probPlanetary) (:domain planetary) (:objects
 robot1 - robot
 LOCATION0 LOCATION1 LOCATION2 - location
 SLOW - speedType
 task1 - taskType
)
(:init (= (totalTime) 0) (= (totalBattery) 0) (= (totalDistance) 0) (= (recharges) 0)
 (at robot1 LOCATION2)
(= (speed robot1 SLOW) 10)(= (moveBurn robot1 SLOW) 1)
(= (battery robot1) 400) (= (maxBattery robot1) 500) (= (rechargeRate robot1) 1)
(= (taskDuration robot1 task1) 20) (= (taskBurn robot1 task1) 1)


 (= (tasks LOCATION0 task1) 0)(= (tasks LOCATION1 task1) 0)(= (tasks LOCATION2 task1) 0)

  (= (distance LOCATION0 LOCATION1) 86) (= (distance LOCATION0 LOCATION2) 338) (= (distance LOCATION1 LOCATION0) 86)  (= (distance LOCATION1 LOCATION2) 408) (= (distance LOCATION2 LOCATION0) 338) (= (distance LOCATION2 LOCATION1) 408) 

 (connected LOCATION0 LOCATION1) (connected LOCATION1 LOCATION0) (connected LOCATION0 LOCATION2) (connected LOCATION1 LOCATION2) (connected LOCATION2 LOCATION1) (connected LOCATION2 LOCATION0)

)(:goal (and
 (= (tasks LOCATION0 task1) 1)
 (= (tasks LOCATION1 task1) 1)
))
 (:metric minimize (totalTime))
)
