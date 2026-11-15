import streamlit as st
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import math
import platform

# ------------------------------------------------------------
# Page setup
# ------------------------------------------------------------
st.set_page_config(
    page_title="니트로글리세린 작용 원리 탐구",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded",
)

# Matplotlib 한글 폰트 설정 (OS별 자동 지정)
if platform.system() == 'Darwin':  # Mac
    plt.rc('font', family='AppleGothic')
elif platform.system() == 'Windows':  # Windows
    plt.rc('font', family='Malgun Gothic')
else:  # Linux / Streamlit Cloud 등
    plt.rc('font', family='NanumGothic')

plt.rcParams['axes.unicode_minus'] = False  # 마이너스 부호 깨짐 방지

# Monochrome visual system: no emoji, icons, gradients, or decorative colors.
st.markdown(
    """
    <style>
    :root {
        --ink: #111111;
        --muted: #333333;
        --line: #B8B8B8;
        --panel: #F0F0F0;
        --paper: #FFFFFF;
    }
    html, body, [class*="css"] {
        color: #111111 !important;
        font-family: "Noto Sans KR", "Malgun Gothic", sans-serif;
        font-weight: 600;
    }
    .stApp {
        background: var(--paper);
    }
    section[data-testid="stSidebar"] {
        background: #F5F5F5;
        border-right: 1px solid var(--line);
    }
    h1, h2, h3, h4, p, li, label, .stMarkdown, .stText, [data-testid="stMetricValue"] {
        color: #111111 !important;
        font-weight: 650 !important;
        letter-spacing: -0.015em;
    }
    h1 { font-weight: 800 !important; }
    h2, h3 { font-weight: 750 !important; }
    .eyebrow, .panel-label { color: #333333 !important; font-weight: 750 !important; }
    .lead { color: #222222 !important; font-weight: 650 !important; }
    .eyebrow {
        color: var(--muted);
        font-size: 0.78rem;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        margin-bottom: 0.45rem;
    }
    .lead {
        color: #222222;
        font-weight: 650;
        font-size: 1.05rem;
        line-height: 1.8;
        max-width: 850px;
    }
    .panel {
        border: 1px solid var(--line);
        background: var(--panel);
        border-radius: 12px;
        padding: 1.1rem 1.2rem;
        min-height: 120px;
    }
    .panel-label {
        color: var(--muted);
        font-size: 0.82rem;
        margin-bottom: 0.45rem;
    }
    .panel-value {
        color: var(--ink);
        font-size: 1.12rem;
        font-weight: 650;
    }
    .note {
        border-left: 3px solid #777777;
        padding: 0.7rem 1rem;
        background: #F6F6F6;
        color: #222222;
        font-weight: 650;
        line-height: 1.7;
        margin: 0.8rem 0;
    }
    div[data-testid="stMetric"] {
        border: 1px solid var(--line);
        padding: 0.8rem;
        border-radius: 10px;
        background: #FAFAFA;
    }
    div.stButton > button {
        border: 1px solid #444444;
        border-radius: 7px;
        background: #242424;
        color: white;
        min-height: 2.7rem;
    }
    div.stButton > button:hover {
        border-color: #000000;
        background: #444444;
        color: white;
    }
    div[data-baseweb="tab-list"] {
        gap: 0.4rem;
    }
    div[data-baseweb="tab"] {
        color: #444444;
    }
    footer {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True,
)


# ------------------------------------------------------------
# Diagram helpers
# ------------------------------------------------------------
def draw_process_diagram(active_step: int):
    """Six-stage educational diagram of the established NO-sGC-cGMP-PKG pathway."""
    fig, ax = plt.subplots(figsize=(13, 3.6))
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")
    ax.set_xlim(0, 13)
    ax.set_ylim(0, 3.2)
    ax.axis("off")

    labels = [
        ("생체 활성화", "GTN의 활성화"),
        ("NO 관련 신호", "NO 또는 관련 활성종"),
        ("sGC 활성", "효소 활성 증가"),
        ("cGMP 증가", "세포 내 신호 물질"),
        ("PKG 활성", "단백질 인산화 조절"),
        ("평활근 이완", "혈관 확장으로 연결"),
    ]
    xs = [0.12, 2.28, 4.44, 6.60, 8.76, 10.92]
    width, height, y = 1.82, 1.18, 1.0

    for i, (title, subtitle) in enumerate(labels):
        edge = "#111111" if i == active_step else "#777777"
        face = "#DCDCDC" if i == active_step else "#F4F4F4"
        box = FancyBboxPatch(
            (xs[i], y), width, height,
            boxstyle="round,pad=0.06,rounding_size=0.07",
            linewidth=2.0 if i == active_step else 1.25,
            edgecolor=edge,
            facecolor=face,
        )
        ax.add_patch(box)
        ax.text(xs[i] + width / 2, y + 0.77, title,
                ha="center", va="center", fontsize=9.5,
                fontweight="bold", color="#111111")
        ax.text(xs[i] + width / 2, y + 0.38, subtitle,
                ha="center", va="center", fontsize=7.4,
                fontweight="bold", color="#333333")
        if i < len(labels) - 1:
            arrow = FancyArrowPatch(
                (xs[i] + width + 0.015, y + height / 2),
                (xs[i + 1] - 0.035, y + height / 2),
                arrowstyle="-|>", mutation_scale=11,
                linewidth=1.35, color="#333333",
            )
            ax.add_patch(arrow)

    ax.text(6.5, 2.72, "니트로글리세린의 의학적 작용 경로",
            ha="center", va="center", fontsize=12,
            fontweight="bold", color="#111111")
    plt.tight_layout(pad=0.5)
    return fig

def draw_vessel_diagram(dilated: bool):
    """Schematic cross-section: wider lumen after smooth-muscle relaxation."""
    fig, ax = plt.subplots(figsize=(5.5, 3.2))
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.axis("off")

    center_y = 3
    outer_h = 3.8
    inner_h = 2.1 if not dilated else 3.0

    outer = FancyBboxPatch(
        (0.7, center_y - outer_h / 2), 8.6, outer_h,
        boxstyle="round,pad=0.02,rounding_size=0.6",
        facecolor="#D0D0D0", edgecolor="#555555", linewidth=1.3,
    )
    lumen = FancyBboxPatch(
        (0.9, center_y - inner_h / 2), 8.2, inner_h,
        boxstyle="round,pad=0.02,rounding_size=0.5",
        facecolor="white", edgecolor="#777777", linewidth=1.0,
    )
    ax.add_patch(outer)
    ax.add_patch(lumen)
    ax.text(5, 5.35, "혈관 단면 모형", ha="center",
            fontsize=11, fontweight="bold", color="#202020")
    ax.text(5, 0.35, "혈관 벽", ha="center", fontsize=9, color="#555555")
    ax.text(5, center_y, "혈액이 흐르는 공간", ha="center",
            va="center", fontsize=9, color="#555555")
    plt.tight_layout(pad=0.2)
    return fig



def draw_release_concept(view_mode: str = "both"):
    """Qualitative concept graph: how fast energy is released. No real values."""
    t = [i * 10 / 399 for i in range(400)]
    slow = [0.35 * math.exp(-((x - 5.0) ** 2) / 6.0) for x in t]
    fast = [1.0 * math.exp(-((x - 2.0) ** 2) / 0.04) for x in t]

    fig, ax = plt.subplots(figsize=(6.2, 3.3))
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")
    if view_mode in ("both", "medical"):
        ax.plot(t, slow, color="#555555", linewidth=2.2, label="의학적 작용 (생체 신호, 조절됨)")
        ax.fill_between(t, slow, 0, color="#DDDDDD")
    if view_mode in ("both", "explosive"):
        ax.plot(t, fast, color="#111111", linewidth=2.2, linestyle="--", label="폭발물로서의 작용 (급격한 에너지 방출)")
    ax.set_ylim(0, 1.15)
    ax.set_xlim(0, 10)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xlabel("시간 (개념 표현, 실제 단위 없음)", fontsize=9)
    ax.set_ylabel("에너지 방출 속도 (상대 개념)", fontsize=9)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.legend(fontsize=8, frameon=False, loc="upper right")
    plt.tight_layout(pad=0.6)
    return fig


def step_dots(n: int, current: int, dark: str = "#111111", light: str = "#A0A0A0"):
    """Draw one dot per step on the slider bar (current step and earlier: dark)."""
    layers = []
    for i in range(n):
        pos = i / (n - 1) * 100 if n > 1 else 0
        color = dark if i <= current else light
        layers.append(
            f"radial-gradient(circle, {color} 0 3.5px, transparent 4.2px) "
            f"{pos:.2f}% 50% / 12px 12px no-repeat"
        )
    bg = ", ".join(layers)
    st.markdown(
        f"""
        <style>
        div[data-testid="stSlider"] div[data-baseweb="slider"] > div > div:first-child {{
            position: relative;
            overflow: visible !important;
        }}
        div[data-testid="stSlider"] div[data-baseweb="slider"] > div > div:first-child::after {{
            content: "";
            position: absolute;
            left: 0; right: 0; top: 50%;
            height: 12px;
            transform: translateY(-50%);
            background: {bg};
            pointer-events: none;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


# ------------------------------------------------------------
# Content
# ------------------------------------------------------------
medical_steps = [
    {
        "title": "1. 생체 활성화",
        "short": "체내에서 약물이 활성화되는 단계",
        "detail": "GTN이 효소 작용으로 생체 활성화됨. ALDH2가 기여하는 것으로 알려졌으나 하나의 효소만으로는 설명 불가.",
    },
    {
        "title": "2. NO 관련 신호",
        "short": "NO 또는 관련 활성종이 신호에 관여",
        "detail": "활성화 과정에서 NO 또는 관련 활성종 생성. 혈관 평활근 세포의 신호 전달에 관여. 실제 과정은 세포 환경에 따라 복합적.",
    },
    {
        "title": "3. sGC 활성",
        "short": "sGC 활성 증가",
        "detail": "NO가 가용성 구아닐산고리화효소(sGC)에 결합해 활성 증가. sGC가 GTP로부터 cGMP 생성을 촉진.",
    },
    {
        "title": "4. cGMP 증가",
        "short": "세포 내 2차 전달자 증가",
        "detail": "sGC 활성화로 세포 내 cGMP 농도 증가. cGMP는 다음 단계 신호를 잇는 2차 전달자.",
    },
    {
        "title": "5. PKG 활성 및 평활근 이완",
        "short": "수축 신호가 완화되는 단계",
        "detail": "cGMP가 PKG를 활성화. 칼슘 조절과 미오신 경사슬 인산화 조절에 영향. 평활근 수축 완화, 이완 촉진.",
    },
    {
        "title": "6. 혈관 확장",
        "short": "평활근 이완의 결과",
        "detail": "평활근 이완으로 혈관 내강 확대. 이 작용으로 협심증 증상 완화에 사용. 개인별 혈압·혈류량 예측은 불가.",
    },
]

st.sidebar.markdown('<div class="eyebrow">PROJECT NAVIGATION</div>', unsafe_allow_html=True)
st.sidebar.title("탐구 프로그램")
page = st.sidebar.radio(
    "화면 선택",
    ["프로젝트 소개", "혈관 확장제로서의 기능", "폭발물로서의 기능", "기능 비교"],
    label_visibility="collapsed",
)
st.sidebar.markdown("---")
st.sidebar.caption("탐구용 개념 시각화")


# ------------------------------------------------------------
# Page 1: Introduction
# ------------------------------------------------------------
if page == "프로젝트 소개":
    st.markdown('<div class="eyebrow">CHEMISTRY · BIOLOGY · PROGRAMMING</div>', unsafe_allow_html=True)
    st.title("니트로글리세린 작용 원리 탐구")
    st.markdown(
        '<p class="lead">하나의 물질이 의학과 산업에서 다르게 쓰이는 사례 탐구. '
        '혈관 확장 신호 전달 과정을 단계별 모형으로 이해.</p>',
        unsafe_allow_html=True,
    )
    st.markdown("---")

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(
            '<div class="panel"><div class="panel-label">탐구 주제</div>'
            '<div class="panel-value">물질의 이중적 활용</div></div>',
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            '<div class="panel"><div class="panel-label">핵심 학습 내용</div>'
            '<div class="panel-value">NO–cGMP 신호 전달</div></div>',
            unsafe_allow_html=True,
        )
    with c3:
        st.markdown(
            '<div class="panel"><div class="panel-label">개발 도구</div>'
            '<div class="panel-value">Python · Streamlit</div></div>',
            unsafe_allow_html=True,
        )

    st.subheader("프로그램의 목적")
    st.write(
        "니트로글리세린의 두 기능(혈관 확장제, 폭발물)을 도식과 텍스트로 비교하는 프로그램."
    )
    st.markdown(
        '<div class="note">범위: 의학적 작용과 일반 활용 분야 설명. 폭발물 기능은 역사·개념·안전 관리 수준만 다룸. '
        '제조, 취급, 반응 재현, 작동 조건, 수치는 제외.</div>',
        unsafe_allow_html=True,
    )

    st.subheader("화면 구성")
    st.write("왼쪽 메뉴에서 화면 이동.")
    st.markdown(
        """
        1. **프로젝트 소개** — 주제와 목적
        2. **혈관 확장제로서의 기능** — NO 신호에서 혈관 확장까지
        3. **폭발물로서의 기능** — 성질, 위험성, 보관, 규제
        4. **기능 비교** — 목적, 방출 방식, 통제 방식 비교
        """
    )


# ------------------------------------------------------------
# Page 2: Vasodilator function
# ------------------------------------------------------------
elif page == "혈관 확장제로서의 기능":
    st.markdown('<div class="eyebrow">FUNCTION 01 · VASODILATOR</div>', unsafe_allow_html=True)
    st.title("혈관 확장제로서의 기능")
    st.write(
        "슬라이더로 단계를 선택하면 도식, 설명, 혈관 모형이 함께 변경."
    )

    selected = st.select_slider(
        "작용 단계 선택",
        options=list(range(len(medical_steps))),
        value=0,
        format_func=lambda x: medical_steps[x]["title"],
    )
    step_dots(len(medical_steps), selected)

    st.pyplot(draw_process_diagram(selected), use_container_width=True)

    left, right = st.columns([1.15, 0.85], gap="large")
    with left:
        st.subheader(medical_steps[selected]["title"])
        st.write(medical_steps[selected]["detail"])
        st.markdown(
            f'<div class="note">단계 요약: {medical_steps[selected]["short"]}</div>',
            unsafe_allow_html=True,
        )
        st.progress((selected + 1) / len(medical_steps))
        st.caption(f"전체 6단계 중 {selected + 1}단계")
    with right:
        st.subheader("혈관 단면 개념 모형")
        is_dilated = selected == 5
        st.pyplot(draw_vessel_diagram(is_dilated), use_container_width=True)
        if is_dilated:
            st.caption("마지막 단계의 혈관 확장 개념 모형. 실제 측정값 아님.")
        else:
            st.caption("단순화한 혈관 모형. 실제 치수와 무관.")

    st.markdown("---")
    st.subheader("핵심 흐름")
    st.write("생체 활성화 → NO 관련 신호 → sGC 활성 → cGMP 증가 → PKG 활성 → 평활근 이완 → 혈관 확장")



# ------------------------------------------------------------
# Page 3: Explosive function (PubChem-based, non-operational)
# ------------------------------------------------------------
elif page == "폭발물로서의 기능":
    st.markdown('<div class="eyebrow">FUNCTION 02 · ENERGETIC MATERIAL</div>', unsafe_allow_html=True)
    st.title("폭발물로서의 기능")
    st.write("PubChem 실험적 성질 자료(CID 4510) 기반 정리. 폭발 반응의 조건·수치는 제외.")

    explosive_steps = [
        {
            "title": "1. 물리적 성질",
            "points": [
                "무색~담황색의 점성 액체, 기름 같은 질감",
                "낮은 온도에서 결정화, 녹는점 약 13.5 °C",
                "물보다 무거워 물에 가라앉음, 밀도 약 1.6",
                "물에 잘 녹지 않음, 에탄올 등 유기용매에는 비교적 잘 녹음",
                "증기압 매우 낮음, 증기는 공기보다 무거움",
            ],
            "table": {
                "항목": ["외관", "녹는점", "밀도(물=1)", "물에 대한 용해도", "증기 밀도(공기=1)"],
                "값": ["무색~담황색 점성 액체", "약 13.5 °C", "약 1.6", "낮음", "약 7.8"],
            },
        },
        {
            "title": "2. 위험성 분류",
            "points": [
                "충격·열에 민감한 물질로 분류",
                "마찰이나 충격으로도 위험",
                "장시간 화염·열에 노출되면 폭발 가능",
                "주된 위험은 파편보다 순간적인 폭풍",
                "MeSH 분류: 폭발성 물질(Explosive Agents), 열·압력·소음을 동반한 갑작스러운 팽창을 일으키는 에너지적 불안정 물질",
            ],
        },
        {
            "title": "3. 둔감화와 보관",
            "points": [
                "물·에탄올 용액 등 희석된 형태는 위험 완화",
                "용매가 증발하면 다시 민감해지므로 건조 주의",
                "의약품은 둔감화된 형태로 사용",
                "빛·열·습기·극한 온도 차단, 유리 용기 보관",
                "중성~약산성 용액에서 안정, 강산성·알칼리성에서는 분해 빨라짐",
            ],
        },
        {
            "title": "4. 산업 활용과 규제",
            "points": [
                "다이너마이트의 폭발성 성분 중 하나",
                "노벨이 안정화해 다이너마이트로 개발",
                "광업·터널·도로 등 토목 분야에서 역사적으로 활용",
                "오늘날 대부분 국가에서 법으로 엄격히 규제",
                "허가받은 전문 기관만 취급 가능, 일반인의 임의 취급은 불법이며 매우 위험",
            ],
        },
    ]

    sel = st.select_slider(
        "정리 항목 선택",
        options=list(range(len(explosive_steps))),
        value=0,
        format_func=lambda x: explosive_steps[x]["title"],
    )
    step_dots(len(explosive_steps), sel)
    step = explosive_steps[sel]

    left, right = st.columns([1.1, 0.9], gap="large")
    with left:
        st.subheader(step["title"])
        st.markdown("\n".join(f"- {p}" for p in step["points"]))
        if "table" in step:
            st.table(step["table"])
        st.progress((sel + 1) / len(explosive_steps))
        st.caption(f"전체 {len(explosive_steps)}항목 중 {sel + 1}번째")
    with right:
        st.subheader("에너지 방출 속도 개념 그래프")
        st.pyplot(draw_release_concept("explosive"), use_container_width=True)
        st.caption("개념 표현. 실제 반응 속도·에너지량·조건과 무관.")

    st.markdown(
        '<div class="note">제외 범위: 제조, 취급 방법, 폭발 발생 조건, 폭속·분해 온도 등 정량 수치. '
        '출처: PubChem, Nitroglycerin (CID 4510), Experimental Properties.</div>',
        unsafe_allow_html=True,
    )


# ------------------------------------------------------------
# Page 4: Function comparison
# ------------------------------------------------------------
elif page == "기능 비교":
    st.markdown('<div class="eyebrow">FUNCTION 03 · COMPARISON</div>', unsafe_allow_html=True)
    st.title("기능 비교")
    st.write(
        "같은 물질의 두 역할을 목적, 방출 방식, 통제 방식으로 비교."
    )

    st.subheader("에너지 방출 방식 비교 (개념 그래프)")
    view = st.radio(
        "표시할 기능 선택",
        ["둘 다 보기", "혈관 확장제로서의 기능", "폭발물로서의 기능"],
        horizontal=True,
    )
    mode = {"둘 다 보기": "both", "혈관 확장제로서의 기능": "medical", "폭발물로서의 기능": "explosive"}[view]
    st.pyplot(draw_release_concept(mode), use_container_width=True)
    st.caption("상대적 차이만 나타낸 개념도. 실제 값 아님.")

    st.markdown("---")
    st.subheader("관점별 비교")
    aspect = st.selectbox(
        "비교 관점 선택",
        ["활용 목적", "작용 방식", "통제 가능성", "결과", "사회적 관리"],
    )
    table = {
        "활용 목적": ("협심증 증상 완화", "굴착·토목 작업 (역사적 활용)"),
        "작용 방식": ("NO–sGC–cGMP–PKG 신호로 평활근 이완", "저장된 화학 에너지의 급격한 방출"),
        "통제 가능성": ("처방·용량 관리로 조절되는 소량 투여", "전문 관리 없이는 통제 불가, 매우 위험"),
        "결과": ("혈관 확장, 증상 완화", "급격한 에너지 방출, 물리적 변화"),
        "사회적 관리": ("의약품 허가·처방 체계", "화약류 법률, 허가·보관·운송 규제"),
    }
    med, exp = table[aspect]
    c1, c2 = st.columns(2, gap="large")
    with c1:
        st.markdown(
            f'<div class="panel"><div class="panel-label">혈관 확장제로서의 기능</div>'
            f'<div class="panel-value">{med}</div></div>',
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            f'<div class="panel"><div class="panel-label">폭발물로서의 기능</div>'
            f'<div class="panel-value">{exp}</div></div>',
            unsafe_allow_html=True,
        )

    st.markdown("---")
    st.subheader("전체 비교표")
    st.table({
        "비교 항목": list(table.keys()),
        "혈관 확장제": [v[0] for v in table.values()],
        "폭발물": [v[1] for v in table.values()],
    })

    st.markdown(
        '<div class="note">핵심: 에너지 방출 속도, 통제 방식, 사용 맥락에 따라 치료제 또는 엄격 관리 대상이 됨.</div>',
        unsafe_allow_html=True,
    )