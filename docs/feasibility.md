# 중앙 트랙볼의 실현 가능성과 대안

확인일: 2026-10-29. 대상은 사용자가 보유한 NovelKeys 최신 판매 버전의 Keycult No.1/60 WK다. 정확한 리비전과 내부 치수는 아직 확인되지 않았다. 사용자는 G/H 사이 중앙을 유지하는 작은 볼 또는 터치패드와, 완성 가능성을 우선하는 외부 별도 모듈을 모두 검토하기로 했다. 이 문서는 후보 비교이며 현재 34mm Keyball 예비 배치를 수정하거나 대체품 채택을 확정하지 않는다.

## 판단

**34mm Keyball 중앙 통합은 기구 시제품으로 검토할 가치는 있지만, 현재 근거로 PCB와 보강판 제작에 바로 착수할 만큼 확실한 계획은 아니다.** 평면 배치의 가능성은 확인했지만 실제 홀더, 수직 공간, 장착 강성, 사용자 손의 접근을 함께 검증하지 않았다. 34mm가 필수 조건이 아니라면 중앙 터치패드와 외부 USB 장치를 먼저 시험하는 쪽을 권한다.

중앙 위치를 유지할 때는 **Cirque의 기존 Pinnacle 기반 23mm 또는 35mm 터치패드가 수직 공간 문제를 줄일 근거가 가장 구체적인 후보**다. 제조사가 부품을 포함한 두께를 공개하며 QMK도 해당 컨트롤러를 명시적으로 지원한다. 다만 같은 TM023023/TM035035 제품군의 신형 Gen6s는 통신 방식이 다르므로, 주문할 전체 부품번호와 컨트롤러를 확인해야 한다. 작은 트랙볼의 완성 조립체 치수를 확보하지 않은 상태에서 볼 지름만 줄여 공간 문제가 해결된다고 판단할 수 없다. [Cirque 문서 목록](https://www.cirque.com/documentation), [QMK 포인팅 장치 문서](https://docs.qmk.fm/features/pointing_device#cirque-trackpad)

외부 장치를 허용하면 **조립된 USB 트랙볼을 먼저 사용하고 필요할 때 받침만 제작하는 방법이 기구 제작 부담을 가장 줄인다**. 작은 후보인 Ploopy Nano 2는 조립된 상태로 판매하며 QMK와 VIA를 제공한다. 키보드 앞 중앙이나 옆에 둘 수 있지만 손목과 스페이스바 접근을 시험해야 하고, G/H 사이 중앙 내장 조건은 충족하지 않는다. 기존 케이스, PCB와 보강판을 그대로 사용할 수 있다는 것이 이 방법의 장점이다. [Nano 2 판매 사양](https://ploopy.co/shop/nano-2-trackball/)

## 34mm 안에서 아직 풀지 못한 문제

**보유 케이스와 과거 도면의 일치 여부.** NovelKeys 판매 페이지는 No.1/60 재출시와 부품 선택 구성을 설명하지만, 확인한 설명에서 초기형 및 Rev.1 공개 CAD와의 내부 치수 호환을 명시하지 않는다. 기존 저장소의 285.75 x 108.25mm 플레이트 측정값과 과거 윤곽 검사를 보유 케이스의 장착 검증으로 사용할 수 없다. WK라는 정보는 기록하되 내부 개구부와 체결 기준은 실측해야 한다. [NovelKeys 제품 페이지](https://novelkeys.com/products/keycult-no-1-60-keyboard), [기존 측정 출처](../design/preliminary/sources/README.md)

**볼과 완성 모듈의 크기 차이.** Keyball 공식 가이드는 34mm 볼과 홀더 뒤쪽에 세우는 센서 PCB를 설명한다. 조사한 공개 파일에서 생산 홀더의 독립 CAD나 전체 조립 외곽 치수는 확보하지 못했다. 기존 22 x 25mm 값은 센서 기판에만 해당한다. [고정 리비전의 Keyball 조립 가이드](https://github.com/Yowkees/keyball/blob/e1d1948e6e60a83f6b3566a209326508200d64ce/keyball44/doc/rev1/buildguide_en.md)

비교 사례로 BastardKB의 독립 `34-mm-trackball-holder`는 STEP/STL을 제공하고 반경 21mm, 높이 2mm의 통합용 링을 지정한다. 고정 커밋 `1bb7b1a49d6d5beca8eb48987bdb35460ba3529e`의 상부와 하부 binary STL 꼭짓점 범위를 계산하면 원본 X/Z 방향의 최대 외곽은 약 45.6mm다. 이는 플라스틱 부품만의 치수이며 Keyball 홀더 치수나 완성 모듈의 설치 깊이가 아니다. 저장소명은 34mm지만 README는 35mm라고 적으므로, 해당 부품을 채택하려면 실제 볼 호환도 확인해야 한다. [BastardKB 홀더와 원본 파일](https://github.com/Bastardkb/34-mm-trackball-holder/tree/1bb7b1a49d6d5beca8eb48987bdb35460ba3529e)

**높이를 줄이면 돌출이 커지는 제약.** 플레이트 아래에서 볼에 쓸 수 있는 깊이를 D, 플레이트 위 볼 중심을 c로 두면, 지름 34mm 볼 자체만으로도 `c - 17 >= -D`, 따라서 볼 최상단은 `c + 17 >= 34 - D`다. 예를 들어 D가 10mm라면 볼 위끝은 최소 24mm 위로 올라온다. 이는 설명용 기하 계산이며 실제 케이스 깊이가 10mm라는 뜻이 아니다. 홀더, 센서, 커넥터, 절연과 휨 여유를 넣으면 제약이 더 생긴다. 모듈을 위로 올리는 방법은 수납을 도울 수 있지만 손가락 접근과 타건 간섭을 함께 시험해야 한다.

**볼을 조작할 때의 강성과 접근성.** 기존 Keycult 설명의 플레이트는 가스켓으로 케이스에서 분리된다. 중앙 절개와 모듈 질량을 추가한 뒤에도 같은 타건감과 강성을 유지한다고 가정할 수 없다. 볼과 센서를 같은 강체에 고정한 모듈, 충분한 중앙 보강, 또는 실물의 기존 체결점을 쓰는 브래킷을 검토할 수 있으나 어느 방식도 아직 설계되지 않았다. 기존 3u 중앙안의 G/H 중심 간격은 76.20mm이므로 사용자 손에 맞는지도 별도 시험해야 한다. [Keycult의 기존 장착 구조 설명](https://keycult.com/pages/no-1-60-no-1-65), [현재 장착 검토](../design/preliminary/design.md)

## 확인된 치수와 구분해야 할 외곽

| 후보 | 제조사 또는 설계자 자료에서 확인한 값 | 확인되지 않은 값과 설치 조건 |
| --- | --- | --- |
| Cirque TM023023, 기존 Pinnacle | 모듈 지름 23.20 +/- 0.25mm, 감지 영역 지름 21.60mm. PCB 0.74mm, PCB와 접착층 0.89mm, PCB와 접착층 및 부품 5.04 +/- 0.320mm. [23mm 사양서, v1.1, p.6](https://www.dropbox.com/scl/fi/0cdhpythfobsarivtsosw/GP-DS-170805-TM023023-SPI-I2C-PINN-Trackpad-Spec.pdf?rlkey=331uxyu8esyjjo20zn1kjw944&dl=0) | 5.04mm는 별도 상부 오버레이와 장착 지지체까지 포함한 완성 설치 높이가 아니다. FFC 케이블의 굴곡 공간도 확보해야 한다. |
| Cirque TM035035, 기존 Pinnacle | 모듈 지름 35.0mm, 감지 영역 지름 31.00mm. PCB 1.00 +/- 0.125mm, PCB와 오버레이 1.25mm, PCB와 오버레이 및 부품 5.40 +/- 0.20mm. [35mm 사양서, v1.3, p.6](https://www.dropbox.com/scl/fi/fl600un1qv1cupbfjng95/GP-DS-170409-TM035035-SPI-I2C-PINN-Trackpad-Spec.pdf?rlkey=1pl0tw13air87pt92mkj72igx&dl=0) | 지름이 34mm 볼보다 작지는 않지만 볼과 홀더를 설치할 깊이가 필요하지 않다. 하부 지지체와 케이블은 표의 두께 외에 필요하다. |
| Pimoroni Trackball Breakout, PIM447 | 현재 제조사 페이지의 외곽 치수는 25 x 22 x 11mm다. 볼, 사출 홀더, Hall 센서와 MCU가 있는 기판의 제품이며 I2C, 3.3V 또는 5V를 사용한다. [Pimoroni 제품 사양](https://shop.pimoroni.com/products/trackball-breakout) | 25mm는 볼 지름이 아니다. 별도 장착체와 배선까지 포함한 치수가 아니며, 볼 지름과 광학 트랙볼에 대응하는 정확도는 해당 사양에 명시되지 않는다. 구형 자료의 9.5mm 높이를 현재 제품에 그대로 적용하지 않는다. |
| Azoteq TPS43 | 43 x 40mm 직사각형 터치패드로 IQS572 컨트롤러와 6핀 I2C 연결을 사용한다. PCB 두께는 1mm이며 오버레이 선택에 따라 적층이 달라진다. [제조사 제품 설명](https://www.azoteq.com/product/i2c-trackpad-modules/), [사양서 v1.06](https://www.azoteq.com/images/stories/pdf/proxsense_i2c_trackpad_datasheet.pdf) | PCB 1mm를 부품, 오버레이와 장착체가 포함된 높이로 사용하지 않는다. 43mm와 40mm 어느 방향도 2u 비교안의 39.15mm 키캡 사이 통로보다 크므로 3u 중앙안에서 비교할 후보다. |
| Oddball v2의 25mm 광학 트랙볼 구조 | 설계자가 25mm 볼, 3.175mm 지지구 3개, ADNS9800 또는 PMW3360 센서와 별도 지지체를 사용한다. 조립 가이드에 CAD 링크와 QMK 빌드 명령이 있다. [Oddball v2 가이드](https://atulloh.github.io/oddball/v2/build-guide.html) | 25mm는 볼 지름이다. 중앙에 이식할 전체 조립체 W/H/Z를 이 조사에서 확정하지 않았다. 원 설계자는 센서 높이와 각도 때문에 기울어진 케이스가 필요하다고 설명하므로, 낮은 No.1/60 중앙에 그대로 맞는 모듈로 볼 수 없다. [설계자 README](https://github.com/atulloh/oddball) |
| Ploopy Nano 2 | 공식 부품 목록은 1.5인치 볼과 MR63ZZ 롤러 베어링 3개다. 1.5인치의 환산값은 38.10mm이며 하드웨어 문서는 약 38.00mm로 표기한다. 제품 소개의 Case Dimensions는 62 x 54 x 49mm다. [Nano 2 하드웨어 문서](https://ploopyco.github.io/nano-2-trackball/appendices/hardware/), [제품 소개](https://ploopy.co/nano-2/) | 더 작은 볼을 쓰는 대안이 아니다. 판매 페이지의 Additional information에 있는 8 x 7 x 7cm와 제품 소개의 케이스 치수를 구분한다. 외부 USB 장치로 비교하며 받침과 케이블 공간은 추가로 필요하다. |

## 중앙 너비에 미치는 영향

다음 값은 현재 저장소의 19.05mm 피치와 18mm 키캡 가정을 이용한 계산이며 실물 측정값이 아니다. 14u 비교안의 G/H 중심이 x = +/-28.575mm이면 두 키캡 안쪽 면의 간격은 `2 x 28.575 - 18 = 39.15mm`다. 현재 15u 추천안에서는 같은 간격이 `2 x 38.10 - 18 = 58.20mm`다. [현재 배치의 기준](project-context.md)

| 장치 외곽을 14u 중앙에 놓는 가정 | 양쪽에 남는 명목 간격 | 해석 |
| --- | --- | --- |
| Cirque 23.20mm 모듈 | 각각 7.975mm | 하부 지지체, 베젤, 케이블을 이 간격 안이나 다른 높이에 배치할 수 있는지 추가 확인 필요 |
| Cirque 35.0mm 모듈 | 각각 2.075mm | 모듈 자체의 평면 배치는 가능성이 있지만 키캡 스트로크, 손가락 접근과 장착 테두리의 여유가 작음 |
| Pimoroni의 25mm 변을 중앙 폭으로 사용 | 각각 7.075mm | 실제 장착체와 배선을 제외한 제품 치수에 대한 계산 |
| 지름 25mm 볼만 사용 | 각각 7.075mm | 홀더, 지지점, 렌즈, 센서와 나사의 여유를 뜻하지 않으므로 조립체 수납 판단에 사용 불가 |

따라서 작은 터치패드와 PIM447은 현재 50 x 50mm 임시 예약 영역보다 작은 제품 외곽을 제시한다. 이로부터 14u안을 다시 검토할 이유는 생기지만, 실제 케이스 개구부 통과나 전체 키 수를 유지하는 새 배열의 성립은 별도 문제다. 키캡 사이의 명목 공간이 있다고 해서 인접 스위치 하우징, 소켓, 부품 및 케이블과 같은 높이에서 충돌하지 않는다는 뜻은 아니다.

## 펌웨어와 사용성의 타협

- **Cirque Pinnacle**: QMK는 Pinnacle 1CA027을 사용하는 TM023023, TM035035, TM040040을 명시하고 I2C 및 SPI 드라이버를 제공한다. 탭과 원형 스크롤 등의 기능을 설정할 수 있으나 이를 노트북의 모든 멀티터치 기능과 동일시하지 않는다. 23mm의 실제 감지 지름은 21.60mm이므로 짧은 손가락 이동 거리와 커서 감도 사이의 타협을 시제품으로 평가해야 한다. [QMK 지원 범위와 설정](https://docs.qmk.fm/features/pointing_device#cirque-trackpad)
- **Cirque Gen6s**: 제조사 문서 목록은 기존 Pinnacle 사양을 Deprecated로 분류한다. 현재 23mm Gen6s 사양은 I2C 주소 0x2C의 HID over I2C이며 6핀 커넥터를 사용한다. 기존 Pinnacle의 드라이버와 배선을 그대로 적용할 근거가 없으므로 기존 부품 확보 여부 또는 새 드라이버 필요성을 먼저 확인한다. 23mm Gen6s는 모듈 지름 23.00 +/- 0.15mm, 감지 영역 지름 21.00mm, PCB와 Mylar 오버레이 및 부품 높이 5.05 +/- 0.320mm를 명시한다. 파일명은 GP-DS-230612이지만 문서 본문은 GP-DS-240605 v1.3이다. [제조사 문서 목록](https://www.cirque.com/documentation), [Gen6s 사양서, p.5-8, 12](https://www.dropbox.com/scl/fi/jqbt0uy83zhshvf3oyvsa/GP-DS-230612-TM023023-Gen6s-Touchpad-Specification.pdf?rlkey=h2e66gosfo6gbo7pbuf0hxpqj&dl=0)
- **Pimoroni**: QMK의 `pimoroni_trackball` 드라이버가 있다. 제조사가 설명하는 방식은 회전하는 자석을 Hall 센서로 읽는 구조이므로 PMW3360 광학 센서와 같은 정밀도나 빠른 이동 추적 성능을 보장할 수 없다. 공간 검증용 후보로는 구체적이지만 주 포인팅 장치를 대체할 수 있는지는 직접 사용해 확인해야 한다. [QMK 지원](https://docs.qmk.fm/features/pointing_device#pimoroni-trackball), [제조사 구조 설명](https://shop.pimoroni.com/products/trackball-breakout)
- **Azoteq TPS43**: QMK는 `azoteq_iqs5xx`와 TPS43 프로파일, 두 손가락 탭 및 스크롤 설정을 제공한다. holykeebs에도 TPS43 기반 모듈의 조립 사례가 있다. 다만 제조사 목록은 IQS572-B000을 새 설계에 권장하지 않는 NRFND로 표시하므로 확보할 부품과 공급 지속성을 확인해야 한다. 기존 3u 중앙 공간을 유지하면서 넓은 입력 면적을 원할 때의 비교 후보이며 노트북 터치패드와 같은 사용감을 보장하지 않는다. [QMK 지원](https://docs.qmk.fm/features/pointing_device#azoteq-iqs5xx-trackpad), [모듈 사례](https://holykeebs.com/products/touchpad-module), [제조사 부품 상태](https://www.azoteq.com/design/datasheets/)
- **Oddball 25mm**: 광학 센서와 볼을 유지할 수 있는 설계 사례다. 그러나 전용 텐팅 구조와 설계자 QMK fork를 No.1/60용 새 기구 및 펌웨어에 맞춰야 하므로 즉시 사용할 소형 완성 모듈로 추천하지 않는다. [설계자 자료](https://github.com/atulloh/oddball), [조립 및 펌웨어 가이드](https://atulloh.github.io/oddball/v2/build-guide.html)
- **외부 Nano 2**: 별도 USB 케이블로 연결하는 완성 장치는 새 PCB의 포인팅 센서 통합을 필요로 하지 않는다. 물리 버튼이 하나이므로 클릭과 스크롤을 어떻게 배정할지 확인해야 하며, 제조사는 롤러 베어링 소음도 명시한다. USB 허브만으로 키보드의 QMK 레이어 상태와 별도 트랙볼의 스크롤 모드가 연동되지는 않는다. 첫 시험은 장치 자체 버튼과 별도 USB 연결을 사용한다. [Nano 2 제품 설명](https://ploopy.co/shop/nano-2-trackball/), [제조사 저장소](https://github.com/ploopyco/nano-2-trackball)

Cirque 설치는 하부에서 지지해 탭 동작 시 과도한 휨을 막고, 베젤에 도전성 재료를 사용하지 않도록 하는 제조사 권고를 따라야 한다. 금속 Keycult 케이스와 금속 플레이트에 직접 밀착시키는 방식의 적합성을 가정하지 않는다. 이 조건은 비도전성 베젤과 지지체를 실제 높이에 포함해야 하는 이유다. [35mm 사양서, p.12](https://www.dropbox.com/scl/fi/fl600un1qv1cupbfjng95/GP-DS-170409-TM035035-SPI-I2C-PINN-Trackpad-Spec.pdf?rlkey=1pl0tw13air87pt92mkj72igx&dl=0)

TrackPoint 방식도 중앙 포인팅의 별도 후보다. holykeebs는 센서와 드라이버가 분리된 3.3V `SK8707-01-004`를 제공하고, QMK는 PS/2 포인팅 장치를 지원한다. 다만 기존 분리형 키보드용 완성 어댑터를 No.1/60에 그대로 넣을 수 있다는 뜻은 아니다. 고정 구조, 스틱과 키캡 사이 간섭, 배선과 초기화 회로를 검토해야 하며 힘으로 커서를 움직이는 조작감도 트랙볼과 다르다. 키캡 사이에 보이는 스틱 크기만으로 하부 조립체의 수납을 판단할 수 없어 이번 우선 후보에서는 제외한다. [센서 제품과 사양서](https://holykeebs.com/products/sk8707-01-trackpoint-sensor), [QMK PS/2 지원](https://docs.qmk.fm/features/ps2_mouse)

외부 장치에서 물리 클릭 버튼이 더 필요하면 6버튼과 drag scroll을 제공하는 Ploopy Adept 같은 완성 제품도 비교할 수 있다. Nano 2의 작은 크기와 단일 버튼이라는 타협을 받아들일 수 있는지에 따라 선택한다. 최신 A+는 8버튼과 두 회전 노브를 제공하는 후속 제품이지만 조사 시점에 예약 판매로 안내되므로 즉시 확보할 수 있다고 가정하지 않는다. [Adept 제품 소개](https://ploopy.co/adept-trackball/), [A+ 공식 발표](https://blog.ploopy.co/the-aplus-is-finally-here-499), [A+ 판매 안내](https://ploopy.co/shop/a-trackball-fully-assembled-preorder-tier-d/)

## 다음 선택과 검증

1. **완성 가능성을 먼저 확인**하려면 외부 USB 장치를 키보드 앞 중앙 또는 옆에 놓고 클릭, 스크롤, 드래그, 타건 중 손목 간섭을 시험한다. 사용감이 충분하면 내부 PCB 제작을 하지 않고 배치나 받침만 정할 수 있다.
2. **G/H 중앙을 유지**하려면 확보 가능한 전체 부품번호가 명확한 Cirque Pinnacle 23mm와 35mm를 먼저 비교한다. 23mm는 중앙 너비에 유리하고, 35mm는 감지 면적이 넓다. 임시 지지체와 별도 컨트롤러로 입력과 접근성을 먼저 확인하고, 설치 높이와 테두리까지 맞는 경우에 새 PCB 설계로 진행한다. 어느 쪽도 No.1/60 설치가 검증된 것은 아니다.
3. **34mm 안은 실제 조립체가 조건을 통과하면 유지**한다. 케이스와 홀더의 같은 좌표계에서 높이별 간섭이 없어야 하고, 키를 끝까지 누르거나 볼을 누르고 굴릴 때도 바닥 접촉, 센서 상대 변위, 손가락 간섭이 없어야 한다. 불만족하면 더 작은 볼만 구입하거나 홀더를 일률적으로 축소하기보다 앞의 대안을 선택한다.

어떤 중앙 후보를 선택하든 케이스의 중앙 깊이, 개구부, 장착 기준, 모듈과 지지체의 조립 외곽, 케이블 경로를 같은 좌표계로 측정해야 한다. 새 배열을 만들기 전에는 종이에 실제 크기의 감지 면적을 출력해 G/H 사이에서 접근과 이동 거리를 확인하고, 센서 평가용 시제품으로 커서 이동과 클릭 및 스크롤을 확인한다. 요구사항을 실제 변경하면 [프로젝트 맥락](project-context.md), 생성기와 관련 검증을 함께 갱신한다.

이 조사는 제품 구매, CAD 형상 이식, PCB 설계, 펌웨어 빌드 또는 실물 사용 시험을 수행하지 않았다. 치수 표는 공개 사양의 해당 세대에만 적용하며 현재 판매 재고와 배송을 보장하지 않는다. 제3자 CAD와 사양서 원본을 저장소에 복제하지 않았으며, 설계 파일을 재사용할 때의 권한 확인은 [기존 자료 관리 기준](alternatives-and-licenses.md)을 따른다.
