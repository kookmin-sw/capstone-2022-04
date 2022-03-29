# 캡스톤 3주차 보고서

## 1. INT만을 이용하는 감지 모델에서의 한계점

스푸핑 공격이 발생했을 때 Anchor Point (AP)에서 수신 받는 광고 패킷의 수신 간격이 기존보다 비정상적으로 감소하기 때문에 스푸핑 공격의 유무는 정확하게 판단할 수 있습니다. 스푸핑 공격은 Anchor Point (AP)에 해당 공격 비콘 메시지가 수신되기 시작한 순간부터 감지할 수 있습니다. 하지만 감지한 순간에 비정상적인 시간 간격으로 들어오는 비콘 메시지가 총 2개이기 때문에 그 2개의 비콘 메시지 중 어느 것이 우리의 BLE 장치의 비콘 메시지이고 어느 것이 공격자의 비콘 메시지인지 구분할 수 없는 한계점이 존재합니다. 따라서 우리의 BLE 장치의 비콘 메시지와 스푸핑 공격 비콘 메시지를 구분하기 위해 비콘 메시지 내부 패킷 정보 중 하나인 Received Signal Strength Indicator (RSSI) 정보를 이용합니다.

<br />

## 2. What is RSSI ?

RSSI는 Anchor Point (AP)로부터 수신한 전력 수치입니다. 이 값은 송신기와 수신기 사이의 거리, 채널 간섭, 방송 전력 값 등에 의해 변경될 수 있습니다. [1] 따라서 Anchor Point (AP)에 수신되는 우리의 BLE 장치의 비콘 메시지 RSSI 값을 기반으로 해당 RSSI 값과 차이가 많이 나는 값을 지닌 비콘 메시지가 수신되면 해당 비콘 메시지를 스푸핑 공격으로 판단할 수 있습니다.

<br />

## 3. Why use RSSI ?

해당 프로젝트에서 사용하는 광고 패킷 (iBeacon 규격 메시지)은 다음 형식에 따라 총 42바이트 입니다.

| Preamble | Access Address | Header | MAC Address | Type | UUID | Major | Minor | Tx Power | RSSI |
| :------: | :------------: | :----: | :---------: | :--: | :--: | :---: | :---: | :------: | :--: |
|    1     |       4        |   2    |      6      |  7   |  16  |   2   |   2   |    1     |  1   |

해당 표에서 비콘 메시지 식별에 사용할 수 있는 데이터는 Access Address, MAC Address, Type, UUID, RSSI가 있습니다. [2] 그 중에서 UUID와 다양한 주소 정보들이 대표적인 스푸핑 공격 대상입니다. 하지만 RSSI의 값은 송신기와 수신기 사이의 거리에 따라 달라지는 가변적인 전력 수치이기 때문에 공격자 입장에서 쉽게 모방할 수 없는 정보입니다. 따라서 스푸핑 공격 구분 기준으로 RSSI 정보를 사용합니다.

<br />

## 4. How to use RSSI ?

우리의 BLE 장치와 공격자의 장치가 Anchor Point (AP)로부터 서로 다른 거리에 위치해 있을 때, 스푸핑 공격이 발생할 시 기존에 Anchor Point (AP)에 수신되는 RSSI 값과는 다른 RSSI 값이 들어옵니다. 이러한 특징을 이용하여 우리의 BLE 장치의 비콘 메시지와 스푸핑 공격 비콘 메시지를 구분할 수 있습니다. 우리가 시도해 볼 RSSI 검사 방법은 아래와 같습니다.

1. 지속적으로 수집되는 RSSI로 다음 값을 예측한다.
2. 예측된 RSSI 값을 사용하여 발생될 수 있는 RSSI의 정상 범위를 계산한다.
3. 실제 수신된 RSSI 값이 우리가 계산한 범위를 벗어나면 스푸핑 공격임을 감지한다.

계속해서 빠르게 수신되는 비콘 메시지의 RSSI 값을 수집하고 빠르게 정상 범위를 계산하기 위해선 연산이 가벼우면서도 정확도가 높은 방법을 적용해야 합니다. 이 과정을 위해 IQR 개념을 도입합니다.

<br />

## 5. What is IQR ?

RSSI를 사용하려면 이상치 값을 탐지하도록 범위를 설정하는 것이 매우 중요합니다. 따라서 이상치 값의 범위를 설정하는 방법들 중 하나인 IQR 방식을 사용합니다.

IQR 방식은 사분위 (Quantile) 개념이 이용되는데, Anchor Point (AP)로 수신되는 RSSI 값 데이터들을 오름차순으로 정렬하고 정확히 4등분 (25%, 50%, 75%, 100%)으로 나누게 됩니다. 이 중 75% 지점의 값과 25% 지점의 값의 차이를 IQR로 지정하고 해당 IQR 값으로 아래 그림과 같은 기준 범위를 설정합니다. [3]

![1_2c21SkzJMf3frPXPAR_gZA](https://user-images.githubusercontent.com/28584213/160149754-6fa66402-af73-4a39-92f8-ff3e8009abdd.png)

따라서 해당 범위를 벗어나는 RSSI 값이 Anchor Point (AP)에 수신될 때 스푸핑 공격으로 구분할 수 있습니다.

본 [실험](https://github.com/kookmin-sw/capstone-2022-04/blob/main/lab/3%EC%A3%BC%EC%B0%A8/RSSI/IQR_test.ipynb)에서는 IQR 방식을 도입하여 우리의 BLE 장치의 RSSI 이상치 값의 범위를 설정합니다. 이후에 공격자의 장치를 Anchor Point (AP)로부터 거리를 각각 다르게 설정한 후 서로 다른 거리에 따라 다른 RSSI 값을 가진 스푸핑 공격 비콘 메시지에 대해서 IQR 방식을 도입했을 때의 스푸핑 공격 감지 정확도를 측정합니다.

<br />

## References

[1] Pavel Stankoulov, Micro-Location Part 2: BLE and RSSI, https://www.abaltatech.com/blog/microlocation2, January 12, 2021

[2] Kim C. H., Hong S. H., Lee S. W., ‘‘A research on performance improvement of iBeacon using transmission and reception of different beacon signals.’’ The Journal of Korean Institute of Communications and Information Sciences, 40(1), 108-114, pp. 2, 2015

[3] Courtney Taylor, What Is the Interquartile Range Rule?, https://www.thoughtco.com/what-is-the-interquartile-range-rule-3126244, April 26, 2018