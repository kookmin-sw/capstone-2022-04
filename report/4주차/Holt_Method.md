# Holt Exponential Trend Technique



<br />



## What is Holt Exponential Trend Technique?

**홀트 지수 추세 기법은 시계열 데이터의 예측 방법 중 하나로 데이터의 주기성과 추세로 다음 값을 예측하며 [1],** 식은 아래와 같습니다.

 

![CodeCogsEqn (4)](https://user-images.githubusercontent.com/28584258/163704587-0624b19c-9914-415b-843f-00a955c438c5.png)



위 식에서 `Y`<sub>`t+1`</sub>는 다음 예측 값이며,   `l`<sub>`t`</sub>는 시간 `t`에서의 시계열 수준 추정 값, `b`<sub>`t`</sub>는 시간 `t`에서의 시계열 추세 (기울기) 추정 값으로 두 식의 계산식은 아래와 같다.



![CodeCogsEqn (2)](https://user-images.githubusercontent.com/28584258/163704245-acab151f-2a36-4a20-a827-2fa978aad9b4.png)

![CodeCogsEqn (3)](https://user-images.githubusercontent.com/28584258/163704247-c2da110f-41b6-4972-a348-c866078e98ea.png)



이때 `Y`<sub>`t+1`</sub>는 시간 `t`에 대한 실제값이고, `alpha`와 `beta`는 각각 수준과 추세에 대한 매개변수로 0과 1사이의 값을 가진다. 즉, **홀트 지수 추세 기법은** `l`<sub>`t-1`</sub>**과**   **`b`<sub>`t-1`</sub>을 사용하여 시간이**  `t`**일때의 값을 예측하는 one-step-ahead training forecast이다 [1].** 그리고 다음 예측을 위해 사용되는 각각의 추정값들은 `t`일 때의 실제값으로 갱신된다.



<br />



## References

[1] Hyndman, R. J., & Athanasopoulos, G. (2018). Forecasting: principles and practice. OTexts.