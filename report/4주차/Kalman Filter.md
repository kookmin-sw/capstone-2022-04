# Kalman Filter

## What is Kalman Filter ?

칼만 필터 (Kalman Filter)는 가우스 노이즈가 존재하는 선형 시스템에서 신호를 처리하고 값을 예측하는 최적의 기법 중 하나입니다 [1]. 매우 불규칙적인 성향을 보이는 데이터에서 칼만 필터는 불규칙적인 데이터를 평활화하여 노이즈를 줄입니다.

## Kalman Filter 동작 방식

칼만 필터는 잡음이 포함된 측정치를 바탕으로 다음 측정값을 추정하는 재귀 필터로 예측과정과 추정과정으로 나뉩니다. 예측과정에서는 추정값과 오차 공분산을 계산합니다. 아래는 추정값을 구하는 식으로 이전 단계에서 계산된 추정값을 사용하여 `A`와의 계산을 통해 새로운 추정값을 예측합니다.

<img src="https://latex.codecogs.com/svg.image?X_t&space;=&space;AX_{t-1}" title="https://latex.codecogs.com/svg.image?X_t = AX_{t-1}" />

위 식에서 `X`<sub>`t-1`</sub>은 시간 `t-1`에서 계산한 추정값이며 `A`는 추정값을 예츨할 때 사용하는 행렬입니다. 아래는 예측한 값이 평균을 기준으로 어느정도 분포되어 있는지 이전 오차 공분산을 사용하여 새로운 오차 공분산을 예측하는 식입니다.

<img src="https://latex.codecogs.com/svg.image?P_t&space;=&space;AP_{t-1}A^T&space;&plus;&space;Q" title="https://latex.codecogs.com/svg.image?P_t = AP_{t-1}A^T + Q" />

위 식에서 `P`<sub>`t-1`</sub>는 시간 `t-1`에서 계산한 오차 공분산이며 `Q`는 시스템의 노이즈입니다. 이렇게 예측된 추정값과 오차 공분산은 추정과정에서 사용되며 추정과정은 칼만 이득 (Kalman Gain), 추정값, 오차 공분산 계산 순서로 진행됩니다. 칼만 이득은 오차 공분산의 예측값과 측정값의 노이즈로 계산되며 식은 아래와 같습니다.

<img src="https://latex.codecogs.com/svg.image?K_t&space;=&space;P_tH^T(HP_tH^T&space;&plus;&space;R)^{-1}" title="https://latex.codecogs.com/svg.image?K_t = P_tH^T(HP_tH^T + R)^{-1}" />

`H`<sup>`T`</sup>는 측정값의 형태로 변환할 때 필요한 행렬이며 `R`은 측정값의 노이즈입니다. 위 식으로 계산된 칼만 이득은 새로 측정값이 입력되었을 때 추정값을 계산하기 위해 사용되며 추정값의 계산식은 아래와 같습니다.

<img src="https://latex.codecogs.com/svg.image?X_t&space;=&space;X_t&space;&plus;&space;K_t(Z_t&space;-&space;HX_t)" title="https://latex.codecogs.com/svg.image?X_t = X_t + K_t(Z_t - HX_t)" />

`Z`<sub>`t`</sub>는 측정값이며 칼만 이득 `K`<sub>`t`</sub>는 측정값과 이전에 구했던 추정값의 가중치를 결정합니다. 즉, 추정값을 구할 때 측정값의 노이즈가 작아 칼만 이득이 크다면 측정값에 많은 가중치를 부여해 계산하고, 오차 공분산의 예측값이 작아 칼만 이득이 작다면 예측값에 더 많은 가중치를 부여해 계산합니다. 위 식을 통해 추정값 `X`<sub>`t`</sub>가 예측되면 새로운 오차 공분산을 계산하며 식은 아래와 같습니다.

<img src="https://latex.codecogs.com/svg.image?P_t&space;=&space;(1-K_tH)P_t" title="https://latex.codecogs.com/svg.image?P_t = (1-K_tH)P_t" />

이렇게 구해진 추정값과 새로 계산된 오차 공분산은 다음 예측 과정에서 사용되며 위와 같은 계산 과정이 재귀적으로 수행됩니다. 

## References

[1] Simon, D. (2006). Optimal state estimation: Kalman, H infinity, and nonlinear approaches. John Wiley & Sons.
