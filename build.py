"""NOVA 한 화면 샘플 생성. python3 build.py 로 index.html 을 다시 만든다. 구조는 sample-jennie, 메뉴는 soyeong-portfolio."""
import sys, os, time
STAMP = int(time.time())
import html as H
import json

# 마크는 브로슈어 원본을 그대로 잘라 낸 이미지 (images/nova-mark.png, 크림 글자 + 산호 별, 투명 배경). 글자로 다시 치지 않는다
MARK = '<img class="wordmark" src="images/nova-mark.png" alt="NOVA">'
NOVA_IG = "https://www.instagram.com/proj.nova_"
NOVA_YT = "https://www.youtube.com/@projectnova-o2b"
NOVA_EMAIL = "vjvorxmthdud@naver.com"   # 노바 이메일이 오면 여기에. 비어 있으면 메뉴 푸터, About, 섭외 공지에서 자동으로 빠진다
SY_IG = None   # 소영 인스타 주소가 나오면 넣고 프로필에 [ INSTAGRAM ] 을 추가한다
SY_YT = "https://www.youtube.com/@%EC%9D%B4%EC%86%8C%EC%98%81-k3q"
SY_VID = "https://youtu.be/wyKtAE_AEEo"

NAV = [("01", "About", "#aboutDialog"), ("02", "Artists", "#artistsDialog"), ("03", "History", "#showsDialog"), ("04", "Gallery", "#galleryDialog"), ("05", "Notice", "#noticeDialog"), ("06", "Contact", "#contactDialog")]
KO_ROLE = {"Daegeum": "대금", "Geomungo": "거문고", "Haegeum": "해금", "Percussion": "타악"}
members = [
    # (한글, 영문, 악기, slug, 사진, 초점, 소개 [(영문, 한글), ...])
    ("이소영", "Soyeong Lee", "Daegeum", "soyeong", "images/portrait-grey-2.jpg", "56% 23%", [
        ("Soyeong Lee is a daegeum player. On the breath of jeongak and sanjo she layers the sounds of today, exploring how the daegeum can change a stage and a room.", "이소영은 대금 연주자다. 정악과 산조의 호흡 위에 동시대의 소리를 얹어, 대금이 무대와 공간을 어떻게 바꾸는지 탐구한다."),
        ("She gave her first daegeum recital, [Time's Rift (闖塞)], and released a live recording of Moon Shadow on YouTube.", "제 1회 대금독주회 [시간의 틈새(闖塞)] 를 열었고, 실황 가운데 달 그림자를 유튜브에 공개했다."),
    ]),
    ("김채린", "Chaerin Kim", "Geomungo", "chaerin", None, None, []),
    ("황유경", "Yukyung Hwang", "Haegeum", "yukyung", None, None, []),
    ("전정현", "Jeonghyun Jeon", "Percussion", "jeonghyun", None, None, []),
    ("손한별", "Hanbyeol Son", "Daegeum", "hanbyeol", None, None, []),
]
# 멤버별 약력 : (분류, 연도, 한글). 분류는 edu 학력 / career 경력 / award 수상. 각 분류 안에서 최신이 위
CAREER = {"soyeong": [
    ("edu", "2021.02", "부산대학교 대학원 한국음악학과 석사과정 수료"),
    ("edu", "2019.03", "부산대학교 대학원 한국음악학과 석사과정 입학"),
    ("edu", "2019.02", "부산대학교 한국음악학과 졸업"),
    ("edu", "2015.03", "부산대학교 한국음악학과 입학"),
    # 아래 경력, 수상은 모양을 보려고 넣은 예시. 실제 내용이 오면 바꾼다
    ("career", "2026.03", "제 1회 대금독주회 [시간의 틈새(闖塞)]"),
    ("career", "2025.12", "[예시] 송년 국악 음악회 협연"),
    ("career", "2025.09", "[예시] 부산 국제 음악제 출연"),
    ("career", "2025.05", "뮤직 프로젝트 노바 창단 멤버"),
    ("career", "2024.11", "[예시] 국립부산국악원 기획공연 협연"),
    ("career", "2023.06", "[예시] 부산시립국악관현악단 객원 연주"),
    ("award", "2024.08", "[예시] 전국 국악 경연대회 대금 부문 금상"),
    ("award", "2023.10", "[예시] 부산 국악 대전 일반부 대상"),
    ("award", "2021.06", "[예시] 영남 국악 경연대회 관악 부문 은상"),
    ("award", "2019.11", "[예시] 전국 대학 국악 경연대회 장려상"),
]}
LINKS = {"soyeong": [("YouTube", SY_YT)]}   # 멤버별 링크. 인스타 주소가 나오면 ("Instagram", url) 추가
# Notice : (분류, 제목, 날짜, 본문 문단 목록). 분류는 지금 전부 nova. 임시 3건
notices = [
    ("nova", "뮤직 프로젝트 노바 홈페이지가 오픈되었습니다", "2026.11.03", [
        "뮤직 프로젝트 노바의 공식 홈페이지가 오픈되었습니다.",
        "ABOUT 에서 노바를 소개하고, ARTISTS 에서 다섯 연주자의 소개와 약력을, HISTORY 에서 그동안 함께한 무대를, GALLERY 에서 공연 사진을 보실 수 있습니다.",
        "공연 섭외와 협업, 촬영 문의는 CONTACT 의 양식이나 이메일, 인스타그램 메시지로 받고 있습니다.",
        "앞으로 공연 일정과 소식을 이곳 NOTICE 와 인스타그램에서 가장 먼저 알려 드리겠습니다. 많은 관심 부탁드립니다.",
    ]),
    ("nova", "2026 하반기 공연 일정 안내", "2026.09.01", [
        "2026년 하반기 노바의 공연 일정을 안내드립니다.",
        "09.09 AOCMP 2026 및 제72회 한국의학물리학회 추계학술대회 축하공연, 부산항전시컨벤션센터.",
        "이후 일정은 확정되는 대로 이곳과 인스타그램에 공지하겠습니다.",
    ]),
    ("pin", "공연 섭외와 협업 문의 안내", "2026.08.15", [
        "공연 섭외, 협업, 촬영 문의는 CONTACT 메뉴의 문의 양식으로 접수합니다. 인스타그램 메시지로도 받고 있습니다.",
        "유형을 고르고 행사명, 일시, 장소, 희망 구성(인원과 시간)을 적어 주시면 확인 후 이메일로 답변드립니다.",
    ]),
]
if os.environ.get("NOVA_DEMO_NOTICES"):
    _t = ["2026 하반기 정기연주회 예매 안내", "국립부산국악원 협연 공연 안내", "신입 단원 모집", "여름 워크숍 휴무 안내", "방송 출연 소식"]
    notices = notices + [("nova", f"[예시] {_t[i % 5]} {i + 1}", f"2026.{(i % 8) + 1:02d}.{(i * 3) % 28 + 1:02d}", ["예시 본문입니다."]) for i in range(17)]
