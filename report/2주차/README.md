# 캡스톤 2주차 보고서

## 1. Packet Received Time Interval (INT)

![CodeCogsEqn](https://user-images.githubusercontent.com/28584258/160270949-84559003-76b8-4a86-a09e-7126fb43d543.png)

위 식에서 ![img](https://latex.codecogs.com/svg.image?P_{t})는 현재 수신된 패킷의 시간이고, ![img](https://latex.codecogs.com/svg.image?P_{t-1})는 이전에 수신된 패킷의 시간입니다. 

<br />

## 2. How to use INT ?

스푸핑 공격이 발생할 시 우리의 BLE 장치뿐만 아니라 공격자의 장치 또한 광고 패킷 (비콘 메시지)을 방송합니다. 따라서 Anchor Point (AP)가 수신받는 광고 패킷의 수는 약 2배 증가하며 INT는 이전보다 비정상적으로 감소합니다. 이러한 특징을 이용하여 스푸핑 공격 여부를 검사할 수 있습니다. 우리가 시도해 볼 INT 검사 방법은 아래와 같습니다.

1. 지속적으로 수집되는 INT로 다음 값을 예측한다.
2. 예측된 INT 값을 사용하여 발생될 수 있는 INT의 정상 범위를 계산한다.
3. 실제 수신된 INT 값이 우리가 계산한 범위를 벗어나면 스푸핑 공격임을 감지한다.

위와 같은 절차의 유효한 검사를 위해선 예측값의 정확도는 높아야 하고 계산되는 INT의 정상 범위가 정밀해야 합니다. 예측값의 정확도를 높이기 위한 실험을 3, 4 섹션에서 다루겠습니다.

<br />

## 3. What is time series data ?

시계열 데이터는 시간에 따라 순차적으로 발생하는 데이터의 집합입니다. 시계열 데이터의 목적은 데이터들의 패턴을 발견하고 모형화하여 추정된 모형을 기반으로 다음 값을 예측하는 것입니다. 예측의 정확도를 높이기 위해 수집되는 데이터의 시계열 패턴을 잘 찾아야 하고 그 패턴을 적절히 잡아낼 수 있는 예측 기법을 선택해야 합니다. 시계열 데이터는 아래와 같은 세 가지 패턴이 있습니다.

* 주기 (Cycle)
  * 빈도가 고정되어 있지 않고 증가나 감소하는 형태
* 추세 (Trend)
  * 데이터가 장기적으로 증가하거나 감소하는 형태
* 계절성 (Seasonality)
  * 계절적 요인 (e.g. 특정 요일이나 특정 주에 발생)이 시계열에 영향을 미침 

<br />

## 4. Comparison of time series data prediction techniques

일반적으로 시계열 예측은 ARIMA 모델과 지수 평활 (Exponential Smoothing)을 사용합니다. 우리의 실험은 지수 평활에 집중합니다. 지수 평활을 사용하는 예측 기법은 아래와 같이 세 가지가 있습니다.

* 단순 지수 평활 기법 (Simple Exponential Smoothing, SES)
  * 오직 시계열 데이터의 Cycle 패턴만 사용하여 다음 값 예측
  * https://otexts.com/fppkr/ses.html
* 홀트 추세 기법 (Holt Trend Technique)
  * SES의 발전 형태
  * 시계열 데이터의 Cycle, Trend 패턴을 사용하여 다음 값 예측
  * https://otexts.com/fppkr/holt.html
* 홀트-윈터스 계절성 기법 (Holt-Winters Seasonal Technique)
  * Holt Trend Technique의 발전 형태
  * 시계열 데이터의 Cycle, Trend, Seasonality 패턴을 사용하여 다음 값 예측
  * https://otexts.com/fppkr/holt-winters.html

본 [실험](https://github.com/kookmin-sw/capstone-2022-04/blob/main/lab/2%EC%A3%BC%EC%B0%A8/best_technique_test.ipynb)에서는 세 가지 기법의 효율성을 검증합니다. 당연히 모든 패턴을 사용하여 값을 예측하는 홀트-윈터스 계절성 기법의 예측 INT가 실제 INT와 가장 비슷했습니다. 하지만 예측을 위한 시간이 너무 오래 소요되어 빠른 속도로 수신되는 광고 패킷의 INT를 예측하는 것은 부적절합니다. SES의 경우 INT의 예측 속도는 매우 빨랐지만 낮은 예측 정확도를 보입니다. 하지만 홀트 추세 기법의 경우 SES와 예측 속도가 비슷하면서 홀트-윈터스 계절성 기법과 유사한 예측 정확도를 보입니다. 따라서 스푸핑 공격 감지 모델의 INT 검사를 위해 홀트 추세 기법을 사용할 예정입니다.
