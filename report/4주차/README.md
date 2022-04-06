# 캡스톤 4주차 보고서

<br />



## #1 Implementation Spoofing Attack Detection System



### System Architecture

<br />



![dp](https://user-images.githubusercontent.com/28584258/161902267-cc8ed181-3e8d-4f6c-9635-9048df146a07.png)



초기 스푸핑 공격 감지 시스템인 Detection Phase는 Time Interval 검사와 RSSI 검사로 구분됩니다. Time Interval 검사는 모든 경우에서 발생하는 스푸핑 공격을 감지할 수 있습니다. 하지만 실제 수신되는 광고 패킷의 시간 간격은 매우 불안정하여 False Alarm의 가능성이 높고, 단순히 공격을 감지할 뿐 공격자의 광고 패킷을 특정할 수 없어 다음 공격을 예방할 수 없습니다.

따라서 RSSI 검사를 추가로 진행합니다. 이중 검사를 통해 False Alarm 발생률을 낮추고, 광고 패킷을 방송하는 기기와 공격자의 거리가 가깝지않다면 공격자의 광고 패킷도 특정할 수 있습니다. 하지만 아직 기기와 공격자의 거리가 가까운 경우 스푸핑 공격을 감지할 수 없다는 한계점이 존재합니다.

***



### Time Interval Inspection

시간 간격 검사는 수집 단계와 예측 단계로 나누어 실행됩니다.

<br />



* 수집 단계

![INT-ci](https://user-images.githubusercontent.com/28584258/161902927-068433eb-4d9f-4279-a2aa-17587156eb3d.png)



수집 단계는 다음 시간 간격 값 예측에 사용될 데이터를 필터링합니다. 매우 불규칙적인 시간 간격 값들은 다음 값 예측에 매우 큰 부정적 영향을 끼칠 수 있습니다. 따라서 보다 정밀한 예측을 위해 99%의 **신뢰구간** 범위에 속하는 데이터들을 수집합니다.

<br />



* 예측 단계

![INT-pred](https://user-images.githubusercontent.com/28584258/161902942-c61525ff-90cb-4dad-a984-eda272e1b618.png)



수집 단계에서 수집된 데이터를 기반으로 **홀트 추세 기법**을 사용해 다음 값을 예측합니다. 그리고 이전에 예측된 시간 간격과 실제 시간 간격을 비교하여 표준 오차 (SE)를 계산합니다. 계산된 표준 오차는 발생할 수 있는 시간 간격의 하한값을 계산하는데 사용됩니다. 현재 수신된 값이 전에 계산된 하한값보다 작다면 스푸핑 공격으로 간주합니다.

***



### RSSI Inspection

RSSI 검사는 전처리 단계와 감지 단계로 나누어 실행됩니다.

<br />



* 전처리 단계

![rssi-kf](https://user-images.githubusercontent.com/28584258/161902947-b110324c-a14d-420d-bd6f-5bcf5b8e3157.png)

전처리 단계는 비이상적인 RSSI의 범위 계산에 사용될 데이터를 필터링합니다. RSSI 또한 시간 간격과 같이 매우 불규칙적이므로 비이상적인 값들은 스푸핑 공격 범위를 계산하는데 큰 방해가 될 수 있습니다. 따라서 보다 정밀한 범위 계산을 위해 **칼만 필터**를 사용하여 RSSI 데이터를 평활화합니다.

<br />


* 감지 단계

![rssi-iqr](https://user-images.githubusercontent.com/28584258/161902954-5e9fa85d-1ee2-4784-958b-71fd691942c6.png)

감지 단계는 **사분 범위** (IQR)을 이용하여 스푸핑 공격이 발생할 수 있는 RSSI의 범위를 계산합니다. 이후 계산된 범위오 현재 수신된 RSSI를 비교하여 스푸핑 공격 여부를 확인합니다.
