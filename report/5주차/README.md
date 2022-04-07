# 캡스톤 5주차 보고서

## 1. Detection Phase 모델의 성능 평가

4주차 때 구상한 Detection Phase 모델을 구현한 후 해당 모델의 성능을 평가합니다. 따라서 몇 가지 상황의 데이터에 대해서 Time Interval만을 사용했을 때, RSSI만을 사용했을 때, Time Interval과 RSSI 모두 사용했을 때의 성능 평가를 진행한 후 스푸핑 공격 감지 정확도를 비교합니다.

<br />

## 2. Data for Performance Evaluation

|                        |      |        |      |
| ---------------------- | ---- | ------ | ---- |
| **Packet Speed**       | Fast | Normal | Slow |
| **Distance**           | 0m | 1m | 2m |
| **Number of Data** | 50 | 100 | 500 |

* **Packet Speed**
   
   * Speed of the Beacon Data the Anchor Point receives
   * Average Time Interval of **Fast** (0.03ms), **Normal** (0.13ms), **Slow** (0.35ms)
   * RSSI 값은 Packet Speed에 영향을 받지 않으므로 본 실험에선 제외

* **Distance**

   * Distance between the Tag and the Attacker
   * 0m, 1m, 2m
   * INT 값은 Distance에 영향을 받지 않으므로 본 실험에선 제외

* **Number of Data**

   * Number of Data for Spoofing Attack Detection Prediction
   * 50개, 100개, 500개

위의 9가지 상황을 가정하여 27가지의 서로 다른 데이터 케이스를 만들었습니다. 각 케이스별로 100개의 데이터 파일을 수집했으며 총 2700개의 데이터 파일을 수집했습니다.

<br />

## 3. Time Interval만을 사용한 모델과 Detection Phase 모델

본 [실험]()에서는 Time Interval만 사용한 경우와 Detection Phase 모델을 사용한 경우의 정확도 성능을 비교합니다.
(DP = Detection Phase)

#### 스푸핑 공격 감지 예측에 사용된 데이터 갯수에 따른 정확도 비교

![Number of Data (INT)](https://user-images.githubusercontent.com/28584213/162246157-e62db646-4c7e-4838-9d2a-7bdc66b3bab3.png)

일정한 규칙성을 보이지만 환경 요인으로 불규칙하게 수신되는 Time Interval 값으로 인해 정확도가 스푸핑 공격 감지 예측에 사용되는 데이터의 갯수에 크게 영향을 받지 않는다는 것을 확인할 수 있습니다.

#### 광고 패킷의 전송 속도에 따른 정확도 비교

![Packet Speed (INT)](https://user-images.githubusercontent.com/28584213/162246159-2af30215-f9f5-4c40-b313-5ed2b8913b5d.png)

수신받는 광고 패킷의 속도가 느릴수록 스푸핑 공격이 수신될 때 더욱 분명하게 감지할 수 있기 때문에 예상대로 광고 패킷의 전송 속도가 느릴수록 정확도가 높아지는 것을 확인할 수 있습니다.

<br />

## 4. RSSI만을 사용한 모델과 Detection Phase 모델

본 [실험]()에서는 RSSI만 사용한 경우와 Detection Phase 모델을 사용한 경우의 정확도 성능을 비교합니다.
(DP = Detection Phase)

#### 스푸핑 공격 감지 예측에 사용된 데이터 갯수에 따른 정확도 비교

![Number of Data (RSSI)](https://user-images.githubusercontent.com/28584213/162246161-7d584871-1e6b-4791-9797-625d4f8ff58e.png)

환경 요인으로 불규칙하게 수신되는 RSSI 값으로 인해 정확도가 스푸핑 공격 감지 예측에 사용되는 데이터의 갯수에 크게 영향을 받지 않는다는 것을 확인할 수 있습니다.

#### Tag와 공격자 사이의 거리에 따른 정확도 비교

![Distance (RSSI)](https://user-images.githubusercontent.com/28584213/162246164-ab6840ae-8a70-415d-b710-b818faa0492c.png)

Tag와 공격자 사이의 거리가 1m 이상일 때 100%의 정확도로 스푸핑 공격을 감지할 수 있지만 둘 사이의 거리가 매우 가까울 때는 낮은 정확도를 갖는다는 것을 확인할 수 있습니다.

<br />

## 5. Detection Phase 모델의 성능 평가 결론

예상대로 Detection Phase의 성능이 높은 정확도를 보이는 Time Interval만을 이용한 모델의 성능보다 낮았으며 Time Interval Inspection 이후에 RSSI Inspection이 실행되기 때문에 RSSI만을 이용한 모델과 비슷한 성능을 나타냈습니다.

저희의 모델은 수신되는 광고 패킷 중 단순히 스푸핑 공격이 있다는 것을 감지하는 것뿐만이 아니라 RSSI를 이용해 Tag의 광고 패킷과 공격자의 광고 패킷을 구분하는 검사 단계 또한 지니고 있기 때문에 한 가지의 검사 단계만을 갖고 있는 모델보다 낮은 정확도의 성능을 나타냅니다.