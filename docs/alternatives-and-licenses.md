# 대안 비교와 라이선스·배포 범위

확인일: **2026-10-29**. 대상: **Keycult No.1/60 유지, G/H 사이 중앙 34mm Keyball, 직교 배열**의 예비 설계. 아래는 1차 자료에 근거한 기술·배포 검토이며 법률적 확정 판단은 아니다. 판매 페이지의 존재는 재고·배송 보장이 아니다.

## 1. 비교 결론

**Keyball을 예비 기준으로 유지한다.** 사용자가 지정한 34mm 볼과 기존 홀더·센서 조합을 그대로 검토할 수 있고, 공식 가이드가 수직 센서 PCB 설치를 설명한다. Charybdis는 같은 34mm를 쓰는 실질적인 대안이지만 장착부를 새로 맞춰야 한다. Ploopy의 공개 CAD는 재설계 참고 자료로 유용하나 아래 원형 제품들은 34mm 그대로의 대체품이 아니다.

**원형 Ploopy Nano와 Mini는 1.5인치(38.10mm)다.** Classic은 1.75인치(44.45mm)다. 공식 하드웨어 문서의 수치이며 Ploopy 전체를 하나의 볼 크기로 묶지 않는다. 이 비교는 링크한 원형 저장소 기준으로, Nano 2·Classic 2 등 후속 제품의 사양이나 라이선스를 대신하지 않는다. [PN-H][PM-H][PC-H]

| 대상 | 원래 볼·센서·지지 구조 | 확보·재사용 가능한 자료/부품 | 중앙 34mm 설계와의 관계 |
| --- | --- | --- | --- |
| **Keyball** | **34mm**, PMW3360와 렌즈, 세라믹 지지구 3개. 센서 PCB는 수직 설치. [K-B] | 공식 키트의 홀더 상·하부, 별도 판매되는 납땜·동작 확인 센서/렌즈 세트. Keyball46 센서 Gerber·회로도와 QMK 코드 공개. [K-S][K-A][K-G][K-F] | 현재 기준. 홀더·렌즈·센서의 상대 위치를 유지하는 별도 중앙 마운트가 필요하다. **센서 PCB 외곽을 홀더 전체 치수로 간주할 수 없다.** |
| **Ploopy Nano (원형)** | **38.10mm**, ADNS-5050, MR63ZZ 롤러 베어링 3개. 문서상 허용 볼 37.60–38.30mm. [PN-H][PN-E] | 전자 설계, STEP/STL, 조립 문서, QMK 기반 펌웨어. [PN] | 34mm는 명시된 호환 범위 밖이다. 홀더·지지점·광학 위치 재설계가 필요하며 전체 STL의 단순 축소로 해결되지 않는다. |
| **Ploopy Mini (원형)** | **38.10mm**, ADNS-5050, MR63ZZ 3개. 허용 볼 37.60–38.30mm. [PM-H][PM-E] | 전자 설계, STEP/STL, QMK 기반 펌웨어. [PM] | Nano와 마찬가지로 34mm 드롭인 대체품이 아니다. Nano와 하드웨어 라이선스도 다르다. |
| **Ploopy Classic (원형)** | **44.45mm**, PMW3360, MR63ZZ 3개. 허용 볼 44.0–44.6mm. [PC-H][PC-E] | 전자·기구 설계와 펌웨어 공개. [PC] | 원래 볼부터 목표보다 크다. 센서가 같아도 Keyball 홀더·커넥터·렌즈 위치와 호환된다는 뜻은 아니다. |
| **Charybdis** | **34mm**, PMW3360 PCB, MR63 베어링 3개. [C-S][C-B][C-P] | 상·하부 어댑터 STL/3MF, 센서 PCB 설계와 DIY/PCBA 구분, 키트·QMK 코드. 센서 README가 다른 프로젝트 사용 가능성을 명시한다. [C][C-P][C-F] | 34mm 유지가 가능한 유력 대안. 곡면 분리형 키보드용 장착 구조를 No.1/60 평면 중앙에 이식하는 별도 설계가 필요하다. 작거나 낮다고 단정할 근거는 확보하지 않았다. |

