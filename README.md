# SADS : Spoofing Attack Detection System at Indoor Positioning using BLE

## 1. 프로젝트 소개

Bluetooth Low Energy (BLE)를 활용한 실내 위치 측위에서의 스푸핑 공격 감지 기법

본 프로젝트는 BLE 장치와의 일대일 통신을 기반으로 비콘 메시지의 수신 시간 간격과 Received Signal Strength Indicator (RSSI)를 사용하여 스푸핑 공격을 감지하고 공격자의 비콘 메시지를 특정할 수 있는 보안 방법 및 시스템을 소개합니다.

### 실험 환경

<img src = "https://user-images.githubusercontent.com/28584213/169659561-84ea095e-96b5-4036-b4aa-d517c7e073bd.png" width = "100%">

## 2. Abstract

The Received Signal Strength Indicator (RSSI) of the Bluetooth Low Energy (BLE) device varies depending on the distance between the transmitter and the receiver. 
Due to this characteristic, location positioning techniques using beacon messages (Advertising Packets) of BLE devices have been actively studied.
However, since beacon messages that are regularly broadcast by the BLE device are disclosed, so anyone can check the information of beacon messages in a simple way (Beacon scan app, Bluetooth library, etc).
Beacon messages include not only the company name and type of the BLE device, but also Universal Unique Identifier (UUID) and MAC Address, which act as identifiers, making them very vulnerable to spoofing attacks.
Therefore, we propose a Spoofing Attack Detection System (SADS) that can detect spoofing attacks using physical elements of beacon messages.
Based on one-to-one communication between the BLE device and the server, the proposed system detects spoofing attacks regardless of the distance between the tag and the attacker and distinguishes the attacker's beacon message.

## 3. 소개 영상

### 프로젝트 소개 영상

[<img src = "https://user-images.githubusercontent.com/28584213/169656362-ac42cbd2-e7d8-443d-922c-9e87198f2c70.JPG" width = "75%">](https://youtu.be/WM9EzJ98MmY)

### 시연 동영상

[<img src = "https://user-images.githubusercontent.com/28584213/169656361-b405cfa8-261d-4358-bbc2-73f6998f0f93.JPG" width = "75%">](https://youtu.be/CpiUlJJ6qk0)

## 4. 팀 소개

**김상철 교수님**

<img src = "https://user-images.githubusercontent.com/28584213/159163985-37777cfa-d126-428c-aab1-a038c499af15.png" width = "25%">

```markdown
🎓 국민대학교 소프트웨어융합대학 교수
📧 sckim7@kookmin.ac.kr
📌 프로젝트 지도교수
```

**노용준**

<img src = "https://user-images.githubusercontent.com/28584213/157808058-22792714-98fc-49da-a639-515169c2d017.jpg" width = "25%">

```markdown
🎓 20171616
📧 n0y0j@kookmin.ac.kr
📌 연구, 서버 개발, 실험, 성능 평가
```

**문성찬**

<img src = "https://user-images.githubusercontent.com/28584213/158019321-eabfa719-12ae-4342-ad90-de6d5113936a.jpg" width = "25%">

```markdown
🎓 20171620
📧 boyzmsc@kookmin.ac.kr
📌 연구, 서버 개발, 실험, 보고서 작성, 일정 관리
```

## 5. 사용법

* ### Server
  * [Server 설치 및 구동 가이드](https://github.com/kookmin-sw/capstone-2022-04/wiki/%5BServer%5D-Install-and-Running-Guide)

* ### Anchor Point
  * [Anchor Point 설치 및 구동 가이드](https://github.com/kookmin-sw/capstone-2022-04/wiki/%5BAnchor-Point%5D-Install-and-Running-Guide)

* ### Tag / Attacker
  * [Transmitter 설치 및 구동 가이드](https://github.com/kookmin-sw/capstone-2022-04/wiki/%5BTransmitter%5D-Install-and-Running-Guide)

* ### Experiment Manual
  * [SADS 모델 실험 매뉴얼](https://github.com/kookmin-sw/capstone-2022-04/wiki/%5BSADS%5D-Experiment-Manual)