# 공연별 사진 목록 : 첫 장이 대표 사진. History 카드와 Gallery 둘 다 여기서 가져간다. 실제 사진이 오면 파일명만 바꾼다
PHOTOS = {
    "AOCMP 2026 및 제72회 한국의학물리학회 추계학술대회": ["live-aocmp.jpg", "stage-blue.jpg"],
    "꿈꾸는 예술무대 <PAN : ON>": ["nova-panon-gyeongju.jpg", "ensemble-hanbok.jpg", "busking-pink.jpg"],
    "아시아물리올림피아드 개막식": ["live-apho.jpg"],
    "차도 마시Go, 국악도 듣Go, 춤도 추Go": ["live-gimhae.jpg", "stage-pink.jpg"],
    "NMJ 2025 행사 공연": ["live-nmj.jpg"],
    "대구 국가유산야행": ["nova-hero-daegu.jpg", "stage-spotlight.jpg", "ensemble-suit.jpg"],
}
# 아카이브 : 최신 연도가 위. (날짜, 제목, 장소, 주최나 성격). 연도가 늘면 여기에 항목만 추가한다
archive = {
    "2026": [
        ("09.09", "AOCMP 2026 및 제72회 한국의학물리학회 추계학술대회", "부산항전시컨벤션센터", "축하공연"),
        ("08.07", "꿈꾸는 예술무대 <PAN : ON>", "경주 교촌마을", "연주회"),
        ("06.13", "부산교직원불자연합회 대법회", "범어사 보제루", "퓨전 국악 축하공연"),
        ("05.18", "아시아물리올림피아드 개막식", "부경대학교 대학극장", ""),
        ("05.11", "찾아가는 음악회 <프로젝트 노바>", "서감초등학교", ""),
        ("01.14", "한물교 파크골프연습장 개관식", "한물교 파크골프연습장", "금정구"),
        ("01.07", "범어숲 개장식 축하 공연", "금정구", "오프닝 국악 공연"),
    ],
    "2025": [
        ("11.22", "차도 마시Go, 국악도 듣Go, 춤도 추Go", "김해한옥체험관", "김해시"),
        ("11.19", "NMJ 2025 행사 공연", "영주 선비세상", "영주시, 국제나노마이크로조이닝협회"),
        ("11.17", "부산의 보물섬 영도, 중앙동", "부산근현대역사관", "박성희 & 노바"),
        ("10.17", "개산대제 음악회", "범어사 야외무대", "박성희 & 노바"),
        ("10.16", "제29회 봉화송이축제 / 성이성 문화재 축제", "내성천 체육공원", "봉화군, 봉화축제관광재단"),
        ("08.30", "대구 국가유산야행", "경상감영공원", "대구 중구, 국가유산청"),
        ("04 - 12", "국립부산국악원 찾아가는 음악회", "초량, 부산진, 운산, 가야, 대연초등학교", ""),
    ],
}