기구 재사용과 펌웨어 재사용은 별개다. 어떤 후보도 이 조사만으로 No.1/60 내부 개구부, 바닥 간섭, 볼 돌출량, 키캡 간섭까지 검증되지 않았다. 특히 Keyball46 공개 센서 자료와 Keyball44 Rev.1 조립 가이드를 **동일 리비전의 실측 조립체로 합성하지 않는다**. 공식 34mm 사출 홀더 단품의 치수·공차를 갖춘 CAD는 확인하지 못했다. 저장소의 Keyball39 키보드 케이스 STL을 해당 홀더 도면으로 오인하지 않는다. [K-G][K-B][K-T]

## 2. 하드웨어와 소프트웨어 라이선스를 분리한다

| 자료 범위 | 확인된 고지 | 재배포 시 주의 |
| --- | --- | --- |
| **Keyball 공개 저장소** | 최상위 `LICENSE`는 **GNU GPL v3**. 센서 Gerber·회로도는 이 저장소에 있으나 별도 하드웨어 전용 라이선스 설명은 확인하지 못했다. [K-L][K-G] | 공개 자료의 재사용을 무허가 자료와 동일시하지는 않되, 복제·수정 파일의 출처/고지와 해당 GPL 조건을 보존해야 한다. 저장소 고지를 **미공개 홀더 CAD·금형까지의 허가로 확장하지 않는다**. Gerber만으로 대응 소스 의무가 충족된다고 단정하지 않는다. |
| **Keyball 펌웨어의 `keyball.c`, `pmw3360.c`** | 두 파일 헤더는 **GPL-2.0-or-later**. 최상위 GPLv3 파일만 보고 모든 개별 파일을 `GPL-3.0-only`라고 표기하면 부정확하다. [K-F][K-D] | 파일별 저작권·라이선스 고지 유지. 배포하는 펌웨어의 구성 파일, 의존 코드, 센서 SROM의 출처·조건은 실제 배포 범위에서 별도 확인한다. 이 문서는 펌웨어 바이너리 재배포 허가 판정이 아니다. |
| **Ploopy Nano 전자·기구 설계** | **CERN-OHL-1.2**. [PN][PN-L] | 원본 고지·라이선스 보존, 수정 표시, 수정 설계 배포의 같은 라이선스 및 선호 편집 형식 제공, 제품 수령자에게 설계 접근 수단 제공 등 원문 §3–4 적용. 단순 출처 링크만으로 모든 의무가 끝나지 않는다. |
| **Ploopy Mini 전자·기구 설계** | **CERN-OHL-S-2.0**, 강한 상호주의. [PM][PM-L] | 수정 Covered Source와 제품 배포의 Complete Source 조건을 확인한다. Available Components 예외가 있지만 전체 결합 설계의 범위를 검토해야 한다. Nano와 같은 v1.2로 표기하지 않는다. |
| **Ploopy Classic 하드웨어** | **CERN-OHL-1.2**. [PC][PC-L] | Nano와 같은 버전의 조건이지만, 실제 가져오는 파일과 수정 이력을 각각 기록한다. |
| **위 Ploopy 3종 펌웨어** | 각 제품 README의 배포 고지는 **GPLv3**이며 Classic은 별도 `firmware/LICENSE`도 제공한다. [PN][PM][PC][PC-F] | 하드웨어 CERN 라이선스와 구분한다. 이 고지가 QMK 전체를 일률적으로 GPLv3라고 말하는 근거는 아니다. 소스·바이너리 배포 형태별 의무를 확인한다. |
| **Charybdis 기구 저장소 + PMW3360 센서 PCB 저장소** | 두 README 각각 **CC BY-NC-SA 4.0**. [C][C-P] | 비상업적 공유·수정은 명시적으로 허용된다. 출처·라이선스·수정 여부 표시, 비상업 조건, 파생물 ShareAlike를 지킨다. 상업 자유 이용 라이선스가 아니다. [CC] |
| **QMK의 Charybdis 펌웨어** | `charybdis.c`에 **GPL-2.0-or-later** SPDX 고지. [C-F] | 기구/PCB의 CC BY-NC-SA를 펌웨어에 적용하지 않는다. 관련 QMK·라이브러리의 개별 조건을 유지한다. |

다른 프로젝트의 설계 파일을 실제 가져올 때만 그 파일의 조건에 맞는 고지·라이선스·소스를 함께 준비한다. 단순 비교 문서나 독립 작성 코드를 모든 상류 라이선스의 파생물이라고 일괄 분류하지 않는다.

