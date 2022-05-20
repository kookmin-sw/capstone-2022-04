# SADS 모델 성능 평가 Data

## Detection Phase

* Tag (**Moveable**)
  * Tag가 움직이는 경우
  * 0 (Directory)
    * Non-promise time에 공격자의 데이터가 오로지 1개 수신
    * test_data0
      * Tag와 공격자의 사이의 거리 0cm
    * test_data1
      * Tag와 공격자의 사이의 거리 50cm
    * test_data2
      * Tag와 공격자의 사이의 거리 1m
    * test_data3
      * Tag와 공격자의 사이의 거리 2m
  * 1 (Directory)
    * Non-promise time에 공격자의 데이터가 1초동안 수신
    * test_data0
      * Tag와 공격자의 사이의 거리 0cm
    * test_data1
      * Tag와 공격자의 사이의 거리 50cm
    * test_data2
      * Tag와 공격자의 사이의 거리 1m
    * test_data3
      * Tag와 공격자의 사이의 거리 2m
  * 2 (Directory)
    * Non-promise time에 공격자의 데이터가 2초동안 수신
    * test_data0
      * Tag와 공격자의 사이의 거리 0cm
    * test_data1
      * Tag와 공격자의 사이의 거리 50cm
    * test_data2
      * Tag와 공격자의 사이의 거리 1m
    * test_data3
      * Tag와 공격자의 사이의 거리 2m
      
* Tag (**Stationary**)
  * Tag가 움직이지 않는 경우
  * test_data0
    * 공격자의 데이터 오로지 1개 수신
  * test_data1
    * 공격자의 데이터 1초동안 수신
  * test_data2
    * 공격자의 데이터 2초동안 수신
  * test_data3
    * 공격자의 데이터 3초동안 수신
  * test_data4
    * 공격자의 데이터 4초동안 수신
  * test_data5
    * 공격자의 데이터 5초동안 수신

<br />

## SADS (= Detection Phase + Unicast Phase)

* test_data0
  * 공격자의 데이터 오로지 1개가 수신
* test_data1
  * 공격자의 데이터 1초동안 수신
* test_data2
  * 공격자의 데이터 2초동안 수신
* test_data3
  * 공격자의 데이터 3초동안 수신
* test_data4
  * 공격자의 데이터 4초동안 수신
* test_data5
  * 공격자의 데이터 5초동안 수신