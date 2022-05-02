# 캡스톤 6주차 보고서

## 1. Unicast Phase의 도입

앞서 저희의 모델은 Detection Phase 모델의 성능평가를 수행했습니다. 전반적으로 스푸핑 공격 탐지의 높은 확률을 나타냈지만 공격자와 유저가 가까울 때 수신 받는 두 RSSI 값이 매우 비슷하므로 스푸핑 공격을 감지할 수는 있지만 공격자의 패킷을 특정할 수 없다는 한계점을 볼 수 있었습니다. 따라서 해당 한계점을 극복하기 위해 Unicast Phase 단계를 추가합니다.
Unicast Phase에서는 다음과 같은 방식으로 공격자와 유저 사이의 거리가 매우 가깝더라도 스푸핑 공격을 감지하고 공격자의 패킷을 구분합니다.

1. 공격자 입장에서 감지하기 힘든 식별자를 생성함
2. 유저의 BLE 기기와 Server 사이의 규칙을 생성하여 일대일 통신을 가능하게 함

따라서 저희는 먼저 iBeacon 내부 패킷에 있는 Major, Minor 정보를 고유 식별자로 이용합니다.

## 2. Major, Minor 정보란?

해당 프로젝트에서 사용하는 광고 패킷 (iBeacon 규격 메시지)은 다음 형식에 따라 총 42바이트 입니다.

| Preamble | Access Address | Header | MAC Address | Type | UUID | Major | Minor | Tx Power | RSSI |
| :------: | :------------: | :----: | :---------: | :--: | :--: | :---: | :---: | :------: | :--: |
|    1     |       4        |   2    |      6      |  7   |  16  |   2   |   2   |    1     |  1   |

위 표에서 UUID는 각 회사를 나타내는 고유 식별값이며 Major와 Minor 정보는 추가 식별을 위한 식별자로 사용됩니다. Major와 Minor 정보는 각각 2바이트이므로 0x0000 ~ 0xFFFF 범위의 수를 나타낼 수 있습니다.

## 3. Major, Minor 정보 암호화의 필요성

저희는 Major와 Minor 정보를 공격자가 쉽게 인식하지 못하는 고유 식별자로 이용합니다. 하지만 단순한 Major와 Minor 정보 값은 광고 패킷의 방송되는 특징으로 인해 공격자에게도 노출됩니다. 때문에 저희는 공격자가 쉽게 인식하지 못하도록 Major와 Minor 정보를 암호화하는 방안을 구상했습니다. 따라서 비대칭 암호화의 일종인 [타원 곡선 암호화 (ECC)](https://github.com/kookmin-sw/capstone-2022-04/blob/main/report/6%EC%A3%BC%EC%B0%A8/ECC.md)와 유저 BLE 기기와 서버와의 타원 곡선 암호화를 기반으로 통신하는 [Elgamal 알고리즘](https://github.com/kookmin-sw/capstone-2022-04/blob/main/report/6%EC%A3%BC%EC%B0%A8/Elgamal.md)을 적용합니다.

## 4. 암호화 유형

암호화 유형은 크게 다음과 같이 대칭 암호화와 비대칭 암호화로 나뉩니다.

* 대칭 암호화
   * 암호화 및 복호화에 사용되는 개인키가 동일함
   * 매우 빠름

* 비대칭 암호화
   * 대칭 암호화와 다르게 암호화에 사용되는 공개키는 복호화에 사용되는 개인키와 다름
   * 대칭 암호화보다 느리지만 보안이 향상됨

## 5. 비대칭 암호화

비대칭 암호화 알고리즘은 크게 소인수 분해와 이산 로그로 나뉩니다. 그 중에서도 소인수 분해 방식의 RSA 알고리즘은 긴 키와 우수한 보안 기능으로 시장 점유율이 가장 높습니다. 하지만 속도가 매우 느리다는 단점을 가지고 있습니다. 따라서 저희는 이산 로그를 기반으로 속도가 빠른 타원 곡선 암호화 기술을 사용하며 RSA 알고리즘보다 매우 짧은 길이의 키를 사용하면서도 비슷한 수준의 안정성을 제공합니다.

## 6. Unicast Phase 단계 추가 및 모델 수정

앞서 언급드린 Major, Minor 정보를 고유 식별자로 사용하고 해당 정보를 공격자로부터 암호화하여 통신하기 위해 저희의 모델 기능을 수정합니다.

* App (= Tag)
   * Before
      * 광고 패킷 (= 비콘 메시지) 생성에만 사용
   * After
      * 서버로부터 수신된 암호화된 Major, Minor 값 복호화
      * 복호화된 Major, Minor 값으로 광고 패킷 생성 및 방송

* Server
   * Before
      * Anchor Point로부터 광고 패킷 수신
      * Time Interval & RSSI 분석 및 스푸핑 공격 감지 (= Detection Phase)
   * After
      * ECC와 Elgamal 알고리즘을 기반으로 Major, Minor 값을 무작위로 생성 및 암호화
      * Major, Minor 값을 Anchor Point로 전송 (Socket 이용)
      * 암호화된 Major, Minor 값을 App으로 전송 (Firebase 이용)
      * Anchor Point로부터 광고 패킷 수신
      * Time Interval & RSSI 분석 및 스푸핑 공격 감지 (= Detection Phase)

* Anchor Point
   * Before
      * 수신받는 광고 패킷을 Server로 송신
   * After
      * 수신받는 광고 패킷 중 고유 식별자인 Major, Minor 값과 동일한 광고 패킷만을 구분 (= Unicast Phase)
      * 필터링된 광고 패킷을 Server로 송신