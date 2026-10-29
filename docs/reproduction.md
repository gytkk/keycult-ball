# 재생성·검증

명령은 저장소 루트에서 실행한다. 모든 스크립트는 자신의 파일 위치를 기준으로 경로를 찾으며 개인 작업공간 절대 경로를 요구하지 않는다.

## 1. 좌표·벡터·HTML

```bash
uv run design/preliminary/build_artifacts.py
```

Python 표준 라이브러리만 필요하다. 입력은 생성기 안의 배열/상수 및 `sources/keyball-evidence.json`이다. 공식 CAD나 상세 윤곽 좌표 없이 공개 도면을 생성한다. 초록색 사각형은 285.75 × 108.25mm 전체 치수 참고 경계이며 실제 윤곽이나 케이스 개구부가 아니다. 출력은 `layout.json`, `validation.json`, 평면/대안/단면/인쇄 SVG 및 HTML이다. **기존 PNG/PDF나 플레이트 포함 결과는 이 명령만으로 새로 계산되지 않는다.**

설계를 바꿀 때 배열과 치수 상수를 먼저 편집한다. JSON은 모든 키 중심을 다른 CAD 도구로 가져가기 위한 교환 파일이지만 이 생성기의 입력은 아니므로 JSON에만 한 수정은 재생성 시 덮어쓴다. SVG는 벡터 편집기로 열 수 있지만 그 수정도 생성기에는 역반영되지 않는다.

`layout.json`은 66키 기준안, 14u 64키 비교안과 `rear_clearance` 63키 옵션의 좌표를 포함한다. 63키 옵션은 `rear-clearance.svg`와 `rear-clearance-print.svg`/`.html`로 생성하며, 볼 지름 34mm와 나머지 키를 유지하고 상단 중앙 Vol-/Mute/Vol+만 제거한다. 중앙 57.15 × 76.20mm 빈 명목 영역은 가공 구멍이나 확대된 홀더 예약 영역이 아니다.

## 2. PNG·1:1 PDF

