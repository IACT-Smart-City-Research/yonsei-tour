# 개요

사용자의 MBTI 성향, 인구통계적 정보를 기반으로 한국 관광지를 추천해주는 시스템을 제안한다.



# 주제 선정 이유

#### 1. 관광은 고부가가치 산업

[[관광산업①] 한국 관광은 ‘왜’ 이렇게 일본에 뒤처졌을까](https://www.sisajournal.com/news/articleView.html?idxno=177744)

- 인구 감소와 고령화는 소비와 생산, 유통을 동시에 위축시킴
- 관광은 상대적으로 젊은 유동인구를 유입시켜 소비와 유통을 늘리고 생산을 자극 -> 고용유발
- 지방 관광은 지역 사회 발전에도 영향



#### 2. 현 관광산업의 문제점

- 몰개성한 관광지 제안
  - 여행의 트렌드에 따른 코스
  - 여행사 일정에 따른 코스
  - 개인의 특성, 여행 목적과 무관한 코스
- 여행 만족도 하락으로 이어짐



#### 3. 이제는 취향과 개성의 시대 - 맞춤형 관광지 추천



![reason_2](/Users/jaewonheo/Documents/yonsei-tour/mid_report_fig/reason_2.jpg)

[[트렌드 인사이트]여행액티비티 시장 황금의 땅일까 1](http://www.ttlnews.com/article/travel_report/4166)

- 개별 여행의 증가 - 패키지 여행의 감소
- OTA/메타서치(익스피디아 등)를 통한 직접 예약이 증가하는 추세
- 획일화된 패키지 상품 시대에서 개인 맞춤형 상품의 시대로





# 개발 일정 및 팀원 역할

![timeline](/Users/jaewonheo/Documents/yonsei-tour/mid_report_fig/timeline.png)





# 수집 데이터

### 1. Tripadvisor 리뷰 데이터

![trip_crawl](/Users/jaewonheo/Documents/yonsei-tour/mid_report_fig/trip_crawl.png)

- TripAdvisor는 호텔 및 레스토랑 리뷰, 숙박 예약 및 기타 여행 관련 콘텐츠를 보여주는 미국 여행 웹사이트
- 해외 유저들 개개인이 느끼고 경험한 바가 리뷰로 남겨져 있음
- BeautifulSoup를 이용해 서울의 관광지 리스트를 먼저 크롤링한 후, 그 리뷰들을 모음.
- 총 471개 관광지
- csv 예시





### 2. Instagram 피드 데이터

![inst_crwawl](/Users/jaewonheo/Documents/yonsei-tour/mid_report_fig/inst_crwawl.png)

- Instagram은 사진 및 비디오 공유 소셜 네트워킹 서비스

- 어떤 부분에서 관광객들이 매력을 느꼈는지 해시태그를 통해 확인할 수 있음

- csv 예시

  



### 3. 외래관광객 실태조사

- 한국관광공사가 우리나라를 방문한 외래관광객의 한국 여행실태, 한국내 소비실태 및 한국 여행 평가를 조사하여 외래관광객의 한국 여행성향을 파악하고 연도별 변화추이를 비교·분석함으로써, 외래관광객 유치 증대 및 향후 관광수용태세 개선을 위한 관광정책 수립의 기초 자료를 제공하는데 목적이 있는 자료

[인포그래픽](https://kto.visitkorea.or.kr/file/download/bd/522dfda4-6d8e-11e9-b01e-c515ccf49883.pdf.kto)





# 모델링







# 프로토타입 구조

![prototype](/Users/jaewonheo/Documents/yonsei-tour/mid_report_fig/prototype.png)

### 협업 필터링

- 사용자들로부터 얻은 상품에 대한 선호도를 이용하여 관심사를 예측하는 기법

- 아마존, 넷플릭스 등에서 사용되고 있음

  



![CF_0](/Users/jaewonheo/Documents/yonsei-tour/mid_report_fig/CF_0.png)

#### 사용자 기반 필터링

- 선호 이력이 유사한 다른 사용자의 선호 아이템을 탐색
- 아직 구매하지 않은 아이템을 추천
- 사용자 3과 가장 유사한 사용자 1의 선호 아이템을 추천



![CF_1](/Users/jaewonheo/Documents/yonsei-tour/mid_report_fig/CF_1.png)

#### 아이템 기반 필터링

- 사용자 선호 아이템을 탐색
- 해당 아이템과 유사한 아이템을 추천 (사과와 햄버거)
- 햄버거를 구매한 사용자에게 사과를 추천



#### 한계

- 실제 사용자의 데이터가 있어야 한다는 점이 단점
- 단순 아이템 기반 모델링의 한계를 보완하고자 도입 차순위에 두고 진행할 예정