def tiles():
    """3열. 번호, 사진(없으면 머리글자 + 악기), 호버 시 VIEW PROFILE. 5명 뒤 칸은 Coming soon."""
    out = ""
    for i, (ko, en, role, slug, img, pos, bio) in enumerate(members, 1):
        media = f'<img src="{img}" alt="" style="object-position: {pos}">' if img else f'<div class="ph" data-inst="{role.upper()} / {KO_ROLE[role]}"></div>'
        out += (f'      <a class="artist" href="#artists/{slug}" data-artist="{slug}" data-i="{(i - 1) % 3}"><div class="frame">{media}<span class="view">View profile <i>&rarr;</i></span></div>'
                f'<div class="meta"><div class="name">{ko}<small>{en}</small></div><div class="inst">{KO_ROLE[role]} / {role}</div></div></a>\n')
    out += '      <div class="artist soon" data-i="2"><div class="frame"><div>Coming <br>soon</div></div></div>\n'
    return out




notices = [n for n in notices if n[0] == "pin"] + [n for n in notices if n[0] != "pin"]   # 고정 공지가 맨 위
_plain = [i for i, n in enumerate(notices) if n[0] != "pin"]
nums = {i: len(_plain) - k for k, i in enumerate(_plain)}   # 고정 아닌 공지만 최신이 큰 번호


def shows_data():
    """패널용 평탄 목록. 최신 연도, 최신 날짜가 위."""
    out = []
    for y in sorted(archive, reverse=True):
        for d, t, p, h in archive[y]:
            out.append({"y": int(y), "d": d, "t": t, "v": p, "k": h, "img": PHOTOS.get(t)})
    return out


def history_dialog():
    """History 팝업 : 머리 사진 + 사진 카드(2개, 더 보기로 4개씩) + 전체 아카이브 표. history-sample.html 구조 그대로."""
    cards = ''
    for y in sorted(archive, reverse=True):
        for d, t, p, h in archive[y]:
            if t in PHOTOS:
                cards += f'      <a class="hcard" href="#" data-open="#galleryDialog"><div class="img"><img src="images/{PHOTOS[t][0]}" alt="" loading="lazy"></div><h4>{H.escape(t)}</h4><p class="d">{y}.{d}</p></a>\n'
    rows = ''
    for y in sorted(archive, reverse=True):
        rows += f'      <div class="yr"><h3>{y}</h3><div class="list">\n'
        for d, t, p, h in archive[y]:
            meta = ' / '.join(x for x in (p, h) if x)
            rows += f'        <div class="row"><span class="d">{d}</span><span class="t">{H.escape(t)}</span><span class="m">{H.escape(meta)}</span></div>\n'
        rows += '      </div></div>\n'
    return f'''<dialog id="showsDialog">
  <div class="dlg-bar light">
    <a class="dlg-home" href="#" data-close="#showsDialog" aria-label="Home"><img src="images/nova-mark.png" alt="NOVA"></a>
    <span class="dlg-menu" data-menu>[ Menu ]</span>
  </div>
  <button class="totop" type="button" aria-label="Top"><svg viewBox="0 0 24 24"><path d="M6 14l6-6 6 6"/></svg>TOP</button>
  <section class="hhero">
    <img src="images/sy-greenscreen.jpg" alt="">
    <div class="cap"><h2>전통의 깊이, 새로운 울림.</h2><p class="sub">우리의 음악에 오늘의 감각을 더하다.<br>익숙함과 새로움이 어우러지는 국악의 무대.</p></div>
  </section>
  <div class="wrapper">
    <p class="kicker">03 / History</p>
    <h2>노바가 함께한 무대</h2>
    <section class="archive">
{rows}    </section>
    <section class="hgal">
      <div class="hcards">
{cards}      </div>
      <div class="more-wrap" id="cards-more"><a class="more" href="#" data-open="#galleryDialog">더 보기</a></div>
    </section>
  </div>
</dialog>
'''


def gallery_items():
    """갤러리 항목 : 사진 있는 공연을 최신순으로 (History 와 같은 순서). 사진은 PHOTOS 의 목록, 첫 장이 대표."""
    out = []
    for y in sorted(archive, reverse=True):
        for d, t, p, h in archive[y]:
            if t in PHOTOS:
                out.append({"y": int(y), "d": d, "t": t, "v": p, "photos": PHOTOS[t]})
    return out