시스템 Chromium과 [uv](https://docs.astral.sh/uv/)가 필요하다. 스크립트 내 PEP 723 메타데이터로 Playwright 1.56.0을 선언했다. 브라우저를 추가 다운로드하지 않고 시스템 Chromium을 사용한다.

```bash
uv run scripts/render.py
```

`chromium` 또는 `chromium-browser`가 PATH에 없으면 `KEYCULT_CHROMIUM=/절대/경로/chromium`을 지정한다. 명령은 평면 PNG, 단면 PNG, A3 PDF와 63키 옵션의 `rear-clearance.png`, `rear-clearance-print.pdf`를 다시 만든다. SVG/HTML에 외부 폰트·스크립트·이미지 요청은 없다. PNG 렌더는 브라우저/설치 폰트에 따라 작은 차이가 날 수 있다.

## 3. 독립 검증

```bash
uv run scripts/validate.py
```

Shapely 2.1.2와 PyMuPDF 1.26.7을 사용한다. 다음을 검사한다.

- Python AST, JSON, SVG/XML, HTML 파싱과 문서/HTML 로컬 링크.
- 66/64/63키 개수, 중복 좌표, 19.05mm 피치, 중앙 정렬, 문자 키, 키캡 쌍 충돌. 63키 옵션은 기준안에서 상단 중앙 세 키만 제거했는지도 확인.
- 원–사각형 거리로 볼 간섭을 다시 계산하고 저장된 결과와 비교.
- 임시 50mm 영역의 양수/음수 간격 및 일반적인 사각 치수 경계에 대한 Shapely 포함·최소 거리. 결과는 `envelope-containment.json`에 저장한다. 공개 SVG에 상세 윤곽이 아닌 사각 치수 경계가 있는지도 확인한다.
- 미확정 케이스 개구부·깊이·홀더 치수가 JSON에서 계속 `null`인지 확인.
- 기준안과 63키 옵션의 PDF가 각각 한 페이지 A3 가로인지, 벡터상의 100mm 기준선 길이가 맞는지 확인. 결과는 `print-validation.json`과 `rear-clearance-print-validation.json`에 기록.

공개 검증은 공식 윤곽을 사용하지 않으며 실제 윤곽 포함을 증명하지 않는다. `plate-containment.json`은 초기 66/64키 공식 윤곽 조사에서 얻은 스칼라 결과 기록이며 이 명령으로 재계산하지 않고 63키 옵션도 다루지 않는다. 상세 윤곽 재현은 아래 로컬 전용 절차로 수행한다. 이 검증은 PCB DRC, 실제 케이스 개구부, 3D 수납, 소켓·다이오드·배선·하중 검증을 대체하지 않는다.

종이 출력은 **A3 가로 / 100% 실제 크기 / 페이지 맞춤 끄기**로 하고 100mm 선을 자로 확인한다. PDF 내부 길이가 정확해도 프린터 배율까지 보증하지는 않는다.

## 4. 원본 자료 취득과 측정 재확인

원본 STEP/DXF/Gerber는 저장소에 포함하지 않는다. 먼저 [라이선스·사용 조건](alternatives-and-licenses.md)을 확인한다. 아래 명령은 고정 출처 세 ZIP을 git-ignored 디렉터리 `design/preliminary/sources/upstream/`에만 저장하고, 조사 당시 SHA-256과 일치해야 성공한다. 자동 압축 해제나 외부 파일 실행은 하지 않는다.

```bash
uv run scripts/fetch_sources.py
```

[원본 해시와 측정 방법](../design/preliminary/sources/README.md)에 개별 파일 체크섬도 있다. 원본이 바뀌면 해시 실패를 무시하지 말고 새 리비전으로 별도 검토한다.

### 로컬 전용 공식 윤곽 재검증

```bash
uv run scripts/verify_official_contour.py
```

ezdxf 1.4.3와 Shapely 2.1.2를 사용한다. 로컬 ZIP 및 내부 DXF의 고정 SHA-256을 재확인하고, 가장 큰 유효 폐곡선에서 공식 외곽을 복원한다. 키캡/스위치 포함·최소 거리를 재계산해 초기 `plate-containment.json` 수치와 비교한다. 배치 변경 후 차이가 생기면 결과를 검토한 뒤 초기 보고서를 의도적으로 갱신해야 한다.

상세 좌표 `measured-official-dxf.json`, 현재 포함 결과 `plate-containment.json`, 정밀 오버레이 `layout-overlay.svg`는 모두 **git-ignored `design/preliminary/sources/local/`**에만 생성한다. 공개 PNG/PDF는 수정하지 않는다. 원본 윤곽이 들어 있는 로컬 파생물은 공개용 산출물과 구분하며, 배포 조건은 [대안·라이선스 문서](alternatives-and-licenses.md)를 따른다.

초기 측정은 ezdxf와 CadQuery/OpenCascade를 사용했다. 재확인 시:

- DXF: `$INSUNITS=4`; 바깥 폐곡선을 `ezdxf.path.make_path(...).flattening(0.01)`로 샘플링한다. `x=-x_native-142.875`, `y=y_native-47.625`로 변환한다. 네이티브 bulge 꼭짓점도 로컬 전용 `sources/local/measured-official-dxf.json`에 생성한다.
- STEP: `cadquery.importers.importStep(path).val().BoundingBox()`로 x/z 평면과 y 두께를 읽는다. 원본 및 Rev.1 3종 결과는 `measured-official-step.json`에 있다.
- Gerber: 고정 Keyball46 센서 `ball_sensor-Edge_Cuts.gbr`는 mm/4.6 좌표 형식이며 x=100…122, y=−100…−75mm이다. 현재 판매 부품 전체 크기를 뜻하지 않는다.

현재 스크립트는 원본 CAD 측정 전체를 자동화하는 범용 CAD 파이프라인은 아니다. 이후 공식 STEP+실물 홀더를 FreeCAD에서 합쳐 높이와 체결부를 검토한다.


## KiCad 66키·63키 회로·PCB 초안

[PCB 재현 안내](../design/pcb/README.md#reproduction)를 별도로 따른다. 기존 예비 키 좌표는 변경하지 않았으므로 예비 도면 생성기나 PNG/PDF 렌더를 다시 실행할 필요는 없다. 설치된 KiCad 10.0.7의 Python 바인딩은 Python 3.14를 사용한다. 66키 원본은 `design/pcb/keycult66.*`, 63키 원본은 `design/pcb/63/keycult63.*`이며, 각 디렉터리에 BOM·핀맵·배선과 `reports/`, `exports/`를 둔다.

아래 명령은 저장된 배선을 재적용한 뒤 실제 ERC/DRC, netlist, 키 좌표와 예약 영역을 검사하고 SVG/PDF를 내보낸다. 생성기는 현재 CAD를 덮어쓰므로 수동 편집을 보존한 뒤 실행한다. `--keys`를 생략하면 66키를 선택한다.

```bash
uv run --python "$(command -v python3)" scripts/build_pcb.py --keys 66
uv run --python "$(command -v python3)" scripts/route_pcb.py --keys 66 --import-saved
uv run --python "$(command -v python3)" scripts/validate_pcb.py --keys 66
uv run --python "$(command -v python3)" scripts/build_pcb.py --keys 63
uv run --python "$(command -v python3)" scripts/route_pcb.py --keys 63 --import-saved
uv run --python "$(command -v python3)" scripts/validate_pcb.py --keys 63
```

회로나 배열을 변경하면 저장된 배선의 입력 해시가 일치하지 않으므로 `--import-saved` 대신 `--route`로 다시 배선한다.

검증은 기본적으로 미배선이나 DRC 위반이 있으면 실패한다. `--draft`는 미배선만 허용하고 실제 수를 보고하는 검토 모드이며, 기하 DRC 위반은 그대로 실패한다. 검사 상태는 [66키 보고서](../design/pcb/reports/validation.json)와 [63키 보고서](../design/pcb/63/reports/validation.json)를 기준으로 하며 제조 승인으로 해석하지 않는다. KiCad 없이 실행하는 검사 회귀 테스트는 `uv run scripts/test_pcb_validation_gate.py`다.