## 3. Keycult 공식 CAD: 개인 사용 허가와 공개 재배포는 다르다

[Keycult 공식 plate 다운로드 안내][KC]는 다음을 명시한다.

- **개인·비상업적 사용**만 허용한다. 예외는 Keycult의 명시적 서면 허가이며 **그룹바이도 상업적 이용**으로 본다.
- 개인 용도의 수정은 허용하지만, 상업 프로젝트의 기반으로 사용할 수 없다.
- 무보증이며 사용 책임은 이용자에게 있다.

원문의 핵심 표현은 “**These files may only be used for personal, non-commercial purposes**”와 “**You may modify these files as you wish for your personal use**”다. 반면 **공개 Git 저장소에서 원본 또는 수정 CAD를 재배포할 권한은 명시하지 않는다**. 이는 CC BY-NC-SA처럼 비상업적 공유를 명시한 라이선스와 다르다. 따라서 “비상업 공개 저장소이므로 재배포가 확실히 허용된다”거나 “무조건 위법이다” 어느 쪽으로도 단정하지 않는다.

### 이 프로젝트의 공개 배포 경계

1. **공식 ZIP/STEP/DXF는 공개 Git 이관 대상에서 제외**하고 원문 조건 페이지, 아래 다운로드 주소, SHA-256·확인일 및 재취득 절차를 남긴다. 사용자가 조건을 확인한 뒤 추적하지 않는 로컬 디렉터리에 내려받도록 한다. 비공개 보관 경험이 공개 재배포 허가를 대신하지 않는다.
2. **형식 변환은 재배포 문제를 자동 해소하지 않는다.** 원본 윤곽 좌표와 이를 그대로 그린 SVG/PNG/PDF/HTML도 공개 대상에서 제외한다. 공개 `build_artifacts.py`와 배치·인쇄 산출물은 **285.75×108.25mm 일반 직사각형 치수 경계 및 독립 키 배열**을 사용하며 공식 탭·코너 윤곽을 복제하지 않는다. 정확한 좌표는 Git에서 제외하는 `design/preliminary/sources/local/measured-official-dxf.json`에 둔다. 형상을 복제하지 않는 `design/preliminary/sources/measured-official-step.json`의 바운딩 치수 요약은 공개한다.
3. **공개 경계 검증과 공식 윤곽 검증을 분리한다.** 공개 검증은 일반 직사각형 내 포함·평면 간격만 확인한다. `design/preliminary/plate-containment.json`은 과거 공식 윤곽 검사의 수치 기록이며 현재 공개 도형의 검증 결과가 아니다. 공식 DXF를 로컬 취득한 뒤 `uv run scripts/verify_official_contour.py`로 별도 재현하고, 좌표·재검사 출력은 Git에서 제외하는 `design/preliminary/sources/local/`에 저장한다. 직사각형 경계 통과만으로 정확한 윤곽 포함을 주장하지 않는다.
4. 독립 작성 레이아웃·검증 코드·요약 측정값과 상류 형상 복제본을 구분한다. 개인 수정 plate를 공개 CAD로 배포하거나 상업화할 경우에는 **그 용도를 포괄하는 권리자의 허가가 확인되어야 한다**. 이 조사에서는 그러한 추가 허가를 확보하지 않았다.
5. Keyball Gerber 발췌나 조립 가이드 원문도 라이선스 없는 자체 작성물로 이관하지 않는다. 초기 공개본에는 핀 고정 링크·직접 작성 요약을 우선 사용하고, 실제 파일을 동봉하려면 해당 고지와 의무를 별도로 처리한다.

공식 파일 재취득 주소:

- No.1/60: <https://resources.keycult.com/plate_files/No160-Plate.zip>
- No.1/60 Rev.1: <https://resources.keycult.com/plate_files/No160-Rev1-Plates.zip>
- 다운로드 전 조건: <https://resources.keycult.com/downloads_plate_files.html>

**Keycult 원본 CAD·그 형상을 복제한 파생 파일의 공개 재배포 허가는 확인되지 않았다.** 현재 공개본은 해당 원본/윤곽 복제 파일을 제외하고 독립 레이아웃·요약 측정값·과거 검사 수치·재취득 링크를 제공한다. 이 분리가 향후 원본이나 수정 CAD까지 공개할 허가를 뜻하지는 않는다. 기구 제작의 미해결점은 별도로 홀더 실측, 실제 Keycult 장착 기준·내부 여유, 수직 스택 검증이다.

