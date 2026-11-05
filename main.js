// 한 화면 + 팝업 (jennie 구조). 메뉴는 maxrichter 식 오버레이.
// 팝업은 전부 주소(#about, #artists/soyeong, #history/2026, #notice/2)로 다룬다.
// 그래서 브라우저 뒤로가기가 한 단계씩 돌아오고, 새로고침해도 보던 팝업이 그대로 열린다.
const body = document.body;
const $ = (s) => document.querySelector(s);
window.addEventListener("load", () => body.classList.add("loaded"));

// ---- 라우트 ↔ 팝업 ----
const ROUTE = { about: "#aboutDialog", artists: "#artistsDialog", history: "#showsDialog", gallery: "#galleryDialog", notice: "#noticeDialog", contact: "#contactDialog", privacy: "#privacyDialog" };
const DIALOG = Object.fromEntries(Object.entries(ROUTE).map(([k, v]) => [v, k]));
let openGalleryView = () => {};   // 아래 Gallery 블록에서 채운다. 첫 render 보다 먼저 선언
function parse(hash) {
  const h = (hash || "").replace(/^#/, "");
  const [top, sub] = h.split("/");
  return ROUTE[top] ? { top, sub: sub || null } : { top: null, sub: null };
}
// Contact 양식에 적은 게 있으면 다른 곳으로 가기 전에 묻는다. 확인하면 pending 을 실행
let contactDirty = () => false, askLeave = (go) => go();
function navigate(route, replace) {
  if (parse(location.hash).top === "contact" && parse(route).top !== "contact" && contactDirty()) { askLeave(() => navigate(route, replace)); return; }
  const url = route ? "#" + route : location.pathname + location.search;
  const next = parse(route), cur = parse(location.hash);
  // 하위 팝업(공지 상세, 프로필, 전체 목록)을 다른 곳에서 바로 열면 상위 주소를 먼저 쌓아 뒤로가기가 상위로 가게 한다
  if (!replace && next.sub && cur.top !== next.top) history.pushState({ nova: true }, "", "#" + next.top);
  if (replace) history.replaceState({ nova: true }, "", url); else history.pushState({ nova: true }, "", url);
  lastHash = location.hash; render(route);
}
// 닫기 : 우리가 쌓은 기록이면 한 단계 뒤로, 새로고침으로 바로 들어온 경우면 상위 주소로 바꿔 끼운다
function closeTo(parent) {
  if (history.state && history.state.nova && parse(location.hash).top) history.back();
  else navigate(parent, true);
}
let lastHash = location.hash, leaving = false;
window.addEventListener("popstate", () => {
  const was = parse(lastHash).top, now = parse(location.hash).top;
  if (!leaving && was === "contact" && now !== "contact" && contactDirty()) {
    // 뒤로가기로 나가려 함 : 일단 되돌려 놓고 묻는다
    const target = location.hash; history.pushState({ nova: true }, "", lastHash);
    askLeave(() => { leaving = true; history.back(); setTimeout(() => { leaving = false; }, 50); });
    return;
  }
  lastHash = location.hash; render(location.hash.replace(/^#/, ""));
});
const _origNavigate = navigate;

// ---- 메뉴 : dialog 로 열어 어떤 팝업 위에서도 뜬다 (주소에는 안 남긴다) ----
let timer = null;
const menu = $("#menuDialog");
function openMenu() {
  if (menu.open) return;
  menu.showModal(); requestAnimationFrame(() => menu.classList.add("show"));
  const cols = Array.from(menu.querySelectorAll(".menu-column")); let i = 0;
  if (timer) clearInterval(timer);
  timer = setInterval(() => { if (i < cols.length) cols[i++].classList.add("show"); else { clearInterval(timer); timer = null; } }, 65);
}
function closeMenu() {
  if (!menu.open) return;
  menu.classList.remove("show"); if (timer) clearInterval(timer);
  menu.querySelectorAll(".menu-column").forEach((c) => c.classList.remove("show"));
  setTimeout(() => { if (!menu.classList.contains("show")) menu.close(); }, 350);
}
$("#menu-trigger").addEventListener("click", openMenu);
$("#menu-close").addEventListener("click", closeMenu);
menu.addEventListener("cancel", (e) => { e.preventDefault(); closeMenu(); });
document.querySelectorAll("[data-menu]").forEach((el) => el.addEventListener("click", openMenu));
document.querySelectorAll("[data-home]").forEach((el) => el.addEventListener("click", (e) => { e.preventDefault(); navigate(""); }));

// ---- 팝업 열고 닫기 (애니메이션 포함) ----
function openPlain(sel) { const d = $(sel); if (!d.open) { d.showModal(); d.scrollTop = 0; } if (document.activeElement && document.activeElement.closest(".dlg-bar")) document.activeElement.blur(); }
function closePlain(sel) { const d = $(sel); if (d.open) d.close(); }
function openDetail(i) {
  const n = window.NOTICES[i]; if (!n) return;
  $("#nd-title").textContent = n.title; $("#nd-date").textContent = n.date;
  // oddatelier 식 : 한글 본문 전체, 가는 선, 영어 본문 전체
  $("#nd-body").innerHTML = n.body.map((p) => "<p>" + p + "</p>").join("") + (n.en && n.en.length ? '<div class="nd-en">' + n.en.map((p) => "<p>" + p + "</p>").join("") + "</div>" : "");
  $("#nd-prev").hidden = i === 0; $("#nd-next").hidden = i === window.NOTICES.length - 1;
  const d = $("#noticeDetail"); if (!d.open) { d.showModal(); setTimeout(() => d.classList.add("show"), 10); } d.scrollTop = 0;
  if (document.activeElement && d.contains(document.activeElement)) document.activeElement.blur();   // 열릴 때 [ Next ] 에 파란 포커스 테두리가 잡히지 않게
}
function closeDetail() { const d = $("#noticeDetail"); if (!d.open) return; d.classList.remove("show"); setTimeout(() => { if (!d.classList.contains("show")) d.close(); }, 150); }

// ---- 멤버 프로필 : 데이터로 채우고 Previous, Next 로 넘긴다 ----
const ICONS = {
  Instagram: '<svg viewBox="0 0 24 24"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r=".8" fill="currentColor"/></svg>',
  YouTube: '<svg viewBox="0 0 24 24"><path d="M22 8.2a3 3 0 0 0-2.1-2.1C18 5.6 12 5.6 12 5.6s-6 0-7.9.5A3 3 0 0 0 2 8.2 31 31 0 0 0 1.6 12 31 31 0 0 0 2 15.8a3 3 0 0 0 2.1 2.1c1.9.5 7.9.5 7.9.5s6 0 7.9-.5a3 3 0 0 0 2.1-2.1 31 31 0 0 0 .4-3.8 31 31 0 0 0-.4-3.8z"/><path d="M10 9.5v5l4.5-2.5z" fill="currentColor" stroke="none"/></svg>',
};
const media = (a) => a.img ? `<img src="${a.img}" alt="" style="object-position: ${a.pos}">` : `<div class="ph" data-inst="${a.role.toUpperCase()} / ${a.roleKo}"></div>`;
function openArtist(slug) {
  const list = window.ARTISTS || []; const i = list.findIndex((a) => a.slug === slug); if (i < 0) return;
  const a = list[i];
  const apply = () => {
    $("#artistDialog .kicker").innerHTML = `<a href="#artists">02 / Artists</a> / ${a.en}`;
    $("#artistDialog .kicker a").addEventListener("click", (e) => { e.preventDefault(); navigate("artists"); });
    $("#ar-name").innerHTML = a.en.toUpperCase().split(" ").map((w, k) => `<span style="animation-delay: ${k * .1}s">${w}</span>`).join(" ");
    $("#ar-inst").textContent = a.role;
    $("#ar-photo").innerHTML = media(a);
    const bio = a.bio.length ? a.bio : [["Profile coming soon.", "소개가 준비되는 대로 올리겠습니다."]];
    $("#ar-bio").innerHTML = bio.map(([en, ko]) => `<p class="ko">${ko}</p><p class="en">${en}</p>`).join("");   // 한글 먼저, 영어는 아래 작게
    const career = a.career || [];
    $("#ar-tabs").hidden = !career.length;
    renderCareer(career);
    showPane("bio");
    $("#ar-links").innerHTML = `<span aria-label="Instagram">${ICONS.Instagram}</span>` + a.links.map(([n, u]) => `<a href="${u}" target="_blank" rel="noreferrer" aria-label="${n}">${ICONS[n] || ""}</a>`).join("");
    const prev = list[i - 1], next = list[i + 1];
    $("#ar-prev").hidden = !prev; $("#ar-next").hidden = !next;
    openPlain("#artistDialog");
  };
  const from = document.querySelector(`.artist[data-artist="${slug}"] .frame`);
  if (from && document.startViewTransition && !$("#artistDialog").open) { from.style.viewTransitionName = "hero"; document.startViewTransition(() => { from.style.viewTransitionName = ""; apply(); $("#ar-photo").style.viewTransitionName = "hero"; }).finished.then(() => { $("#ar-photo").style.viewTransitionName = ""; }); }
  else apply();
}
const CATS = [["edu", "Education", "학력"], ["career", "Career", "경력"], ["award", "Awards", "수상"]];
const PER = 4;   // 묶음마다 한 번에 보이는 줄 수. 넘으면 그 묶음에만 Previous / Next
function renderCareer(career) {
  const groups = CATS.map(([k, en, ko]) => ({ en, ko, rows: career.filter((c) => c[0] === k), page: 0 })).filter((g) => g.rows.length);
  const box = $("#ar-career");
  box.innerHTML = groups.map((g, gi) => `<div class="blk" data-g="${gi}"><div class="bhead"><h3>${g.en}<span>${g.ko}</span></h3><div class="cnav"></div></div><div class="rows"></div></div>`).join("");
  groups.forEach((g, gi) => {
    const blk = box.querySelector(`.blk[data-g="${gi}"]`), rowsEl = blk.querySelector(".rows"), navEl = blk.querySelector(".cnav");
    const pages = Math.ceil(g.rows.length / PER);
    const draw = () => {
      rowsEl.innerHTML = g.rows.slice(g.page * PER, g.page * PER + PER).map(([, y, ko]) => `<div class="crow"><span class="y">${y}</span><p class="ko">${ko}</p></div>`).join("");
      navEl.innerHTML = pages > 1 ? `<a href="#" class="cprev" aria-label="Prev" ${g.page === 0 ? "disabled" : ""}><svg viewBox="0 0 24 24"><path d="M15 5l-7 7 7 7"/></svg></a><span class="cpage">${g.page + 1} / ${pages}</span><a href="#" class="cnext" aria-label="Next" ${g.page === pages - 1 ? "disabled" : ""}><svg viewBox="0 0 24 24"><path d="M9 5l7 7-7 7"/></svg></a>` : "";
      const prev = navEl.querySelector(".cprev"), next = navEl.querySelector(".cnext");
      if (prev) prev.addEventListener("click", (e) => { e.preventDefault(); if (g.page > 0) { g.page--; draw(); } });
      if (next) next.addEventListener("click", (e) => { e.preventDefault(); if (g.page < pages - 1) { g.page++; draw(); } });
    };
    draw();
  });
}
function showPane(name) {
  const dlg = $("#artistDialog"), keep = dlg.scrollTop;   // 탭을 바꿔도 보던 자리 그대로
  document.querySelectorAll("#ar-tabs button").forEach((t) => t.classList.toggle("current", t.dataset.tab === name));
  document.querySelectorAll("#artistDialog .pane").forEach((p) => { p.hidden = p.dataset.pane !== name; });
  dlg.scrollTop = keep;
}
(function () {
  document.querySelectorAll("#ar-tabs button").forEach((t) => t.addEventListener("click", () => showPane(t.dataset.tab)));
  const cur = () => (window.ARTISTS || []).findIndex((a) => a.slug === parse(location.hash).sub);
  const go = (d) => { const list = window.ARTISTS; const i = cur() + d; if (i >= 0 && i < list.length) navigate("artists/" + list[i].slug, true); };
  $("#ar-prev").addEventListener("click", (e) => { e.preventDefault(); go(-1); });
  $("#ar-next").addEventListener("click", (e) => { e.preventDefault(); go(1); });
  document.addEventListener("keydown", (e) => { if (!$("#artistDialog").open) return; if (e.key === "ArrowRight") go(1); if (e.key === "ArrowLeft") go(-1); });
})();
// 목록 카드 : 화면에 들어올 때 열별로 조금씩 늦게 떠오른다
(function () {
  const grid = $("#artist-grid"); if (!grid) return;
  const io = new IntersectionObserver((es) => es.forEach((e) => { if (e.isIntersecting) { setTimeout(() => e.target.classList.add("in"), (+e.target.dataset.i || 0) * 90); io.unobserve(e.target); } }), { threshold: .15, root: $("#artistsDialog") });
  [...grid.children].forEach((c) => io.observe(c));
})();
document.querySelectorAll("[data-artist]").forEach((el) => el.addEventListener("click", (e) => { e.preventDefault(); navigate("artists/" + el.dataset.artist); }));

// ---- 상태를 주소에 맞춘다 ----
function render(route) {
  closeMenu();
  const { top, sub } = parse(route);
  const want = new Set();
  if (top) want.add(ROUTE[top]);
  if (top === "artists" && sub) want.add("#artistDialog");
  if (!(top === "notice" && sub)) closeDetail();
  if (!(top === "gallery" && sub)) { const v = $("#galleryView"); if (v.open) { v.classList.remove("show"); v.close(); } }
  ["#artistDialog", "#aboutDialog", "#artistsDialog", "#showsDialog", "#galleryDialog", "#noticeDialog", "#contactDialog", "#privacyDialog"].forEach((id) => { if (!want.has(id)) closePlain(id); });
  if (top) openPlain(ROUTE[top]);
  if (top === "artists" && sub) openArtist(sub);
  if (top === "gallery" && sub) openGalleryView(+sub);
  if (top === "notice" && sub) openDetail(+sub);
}

document.querySelectorAll("[data-open]").forEach((el) => el.addEventListener("click", (e) => { e.preventDefault(); navigate(DIALOG[el.dataset.open] || ""); }));
const parentOfCurrent = () => { const { top, sub } = parse(location.hash); return sub ? top : ""; };
// Esc : 한 단계 위로. 바깥 클릭으로는 닫지 않는다 (팝업이 화면 전체라 여백 클릭이나 드래그 끝이 닫기로 잡히던 문제)
document.querySelectorAll("dialog:not(#menuDialog)").forEach((d) => {
  d.addEventListener("cancel", (e) => { e.preventDefault(); closeTo(parentOfCurrent()); });
});
// 공지 상세만 OA 처럼 회색 덮개를 누르면 닫힌다. 드래그가 아니라 진짜 클릭일 때만
(function () {
  const d = $("#noticeDetail"); let downOnBackdrop = false;
  d.addEventListener("mousedown", (e) => { downOnBackdrop = e.target === d; });
  d.addEventListener("click", (e) => { if (e.target === d && downOnBackdrop && !getSelection().toString()) closeTo(parentOfCurrent()); downOnBackdrop = false; });
})();
// 좌상단 마크 : 홈. 공지 상세의 X : 한 단계 위
document.querySelectorAll("[data-close]").forEach((el) => el.addEventListener("click", (e) => { e.preventDefault(); if (el.classList.contains("dlg-home")) navigate(""); else closeTo(parentOfCurrent()); }));

// ---- History : 사진 카드 2개 + 더 보기(4개씩, 다음 두 장은 흐리게 살짝). 머리 사진을 지나면 상단 바를 검정으로 ----
(function () {
  const dlg = $("#showsDialog"); if (!dlg) return;
  const cards = [...dlg.querySelectorAll(".hcard")];
  cards.forEach((c, i) => { c.classList.toggle("hid", i >= 4); c.classList.toggle("peek", i >= 2 && i < 4); });
  cards.forEach((c) => c.addEventListener("click", (e) => e.preventDefault()));
  const bar = dlg.querySelector(".dlg-bar"), mark = bar.querySelector("img");
  new IntersectionObserver(([en]) => { const light = en.isIntersecting && en.intersectionRatio > .08; bar.classList.toggle("light", light); mark.src = light ? "images/nova-mark.png" : "images/nova-mark-dark.png"; }, { root: dlg, threshold: [0, .08, .2] }).observe(dlg.querySelector(".hhero"));
})();

// ---- Notice : 검색, 상세 ----
(function () {
  const table = $("#notice-table"); if (!table || !window.NOTICES) return;
  const rows = Array.from(table.querySelectorAll("tbody tr"));
  const input = $("#notice-search"); const empty = $("#notice-empty");
  // 처음 10줄, 더 보기마다 10줄. 검색하면 처음부터 다시
  const PAGE = 10, more = $("#notice-more"); let shown = PAGE;
  function apply() {
    const q = input.value.trim().toLowerCase(); let n = 0;
    // 고정 공지는 검색만 타고 쪽수에는 안 센다
    let total = 0;
    rows.forEach((r) => { const ok = !q || r.querySelector(".title").textContent.toLowerCase().includes(q); const pin = r.classList.contains("pinned"); if (ok) { total++; if (!pin) n++; } r.hidden = !ok || (!pin && n > shown); });
    empty.hidden = total > 0; more.hidden = n <= shown;
  }
  input.addEventListener("input", () => { shown = PAGE; apply(); });
  more.querySelector(".more").addEventListener("click", () => { shown += PAGE; apply(); });
  apply();
  table.querySelectorAll("a[data-notice]").forEach((a) => a.addEventListener("click", (e) => { e.preventDefault(); navigate("notice/" + a.dataset.notice); }));
  const cur = () => +(parse(location.hash).sub || 0);
  $("#nd-prev").addEventListener("click", (e) => { e.preventDefault(); if (cur() > 0) navigate("notice/" + (cur() - 1), true); });
  $("#nd-next").addEventListener("click", (e) => { e.preventDefault(); if (cur() < window.NOTICES.length - 1) navigate("notice/" + (cur() + 1), true); });
})();

// 첫 진입 : 주소에 맞춰 연다 (새로고침, 공유 링크)
// ---- Gallery : 전체 / 연도 탭 + 검색, 처음 4개 + 더 보기 4개씩(다음 두 장 흐리게). 카드를 누르면 #gallery/<번호> 흰 글 페이지 ----
(function () {
  const grid = $("#gallery-grid"); if (!grid || !window.GALLERY) return;
  const G = window.GALLERY, cards = [...grid.querySelectorAll(".hcard")], more = $("#gallery-more"), empty = $("#gallery-empty"), tabs = $("#gallery-tabs"), input = $("#gallery-search");
  // 한 줄 단위로 보여준다 : 데스크톱 3열이면 처음 3장, 다음 줄 3장은 흐린 미리보기. 모바일 1열이면 3장 + 미리보기 1장
  const cols = () => (window.matchMedia("(max-width: 820px)").matches ? 1 : 3);   // 데스크톱 3열, 모바일 1열 (CSS 와 같은 기준)
  const PER = () => 3, PEEK = () => (cols() >= 3 ? 3 : 1);
  let year = "all", shown = PER(), q = "";
  const visible = () => G.map((g, i) => i).filter((i) => { const g = G[i]; return (year === "all" || g.y === +year) && (!q || (g.t + " " + g.v).toLowerCase().includes(q)); });
  const draw = () => {
    const vis = visible(); let n = 0; const peek = PEEK();
    cards.forEach((c, i) => { const ok = vis.includes(i); if (ok) n++; c.classList.toggle("hid", !ok || n > shown + peek); c.classList.toggle("peek", ok && n > shown && n <= shown + peek); });
    empty.hidden = vis.length > 0; more.hidden = vis.length <= shown;
  };
  tabs.addEventListener("click", (e) => { const b = e.target.closest("button"); if (!b) return; year = b.dataset.y; shown = PER(); tabs.querySelectorAll("button").forEach((x) => x.classList.toggle("current", x === b)); draw(); });
  input.addEventListener("input", () => { q = input.value.trim().toLowerCase(); shown = PER(); draw(); });
  more.querySelector(".more").addEventListener("click", () => { shown += PER(); draw(); });
  window.addEventListener("resize", draw);
  draw();
  cards.forEach((c) => c.addEventListener("click", (e) => { e.preventDefault(); navigate("gallery/" + c.dataset.g); }));
  // 상세 : oddatelier 뉴스 글처럼. 첫 장 크게, 뒤는 두 장씩, 아래 이전 / 목록 / 다음 공연 (현재 탭과 검색 안에서 이동)
  const view = $("#galleryView"); let cur = 0;
  const layout = (ph) => { const out = []; let i = 0; if (ph.length) { out.push(`<img src="images/${ph[0]}" alt="">`); i = 1; } while (i < ph.length) { if (i + 1 < ph.length) { out.push(`<div class="pair"><img src="images/${ph[i]}" alt="" loading="lazy"><img src="images/${ph[i + 1]}" alt="" loading="lazy"></div>`); i += 2; } else { out.push(`<img src="images/${ph[i]}" alt="" loading="lazy">`); i++; } } return out.join(""); };
  openGalleryView = (i) => {
    const g = G[i]; if (!g) return; cur = i;
    const apply = () => {
      $("#gv-date").textContent = `${g.y}.${g.d}  /  ${g.v}`; $("#gv-title").textContent = g.t; $("#gv-photos").innerHTML = layout(g.photos);
      const vis = visible(), k = vis.indexOf(i), p = vis[k - 1], n = vis[k + 1];
      $("#gv-prev").toggleAttribute("disabled", p === undefined); $("#gv-next").toggleAttribute("disabled", n === undefined);
      if (!view.open) { view.showModal(); view.classList.add("show"); }
      view.scrollTo(0, 0);
      if (document.activeElement && view.contains(document.activeElement)) document.activeElement.blur();
    };
    // 프로필처럼 : 누른 카드의 사진이 상세의 첫 사진으로 자연스럽게 커진다 (View Transition)
    const from = cards[i] && cards[i].querySelector(".img");
    if (from && document.startViewTransition && !view.open) {
      from.style.viewTransitionName = "hero";
      document.startViewTransition(() => { from.style.viewTransitionName = ""; apply(); const first = $("#gv-photos img"); if (first) first.style.viewTransitionName = "hero"; }).finished.then(() => { const first = $("#gv-photos img"); if (first) first.style.viewTransitionName = ""; });
    } else apply();
  };
  const go = (d) => { const vis = visible(), k = vis.indexOf(cur) + d; if (k >= 0 && k < vis.length) navigate("gallery/" + vis[k], true); };
  $("#gv-prev").addEventListener("click", (e) => { e.preventDefault(); go(-1); });
  $("#gv-next").addEventListener("click", (e) => { e.preventDefault(); go(1); });
  $("#gv-list").addEventListener("click", (e) => { e.preventDefault(); closeTo("gallery"); });
})();
render(location.hash.replace(/^#/, ""));

const y = document.getElementById("year"); if (y) y.textContent = new Date().getFullYear();


// ---- 메인 메일 아이콘 : 주소 창을 띄우고 복사 ----
(function () {
  const open = $("#mail-open"), dlg = $("#mailDialog"); if (!open || !dlg) return;
  const show = () => { dlg.showModal(); requestAnimationFrame(() => dlg.classList.add("show")); if (document.activeElement && dlg.contains(document.activeElement)) document.activeElement.blur(); };
  const hide = () => { dlg.classList.remove("show"); $("#mail-copied").classList.remove("on"); setTimeout(() => { if (!dlg.classList.contains("show")) dlg.close(); }, 200); };
  open.addEventListener("click", (e) => { e.preventDefault(); show(); });
  $("#mail-close").addEventListener("click", hide);
  dlg.addEventListener("cancel", (e) => { e.preventDefault(); hide(); });
  let down = false; dlg.addEventListener("mousedown", (e) => { down = e.target === dlg; }); dlg.addEventListener("click", (e) => { if (e.target === dlg && down) hide(); down = false; });
  const copy = async (text) => { try { await navigator.clipboard.writeText(text); } catch (_) { const ta = document.createElement("textarea"); ta.value = text; ta.style.position = "fixed"; ta.style.opacity = "0"; document.body.appendChild(ta); ta.select(); document.execCommand("copy"); ta.remove(); } const c = $("#mail-copied"); c.classList.remove("on"); void c.offsetWidth; c.classList.add("on"); clearTimeout(c._t); c._t = setTimeout(() => c.classList.remove("on"), 2200); };
  dlg.querySelectorAll("button[data-copy]").forEach((btn) => btn.addEventListener("click", () => copy(btn.dataset.copy)));
})();

// ---- TOP 버튼 : 각 팝업을 300px 넘게 내리면 보이고, 누르면 부드럽게 맨 위로 ----
document.querySelectorAll("dialog .totop").forEach((btn) => {
  const dlg = btn.closest("dialog");
  // 상단 바(마크, MENU) : 아래로 내리면 숨고 위로 올리면 바로 다시 보인다 (ibighit 식)
  let last = 0;
  dlg.addEventListener("scroll", () => {
    const y = dlg.scrollTop; btn.classList.toggle("on", y > 300);
    dlg.classList.toggle("bar-hide", y > 80 && y > last); last = y;
  }, { passive: true });
  btn.addEventListener("click", () => dlg.scrollTo({ top: 0, behavior: "smooth" }));
});

// ---- Contact : JYP 식 문의 양식. 유형별 칸 이름, 필수 표시, 동의 둘 다 체크해야 등록, 보내기는 mailto ----
(function () {
const EMAIL = window.NOVA_EMAIL;
const f = document.getElementById("bf"); if (!f) return; const submit = document.getElementById("submit");
const REQ = ["type", "event", "name", "phone", "email", "desc"];
// 유형에 따라 칸 이름, 안내, 동의 표가 바뀐다
const KIND = {
  "공연 섭외": { event: ["행사명", "행사명을 입력해 주세요."], date: ["행사 일시", "예: 2026.12.20 (토) 오후 7시. 미정 시 미정으로 기재"], place: ["행사 장소", "예: 부산문화회관 대극장. 미정 시 미정으로 기재"], desc: ["문의 내용", "행사 성격, 희망 구성(인원과 시간), 관객 규모, 음향 장비 유무, 예산 범위 등"], ag: ["행사 정보", "행사명, 행사 일시, 행사 장소", "공연 섭외 검토, 일정 조율"] },
  "협업 제안": { event: ["제안명", "제안 내용을 한 줄로 입력해 주세요."], date: ["희망 시기", "예: 2027년 상반기. 미정 시 미정으로 기재"], place: ["진행 방식", "예: 공동 공연, 음원 제작, 온라인 콘텐츠"], desc: ["제안 내용", "협업의 목적과 범위, 기대 역할, 일정과 예산 등"], ag: ["제안 정보", "제안명, 희망 시기, 진행 방식", "협업 제안 검토, 일정 조율"] },
  "촬영, 인터뷰": { event: ["매체명 또는 프로그램명", "매체명 또는 프로그램명을 입력해 주세요."], date: ["촬영 일시", "예: 2026.12.20 (토) 오후 2시. 미정 시 미정으로 기재"], place: ["촬영 장소", "예: 스튜디오, 공연장. 미정 시 미정으로 기재"], desc: ["요청 내용", "촬영 또는 인터뷰의 목적, 분량, 공개 매체와 시기 등"], ag: ["촬영 정보", "매체명, 촬영 일시, 촬영 장소", "촬영 및 인터뷰 요청 검토, 일정 조율"] },
  "기타 문의": { event: ["제목", "문의 제목을 입력해 주세요."], date: ["관련 일자", "해당하는 경우에만 기재"], place: ["관련 장소", "해당하는 경우에만 기재"], desc: ["문의 내용", "문의하실 내용을 입력해 주세요."], ag: ["문의 정보", "제목, 관련 일자, 관련 장소", "문의 검토 및 답변"] },
};
const setKind = (k) => {
  const d = KIND[k] || KIND["공연 섭외"];
  for (const key of ["event", "date", "place", "desc"]) { const box = document.getElementById("f-" + key); box.querySelector("em").textContent = d[key][0]; f.elements[key].placeholder = d[key][1]; const m = box.querySelector(".msg"); if (m) m.textContent = d[key][0] + (key === "desc" ? "을 입력해 주세요." : "을(를) 입력해 주세요.").replace("을(를)", /[가-힣]$/.test(d[key][0]) && (d[key][0].charCodeAt(d[key][0].length - 1) - 44032) % 28 ? "을" : "를"); }
  document.getElementById("ag2-title").textContent = d.ag[0]; document.getElementById("ag2-items").textContent = d.ag[1]; document.getElementById("ag2-purpose").textContent = d.ag[2];
};
// 유형을 고르기 전에는 나머지 칸과 동의가 잠긴다
const lock = (on) => { f.classList.toggle("locked", on); [...f.elements].forEach((el) => { if (el.name && el.name !== "type") el.disabled = on; }); if (on) submit.disabled = true; else gate(); };
f.elements.type.addEventListener("change", (e) => { e.target.classList.toggle("empty", !e.target.value); setKind(e.target.value); lock(!e.target.value); });
setKind(""); lock(true);
contactDirty = () => [...f.elements].some((el) => el.name && (el.type === "checkbox" ? el.checked : el.value.trim()));
const ld = $("#leaveDialog"); let pending = null;
askLeave = (go) => { pending = go; ld.showModal(); requestAnimationFrame(() => ld.classList.add("show")); if (document.activeElement && ld.contains(document.activeElement)) document.activeElement.blur(); };
const hideLeave = () => { ld.classList.remove("show"); setTimeout(() => { if (!ld.classList.contains("show")) ld.close(); }, 200); };
$("#leave-stay").addEventListener("click", () => { pending = null; hideLeave(); });
$("#leave-go").addEventListener("click", () => { const go = pending; pending = null; f.reset(); f.elements.type.classList.add("empty"); setKind(""); lock(true); hideLeave(); if (go) go(); });
ld.addEventListener("cancel", (e) => { e.preventDefault(); pending = null; hideLeave(); });
// 탭을 닫거나 새로고침할 때는 브라우저 기본 경고
window.addEventListener("beforeunload", (e) => { if (parse(location.hash).top === "contact" && contactDirty()) { e.preventDefault(); e.returnValue = ""; } });
// 동의 두 개를 모두 체크해야 등록이 살아난다
const gate = () => { submit.disabled = !(f.elements.agree1.checked && f.elements.agree2.checked); };
f.elements.agree1.addEventListener("change", gate); f.elements.agree2.addEventListener("change", gate); gate();
// 필수 칸은 입력하면 바로 표시가 사라진다
REQ.forEach((k) => f.elements[k].addEventListener("input", (e) => { if (e.target.value.trim()) e.target.closest(".f").classList.remove("err"); }));
f.addEventListener("submit", (e) => {
  e.preventDefault();
  let ok = true;
  REQ.forEach((k) => { const el = f.elements[k]; const bad = !el.value.trim(); el.closest(".f").classList.toggle("err", bad); if (bad) ok = false; });
  if (!ok) { f.querySelector(".f.err input, .f.err select, .f.err textarea").focus(); return; }
  const v = (k) => (f.elements[k].value || "").trim() || "미정";
  const L = KIND[v("type")] || KIND["공연 섭외"];
  const body = ["[" + v("type") + "] " + v("event"), "", "유형: " + v("type"), L.event[0] + ": " + v("event"), "소속: " + v("org"), "이름: " + v("name"), "연락처: " + v("phone"), "이메일: " + v("email"), L.date[0] + ": " + v("date"), L.place[0] + ": " + v("place"), "", L.desc[0] + ":", v("desc"), "", "개인정보 및 행사 정보 수집, 이용에 동의함"].join("\n");
  location.href = "mailto:" + EMAIL + "?subject=" + encodeURIComponent("[" + v("type") + "] " + v("event")) + "&body=" + encodeURIComponent(body);
  document.getElementById("done").style.display = "block";
});

})();

// ---- 방문자 수 (Notice 머리줄) : 외부 카운터 Abacus. 누적은 열 때마다 1, 접속 중은 20초마다 신호를 보내 최근 1분(3칸) 중 최댓값 ----
(function () {
  const nowEl = $("#vis-now"), totEl = $("#vis-total"); if (!nowEl) return;
  const NS = "music-project-nova", API = "https://abacus.jasoncameron.dev";
  const fmt = (n) => Number(n).toLocaleString("ko-KR");
  const j = (u) => fetch(u).then((r) => r.json());
  j(`${API}/hit/${NS}/total`).then((r) => { totEl.textContent = fmt(r.value); }).catch(() => {});
  let lastSlot = -1; const mine = new Set();
  const ping = async () => {
    const slot = Math.floor(Date.now() / 20000);   // 20초 칸
    if (slot === lastSlot) return; lastSlot = slot;
    try {
      const cur = await j(`${API}/hit/${NS}/s${slot}`); mine.add(slot);
      // 앞 칸은 이 브라우저가 직접 신호를 보낸 칸만 읽는다 (없는 칸을 읽으면 브라우저 콘솔에 404 가 찍히므로)
      const g = (k) => (mine.has(k) ? j(`${API}/get/${NS}/s${k}`).catch(() => ({ value: 0 })) : Promise.resolve({ value: 0 }));
      const [a, b] = await Promise.all([g(slot - 1), g(slot - 2)]);
      // 각 20초 칸에는 열려 있는 브라우저마다 1 씩 들어오므로, 최근 세 칸 중 가장 큰 값이 접속 중인 수
      nowEl.textContent = fmt(Math.max(1, cur.value, a.value || 0, b.value || 0));
    } catch (_) {}
  };
  ping(); setInterval(ping, 20000);
  document.addEventListener("visibilitychange", () => { if (!document.hidden) ping(); });
})();
