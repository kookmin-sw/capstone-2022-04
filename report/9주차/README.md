# 캡스톤 9주차 보고서



## 1. 발전된 SADS의 시스템 구조 (System Architecture)



![그림1](https://user-images.githubusercontent.com/28584258/167064577-1975a0e0-6d64-4533-8524-a9530e9b6b7f.png)



광고 패킷 (비콘 메시지)를 주기적으로 방송하는 BLE 장치 (Tag)와 광고 패킷을 수신하는 수신기 (Anchor Point, AP)의 일대일 통신을 위해 Unicast Phase가 처음으로 실행됩니다. AP에서 광고 패킷이 수신되었을 때, 서버는 광고 패킷의 송수신이 허락된 시간인지 확인하며 아래와 같이 두 가지의 상태로 구분됩니다.



* **Promise time**
  * Tag와 AP가 비콘 메시지를 송수신하는 시간으로 Detection Phase를 통해 스푸핑 공격 여부를 검사합니다.
* **Non-promise time**
  * Tag와 AP가 비콘 메시지를 송수신하지 않는 시간으로 서버에게 스푸핑 공격 알림을 전송합니다.



Detection Phase는 광고 패킷의 물리적 요소인 **Received Time Interval**과 **Received Signal Strength Indicator (RSSI)**를 사용하여 스푸핑 공격을 탐지하는 단계입니다. 만약, 스푸핑 공격이 감지되지 않았다면 현재 수신된 비콘 메시지를 기반으로 다음 스푸핑 공격을 위해 각각의 검사 모델을 재귀적으로 갱신합니다.



## 2. 발전된 SADS의 개요 (Overview)

위와 같이 제안된 발전된 SADS는 상세하게 아래와 같이 작동합니다.



* 일대일 통신 (Unicast Communication)을 위해 양의 정수로 이루어진 배열을 무작위로 생성하기 위한 랜덤 시드를 암호화해야 합니다. 따라서 [타원 곡선 암호 (ECC)](https://github.com/kookmin-sw/capstone-2022-04/blob/main/report/6%EC%A3%BC%EC%B0%A8/ECC.md) 알고리즘을 사용하여 공개키와 비밀키를 생성합니다.
* 서버는 랜덤 시드를 정하고 양의 정수를 무작위로 추출하여 배열을 생성합니다. 이후 생성된 공개키를 사용해 암호화하고, 암호화된 랜덤 시드를 Tag에게 전송합니다.
* 태그는 암호화된 랜덤 시드를 비밀키로 복호화 한 후, 랜덤 시드를 사용하여  무작위로 추출된 양수로 이루어진 배열을 생성합니다. 이때 **태그와 서버는 같은 랜덤 시드를 사용하므로 생성된 배열은 같습니다.**
* 생성된 배열을 사용하여 `Promise time`와 `Non-promise time`을 정의하고 약속된 시간에 맞춰 Tag와 AP의 일대일 통신을 시작합니다. `Non-promise time`에 광고 패킷이 수신되면 스푸핑 공격으로 간주합니다.
* 서버는 광고 패킷이 수신되는 시간 간격을 계산하고, 다음 시간 간격 예측에 사용되는 시간 간격 데이터를 수집합니다.
* 한편, 광고 패킷의 RSSI는 [Kalman Filter (KF)](https://github.com/kookmin-sw/capstone-2022-04/blob/main/report/4%EC%A3%BC%EC%B0%A8/Kalman%20Filter.md)에 의해 평활화되며, 이상치를 구분하는 범위를 계산하기 위해 수집됩니다.
* 예측을 위한 시간 간격 데이터와 평활화된 RSSI가 충분히 수집되었으면 광고 패킷의 다음 시간 간격을 예측합니다. 그리고 시간 간격과 평활화된 RSSI를 사용하여 이상치의 범위를 계산합니다.
* 현재 수신된 광고 패킷의 수신 시간 간격과 RSSI가 이상치의 범위에 있는지 확인하고 스푸핑 공격 여부를 특정합니다.



## 3. 발전된 SADS를 사용하기 위한 과정 (Assumptions)

1. 스푸핑 공격자는 1명으로 가정합니다.
2. Detection Phase에서는 스푸핑 공격이 발생하기 전, 정상적인 광고 패킷이 50개 이상 수신되었다고 가정합니다.



## 4. Unicast Phase

서버는 Tag와 AP의 일대일 통신으로 인한 스푸핑 공격 감지 정확도 향상을 위해 특정 식별자 (UUID, MAC Address 등)를 가진 광고 패킷만 수신합니다. 발전된 SADS는 미리 정의된 시간에만 비콘 메시지를 송수신하기 위해 `Promise time`와 `Non-promise time`을 미리 정의해야 합니다. 이때 서버는 모든 경우에서 동일한 무작위 양수를 생성하기 위한 랜덤 시드를 생성합니다. 만약 공격자가 랜덤 시드를 알고 있으면 공격자는 미리 정의된 시간을 알 수 있습니다. 따라서 랜덤 시드는 타원 곡선으로 암호화되어 각각 Tag와 AP에게 전송됩니다. 이때 공격자에게 노출되는 것을 최소화하기 위하여 아래와 같은 ElGamal 공개키 교환 방법을 사용합니다.



![그림1](https://user-images.githubusercontent.com/28584258/167066538-6ecbec4a-8366-4c7f-8f50-3d5114a5cbd2.png)



위 그림의 공개키 생성 과정에서 `E`<sub>`p`</sub>와 `P`는 타원 곡선 상의 유한체를 정의하기 위한 매개변수이며 `P`는 유한체의 범위를 지정하는 매우 큰 소수입니다. 또한 `e`<sub>`1`</sub>은 암호화에 사용되는 유한체 위의 한 점이고, `pk`는 비밀키로 `e`<sub>`2`</sub>는 `e`<sub>`1`</sub>을 `pk`번 덧셈 연산한 값입니다. 생성된 공개키 (`e`<sub>`1`</sub>, `e`<sub>`2`</sub>, `E`<sub>`p`</sub>, `P`)는 서버로 전송되고 서버는 무작위로 선정한 랜덤 시드 `D`를 아래 식과 같이 암호화합니다.



![CodeCogsEqn](https://user-images.githubusercontent.com/28584258/167067637-acb00148-f880-4240-8ea5-17b679bc0c80.png)

![CodeCogsEqn (1)](https://user-images.githubusercontent.com/28584258/167067640-4cc1d184-cf6b-4778-a7a1-c83914b02c47.png)



`C`<sub>`1`</sub>과 `C`<sub>`2`</sub>는 암호화된 두 점이고 `K`는 암호화에 사용되는 무작위 양수입니다. 위 식으로 암호화된 랜덤 시드는 다시 Tag에게 전송됩니다. 그리고 Tag는 사전에 정의한 비밀키 `pk`를 사용하여 아래와 같이 복호화를 진행합니다.



![CodeCogsEqn (2)](https://user-images.githubusercontent.com/28584258/167067642-967abfe4-2a2a-459e-91a0-e914c3e9f860.png)



위의 식으로 복호화된 랜덤 시드를 사용하여 무작위로 추출된 양수의 배열을 생성합니다. 생성된 배열은 아래 그림과 같은 메커니즘으로 사용됩니다.



![그림2](https://user-images.githubusercontent.com/28584258/167067645-6319720d-f201-4107-ac91-c1256d141e08.png)



위 그림에서 사용되는 무작위 양수 배열의 홀수 번째 인덱스는 광고 패킷을 송수신하는 시간, 즉 `Promise time`을 의미하고 짝수 번째 인덱스는 송수신하지 않는 시간, 즉 `Non-promise time`을 의미합니다. 공격자는 무작위로 생성된 양수에 의해 `Non-promise time`이 시작되는 시간을 쉽게 예상할 수 없습니다. 따라서 `Non-promise time`에 같은 식별자로 수신되는 광고 패킷은 공격자의 스푸핑 광고 패킷으로 간주될 수 있습니다.