def gallery_dialog():
    """Gallery 팝업 : gallery-sample.html 그대로. 전체 / 연도 탭(프로필 탭과 같은 꼴) + 오른쪽 검색, oddatelier 식 2열 카드(제목 호버 산호색), 처음 4개 + 더 보기 4개씩. 누르면 oddatelier 뉴스 글 같은 흰 페이지."""
    items = gallery_items()
    years = sorted({g["y"] for g in items}, reverse=True)
    tabs = '<button type="button" data-y="all" class="current">전체</button>' + ''.join(f'<button type="button" data-y="{y}">{y}</button>' for y in years)
    cards = ''.join(f'      <a class="hcard" href="#" data-g="{i}"><div class="img"><img src="images/{g["photos"][0]}" alt="" loading="lazy">' + (f'<span class="cnt">{len(g["photos"])}장</span>' if len(g["photos"]) > 1 else '') + f'</div><h4>{H.escape(g["t"])}</h4><p class="d">{g["y"]}.{g["d"]}</p></a>\n' for i, g in enumerate(items))
    return dialog("galleryDialog", "04 / Gallery", "공간을 채우고, 사람을 잇는 음악", f'''    <div class="fbar"><div class="ptabs" id="gallery-tabs">{tabs}</div><div class="search"><input id="gallery-search" type="search" placeholder="Search" autocomplete="off"><span class="icon"></span></div></div>
    <div class="hcards" id="gallery-grid">
{cards}    </div>
    <p class="empty" id="gallery-empty" hidden>해당하는 공연이 없습니다.</p>
    <div class="more-wrap" id="gallery-more"><button class="more" type="button">더 보기</button></div>
''') + '''<dialog id="mailDialog" class="maildlg">
  <div class="mailbox">
    <span class="modal-close" id="mail-close" aria-label="Close"></span>
    <p class="mk">Contact</p>
    <div class="citem"><i class="far fa-envelope"></i><div><span class="k">Email</span><span class="v">''' + NOVA_EMAIL + '''</span></div><div class="acts"><button type="button" class="act" data-copy="''' + NOVA_EMAIL + '''">복사</button><a class="act" href="mailto:''' + NOVA_EMAIL + '''">열기</a></div></div>
    <div class="citem"><i class="fab fa-instagram"></i><div><span class="k">Instagram</span><span class="v">@proj.nova_</span></div><div class="acts"><button type="button" class="act" data-copy="''' + NOVA_IG + '''">복사</button><a class="act" href="''' + NOVA_IG + '''" target="_blank" rel="noreferrer">열기</a></div></div>
    <div class="citem"><i class="fab fa-youtube"></i><div><span class="k">YouTube</span><span class="v">Music Project NOVA</span></div><div class="acts"><button type="button" class="act" data-copy="''' + NOVA_YT + '''">복사</button><a class="act" href="''' + NOVA_YT + '''" target="_blank" rel="noreferrer">열기</a></div></div>
    <p class="copied" id="mail-copied" aria-live="polite"><svg viewBox="0 0 24 24" aria-hidden="true"><path class="ck" d="M5 12.5l4.5 4.5L19 7.5"/></svg>복사되었습니다</p>
  </div>
</dialog>
<dialog id="leaveDialog" class="maildlg">
  <div class="mailbox leavebox">
    <p class="lt">작성 중인 문의가 있습니다.</p>
    <p class="ld">이 페이지를 나가면 입력한 내용이 모두 사라집니다.</p>
    <div class="lbtns"><button type="button" class="more" id="leave-stay">계속 작성하기</button><button type="button" class="more ghost" id="leave-go">나가기</button></div>
  </div>
</dialog>
<dialog id="galleryView" class="post">
  <div class="dlg-bar"><a class="dlg-home" href="#" data-home aria-label="Home"><img src="images/nova-mark-dark.png" alt="NOVA"></a><span class="dlg-menu" data-menu>[ Menu ]</span></div>
  <button class="totop" type="button" aria-label="Top"><svg viewBox="0 0 24 24"><path d="M6 14l6-6 6 6"/></svg>TOP</button>
  <article class="pwrap">
    <p class="pk" id="gv-date"></p>
    <h2 id="gv-title"></h2>
    <div class="photos" id="gv-photos"></div>
    <div class="pbot">
      <a href="#" class="prev" id="gv-prev"><span class="dir">Prev</span></a>
      <a href="#" class="more list" id="gv-list">목록</a>
      <a href="#" class="next" id="gv-next"><span class="dir">Next</span></a>
    </div>
  </article>
</dialog>
'''


