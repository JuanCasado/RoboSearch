(define (problem probPlanetary) (:domain planetary) (:objects
 ROBOT0 - robot
 LOCATION0 LOCATION1 LOCATION2 LOCATION3 LOCATION4 LOCATION5 LOCATION6 - location
 SLOW FAST - speedType
 DRILL - taskType
)
(:init (= (totalTime) 0) (= (totalBattery) 0) (= (totalDistance) 0) (= (recharges) 0)
 (at ROBOT0 LOCATION2)
(= (speed ROBOT0 FAST) 0.8)(= (moveBurn ROBOT0 FAST) 4)
 (= (speed ROBOT0 SLOW) 0.5)(= (moveBurn ROBOT0 SLOW) 3)
(= (battery ROBOT0) 200) (= (maxBattery ROBOT0) 500) (= (rechargeRate ROBOT0) 0.01)
(= (taskDuration ROBOT0 DRILL) 20) (= (taskBurn ROBOT0 DRILL) 1)


 (= (tasks LOCATION0 DRILL) 0)(= (tasks LOCATION1 DRILL) 0)(= (tasks LOCATION2 DRILL) 0)(= (tasks LOCATION3 DRILL) 0)(= (tasks LOCATION4 DRILL) 0)(= (tasks LOCATION5 DRILL) 0)(= (tasks LOCATION6 DRILL) 0)

  (= (distance LOCATION0 LOCATION1) 77)     (= (distance LOCATION0 LOCATION6) 67) (= (distance LOCATION1 LOCATION0) 77)     (= (distance LOCATION1 LOCATION5) 75)        (= (distance LOCATION2 LOCATION6) 77)     (= (distance LOCATION3 LOCATION4) 27) (= (distance LOCATION3 LOCATION5) 76)     (= (distance LOCATION4 LOCATION3) 27)     (= (distance LOCATION5 LOCATION1) 75)  (= (distance LOCATION5 LOCATION3) 76)    (= (distance LOCATION6 LOCATION0) 67)  (= (distance LOCATION6 LOCATION2) 77)    

 (connected LOCATION6 LOCATION2) (connected LOCATION0 LOCATION1) (connected LOCATION5 LOCATION3) (connected LOCATION1 LOCATION0) (connected LOCATION4 LOCATION3) (connected LOCATION2 LOCATION6) (connected LOCATION6 LOCATION0) (connected LOCATION1 LOCATION5) (connected LOCATION3 LOCATION4) (connected LOCATION5 LOCATION1) (connected LOCATION3 LOCATION5) (connected LOCATION0 LOCATION6)

)(:goal (and
 (= (tasks LOCATION4 DRILL) 2)
))
 (:metric minimize (totalTime))
)
