# 캡스톤 12주차 보고서

## 1. 최종 SADS 모델 성능 평가 (Detection Phase)

### Tag (Moveable)
  
* 공격자의 데이터가 오로지 1개 수신

<img src = "https://user-images.githubusercontent.com/28584213/169643267-40bd075b-0f5c-44e8-b650-ab8b522fb601.png" width = "75%">

* 공격자의 데이터가 1초동안 수신

<img src = "https://user-images.githubusercontent.com/28584213/169643268-cf9ea5cb-ea53-4fc9-9cf6-83733dc629dd.png" width = "75%">

* 공격자의 데이터가 2초동안 수신

<img src = "https://user-images.githubusercontent.com/28584213/169643270-8678932a-d3b0-4f80-941b-912430cf6fd1.png" width = "75%">

### Tag (Stationary)

* 수신 시간 간격만 이용 (= Time Interval Inspection)

<img src = "https://user-images.githubusercontent.com/28584213/169643271-abad4563-25eb-48b0-9fef-a6830db60ba8.png" width = "75%">

* RSSI 정보만 이용 (= RSSI Inspection)

<img src = "https://user-images.githubusercontent.com/28584213/169643272-1c15a014-c805-4020-ace5-6b398cb585df.png" width = "75%">

* 수신 시간 간격과 RSSI 모두 이용 (= Detection Phase)

<img src = "https://user-images.githubusercontent.com/28584213/169643273-2d58664e-2803-4d1c-9e5b-e6ad35b31429.png" width = "75%">

<br />

## 2. 최종 SADS 모델 성능 평가 (Detection Phase + Unicast Phase)

* 최종 성능 평가 결과

<img src = "https://user-images.githubusercontent.com/28584213/169643274-c15f7673-64f0-4375-ba02-6aef7d344efb.png" width = "75%">

<br />

## 3. SADS의 확장

저희 모델인 SADS는 "Spoofing Attack Detection System at Indoor Positioning using BLE Beacon"을 위해 개발되었습니다. 하지만 BLE 기기의 특성 상 시스템과 연결을 위해 광고 패킷을 송신해야 하고, 공격자 또한 시스템과 연결을 위해 자신의 광고 패킷을 송신해야 합니다. 이러한 특징으로 인해 저희는 단순히 "Spoofing Attack Detection System at Indoor Positioning using BLE Beacon"가 아닌 "Spoofing Attack Detection System on BLE"로 프로젝트의 확장을 생각했습니다.

하지만 모든 BLE 기기에서 스푸핑 공격을 탐지하기 위해서는 단순히 BLE 기기와 연결과 재연결될 때뿐만 아니라 BLE 기기가 시스템과 연결이 되어있는 경우도 스푸핑 공격을 탐지할 수 있어야 합니다. 하지만 아쉽게도 SADS는 BLE 기기가 사용자와 연결되어 있을 때 스푸핑 공격을 탐지할 수 없는 한계점을 가지고 있습니다. 따라서 BLE 통신에서의 스푸핑 공격 탐지는 저희 모델에 적합하지 않습니다.

<img src = "https://user-images.githubusercontent.com/28584213/169644039-44df2f4d-a427-48a8-99bc-01d0f184eacc.png" width = "75%">

한편, 송신기가 송신하는 광고 패킷은 위의 그림과 같이 Header와 Payload로 구성됩니다. 그리고 Payload의 규격에 따라 애플의 iBeacon, 안드로이드의 Alt Beacon, 구글의 Eddystone 등으로 구분됩니다. SADS는 일대일 통신을 기반으로 한 광고 패킷의 수신 시간 간격과 RSSI 정보를 이용하여 스푸핑 공격을 탐지합니다. 따라서 SADS는 위와 같은 다양한 종류의 모든 비콘에서 발생하는 스푸핑 공격을 감지할 수 있습니다.

비콘 신호는 현재 실내 위치 측위, 거리 인식, 물체 인식, 로보틱스 등의 다양한 분야에서 사용되고 있습니다. 따라서 저희는 SADS의 적용을 "Spoofing Attack Detection System at Indoor Positioning using BLE Beacon"에서 "Spoofing Attack Detection System on BLE Beacon"으로 확장할 수 있다고 판단했습니다.
