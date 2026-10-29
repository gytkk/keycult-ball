# keycult-ball

**Keycult No.1/60 케이스를 유지하고, PCB·플레이트를 교체해 유선 QMK 직교 배열과 G/H 사이 중앙 34mm Keyball을 결합하는 개인 프로젝트입니다.**

현재 단계: **예비 기구 배치 / 실제 수납 미확정 / 제조용 CAD·PCB·펌웨어 없음**.

![추천 66키 배치](design/preliminary/layout.png)

## 현재 추천안

- **15u × 5행, 66키**: 19.05mm 피치, 명목 키필드 **285.75 × 95.25mm**.
- 중앙 3열 × 3행을 비우고 볼 중심 `(0,0)`, G `(-38.10,0)`, H `(+38.10,0)`.
- Ø34 볼과 가정한 18mm 키캡 사이 최소 **12.10mm**.
- 주황색 **50 × 50mm는 임시 조립 예약 영역**이며 실제 홀더 외곽·가공 구멍이 아님. 키캡과 최소 **4.10mm**.
- 14u·중앙 2u·64키 대안은 같은 예약 영역과 키캡이 **5.425mm 겹쳐 보류**.
- 공개 도면은 **285.75 × 108.25mm 일반 직사각형 치수 경계**만 표시하며, 공식 플레이트 윤곽을 복제하지 않습니다. 공개 검증도 이 경계와 부품 간 평면 간격에 한정됩니다.
- 과거 공식 윤곽 포함 검사 결과는 별도 기록으로 남깁니다. 직사각형 경계 통과가 정확한 윤곽 포함을 증명하지 않으며, **케이스 내부 개구부·수직 깊이·실제 홀더 외곽 확인이 필요**합니다.

## 자료 안내

| 자료 | 내용 |
|---|---|
| [프로젝트 맥락](docs/project-context.md) | 요구사항, 결정 이유, 확정/가정/미확정, 실측·다음 단계 |
| [상세 설계와 출처](design/preliminary/design.md) | 치수 계산, 장착·flex, 센서 방향, QMK·USB 범위 |
| [Ploopy / Keyball / Charybdis 및 라이선스](docs/alternatives-and-licenses.md) | 제품별 차이, 원본 공개 범위와 재사용 조건 |
| [배치 HTML](design/preliminary/layout.html) · [SVG](design/preliminary/layout.svg) · [JSON](design/preliminary/layout.json) | 브라우저 설명도, 편집 가능한 벡터, 모든 키 중심 좌표 |
| [단면 SVG](design/preliminary/section.svg) · [PNG](design/preliminary/section.png) | 수직 설치 센서와 미확정 Z 스택 |
| [1:1 A3 PDF](design/preliminary/print-1to1.pdf) · [SVG](design/preliminary/print-1to1.svg) | 100mm 기준선 포함 종이 검증용 |
| [재현·검증 방법](docs/reproduction.md) | 좌표 생성, PNG/PDF 렌더, 원본 취득·해시 검증 |

HTML은 내려받아 브라우저에서 엽니다. GitHub에서는 위 PNG로 미리 볼 수 있습니다.

## 빠른 재생성

```bash
python3 design/preliminary/build_artifacts.py
uv run scripts/validate.py
# PNG/PDF도 다시 만들 때 (Chromium 필요)
uv run scripts/render.py
uv run scripts/validate.py
```

`build_artifacts.py`의 배열·치수 상수가 편집 원본이며 JSON/SVG/HTML은 파생 산출물입니다. JSON만 수정한 뒤 생성기를 실행하면 덮어쓰므로 설계 변경은 생성기에 반영합니다.

공식 윤곽 검사는 위 공개 검증과 별개입니다. 원본 조건을 확인하고 공식 DXF를 로컬에 취득한 뒤 `uv run scripts/verify_official_contour.py`로 재현합니다. 추출 좌표와 재검사 출력은 Git에서 제외하는 `design/preliminary/sources/local/`에만 저장합니다. [과거 검사 기록](design/preliminary/plate-containment.json)은 현재 공개 도형의 검증 결과가 아닙니다. 세부 절차는 [재현 문서](docs/reproduction.md)를 따릅니다.

## 범위와 출처 관리

정식 산출물은 이 저장소에서 관리합니다. 원본 대화·개인 메모·인증 정보는 포함하지 않습니다. 제3자 STEP/DXF/Gerber 원본과 공식 플레이트 윤곽 복제본은 재배포하지 않고, 공식 URL·해시·형상을 복제하지 않는 요약 측정값 및 로컬 취득·검사 절차를 제공합니다. 공개 SVG/HTML/PNG/PDF는 독립 키 배열과 일반 직사각형 치수 경계만 사용합니다. 정확한 윤곽 좌표는 Git에서 제외하는 `design/preliminary/sources/local/measured-official-dxf.json`에 두며, 요약 치수만 담은 `measured-official-step.json`은 공개 자료에 남깁니다. 원본의 개인·비상업 사용 조건과 공개 재배포 허가는 별개이며, 저장소 공개 자체가 제3자 자료의 포괄적 재사용 허가를 뜻하지 않습니다. [자료별 라이선스](docs/alternatives-and-licenses.md)를 확인합니다.