## 4. 1차 출처와 고정 리비전

GitHub 코드·라이선스는 아래 커밋에 고정했다. Wiki와 판매·조건 페이지는 확인일 당시 내용이며 고정된 제품 사양이나 영구 허가서가 아니다.

[KC]: https://resources.keycult.com/downloads_plate_files.html
[K-B]: https://github.com/Yowkees/keyball/blob/e1d1948e6e60a83f6b3566a209326508200d64ce/keyball44/doc/rev1/buildguide_en.md
[K-S]: https://shiroganelab.com/products/keyball39
[K-A]: https://shiroganelab.com/products/keyball-pre-soldered-trackball-sensor-lens-set
[K-G]: https://github.com/Yowkees/keyball/tree/e1d1948e6e60a83f6b3566a209326508200d64ce/keyball46/ball_design_data
[K-T]: https://github.com/Yowkees/keyball/tree/e1d1948e6e60a83f6b3566a209326508200d64ce/keyball39/3D_Printer_STL
[K-L]: https://github.com/Yowkees/keyball/blob/e1d1948e6e60a83f6b3566a209326508200d64ce/LICENSE
[K-F]: https://github.com/Yowkees/keyball/blob/e1d1948e6e60a83f6b3566a209326508200d64ce/qmk_firmware/keyboards/keyball/lib/keyball/keyball.c
[K-D]: https://github.com/Yowkees/keyball/blob/e1d1948e6e60a83f6b3566a209326508200d64ce/qmk_firmware/keyboards/keyball/drivers/pmw3360/pmw3360.c
[PN]: https://github.com/ploopyco/nano-trackball/blob/2b5a795a59545fb94b42f846f716fe082698ed1b/README.md
[PN-L]: https://github.com/ploopyco/nano-trackball/blob/2b5a795a59545fb94b42f846f716fe082698ed1b/LICENSE
[PN-H]: https://github.com/ploopyco/nano-trackball/wiki/Appendix-C:-Hardware
[PN-E]: https://github.com/ploopyco/nano-trackball/wiki/Appendix-A:-Printed-circuit-boards
[PM]: https://github.com/ploopyco/mini-trackball/blob/86e8417a0bfd385764769a689a5ef53eaf67997b/README.md
[PM-L]: https://github.com/ploopyco/mini-trackball/blob/86e8417a0bfd385764769a689a5ef53eaf67997b/LICENSE
[PM-H]: https://github.com/ploopyco/mini-trackball/wiki/Appendix-C:-Hardware
[PM-E]: https://github.com/ploopyco/mini-trackball/wiki/Appendix-A:-Printed-circuit-boards
[PC]: https://github.com/ploopyco/classic-trackball/blob/66134a982366751794067b96b1c69276c179b20f/README.md
[PC-L]: https://github.com/ploopyco/classic-trackball/blob/66134a982366751794067b96b1c69276c179b20f/hardware/LICENSE
[PC-F]: https://github.com/ploopyco/classic-trackball/blob/66134a982366751794067b96b1c69276c179b20f/firmware/LICENSE
[PC-H]: https://github.com/ploopyco/classic-trackball/wiki/Appendix-F:-Hardware
[PC-E]: https://github.com/ploopyco/classic-trackball/wiki/Appendix-A:-Printed-circuit-boards
[C]: https://github.com/Bastardkb/Charybdis/blob/47af70b9cd9b8d1d3a055ea88ab95c724bd3c02a/readme.md
[C-B]: https://github.com/Bastardkb/Charybdis/blob/47af70b9cd9b8d1d3a055ea88ab95c724bd3c02a/electronics_bom.md
[C-P]: https://github.com/Bastardkb/charybdis-pmw-3360-sensor-pcb/blob/98c16324fd8e41d10f2e2d6960f064130544eca1/README.md
[C-S]: https://bastardkb.com/product/charybdis-mini-kit/
[C-F]: https://github.com/qmk/qmk_firmware/blob/a3ecbc53f60e2e262a0df5e34a89ca6eeb17dd48/keyboards/bastardkb/charybdis/charybdis.c
[CC]: https://creativecommons.org/licenses/by-nc-sa/4.0/legalcode.en
