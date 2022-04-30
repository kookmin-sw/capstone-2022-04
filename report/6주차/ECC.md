# 타원 곡선 암호학 (Elliptic Curve Cryptography, ECC)

<br />



## 타원 곡선 암호학이란?

타원 곡선 암호학 (ECC)은 RSA 방식과 동일한 기능을 제공하는 타원 곡선 기반의 공개키 암호방식입니다 [1]. 같은 공개키 암호 방식인 RSA 암호와 비교했을 때, ECC가 더 작은 bit 수의 암호키로 RSA 암호와 동일한 암호 성능을 가진다는 장점이 있습니다 [2].

<br />



우리는 무작위로 추출된 양수 배열을 생성하기 위한 랜덤 시드를 암호화 그리고 복호화하기 위해 ECC를 사용합니다. ECC를 이해하기 위해선 **타원 곡선 상의 연산**과 **타원 곡선 상의 유한체 (finite field)**를 이해해야 하며 타원 곡선의 방정식은 아래와 같습니다.

<br />



![CodeCogsEqn](https://user-images.githubusercontent.com/28584258/166096112-fd0c0c58-01dc-4c1b-a1ee-2faef3b1cf3e.png)

<br />



위 식의 형태를 가지는 타원 곡선은 `x`축을 중심으로 대칭되고, 비 수직선에 대해 최대 3개 지점에서 곡선과 교차될 수 있습니다. 이러한 특징으로 타원 곡선의 덧셈 연산은 타원 곡선 상의 두 점 `A(x1, y1)`와 `B(x2, y2)`를 지나는 직선이 타원 곡선과 만나는 교점을 `x`축으로 대칭시킨 점 `C(x3, y3)`를 구하는 것으로 정의하며 식은 아래와 같습니다.

<br />



<img src="https://user-images.githubusercontent.com/28584258/166096199-96ed9ba3-e988-45a7-890b-132725463dad.gif" alt="그림1" style="zoom:33%;" /> <img src="https://user-images.githubusercontent.com/28584258/166096200-a3c888cc-417a-4325-aef0-2933c2ee4418.gif" alt="그림2" style="zoom:33%;" />

<br />



이때 덧셈연산은 `A`와 `B`가 다른 점에 존재할 때와 같은 점에 존재할 때 2가지의 경우로 나뉘며, 각각 `Addition`과 `Doubling` 연산으로 계산됩니다. 다음으로 타원 곡선에서의 곱셈 연산 식은 아래와 같습니다.

<br />



![CodeCogsEqn (1)](https://user-images.githubusercontent.com/28584258/166096238-eb4479cd-4b37-498e-941e-da5d2c4a94be.png)

<br />



위 식에서 `k`는 곱하는 수로 타원 곡선의 덧셈 연산을 `k`번 수행하는 것과 같습니다. 한편 공개키 형식의 ECC는 유한체에서 정의될 수 있으며 유한체를 정의하는 식은 아래와 같습니다.

<br />



![CodeCogsEqn (2)](https://user-images.githubusercontent.com/28584258/166096266-3d647041-5e41-4a89-8e85-6a4307faa007.png)

<br />



유한체의 식은 `0` ~ `p-1`의 좌표 안에서 정의되며 타원 곡선 방정식의 양변에 모듈러 연산을 취한 형태입니다. 이때 `p`는 3보다 큰 소수이며 값이 클수록 대응되는 `y`의 값을 구하기 어려워집니다. 이러한 점을 이용하여 ECC를 암호화 및 복호화에 사용합니다.****

<br />

<br />



## 타원 곡선 암호학의 메커니즘





<img src="https://user-images.githubusercontent.com/28584258/166096329-142b3daa-010f-437d-b5dc-f8fd6f738717.png" alt="그림3" style="zoom: 67%;" />

<br />



데이터를 보내기 위해 암호화하는 Alice는 ECC를 사용하기 위한 값을 초기화합니다. 이때 `E`<sub>`p`</sub>와 `P`는 타원 곡선 상의 유한체를 정의하기 위한 매개변수이며 `P`는 매우 큰 소수입니다. `K`는 암호화에 사용되는 무작위 양수이고, `pk`는 비밀키로 Alice와 Bob에게 알려져 있습니다. `alpha`는 공개키로 유한체 위의 한 점을 무작위로 선택합니다. 마지막으로 `D`는 암호화하는 평문입니다.

<br />



값들의 초기화가 끝나면 `D`를 암호화하여 Bob에게 전송합니다. 그리고 Bob은 비밀키를 사용하여 암호화된 `D`를 복호화합니다. 이때 암호화와 복호화에 사용되는 계산은 위에서 언급된 타원 곡선 상의 덧셈과 곱셈 연산을 사용합니다.

<br />



만약, Alice와 Bob이 독립적으로 운영되는 프로그램이라면 Alice에서 생성된 비밀키를 Bob이 알기 위해선 한번 이상의 통신을 필요로 합니다. 이것을 방지하기 위한 다양한 공개키 교환 알고리즘이 존재하며, 우리는 [Elgamal 공개키 교환 방법](https://github.com/kookmin-sw/capstone-2022-04/blob/main/report/6%EC%A3%BC%EC%B0%A8/Elgamal.md)을 사용했습니다.