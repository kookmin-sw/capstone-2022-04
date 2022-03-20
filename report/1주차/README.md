# 캡스톤 1주차 보고서



## 실내 위치 측위의 필요성

최근 Internet of Things (IoT)의 발전으로 시마트시티가 큰 관심을 받고있다. 스마트시티는 다양한 유형의 전자 센서를 사용하여 수집된 데이터를 기반으로 자산과 자원을 효율적으로 관리하는 데 필요한 정보를 제공하는 도시 지역을 의미합니다 [1]. 즉, 현실에서 수집되는 여러 데이터로 도시 운영과 생활 서비스를 최적화하여 삶의 질을 향상시키는 것을 말합니다 [2] [3]. 이러한 스마트 시티에서 가장 중요한 기술 중 하나는 실내 위치 측위 기술입니다 [4]. 실내 위치 측위 기술은 인간의 삶에서 가장 민감할 수 있는 보안, 의료 등의 분야에서 여러 목적으로 사용될 수 있습니다. 실내 위치 측위 기술을 활용한 몇가지 시나리오는 아래와 같습니다.



* CCTV 설치가 제한되는 탈의실, 화장실 등의 장소에서 도난 사건이 발생했을 때 유력한 용의자를 알아낼 수 있다. 특정 물건이 사라진 위치와 그 장소에 접근했던 사람들만 조사하면 지금보다 훨씬 수월하게 범인을 색출할 수 있다.
* 병원에서 의사나 간호사들이 환자들을 지속적으로 감독하지 않아도 정확한 환자의 위치를 알 수 있다. [5]
* 백화점과 같이 규모가 큰 건물에서 화재가 발생했을 때, 최초 발견자는 건물의 정확한 배치를 알지 못해도 신속하게 시민들을 안전한 장소로 안내할 수 있다 [6]. 그리고 소방관들은 안전 구역으로 이동하지 못한 시민들의 위치를 미리 파악하여 신속하게 구조할 수 있다.





## GPS를 사용하지 못하는 이유

위치 측위와 관련하여 많은 사람들에게 친숙한 시스템은 위성 항법 시스템 (Global Positioning System, GPS)일 것입니다. 아쉽게도 GPS는 크게 두 가지의 이유로 실내 위치 측위에서 사용될 수 없습니다. GPS의 위치 기반 서비스는 가시선 (LoS)에 의존되어 작동되는데, 실내 환경에선 가시선이 닿지 않아 사용하는 것은 매우 어렵습니다. 또한 유효한 실내 위치 측위 오차 범위는 1m인 반면, GPS는 최대 5m의 위치 정확도 오차가 존재하여 실외에 비해 공간이 좁은 실내에서 사용하는 것은 한계가 있습니다 [7]. 따라서 와이파이, 블루투스, VLC, RFID, UWB 등의 무선 기술을 활용한 실내 위치 측위 시스템이 활발히 연구되고 있습니다 [8].





## 무선 기술 중 BLE를 사용하는 이유

와이파이는 실내 위치 측위를 수행하기 위해 최소한의 하드웨어가 사용되므로 가장 간단한 방법일 수 있습니다. 하지만 무선 기술 중 와이파이는 사용 전력이 높은 편에 속하며 이것은 빠른 배터리 고갈의 원인이 됩니다. 따라서 와이파이는 대부분의 실내 위치 측위 시스템에서 이상적이지 않습니다 [9]. BLE는 대부분 배터리가 필요하다는 단점이 있지만, 배터리의 비용이 저렴하고 전력 소비가 낮아 단 한 개의 코인셀 배터리로 수개월 혹은 수년동안 사용될 수 있습니다 [4]. 이러한 이유로 BLE는 실내 위치 측위 시스템에서 초적의 솔루션으로 채택되었습니다 [10].





## Reference

[1] Matt Hamblen, Just what IS a smart city?, https://www.computerworld.com/article/2986403/just-what-is-a-smart-city.html, 2015, Accessed: February 14, 2022

[2] Boyd Cohen, The 3 Generations Of Smart Cities, https://www.fastcompany.com/3047795/the-3-generations-of-smart-cities, 2015, Accessed: February 14, 2022

[3] T. J. H. Gracia and A. C. García, “Sustainable smart cities. Creating spaces for technological, social and business development,” Boletín Científico de las Ciencias Económico Administrativas del ICEA, vol. 6, no. 12, pp. 1–224, 2018.

[4] Y. Shen, B. Hwang, and J. P. Jeong, ‘‘Particle filtering-based indoor positioning system for beacon tag tracking,’’ IEEE Access, vol. 8, pp. 226445–226460, 2020.

[5] S. S. Saab and Z. S. Nakad, ‘‘A standalone RFID indoor positioning system using passive tags,’’ IEEE Trans. Ind. Electron., vol. 58, no. 5, pp. 1961–1970, May 2011

[6] R. Zhang, F. Höflinger, and L. Reindl, ‘‘Inertial sensor based indoor localization and monitoring system for emergency responders,’’ IEEE Sensors J., vol. 13, no. 2, pp. 838–848, Feb. 2013

[7] F. Zafari, “iBeacon based proximity and indoor localization system,” Master’s thesis, Dept. Comput. Inf. Technol., Purdue Univ., West Lafayette, IN, USA, 2016.

[8] J. Kunhoth, A. Karkar, S. Al-Maadeed, and A. Al-Ali, “Indoor positioning and wayfinding systems: a survey,” Human-centric Comput. Inf. Sci., vol. 10, no. 1, p. 18, 2020.

[9] S. Sadowski and P. Spachos, “RSSI-based indoor localization with the Internet of Things,” IEEE Access, vol. 6, pp. 30149–30161, 2018

[10] F. Subhan, A. Khan, S. Saleem, S. Ahmed, M. Imran, Z. Asghar and J. I. Bangash, “Experimental analysis of received signals strength in Bluetooth Low Energy (BLE) and its effect on distance and position estimation,” Transactions on Emerging Telecommunications Technologies, p. e3793, 2019. 

