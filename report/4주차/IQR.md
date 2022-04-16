# InterQuartile Range

## What is IQR ?
사분범위는 중간값을 기준으로 데이터들의 흩어진 정도를 뜻하며, 지속적으로 분포하는 데이터에서 효과적으로 이상치를 찾을 수 있습니다 [1]. 데이터의 이상 범위를 판단하기 위해 사용되며 식은 아래와 같습니다.

$IQR = Q3 - Q1$

$Q3$는 전체 데이터 75%의 값, 즉 3사분위 수이며, $Q1$은 전체 데이터 25%의 값 즉, 1사분위 수입니다. 위 식에서 계산된 $IQR$은 정상 범위의 최솟값과 최댓값을 계산하는데 쓰이며 식은 아래와 같습니다.

$MIN=Q1-(IQR×1.5)$

$MAX=Q3+(IQR×1.5)$

만약 새로 입력된 데이터가 $MIN$ 값보다 작거나 $MAX$ 값보다 크면 그 값을 이상치로 판단하고, $MIN$ 값보다 크거나 같고 $MAX$ 값보다 작거나 같으면 정상으로 판단합니다. 자세한 그림은 다음과 같습니다.

![1_2c21SkzJMf3frPXPAR_gZA](https://user-images.githubusercontent.com/28584213/160149754-6fa66402-af73-4a39-92f8-ff3e8009abdd.png)

<br />

## References

[1] Vinutha, H. P., Poornima, B., & Sagar, B. M. (2018). Detection of outliers using interquartile range technique from intrusion dataset. In Information and Decision Sciences (pp. 511-518). Springer, Singapore.