def dialog(id_, kicker, title, inner):
    return f'''<dialog id="{id_}">
  <div class="dlg-bar">
    <a class="dlg-home" href="#" data-close="#{id_}" aria-label="Home"><img src="images/{'nova-mark.png' if id_ == 'aboutDialog' else 'nova-mark-dark.png'}" alt="NOVA"></a>
    <span class="dlg-menu" data-menu>[ Menu ]</span>
  </div>
  <button class="totop" type="button" aria-label="Top"><svg viewBox="0 0 24 24"><path d="M6 14l6-6 6 6"/></svg>TOP</button>
  <div class="wrapper">
    <p class="kicker">{kicker}</p>
    <h2>{title}</h2>
{inner}  </div>
</dialog>
'''


page = f'''<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<title>NOVA, Music Project</title>
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="description" content="Music Project NOVA 뮤직 프로젝트 노바. 전통의 깊이, 새로운 울림.">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Josefin+Sans:wght@200;300;400;600;700&family=Gothic+A1:wght@200;300;400;500;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css">
<link rel="stylesheet" href="style.css?v={STAMP}">
</head>
<body>
<dialog id="menuDialog" class="menu-container">
  <div class="menu-blur"></div>
  <a class="menu-home" href="#" data-home aria-label="Home"><img src="images/nova-mark.png" alt="NOVA"></a>
  <nav class="menu-nav">
''' + ''.join((f'    <div class="menu-column"><a class="menu-link" href="{h}" target="_blank" rel="noreferrer"><span class="idx">{i}</span>{l}</a></div>\n' if h.startswith("http") else f'    <div class="menu-column"><a class="menu-link" href="#" data-open="{h}"><span class="idx">{i}</span>{l}</a></div>\n') for i, l, h in NAV) + f'''  </nav>
  <div class="menu-footer">
    <div class="col"><a href="{NOVA_IG}" target="_blank" rel="noreferrer">Instagram</a><a href="{NOVA_YT}" target="_blank" rel="noreferrer">YouTube</a></div>
    <div class="col"><span>&copy; <span id="year"></span> Music Project NOVA</span><a href="#" data-open="#privacyDialog">Privacy Policy</a></div>
  </div>
  <div id="menu-close" class="fixed-trigger" role="button" tabindex="0">[ Close ]</div>
</dialog>
<div id="menu-trigger" class="fixed-trigger" role="button" tabindex="0">[ <span class="menu-label">Menu</span><span class="close-label">Close</span> ]</div>

<div id="container">
  <section id="featured" class="page">
    <div class="background"><img src="images/nova-hero-daegu.jpg" alt=""></div>
    <div id="top-gradient" class="gradient"></div>
    <div id="bottom-gradient" class="gradient"></div>

    <div class="hero-mark"><img src="images/nova-mark.png" alt="NOVA"></div>
    <div id="social">
      <a href="{NOVA_IG}" target="_blank" rel="noreferrer" aria-label="Instagram"><i class="fab fa-instagram"></i></a>
      <a href="{NOVA_YT}" target="_blank" rel="noreferrer" aria-label="YouTube"><i class="fab fa-youtube"></i></a>
      {f'<a href="#" id="mail-open" aria-label="Email"><i class="far fa-envelope"></i></a>' if NOVA_EMAIL else ''}
    </div>
    <p class="copyright">&copy; Music Project NOVA. All rights reserved. <br class="m">All of NOVA's content is copyrighted.</p>
  </section>

</div>

''' + dialog("aboutDialog", "01 / About", "", f'''    <div class="about">
      <img class="about-mark" src="images/nova-mark.png" alt="NOVA">
      <p class="lead">Like NOVA, the moment a new light is born, we came together to breathe new life into Korean traditional music.<span class="ko">새로운 빛이 탄생하는 순간을 뜻하는 'NOVA' 처럼, 전통음악에 새로운 숨결을 더하고자 모였습니다.</span></p>
      <p>Music Project NOVA keeps traditional music such as jeongak and minsogak, which carry our culture and sentiment, at its center, and weaves in the senses of popular and contemporary music. Connecting the beauty of traditional music to the present, we deliver music that is comfortable yet special, with sounds anyone can relate to and enjoy.<span class="ko">뮤직 프로젝트 노바는 우리의 문화와 정서가 담긴 정악과 민속악 등 전통음악을 중심에 두고, 대중음악과 현대음악의 감각을 조화롭게 접목합니다. 전통음악의 아름다움을 현재와 연결하며, 익숙함과 새로움이 어우러지는 소리로 누구나 공감하고 즐길 수 있는 편안하면서도 특별한 음악을 전합니다.</span></p>
      <div class="actions"><a class="bracket" href="{NOVA_IG}" target="_blank" rel="noreferrer">Instagram</a><a class="bracket" href="{NOVA_YT}" target="_blank" rel="noreferrer">YouTube</a><a class="bracket" href="#" data-open="#artistsDialog">Artists</a></div>
    </div>
''') + dialog("artistsDialog", "02 / Artists", "새로운 빛으로 만나는 우리 음악", f'''    <p class="lead intro">Like NOVA, the moment a new light is born, we came together to breathe new life into Korean traditional music.<span class="ko">새로운 빛이 탄생하는 순간을 뜻하는 'NOVA' 처럼, 전통음악에 새로운 숨결을 더하고자 모였습니다.</span></p>
    <div class="rule"></div>
    <div class="grid" id="artist-grid">
{tiles()}    </div>
''') + dialog("artistDialog", "", "", f'''    <div class="head va" id="ar-head"><h2 class="bigname" id="ar-name"></h2><p class="inst" id="ar-inst"></p></div>
    <div class="cols">
      <div class="photo"><div class="frame" id="ar-photo"></div></div>
      <div class="text">
        <div class="ptabs" id="ar-tabs"><button type="button" data-tab="bio" class="current">About</button><button type="button" data-tab="career">Profile</button></div>
        <div class="pane" data-pane="bio"><div class="bio" id="ar-bio"></div><div class="icons" id="ar-links"></div></div>
        <div class="pane career" data-pane="career" id="ar-career" hidden></div>
      </div>
    </div>
    <div class="artist-nav"><a href="#" id="ar-prev"><span class="dir">Prev</span></a><a href="#" class="more list" data-open="#artistsDialog">목록</a><a href="#" id="ar-next"><span class="dir">Next</span></a></div>
''') + history_dialog() + gallery_dialog() + dialog("contactDialog", "06 / Contact", "문의", '''    <p class="intro">공연 섭외, 협업, 촬영 문의는 아래 양식이나 인스타그램 메시지로 남겨 주세요.</p>
  <div class="info"><h2>MUSIC PROJECT NOVA</h2><div class="v">대표 이소영<br>부산, 대한민국<small>Busan, Republic of Korea</small></div><div class="r"><a href="mailto:''' + NOVA_EMAIL + '''">''' + NOVA_EMAIL + '''</a></div></div>
  <div class="info"><h2>SNS</h2><div class="v"><a href="''' + NOVA_IG + '''" target="_blank" rel="noreferrer">Instagram @proj.nova_</a><br><a href="''' + NOVA_YT + '''" target="_blank" rel="noreferrer">YouTube Music Project NOVA</a></div><div class="r"></div></div>

  <section class="inq" id="inquiry">
    <h2>Inquiry</h2>
    <p class="lead">문의하신 내용 확인 후 담당자가 개별 연락 드리도록 하겠습니다. 일시와 장소가 미정인 경우 "미정" 으로 기재해 주세요.</p>
    <form id="bf" novalidate>
      <div class="f"><span>유형<b>*</b></span><select name="type" class="empty"><option value="">선택</option><option>공연 섭외</option><option>협업 제안</option><option>촬영, 인터뷰</option><option>기타 문의</option></select><p class="msg">유형을 선택해 주세요.</p></div>
      <div class="two">
        <div class="f" id="f-event"><span><em>행사명</em><b>*</b></span><input name="event" type="text" placeholder="행사명을 입력해 주세요."><p class="msg">행사명을 입력해 주세요.</p></div>
        <div class="f"><span>소속</span><input name="org" type="text" placeholder="단체명 또는 회사명"></div>
      </div>
      <div class="two">
        <div class="f"><span>이름<b>*</b></span><input name="name" type="text" placeholder="이름을 입력해 주세요."><p class="msg">이름을 입력해 주세요.</p></div>
        <div class="f"><span>연락처<b>*</b></span><input name="phone" type="tel" placeholder="연락처를 입력해 주세요."><p class="msg">연락처를 입력해 주세요.</p></div>
      </div>
      <div class="two">
        <div class="f"><span>이메일<b>*</b></span><input name="email" type="email" placeholder="이메일 주소를 입력해 주세요."><p class="msg">이메일 주소를 입력해 주세요.</p></div>
        <div class="f" id="f-date"><span><em>행사 일시</em></span><input name="date" type="text" placeholder="예: 2026.12.20 (토) 오후 7시. 미정 시 미정으로 기재"></div>
      </div>
      <div class="f" id="f-place"><span><em>행사 장소</em></span><input name="place" type="text" placeholder="예: 부산문화회관 중극장. 미정 시 미정으로 기재"></div>
      <div class="f" id="f-desc"><span><em>문의 내용</em><b>*</b></span><textarea name="desc" placeholder="행사 성격, 희망 구성(인원과 시간), 관객 규모, 음향 장비 유무, 예산 범위 등"></textarea><p class="msg">문의 내용을 입력해 주세요.</p></div>

      <div class="agree" id="ag1">
        <span>개인정보 수집, 이용 동의<b>*</b></span>
        <table><thead><tr><th>수집, 이용 항목</th><th>수집, 이용 목적</th><th>보유 기간</th></tr></thead><tbody><tr><td>이름, 연락처, 이메일</td><td>문의 답변, 섭외 협의</td><td>협의 종료 후 12개월</td></tr></tbody></table>
        <p class="note">개인정보 수집 및 이용에 대한 동의를 거부할 수 있으며, 동의를 거부할 경우 문의 접수가 제한됩니다.</p>
        <label class="chk"><input type="checkbox" name="agree1">동의합니다.</label>
      </div>
      <div class="agree" id="ag2">
        <span><em id="ag2-title">행사 정보</em> 수집, 이용 동의<b>*</b></span>
        <table><thead><tr><th>수집, 이용 항목</th><th>수집, 이용 목적</th><th>보유 기간</th></tr></thead><tbody><tr><td>소속, <span id="ag2-items">행사명, 행사 일시, 행사 장소</span>, 문의 내용</td><td><span id="ag2-purpose">공연 섭외 검토, 일정 조율</span></td><td>협의 종료 후 12개월</td></tr></tbody></table>
        <p class="note">수집 및 이용에 대한 동의를 거부할 수 있으며, 동의를 거부할 경우 문의 접수가 제한됩니다.</p>
        <label class="chk"><input type="checkbox" name="agree2">동의합니다.</label>
      </div>

      <div class="submit"><button class="cbtn" type="submit" id="submit" disabled>등록</button><p class="done" id="done">메일 앱이 열렸습니다. 보내기를 누르면 접수됩니다.</p></div>
    </form>
  </section>
''') + dialog("privacyDialog", "Privacy Policy", "개인정보 처리방침", '''    <div class="policy">
      <p class="pv">시행일 2026년 11월 3일</p>
      <p>뮤직 프로젝트 노바(이하 "노바")는 ｢개인정보 보호법｣ 을 지키며 이 홈페이지(이하 "사이트")를 운영합니다. 이 방침은 사이트 방문자의 개인정보가 어떻게 다뤄지는지를 알려 드리기 위한 것입니다.</p>
      <ol>
        <li>수집하는 개인정보, 처리 목적, 보유 기간<p>사이트는 회원 가입, 댓글 기능을 두지 않으며 방문자의 개인정보를 자동으로 수집하거나 저장하지 않습니다. 문의를 보내 주시는 경우에만 아래 정보를 받습니다.</p>
          <table class="ptab"><thead><tr><th>수집 시점</th><th>처리 목적</th><th>수집 항목</th><th>보유 기간</th></tr></thead><tbody>
            <tr><td>이메일, 인스타그램 메시지 문의</td><td>문의 답변, 섭외 협의</td><td>이름, 연락처(전화번호 또는 이메일), 소속, 문의 내용</td><td>협의 종료 후 1년</td></tr>
            <tr><td>섭외 문의 양식 (사이트)</td><td>공연 섭외 검토와 회신</td><td>행사명, 주최, 담당자 이름, 연락처, 이메일, 행사 일시와 장소, 희망 구성, 요청 사항</td><td>협의 종료 후 1년</td></tr>
            <tr><td>공연 계약 체결</td><td>계약 이행, 정산, 세무 신고</td><td>계약서에 적힌 담당자 정보, 정산 정보</td><td>관련 법령이 정한 기간 (국세기본법 5년)</td></tr>
          </tbody></table></li>
        <li>제3자 제공과 위탁<p>받은 정보를 다른 사람이나 단체에 제공하거나 처리를 맡기지 않습니다. 법령에 따라 제출 의무가 생기는 경우는 예외입니다.</p></li>
        <li>쿠키와 자동 수집<p>사이트는 쿠키, 방문 분석 도구, 광고 추적 도구를 쓰지 않습니다. 사이트를 띄우는 서버가 남기는 기록은 아래와 같습니다.</p>
          <table class="ptab"><thead><tr><th>항목</th><th>목적</th><th>보유 기간</th></tr></thead><tbody>
            <tr><td>IP 주소, 접속 시각, 요청한 페이지</td><td>서버 보안, 장애 확인</td><td>서버 사업자의 기본 보관 기간 (최대 3개월), 따로 분석하지 않음</td></tr>
          </tbody></table></li>
        <li>외부 링크<p>사이트의 인스타그램, 유튜브 링크는 각 서비스로 연결됩니다. 그곳에서의 개인정보 처리는 각 서비스의 방침을 따릅니다.</p></li>
        <li>정보주체의 권리<p>문의로 보내 주신 정보의 열람, 정정, 삭제를 언제든 요청하실 수 있습니다. 아래 연락처로 알려 주시면 지체 없이 처리합니다.</p></li>
        <li>사진, 영상, 음원<p>사이트의 사진, 영상, 음원과 글은 노바의 소유이며 허락 없이 복제하거나 배포할 수 없습니다. 사진 속 인물의 삭제 요청은 아래 연락처로 보내 주시면 바로 조치합니다.</p></li>
        <li>방침의 변경<p>내용이 바뀌면 이 페이지에 시행일과 함께 올립니다.</p></li>
        <li>문의<p>개인정보 관련 문의와 권리 행사는 아래로 연락해 주세요.</p>
          <table class="ptab"><thead><tr><th>구분</th><th>연락처</th></tr></thead><tbody>
            <tr><td>뮤직 프로젝트 노바 (개인정보 보호책임자: 대표 이소영)</td><td>''' + NOVA_EMAIL + '''</td></tr>
            <tr><td>개인정보침해신고센터</td><td>privacy.kisa.or.kr / 국번 없이 118</td></tr>
            <tr><td>개인정보분쟁조정위원회</td><td>www.kopico.go.kr / 1833-6972</td></tr>
          </tbody></table></li>
      </ol>
    </div>
''') + dialog("noticeDialog", "05 / Notice", "공지", f'''    <div class="nbar"><div class="search"><input id="notice-search" type="search" placeholder="Search" autocomplete="off"><span class="icon"></span></div><p class="vis"><span class="dot"></span>Now <b id="vis-now">-</b> Total <b id="vis-total">-</b></p></div>
    <table class="list" id="notice-table">
      <thead><tr><th>No.</th><th>Title</th><th>Writer</th><th>Date</th></tr></thead>
      <tbody>
''' + ''.join(f'        <tr data-topic="{c}" data-id="{i}"{" class=\"pinned\"" if c == "pin" else ""}><td class="no">{"<svg class=\"pinicon\" viewBox=\"0 0 24 24\" aria-label=\"고정\"><path d=\"M14 3l7 7-3 1-3.5 3.5L15 20l-4-4-6 6 6-6-4-4 5.5.5L16 9l1-3z\"/></svg>" if c == "pin" else f"{nums[i]:02d}"}</td><td class="title"><a href="#" data-notice="{i}">{H.escape(t)}</a></td><td class="writer">NOVA</td><td class="date">{d}</td></tr>\n' for i, (c, t, d, body) in enumerate(notices)) + '''      </tbody>
    </table>
    <p class="empty" id="notice-empty" hidden>No notices found.<span class="ko">해당하는 공지가 없습니다.</span></p>
    <div class="more-wrap" id="notice-more" hidden><button class="more" type="button">더 보기</button></div>
''') + '''<dialog id="noticeDetail" class="detail">
  <div class="modal-content">
    <span class="modal-close" data-close="#noticeDetail" aria-label="Close"></span>
    <div class="modal-header">
      <h2 class="modal-kicker">Notice</h2>
      <div id="nd-title" class="modal-title"></div>
      <div class="modal-info"><span id="nd-topic">NOVA</span><span id="nd-date"></span></div>
    </div>
    <div id="nd-body" class="modal-body"></div>
    <div class="modal-nav"><a class="bracket" href="#" id="nd-prev">Prev</a><a class="bracket" href="#" id="nd-next">Next</a></div>
  </div>
</dialog>
<script>window.NOVA_EMAIL = ''' + json.dumps(NOVA_EMAIL) + ''';</script>
<script>window.GALLERY = ''' + json.dumps(gallery_items(), ensure_ascii=False) + ''';</script>
<script>window.ARTISTS = ''' + json.dumps([{"slug": s, "ko": ko, "en": en, "role": role, "roleKo": KO_ROLE[role], "img": img, "pos": pos, "bio": bio, "links": LINKS.get(s, []), "career": CAREER.get(s, [])} for ko, en, role, s, img, pos, bio in members], ensure_ascii=False) + ''';</script>
<script>window.NOTICES = ''' + json.dumps([{"topic": c, "title": t, "date": d, "body": body} for c, t, d, body in notices], ensure_ascii=False) + ''';</script>
<script src="main.js?v=''' + str(STAMP) + '''"></script>
</body>
</html>
'''
OUT = sys.argv[1] if len(sys.argv) > 1 else "index.html"
open(OUT, "w").write(page)
print(OUT, "written")
