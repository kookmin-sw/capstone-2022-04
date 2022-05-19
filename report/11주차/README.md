# 캡스톤 11주차 보고서

## 1. SADS 모델 시퀀스 조정

#### **이전 SADS 모델 시퀀스**
![이전](https://user-images.githubusercontent.com/28584258/167064577-1975a0e0-6d64-4533-8524-a9530e9b6b7f.png)

* **Unicast Phase**가 먼저 실행됨
* **Unicast Phase**에서 **Promise Time**과 **Non-promise Time**이 반복적으로 실행되어 **Real-Time Based 시스템**에 적용하기 힘듦
* 누적되는 Delay로 인해 **False Alarm** 빈도 증가 등 한계점 존재

#### **조정된 SADS 모델 시퀀스**
![이후](https://user-images.githubusercontent.com/28584213/169297269-faff7bce-1c05-4989-b3af-782ca11826d4.png)

* **Detection Phase**가 먼저 실행됨
* **Detection Phase**에서 사용자와 공격자 사이의 거리가 매우 가까운 경우를 제외하면 높은 탐지 정확도를 보임
* 사용자와 공격자 사이의 거리가 매우 가까울 때만 **Unicast Phase**로 넘어가기 때문에 **Promise Time**과 **Non-promise Time**을 무분별하게 이용할 필요가 없음
* **Unicast Phase**에서 단 한번의 **Delay Time**과 **Non-promise Time**으로 공격자의 광고 패킷을 탐지하고 구분하여 Delay 누적 문제를 해결할 수 있음
* 또한 **Unicast Phase** 단계에서 **Promise Time**과 **Non-promise Time**이 무분별하게 사용되지 않기 때문에 **Real-Time Based 시스템**에서도 활용할 수 있음

<br />

## 2. Unicast Phase 수정

![Unicast Phase](https://user-images.githubusercontent.com/28584213/169298143-6953fe94-7e77-430d-bf19-4936085e4e5d.png)

* 사용자와 공격자 사이의 거리가 매우 가까워 **Detection Phase**에서 스푸핑 공격을 확정할 수는 없지만 의심가는 상황에서 실행됨
* 사용자와 시스템 사이의 일대일 통신을 위해 사전에 공유한 랜덤 시드를 이용해 동일한 값의 랜덤 약속 시간 리스트 생성
* 해당 리스트를 이용해 **Delay Time**과 **Non-promise Time** 설정 및 실행
* **Delay Time** : 공격자를 교란시키기 위해 만든 지연 시간으로 해당 시간에 사용자는 정상적으로 광고 패킷을 송신하지만 시스템은 광고 패킷을 수신하지는 않음
* **Non-promise Time** : 지연 시간 이후의 시간으로 사용자는 광고 패킷을 송신하지 않으며 시스템 또한 광고 패킷을 수신하지 않음, 이때 사용자와 동일한 UUID로 수신되는 광고 패킷이 감지되면 해당 광고 패킷을 스푸핑 공격으로 특정함

<br />

## 3. 최종 SADS 모델 동작 개요 및 순서

![SADS](https://user-images.githubusercontent.com/28584213/169299989-ad59ccb9-4a60-48fe-bf1f-dc3e45d5170e.png)

1. **Tag** (송신기)에서 공개키, 개인키 생성 및 공개키 **Server**로 전송
2. **Server**에서 일대일 통신을 위한 랜덤 시드 생성 및 공개키로 암호화, 해당 암호문 **Tag**로 전송, 랜덤 시드를 이용해 약속 리스트 생성
3. **Tag**에서 개인키로 암호문 복호화 및 랜덤 시드를 이용해 약속 리스트 생성, 광고 패킷 생성 및 방송
4. **AP** (Anchor Point)에서 광고 패킷 수신 및 **Server**로 수신한 광고 패킷 전송
5. **Server**에서 수신받은 광고 패킷을 검사 및 스푸핑 공격 탐지 진행 (= **Detection Phase** + **Unicast Phase**)