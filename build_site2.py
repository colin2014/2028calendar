import json

lessons = json.load(open('/home/claude/g11_planner_v2/g11_lessons_v3.json'))
catalog = json.load(open('/home/claude/g11_planner_v2/g11_all_items.json'))

LESSONS_JSON = json.dumps(lessons, separators=(',', ':'))
CATALOG_JSON = json.dumps(catalog, separators=(',', ':'))

html = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<title>DP1 HL Computer Science Calendar</title>
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Baloo+2:wght@600;700;800&family=IBM+Plex+Sans:ital,wght@0,400;0,500;0,600;0,700;1,400&family=IBM+Plex+Mono:wght@400;500;600&display=swap">
<style>
:root{
  --paper:#f6f1e4;
  --paper-dot: rgba(28,43,74,0.12);
  --surface:#fffdf8;
  --surface-alt:#efe7d3;
  --ink:#1c2b4a;
  --ink-2:#4c5a75;
  --ink-3:#8b93a6;
  --border:rgba(28,43,74,0.14);
  --border-strong:rgba(28,43,74,0.28);
  --accent:#d6607e;
  --accent-deep:#b8425f;
  --accent-soft:#f8e3e8;
  --navy-block:#1c2b4a;
  --navy-block-ink:#fbf6ea;
  --theme-a:#2f6fb0;
  --theme-a-soft:#e3edf7;
  --theme-b:#1f8a72;
  --theme-b-soft:#e1f2ec;
  --ia:#a8721c;
  --ia-soft:#f5ead2;
  --assessment:#b8425f;
  --assessment-soft:#f8e3e8;
  --buffer:#7d7398;
  --buffer-soft:#ece9f2;
  --done:#3f7d52;
  --done-soft:#e3f0e6;
  --warn:#b8642a;
  --warn-soft:#f6e6d5;
  --shadow: 0 1px 2px rgba(28,20,10,0.06), 0 10px 26px -14px rgba(28,20,10,0.28);
  --shadow-lg: 0 6px 14px rgba(28,20,10,0.10), 0 24px 48px -18px rgba(28,20,10,0.34);
  --radius: 12px;
  color-scheme: light;
}
/* This calendar is deliberately locked to its warm cream/navy/pink "desk calendar"
   look at all times - it does not switch with system/device dark mode. */

*{box-sizing:border-box;}
html,body{margin:0;padding:0;}
body{
  background:
    radial-gradient(var(--paper-dot) 1.1px, transparent 1.1px) 0 0/16px 16px,
    var(--paper);
  color:var(--ink);
  font-family:"IBM Plex Sans", system-ui, sans-serif;
  line-height:1.45;
}
.mono{font-family:"IBM Plex Mono", ui-monospace, monospace;}
.display{font-family:"Baloo 2", "IBM Plex Sans", sans-serif;}
button{font-family:inherit;}
h1,h2,h3{margin:0; text-wrap:balance;}

.spiral{
  display:flex; justify-content:center; gap:14px; padding:10px 0 0;
}
.spiral span{
  width:11px; height:11px; border-radius:50%;
  background:var(--surface); border:2.5px solid var(--border-strong);
}

.shell{max-width:1240px; margin:0 auto; padding:6px 18px 56px;}

/* ---------- Header ---------- */
header.top{
  display:flex; align-items:flex-end; justify-content:space-between; gap:16px;
  flex-wrap:wrap; padding:14px 4px 16px; border-bottom:3px solid var(--accent); margin-bottom:16px;
}
header.top .title-block{display:flex; align-items:center; gap:10px;}
header.top .title-block .mark{
  width:34px; height:34px; border-radius:9px; background:var(--navy-block); color:var(--navy-block-ink);
  display:flex; align-items:center; justify-content:center; font-family:"IBM Plex Mono",monospace; font-weight:700; font-size:14px;
}
header.top h1{font-family:"Baloo 2",sans-serif; font-weight:700; font-size:26px; color:var(--ink); letter-spacing:.2px;}
header.top .sub{font-size:12px; color:var(--ink-3); margin-top:1px;}
.nav-cluster{display:flex; align-items:center; gap:10px;}
.month-label{font-family:"Baloo 2",sans-serif; font-weight:700; font-size:22px; color:var(--ink); min-width:200px; text-align:right; font-variant-numeric:tabular-nums;}
.iconbtn{
  border:1.5px solid var(--border-strong); background:var(--surface); color:var(--ink-2);
  border-radius:8px; width:32px; height:32px; display:inline-flex; align-items:center; justify-content:center;
  cursor:pointer; font-size:15px;
}
.iconbtn:hover{background:var(--surface-alt); color:var(--ink);}
.todaybtn{
  border:1.5px solid var(--border-strong); background:var(--surface); color:var(--ink);
  border-radius:8px; padding:6px 13px; font-size:12.5px; font-weight:600; cursor:pointer;
}
.todaybtn:hover{background:var(--surface-alt);}

/* ---------- Main layout ---------- */
.mainrow{display:grid; grid-template-columns:1fr 306px; gap:18px; align-items:flex-start;}
@media (max-width:880px){ .mainrow{grid-template-columns:1fr;} .sidebar{position:static;} }

/* ---------- Calendar ---------- */
.cal-panel{
  background:var(--surface); border:1px solid var(--border); border-radius:var(--radius);
  box-shadow:var(--shadow); overflow:hidden;
}
.cal-grid{display:grid; grid-template-columns:repeat(7,1fr);}
.cal-grid .dow{
  font-size:11px; font-weight:700; text-transform:uppercase; letter-spacing:.06em;
  color:#fff; text-align:center; padding:9px 0; background:var(--accent);
}
.cal-cell{
  min-height:98px; border-right:1px solid var(--border); border-bottom:1px solid var(--border);
  padding:6px 6px 8px; display:flex; flex-direction:column; gap:4px; background:var(--surface);
}
.cal-cell.weekend{background:var(--surface-alt);}
.cal-cell.empty{background:var(--surface-alt);}
.cal-cell.has-day{cursor:pointer; transition:background-color .1s ease;}
.cal-cell.has-day:hover{background:var(--surface-alt);}
.cal-cell.has-day.weekend:hover{background:var(--paper-dot);}
.cal-cell .datenum{
  font-size:12px; color:var(--ink-3); font-variant-numeric:tabular-nums; align-self:flex-start;
  width:22px; height:22px; display:flex; align-items:center; justify-content:center; border-radius:50%;
  font-weight:600;
}
.cal-cell.is-today .datenum{border:2px solid var(--accent); color:var(--accent);}
.chip{
  display:flex; align-items:center; gap:5px; border-radius:6px; padding:3px 6px;
  font-size:11px; cursor:pointer; border:1px solid transparent; line-height:1.25;
}
.chip:hover{box-shadow:var(--shadow); border-color:var(--border-strong);}
.chip.type-buffer{cursor:default;}
.chip.type-buffer:hover{box-shadow:none; border-color:transparent;}
.chip .cb{
  flex:0 0 auto; width:12px; height:12px; border-radius:3px; border:1.5px solid currentColor;
  display:inline-flex; align-items:center; justify-content:center; font-size:8px; color:inherit;
}
.chip.done .cb{background:currentColor;}
.chip.done .cb:after{content:"\2713"; color:var(--surface); font-size:8px; font-weight:700;}
.chip .txt{overflow:hidden; text-overflow:ellipsis; white-space:nowrap; font-family:"IBM Plex Mono",monospace; font-weight:600;}
.chip.done .txt{text-decoration:line-through; opacity:.65;}
.chip.type-content.theme-a{background:var(--theme-a-soft); color:var(--theme-a);}
.chip.type-content.theme-b{background:var(--theme-b-soft); color:var(--theme-b);}
.chip.type-ia{background:var(--ia-soft); color:var(--ia);}
.chip.type-assessment{background:var(--assessment-soft); color:var(--assessment); font-weight:700;}
.chip.type-buffer{background:var(--buffer-soft); color:var(--buffer); font-style:italic;}
.chip.selected{outline:2px solid var(--accent); outline-offset:1px;}
.link-dot{width:5px; height:5px; border-radius:50%; background:currentColor; display:inline-block; margin-left:auto; flex:0 0 auto;}

/* ---------- Sidebar ---------- */
.sidebar{position:sticky; top:14px; display:flex; flex-direction:column; gap:14px;}
.blockcard{background:var(--surface); border:1px solid var(--border); border-radius:var(--radius); box-shadow:var(--shadow); overflow:hidden;}
.blockcard .blockhead{
  background:var(--navy-block); color:var(--navy-block-ink); font-family:"Baloo 2",sans-serif; font-weight:700;
  font-size:13px; letter-spacing:.04em; text-transform:uppercase; padding:9px 14px;
}
.blockcard .blockbody{padding:14px 16px;}
.empty-hint{color:var(--ink-3); font-size:13px; font-style:italic;}

.detail .code{font-family:"IBM Plex Mono",monospace; font-size:13.5px; font-weight:700; color:var(--accent);}
.detail h3{font-size:16px; margin:4px 0 6px;}
.detail p.meta{margin:0 0 10px; color:var(--ink-2); font-size:12px;}
.detail p.detail-text{margin:0 0 12px; color:var(--ink-2); font-size:13px;}
.badges{display:flex; gap:6px; flex-wrap:wrap; margin-bottom:10px;}
.badge{font-size:10.5px; font-weight:600; padding:2px 8px; border-radius:20px; border:1px solid var(--border-strong); color:var(--ink-2);}
.badge.hl{background:var(--accent-soft); color:var(--accent-deep); border-color:transparent;}
.badge.ia{background:var(--ia-soft); color:var(--ia); border-color:transparent;}
.badge.assessment{background:var(--assessment-soft); color:var(--assessment); border-color:transparent;}
.badge.buffer{background:var(--buffer-soft); color:var(--buffer); border-color:transparent;}

.complete-row{display:flex; align-items:center; gap:8px; padding:8px 10px; background:var(--surface-alt); border:1px solid var(--border); border-radius:8px; margin-bottom:10px; cursor:pointer;}
.complete-row .big-check{
  width:18px; height:18px; border-radius:5px; border:2px solid var(--border-strong);
  display:flex; align-items:center; justify-content:center; color:var(--done); flex:0 0 auto;
}
.complete-row .big-check.done{background:var(--done); border-color:var(--done);}
.complete-row .big-check.done:after{content:"\2713"; color:#fff; font-size:12px; font-weight:700;}
.complete-row span{font-size:12.5px; font-weight:600;}

.item-block{border-top:1px dashed var(--border-strong); padding-top:10px; margin-top:10px;}
.item-block:first-child{border-top:none; padding-top:0; margin-top:0;}

/* ---------- File-style link buttons (slides / exit ticket) ---------- */
.filefield{margin-bottom:8px;}
.filefield:last-child{margin-bottom:0;}
.filerow{display:flex; align-items:stretch; gap:6px;}
.filebtn{
  flex:1 1 auto; display:flex; align-items:center; gap:8px; min-width:0;
  padding:0 12px; height:36px; border-radius:8px; border:1.5px solid var(--border-strong);
  background:var(--surface); color:var(--ink); text-decoration:none; font-size:12.5px; font-weight:700;
}
.filebtn .ico{flex:0 0 auto; display:flex; color:inherit;}
.filebtn .lbl{overflow:hidden; text-overflow:ellipsis; white-space:nowrap;}
.filebtn.has-link{background:var(--accent-soft); border-color:var(--accent); color:var(--accent-deep); cursor:pointer;}
.filebtn.has-link:hover{background:var(--accent); color:#fff;}
.filebtn.empty{border-style:dashed; color:var(--ink-3); font-weight:600;}
.editbtn{
  flex:0 0 auto; width:36px; height:36px; display:inline-flex; align-items:center; justify-content:center;
  border-radius:8px; border:1.5px solid var(--border-strong); background:var(--surface); color:var(--ink-2); cursor:pointer;
}
.editbtn:hover{background:var(--surface-alt); color:var(--ink);}
.link-editor{display:flex; gap:5px; margin-top:6px;}
.link-editor[hidden]{display:none;}
.link-editor input[type=text]{flex:1 1 auto; min-width:0; font-size:12px; padding:6px 8px;}
.iconbtn2{
  flex:0 0 auto; width:30px; height:30px; padding:0; display:inline-flex; align-items:center; justify-content:center;
  border-radius:7px; border:1px solid var(--border-strong); background:var(--surface); color:var(--ink-2); cursor:pointer;
}
.iconbtn2:hover{background:var(--surface-alt); color:var(--ink);}
.iconbtn2.save{color:var(--done); border-color:var(--done);}
.iconbtn2.save:hover{background:var(--done); color:#fff;}
.iconbtn2.cancel:hover{background:var(--warn-soft); color:var(--warn);}
.assessed-list{font-size:12px; color:var(--ink-2); margin:0; padding-left:16px;}
.assessed-list li{margin-bottom:2px;}

.legend-row{display:flex; align-items:center; gap:8px; font-size:12px; color:var(--ink-2); margin-bottom:7px;}
.legend-row:last-child{margin-bottom:0;}
.legend-row .dot{width:10px; height:10px; border-radius:3px; flex:0 0 auto;}
.progress-track{width:100%; height:8px; background:var(--surface-alt); border-radius:6px; overflow:hidden; border:1px solid var(--border); margin:6px 0 8px;}
.progress-fill{height:100%; background:var(--done); border-radius:6px; transition:width .3s ease;}
.progress-label{font-size:12px; color:var(--ink-2);}
.progress-label b{color:var(--ink); font-variant-numeric:tabular-nums;}
.mini-stats{display:flex; flex-wrap:wrap; gap:10px; margin-top:8px;}
.mini-stats .mi{font-size:11px; color:var(--ink-3);}
.mini-stats .mi b{display:block; font-size:14px; color:var(--ink); font-variant-numeric:tabular-nums;}

/* ---------- Exam countdown ---------- */
.cd-grid{display:grid; grid-template-columns:repeat(4,1fr); gap:6px;}
.cd-unit{background:var(--navy-block); color:var(--navy-block-ink); border-radius:8px; padding:8px 2px 7px; text-align:center;}
.cd-num{font-family:"IBM Plex Mono",monospace; font-weight:700; font-size:19px; font-variant-numeric:tabular-nums; line-height:1.1;}
.cd-lbl{font-size:8.5px; text-transform:uppercase; letter-spacing:.06em; opacity:.7; margin-top:3px;}
.cd-sub{font-size:11px; color:var(--ink-3); margin-top:9px; text-align:center;}

input[type=text],input[type=password]{
  font-family:inherit; font-size:13px; border:1px solid var(--border-strong);
  border-radius:7px; padding:7px 10px; background:var(--surface); color:var(--ink);
}
button.btn{font-size:12.5px; cursor:pointer; border-radius:7px; border:1px solid var(--border-strong); background:var(--surface); color:var(--ink); padding:6px 11px;}
button.btn:hover{background:var(--surface-alt);}
button.btn.primary{background:var(--accent); border-color:var(--accent); color:#fff; font-weight:600;}
button.btn.primary:hover{background:var(--accent-deep); border-color:var(--accent-deep);}
button.btn:disabled{opacity:.4; cursor:not-allowed;}

/* ---------- Below-the-fold sections ---------- */
.lowerwrap{max-width:1240px; margin:26px auto 0; padding:0 18px;}
.section-toggle{
  display:flex; align-items:center; gap:8px; cursor:pointer; padding:10px 2px; color:var(--ink-2);
  font-size:13px; font-weight:600; user-select:none;
}
.section-toggle .car{transition:transform .15s ease; font-size:11px;}
.section-toggle.open .car{transform:rotate(90deg);}
.section-body{display:none; padding:4px 2px 20px;}
.section-body.open{display:block;}
.panel{background:var(--surface); border:1px solid var(--border); border-radius:var(--radius); padding:16px 18px; box-shadow:var(--shadow);}
.search-row{display:flex; gap:8px; margin-bottom:10px; flex-wrap:wrap;}
input[type=text]#searchBox{flex:1 1 220px; min-width:160px;}
table.agenda{width:100%; border-collapse:collapse; font-size:13px;}
table.agenda th{
  text-align:left; font-size:11px; text-transform:uppercase; letter-spacing:.04em;
  color:var(--ink-3); padding:7px 10px; border-bottom:1px solid var(--border-strong);
  position:sticky; top:0; background:var(--surface-alt);
}
table.agenda td{padding:6px 10px; border-bottom:1px solid var(--border); vertical-align:top;}
table.agenda tr:hover td{background:var(--surface-alt); cursor:pointer;}
table.agenda tr.done td{color:var(--ink-3);}
table.agenda tr.done td.focuscell{text-decoration:line-through;}
table.agenda td.code{font-family:"IBM Plex Mono",monospace; white-space:nowrap;}
.agenda-scroll{max-height:420px; overflow:auto; border:1px solid var(--border); border-radius:8px;}
.check-td{width:26px; text-align:center;}
.mini-check{width:15px; height:15px; border-radius:3px; border:1.5px solid var(--border-strong); cursor:pointer; display:inline-flex; align-items:center; justify-content:center; color:var(--done);}
.mini-check.done{background:var(--done-soft); border-color:var(--done); color:var(--done);}
.mini-check.done:after{content:"\2713"; font-size:10px; font-weight:700;}
.lock-row{display:flex; align-items:center; gap:8px; flex-wrap:wrap;}
.import-active{display:none;}
.import-active.show{display:block; margin-top:12px;}
.file-drop{border:1.5px dashed var(--border-strong); border-radius:8px; padding:16px; text-align:center; color:var(--ink-2); font-size:13px; background:var(--surface-alt);}
.file-drop input[type=file]{margin-top:8px;}
.syllabus-topic{margin-bottom:6px;}
.syllabus-topic summary{cursor:pointer; font-weight:600; padding:6px 4px; font-size:13.5px;}
.syllabus-topic summary .hrs{color:var(--ink-3); font-weight:400; font-size:12px;}
.syllabus-sub{margin:4px 0 8px 18px;}
.syllabus-sub .st-title{font-size:12px; color:var(--ink-2); font-weight:600; margin:6px 0 3px;}
.syllabus-item{display:flex; gap:8px; align-items:baseline; font-size:12.5px; padding:2px 0; color:var(--ink-2);}
.syllabus-item .code{font-family:"IBM Plex Mono",monospace; color:var(--ink); min-width:56px; flex:0 0 auto;}
.syllabus-item.covered{opacity:0.55;}
.syllabus-item.covered .code{color:var(--done);}
.assumptions-foot{font-size:12px; color:var(--ink-2);}
.assumptions-foot ul{margin:8px 0 0; padding-left:18px;}
.assumptions-foot li{margin-bottom:5px;}
.assumptions-foot li b{color:var(--ink);}
.toast{
  position:fixed; bottom:20px; left:50%; transform:translateX(-50%);
  background:var(--navy-block); color:var(--navy-block-ink); padding:10px 18px; border-radius:8px;
  font-size:13px; box-shadow:var(--shadow); opacity:0; pointer-events:none;
  transition:opacity .2s ease, transform .2s ease; z-index:50; max-width:90vw; text-align:center;
}
.toast.show{opacity:1; transform:translateX(-50%) translateY(-6px);}
.footer-note{text-align:center; color:var(--ink-3); font-size:11px; margin-top:22px;}
.hidden{display:none !important;}

@media (max-width:640px){
  .cal-cell{min-height:64px;}
  .chip .txt{max-width:46px;}
  header.top{align-items:flex-start;}
  .month-label{text-align:left; min-width:0;}
}
</style>
</head>
<body>

<div class="spiral">
  <span></span><span></span><span></span><span></span><span></span><span></span><span></span><span></span>
  <span></span><span></span><span></span><span></span><span></span><span></span><span></span><span></span>
  <span></span><span></span><span></span><span></span>
</div>

<div class="shell">

  <header class="top">
    <div class="title-block">
      <div class="mark">{}</div>
      <div>
        <h1>DP1 Lesson Calendar</h1>
        <div class="sub">HL Computer Science &middot; first assessment 2028</div>
      </div>
    </div>
    <div class="nav-cluster">
      <button class="todaybtn" id="todayBtn">Today</button>
      <button class="iconbtn" id="prevBtn" aria-label="Previous month">&larr;</button>
      <div class="month-label" id="monthLabel"></div>
      <button class="iconbtn" id="nextBtn" aria-label="Next month">&rarr;</button>
    </div>
  </header>

  <div class="mainrow">
    <div class="cal-panel">
      <div class="cal-grid" id="calGridHead"></div>
      <div class="cal-grid" id="calGrid"></div>
    </div>

    <div class="sidebar">
      <div class="blockcard" id="detailCard">
        <div class="blockhead" id="detailHead">Selected day</div>
        <div class="blockbody">
          <div class="empty-hint" id="detailEmpty">Click a day on the calendar to see what's planned.</div>
          <div class="detail" id="detailBody" style="display:none;"></div>
        </div>
      </div>

      <div class="blockcard">
        <div class="blockhead"><svg viewBox="0 0 24 24" width="12" height="12" style="vertical-align:-1px;margin-right:6px;" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 3"/></svg>Countdown to exams</div>
        <div class="blockbody">
          <div class="cd-grid">
            <div class="cd-unit"><div class="cd-num" id="cdDays">0</div><div class="cd-lbl">Days</div></div>
            <div class="cd-unit"><div class="cd-num" id="cdHours">00</div><div class="cd-lbl">Hrs</div></div>
            <div class="cd-unit"><div class="cd-num" id="cdMins">00</div><div class="cd-lbl">Min</div></div>
            <div class="cd-unit"><div class="cd-num" id="cdSecs">00</div><div class="cd-lbl">Sec</div></div>
          </div>
          <div class="cd-sub">to first assessment &middot; 25 Apr 2028</div>
        </div>
      </div>

      <div class="blockcard">
        <div class="blockhead">Legend</div>
        <div class="blockbody">
          <div class="legend-row"><span class="dot" style="background:var(--theme-a)"></span> Theme A &ndash; Concepts</div>
          <div class="legend-row"><span class="dot" style="background:var(--theme-b)"></span> Theme B &ndash; Computational thinking</div>
          <div class="legend-row"><span class="dot" style="background:var(--assessment)"></span> Assessment</div>
          <div class="legend-row"><span class="dot" style="background:var(--ia)"></span> Internal Assessment</div>
          <div class="legend-row"><span class="dot" style="background:var(--buffer)"></span> Review / catch-up</div>
          <div class="legend-row"><span style="width:10px;height:10px;border-radius:50%;border:2px solid var(--accent);flex:0 0 auto;"></span> Today</div>
        </div>
      </div>

      <div class="blockcard">
        <div class="blockhead">Progress</div>
        <div class="blockbody">
          <div class="progress-label"><b id="progressCount">0/125</b> lessons marked complete</div>
          <div class="progress-track"><div class="progress-fill" id="progressFill"></div></div>
          <div class="mini-stats" id="statsMini"></div>
        </div>
      </div>
    </div>
  </div>
</div>

<div class="lowerwrap">
  <div class="section-toggle" data-target="sec-agenda"><span class="car">&#9656;</span> Search &amp; full agenda</div>
  <div class="section-body" id="sec-agenda">
    <div class="panel">
      <div class="search-row"><input type="text" id="searchBox" placeholder="Search code or topic&hellip;"></div>
      <div class="agenda-scroll">
        <table class="agenda">
          <thead><tr><th class="check-td"></th><th>Date</th><th>Day</th><th>Period</th><th>Code</th><th>Focus</th><th>Links</th></tr></thead>
          <tbody id="agendaBody"></tbody>
        </table>
      </div>
    </div>
  </div>

  <div class="section-toggle" data-target="sec-export"><span class="car">&#9656;</span> Export &amp; import schedule</div>
  <div class="section-body" id="sec-export">
    <div class="panel">
      <p style="color:var(--ink-2); font-size:13px; margin:0 0 12px;">Export gives you the whole calendar as a CSV. Import reads a CSV or .xlsx back in for bulk date changes. Ticking lessons complete and adding links saves automatically as you go; import is password-protected since it can replace whole dates.</p>
      <div class="lock-row">
        <button class="btn primary" id="exportBtn">Export calendar as CSV</button>
        <button class="btn" id="unlockBtn">Unlock import&hellip;</button>
        <span id="lockedNote" style="color:var(--ink-3); font-size:12px;">Soft deterrent only.</span>
      </div>
      <div id="passwordRow" class="import-active">
        <div class="lock-row">
          <input type="password" id="pwInput" placeholder="Password">
          <button class="btn primary" id="pwSubmit">Unlock</button>
          <span id="pwError" style="color:var(--warn); font-size:12px;"></span>
        </div>
      </div>
      <div id="importArea" class="import-active">
        <div class="file-drop">
          Choose a CSV or .xlsx file with columns <span class="mono">Date, Period, Type, Codes, Focus, Notes, Completed, SlidesUrls, ExitTicketUrls</span> (only Date + Period are required).
          <br><input type="file" id="fileInput" accept=".csv,.xlsx">
        </div>
        <div id="importMsg" style="font-size:12px; color:var(--ink-2); margin-top:8px;"></div>
      </div>
    </div>
  </div>

  <div class="section-toggle" data-target="sec-syllabus"><span class="car">&#9656;</span> Full syllabus reference</div>
  <div class="section-body" id="sec-syllabus">
    <div class="panel">
      <p style="color:var(--ink-2); font-size:13px; margin:0 0 10px;">All 112 content statements, grouped by topic. Greyed-out items are already covered.</p>
      <div id="syllabusRef"></div>
    </div>
  </div>

  <div class="section-toggle" data-target="sec-assumptions"><span class="car">&#9656;</span> Assumptions built into this calendar</div>
  <div class="section-body" id="sec-assumptions">
    <div class="panel assumptions-foot">
      <ul>
        <li><b>Start date:</b> Tuesday 8 September 2026.</li>
        <li><b>Timetable:</b> Monday P1 (08:55&ndash;09:55), Tuesday P3 (11:30&ndash;12:30), Thursday P4 (13:30&ndash;14:30), Friday P1 (08:55&ndash;09:55) &mdash; P4's time wasn't given to me, so 13:30&ndash;14:30 is a guess. Fix it via Import if wrong.</li>
        <li><b>Assessments:</b> every other Friday (alternating with a content lesson), each covering everything taught since the previous assessment. First Friday (11 Sept) carries content; the following Friday (18 Sept) is the first assessment.</li>
        <li><b>Term breaks:</b> mirrored from Grade 12's calendar &mdash; Oct 15&ndash;Nov 1, Dec 17&ndash;Jan 5, Feb 13&ndash;21 &mdash; plus an <b>assumed</b> two-week spring break, Mar 29&ndash;Apr 11.</li>
        <li><b>Last day of class:</b> Friday 11 June 2027 &mdash; my reading of "mid-June."</li>
        <li><b>Ordering &amp; bundling:</b> straight theme order (A1&rarr;A2&rarr;A3&rarr;A4&rarr;B1&rarr;B2&rarr;B3&rarr;B4) continuing on from A1.1.1 / A1.1.2 already covered. Each subtopic is judged individually: 12 pairs of adjacent, lighter subtopics (roughly a half-hour of content each) share a single lesson, spread across the year rather than bunched together, while denser or hands-on subtopics keep a full lesson to themselves. Only 5 review/catch-up lessons remain, and the last 8 lessons (31 May&ndash;11 Jun) are held for an early introduction to the Internal Assessment.</li>
      </ul>
    </div>
  </div>

  <p class="footer-note">Built for DP1 HL Computer Science &middot; content codes follow the IB syllabus for first assessment 2028</p>
</div>

<div class="toast" id="toast"></div>

<script src="https://cdnjs.cloudflare.com/ajax/libs/xlsx/0.18.5/xlsx.full.min.js"></script>
<script>
const IMPORT_PASSWORD = "cs2027"; // change this line to set your own import password

let LESSONS = __LESSONS_JSON__;
const CATALOG = __CATALOG_JSON__;

const CATALOG_BY_CODE = {};
CATALOG.forEach(it => CATALOG_BY_CODE[it.code] = it);

const PERIOD_TIMES = {P1:'08:55-09:55', P2:'10:25-11:25', P3:'11:30-12:30', P4:'13:30-14:30', P5:'14:30-15:30'};
const TODAY_ISO = new Date().toISOString().slice(0,10);

function parseISO(s){ const [y,m,d] = s.split('-').map(Number); return new Date(y, m-1, d); }
function fmtDate(d){ return d.toLocaleDateString('en-GB', {day:'2-digit', month:'short', year:'numeric'}); }
function monthKey(d){ return d.getFullYear() + '-' + String(d.getMonth()+1).padStart(2,'0'); }
function escapeHtml(s){ return String(s).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c])); }
function themeOf(code){ if(!code) return 'a'; return code.startsWith('B') ? 'b' : 'a'; }

/* ---------- Small inline icons (link fields) ---------- */
const ICON_SLIDES = '<svg viewBox="0 0 24 24" width="13" height="13" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="12" rx="1.6"/><path d="M8 20h8M12 16v4"/><path d="M10 8.3v3.4l3-1.7-3-1.7Z" fill="currentColor" stroke="none"/></svg>';
const ICON_TICKET = '<svg viewBox="0 0 24 24" width="13" height="13" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M3 8.5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2v2a2 2 0 0 0 0 3v2a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-2a2 2 0 0 0 0-3Z"/><path d="M9.5 6.5v11" stroke-dasharray="2.2 2.2"/></svg>';
const ICON_SAVE = '<svg viewBox="0 0 24 24" width="15" height="15" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 5a2 2 0 0 1 2-2h9l5 5v11a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2Z"/><path d="M16.5 21v-7h-9v7M7.5 3v5h7"/></svg>';
const ICON_OPEN = '<svg viewBox="0 0 24 24" width="15" height="15" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 13.2V19a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h5.8"/><path d="M14.5 3H21v6.5"/><path d="M10.3 13.7 21 3"/></svg>';
const ICON_PENCIL = '<svg viewBox="0 0 24 24" width="13" height="13" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 20h9"/><path d="M16.5 3.5a2.12 2.12 0 0 1 3 3L7 19l-4 1 1-4Z"/></svg>';
const ICON_PLUS = '<svg viewBox="0 0 24 24" width="13" height="13" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 5v14M5 12h14"/></svg>';
const ICON_CLOSE = '<svg viewBox="0 0 24 24" width="13" height="13" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 6 6 18M6 6l12 12"/></svg>';

/*
 * ---------- Live schedule reflow ----------
 * LESSONS is the stored record. computeDisplaySchedule() computes what's
 * actually shown: anything before today, or already ticked complete
 * (wherever its date is), is frozen exactly as stored. From today onward,
 * anything not yet complete is re-queued in its original order across the
 * still-open content/review dates - so a lesson that never got ticked off
 * reappears at the next slot instead of being skipped, and everything after
 * it shifts out by one. Assessment and IA sessions are never moved.
 */
function buildCodeIndex(){
  const idx = {};
  LESSONS.forEach(l => { if(l.type === 'content') (l.items||[]).forEach(it => { idx[it.code] = l; }); });
  return idx;
}

function computeDisplaySchedule(){
  const codeIdx = buildCodeIndex();
  const orderedKeys = LESSONS.filter(l => l.type === 'content').map(l => l.items[0].code);
  const pending = orderedKeys.filter(code => !codeIdx[code].completed);

  const isFrozen = l => l.date < TODAY_ISO || (l.type === 'content' && l.completed);
  const eligible = LESSONS.filter(l => (l.type === 'content' || l.type === 'buffer') && !isFrozen(l));
  const eligibleContentCount = eligible.filter(l => l.type === 'content').length;
  const overflow = Math.max(0, pending.length - eligibleContentCount);

  let pi = 0, bufferConsumed = 0, pushedCount = 0;
  const display = LESSONS.map(l => {
    if(l.type === 'ia' || l.type === 'assessment') return l;
    if(isFrozen(l)) return l;
    const isContentSlot = l.type === 'content';
    const canUseBuffer = !isContentSlot && bufferConsumed < overflow;
    if((isContentSlot || canUseBuffer) && pi < pending.length){
      if(!isContentSlot) bufferConsumed++;
      const code = pending[pi++];
      const src = codeIdx[code];
      if(src.date !== l.date) pushedCount++;
      return { date:l.date, day:l.day, period:l.period, time:l.time, type:'content', items: src.items, completed:false };
    }
    return {date:l.date, day:l.day, period:l.period, time:l.time, type:'buffer', items:[], completed:false};
  });
  display._pushedCount = pushedCount;
  return display;
}

function lessonsByDate(schedule){
  const m = {};
  schedule.forEach(l => { (m[l.date] = m[l.date] || []).push(l); });
  return m;
}
function monthList(schedule){
  const set = new Set();
  schedule.forEach(l => set.add(monthKey(parseISO(l.date))));
  return Array.from(set).sort();
}

let MONTHS = monthList(LESSONS);
let monthIdx = 0;
let selected = null; // {kind:'content'|'ia'|'assessment', key}
let saveTimer = null;

function renderStats(display){
  const trackable = LESSONS.filter(l => l.type === 'content' || l.type === 'ia' || l.type === 'assessment');
  const done = trackable.filter(l => l.completed).length;
  const pct = trackable.length ? Math.round(done/trackable.length*100) : 0;
  document.getElementById('progressFill').style.width = pct + '%';
  document.getElementById('progressCount').textContent = done + '/' + trackable.length;

  const content = LESSONS.filter(l=>l.type==='content').length;
  const ia = LESSONS.filter(l=>l.type==='ia').length;
  const assess = LESSONS.filter(l=>l.type==='assessment').length;
  const pushed = display._pushedCount || 0;
  const mini = [[content,'Content'],[assess,'Assess.'],[ia,'IA'],[pushed,'Pushed fwd']];
  document.getElementById('statsMini').innerHTML = mini.map(([n,l]) => `<div class="mi"><b>${n}</b>${l}</div>`).join('');
}

function keyOf(lesson){
  if(lesson.type === 'content') return lesson.items[0] ? lesson.items[0].code : null;
  if(lesson.type === 'ia' || lesson.type === 'assessment') return lesson.date;
  return null;
}

function isSelected(lesson){
  if(!selected) return false;
  if(lesson.type === 'content') return selected.kind === 'content' && lesson.items.some(i => i.code === selected.key);
  return selected.kind === lesson.type && selected.key === lesson.date;
}

function chipHtml(lesson, item){
  const done = lesson.completed;
  let cls = 'chip type-' + lesson.type + (done ? ' done' : '');
  let label = '';
  let hasLink = false;
  let key;
  if(lesson.type === 'content'){
    key = item.code;
    cls += ' theme-' + themeOf(item.code);
    label = item.code;
    hasLink = !!(item.slidesUrl || item.exitTicketUrl);
  } else if(lesson.type === 'ia'){
    key = lesson.date;
    label = 'IA';
    hasLink = !!(lesson.slidesUrl || lesson.exitTicketUrl);
  } else if(lesson.type === 'assessment'){
    key = lesson.date;
    label = 'Assess.';
    hasLink = !!(lesson.slidesUrl || lesson.exitTicketUrl);
  } else {
    key = '';
    label = 'Review';
  }
  const sel = isSelected(lesson) ? ' selected' : '';
  const clickable = lesson.type !== 'buffer';
  return `<div class="${cls}${sel}" data-kind="${lesson.type}" data-key="${key||''}">
    ${clickable ? `<span class="cb" data-action="toggle" data-kind="${lesson.type}" data-key="${key}"></span>` : ''}
    <span class="txt">${label}</span>
    ${hasLink ? '<span class="link-dot"></span>' : ''}
  </div>`;
}

function chipsForLesson(lesson){
  if(lesson.type === 'content') return lesson.items.map(it => chipHtml(lesson, it));
  return [chipHtml(lesson, null)];
}

function renderMonth(){
  const display = computeDisplaySchedule();
  renderStats(display);

  const [y,m] = MONTHS[monthIdx].split('-').map(Number);
  const label = new Date(y, m-1, 1).toLocaleDateString('en-GB', {month:'long', year:'numeric'});
  document.getElementById('monthLabel').textContent = label;
  document.getElementById('prevBtn').disabled = monthIdx === 0;
  document.getElementById('nextBtn').disabled = monthIdx === MONTHS.length - 1;

  const byDate = lessonsByDate(display);
  const grid = document.getElementById('calGrid');
  const firstOfMonth = new Date(y, m-1, 1);
  const startWeekday = (firstOfMonth.getDay() + 6) % 7;
  const daysInMonth = new Date(y, m, 0).getDate();

  let html = '';
  for(let i=0;i<startWeekday;i++) html += `<div class="cal-cell empty"></div>`;
  for(let day=1; day<=daysInMonth; day++){
    const iso = `${y}-${String(m).padStart(2,'0')}-${String(day).padStart(2,'0')}`;
    const dow = new Date(y,m-1,day).getDay();
    const isWeekend = (dow === 0 || dow === 6) ? ' weekend' : '';
    const ls = byDate[iso];
    const isToday = iso === TODAY_ISO ? ' is-today' : '';
    const dayLesson = ls ? ls.find(l => l.type !== 'buffer') : null;
    const dayCls = dayLesson ? ' has-day' : '';
    html += `<div class="cal-cell${isToday}${isWeekend}${dayCls}" data-date="${iso}">
      <span class="datenum">${day}</span>
      ${ls ? ls.flatMap(chipsForLesson).join('') : ''}
    </div>`;
  }
  grid.innerHTML = html;

  grid.querySelectorAll('.chip').forEach(chip => {
    if(chip.getAttribute('data-kind') === 'buffer') return;
    chip.addEventListener('click', e => {
      e.stopPropagation();
      const kind = chip.getAttribute('data-kind');
      const key = chip.getAttribute('data-key');
      if(e.target.getAttribute('data-action') === 'toggle'){
        toggleComplete(kind, key);
      } else {
        selectItem(kind, key);
      }
    });
  });

  grid.querySelectorAll('.cal-cell.has-day').forEach(cell => {
    cell.addEventListener('click', () => {
      const iso = cell.getAttribute('data-date');
      const lesson = (byDate[iso] || []).find(l => l.type !== 'buffer');
      if(!lesson) return;
      selectItem(lesson.type, keyOf(lesson));
    });
  });
}

function renderCalHead(){
  const dows = ['Mon','Tue','Wed','Thu','Fri','Sat','Sun'];
  document.getElementById('calGridHead').innerHTML = dows.map(d => `<div class="dow">${d}</div>`).join('');
}

/* ---------- Sidebar detail ---------- */
function resolveLesson(kind, key){
  if(kind === 'ia' || kind === 'assessment') return LESSONS.find(l => l.type === kind && l.date === key);
  if(kind === 'content') return buildCodeIndex()[key];
  return null;
}

function toggleComplete(kind, key){
  const lesson = resolveLesson(kind, key);
  if(!lesson) return;
  lesson.completed = !lesson.completed;
  renderMonth(); renderAgenda(document.getElementById('searchBox').value);
  if(selected && isSelected(lesson)) renderEventCard(selected.kind, selected.key);
  scheduleSave();
}

function saveContentItemLink(code, itemCode, field, value){
  const lesson = buildCodeIndex()[code];
  if(!lesson) return;
  const item = lesson.items.find(i => i.code === itemCode);
  if(!item) return;
  item[field] = value.trim();
  renderMonth(); renderAgenda(document.getElementById('searchBox').value);
  scheduleSave();
  showToast('Saved');
}

function saveLessonLink(kind, key, field, value){
  const lesson = resolveLesson(kind, key);
  if(!lesson) return;
  lesson[field] = value.trim();
  renderMonth(); renderAgenda(document.getElementById('searchBox').value);
  scheduleSave();
  showToast('Saved');
}

function fileFieldHtml(icon, label, field, url, saveAttrs){
  const has = !!url;
  const tag = has ? 'a' : 'span';
  const openAttrs = has ? `href="${escapeHtml(url)}" target="_blank" rel="noopener"` : '';
  return `
    <div class="filefield">
      <div class="filerow">
        <${tag} class="filebtn ${has ? 'has-link' : 'empty'}" ${openAttrs} title="${has ? 'Open ' + label : label + ' not added yet'}">
          <span class="ico">${icon}</span><span class="lbl">${label}</span>
        </${tag}>
        <button class="editbtn" data-action="toggle-edit" title="${has ? 'Change' : 'Add'} ${label} link" aria-label="${has ? 'Change' : 'Add'} ${label} link">${has ? ICON_PENCIL : ICON_PLUS}</button>
      </div>
      <div class="link-editor" hidden>
        <input type="text" data-field="${field}" placeholder="Paste ${label} link&hellip;" value="${escapeHtml(url || '')}">
        <button class="iconbtn2 save" ${saveAttrs} data-field="${field}" title="Save" aria-label="Save ${label} link">${ICON_SAVE}</button>
        <button class="iconbtn2 cancel" data-action="cancel-edit" title="Cancel" aria-label="Cancel">${ICON_CLOSE}</button>
      </div>
    </div>`;
}

function itemLinkFieldsHtml(code, item){
  const rows = [['slidesUrl','Slides', ICON_SLIDES], ['exitTicketUrl','Exit ticket', ICON_TICKET]];
  return rows.map(([field, label, icon]) =>
    fileFieldHtml(icon, label, field, item[field], `data-itemcode="${item.code}" data-savefield="${field}"`)
  ).join('');
}

function lessonLinkFieldsHtml(kind, key, lesson, labels){
  const rows = [['slidesUrl', labels[0], ICON_SLIDES], ['exitTicketUrl', labels[1], ICON_TICKET]];
  return rows.map(([field, label, icon]) =>
    fileFieldHtml(icon, label, field, lesson[field], `data-lessonfield="${field}"`)
  ).join('');
}

function renderEventCard(kind, key){
  const display = computeDisplaySchedule();
  const lesson = kind === 'content'
    ? display.find(l => l.type === 'content' && l.items.some(i => i.code === key))
    : display.find(l => l.type === kind && l.date === key);
  if(!lesson) return;

  document.getElementById('detailEmpty').style.display = 'none';
  const body = document.getElementById('detailBody');
  body.style.display = 'block';
  const d = parseISO(lesson.date);
  const dateStr = fmtDate(d) + ' &middot; ' + lesson.day + ' &middot; ' + lesson.period + ' (' + lesson.time + ')';

  if(lesson.type === 'content'){
    document.getElementById('detailHead').textContent = lesson.items.length > 1 ? 'Lesson (' + lesson.items.length + ' topics)' : 'Lesson';
    let itemsHtml = lesson.items.map((it, idx) => {
      const full = CATALOG_BY_CODE[it.code] || {};
      const th = themeOf(it.code);
      return `<div class="item-block">
        <div class="code" style="color:var(--theme-${th})">${it.code}</div>
        <h3>${it.text}</h3>
        <p class="meta">${full.subtopic_title||''}</p>
        <p class="detail-text">${full.detail||''}</p>
        <div class="badges">${it.level==='hl' ? '<span class="badge hl">HL only</span>' : '<span class="badge">Core</span>'}</div>
        ${itemLinkFieldsHtml(key, it)}
      </div>`;
    }).join('');
    body.innerHTML = `
      <p class="meta" style="margin-bottom:10px;">${dateStr}</p>
      <div class="complete-row" id="completeRow">
        <div class="big-check ${lesson.completed?'done':''}" id="bigCheck"></div>
        <span id="completeLabel">${lesson.completed ? 'Marked complete' : 'Mark lesson complete'}</span>
      </div>
      ${itemsHtml}
    `;
  } else if(lesson.type === 'assessment'){
    document.getElementById('detailHead').textContent = 'Assessment';
    const list = (lesson.assessedCodes||[]).map(code => {
      const full = CATALOG_BY_CODE[code] || {};
      return `<li><span class="mono">${code}</span> ${full.text||''}</li>`;
    }).join('');
    body.innerHTML = `
      <div class="code" style="color:var(--assessment)">Assessment</div>
      <h3>Content check</h3>
      <p class="meta">${dateStr}</p>
      <p class="detail-text">Covers everything taught since the last assessment:</p>
      <ul class="assessed-list">${list || '<li>No new content since the last assessment</li>'}</ul>
      <div class="badges"><span class="badge assessment">Assessment</span></div>
      <div class="complete-row" id="completeRow">
        <div class="big-check ${lesson.completed?'done':''}" id="bigCheck"></div>
        <span id="completeLabel">${lesson.completed ? 'Marked complete' : 'Mark assessment complete'}</span>
      </div>
      ${lessonLinkFieldsHtml('assessment', key, lesson, ['Assessment','Mark scheme'])}
    `;
  } else {
    document.getElementById('detailHead').textContent = 'Internal Assessment';
    body.innerHTML = `
      <div class="code" style="color:var(--ia)">Internal Assessment</div>
      <h3>IA introduction &amp; work session</h3>
      <p class="meta">${dateStr}</p>
      <p class="detail-text">Early introduction to "The Computational Solution" &ndash; requirements briefing, topic selection, tool/tech scoping, and initial planning ahead of the IA proper in DP2.</p>
      <div class="badges"><span class="badge ia">IA</span></div>
      <div class="complete-row" id="completeRow">
        <div class="big-check ${lesson.completed?'done':''}" id="bigCheck"></div>
        <span id="completeLabel">${lesson.completed ? 'Marked complete' : 'Mark lesson complete'}</span>
      </div>
      ${lessonLinkFieldsHtml('ia', key, lesson, ['Slides','Exit ticket'])}
    `;
  }

  document.getElementById('completeRow').addEventListener('click', () => toggleComplete(kind, key));
  body.querySelectorAll('[data-action="toggle-edit"]').forEach(btn => {
    btn.addEventListener('click', () => {
      const field = btn.closest('.filefield').querySelector('.link-editor');
      field.hidden = !field.hidden;
      if(!field.hidden) field.querySelector('input').focus();
    });
  });
  body.querySelectorAll('[data-action="cancel-edit"]').forEach(btn => {
    btn.addEventListener('click', () => { btn.closest('.link-editor').hidden = true; });
  });
  body.querySelectorAll('[data-savefield]').forEach(btn => {
    btn.addEventListener('click', () => {
      const row = btn.closest('.filefield');
      const input = row.querySelector('input');
      saveContentItemLink(key, btn.getAttribute('data-itemcode'), btn.getAttribute('data-savefield'), input.value);
      renderEventCard(kind, key);
    });
  });
  body.querySelectorAll('[data-lessonfield]').forEach(btn => {
    btn.addEventListener('click', () => {
      const row = btn.closest('.filefield');
      const input = row.querySelector('input');
      saveLessonLink(kind, key, btn.getAttribute('data-lessonfield'), input.value);
      renderEventCard(kind, key);
    });
  });
  body.querySelectorAll('.link-editor input').forEach(inp => {
    inp.addEventListener('keydown', e => { if(e.key === 'Enter') inp.closest('.link-editor').querySelector('.save').click(); });
  });
}

function selectItem(kind, key){
  if(kind === 'buffer' || !key) return;
  selected = {kind, key};
  renderMonth();
  renderEventCard(kind, key);
}

/* ---------- Agenda ---------- */
function renderAgenda(filter){
  const display = computeDisplaySchedule();
  const body = document.getElementById('agendaBody');
  const f = (filter || '').trim().toLowerCase();
  let rows = display.map(l => {
    const d = parseISO(l.date);
    const code = l.type === 'content' ? l.items.map(i=>i.code).join(' + ') : (l.type === 'ia' ? 'IA' : l.type === 'assessment' ? 'Test' : '—');
    const focus = l.type === 'content' ? l.items.map(i=>i.text).join(' + ')
                : l.type === 'ia' ? 'IA introduction & work session'
                : l.type === 'assessment' ? 'Assessment'
                : 'Review / catch-up';
    const searchable = (l.date + ' ' + l.day + ' ' + code + ' ' + focus).toLowerCase();
    return {l, d, code, focus, searchable, key: keyOf(l)};
  });
  if(f) rows = rows.filter(r => r.searchable.includes(f));
  body.innerHTML = rows.map(r => {
    const hasLink = r.l.type === 'content' ? r.l.items.some(i=>i.slidesUrl||i.exitTicketUrl) : (r.l.slidesUrl || r.l.exitTicketUrl);
    let links = '';
    if(r.l.type === 'content'){
      links = r.l.items.filter(i=>i.slidesUrl||i.exitTicketUrl).map(i => `${i.code}: ${i.slidesUrl?`<a href="${escapeHtml(i.slidesUrl)}" target="_blank" rel="noopener">Slides</a>`:''}${i.exitTicketUrl?` <a href="${escapeHtml(i.exitTicketUrl)}" target="_blank" rel="noopener">Exit</a>`:''}`).join('; ');
    } else if(hasLink){
      links = [r.l.slidesUrl?`<a href="${escapeHtml(r.l.slidesUrl)}" target="_blank" rel="noopener">Link 1</a>`:'', r.l.exitTicketUrl?`<a href="${escapeHtml(r.l.exitTicketUrl)}" target="_blank" rel="noopener">Link 2</a>`:''].filter(Boolean).join(' &middot; ');
    }
    const clickable = r.l.type !== 'buffer';
    return `
    <tr class="type-${r.l.type}${r.l.completed ? ' done' : ''}" data-kind="${r.l.type}" data-key="${r.key||''}" data-date="${r.l.date}">
      <td class="check-td">${clickable ? `<span class="mini-check${r.l.completed?' done':''}" data-action="toggle" data-kind="${r.l.type}" data-key="${r.key}"></span>` : ''}</td>
      <td class="code">${fmtDate(r.d)}</td>
      <td>${r.l.day}</td>
      <td class="code">${r.l.period}</td>
      <td class="code">${r.code}</td>
      <td class="focuscell">${r.focus}</td>
      <td style="font-size:11.5px;">${links || '<span style=\"color:var(--ink-3)\">—</span>'}</td>
    </tr>`;
  }).join('');

  body.querySelectorAll('.mini-check').forEach(el => {
    el.addEventListener('click', e => { e.stopPropagation(); toggleComplete(el.getAttribute('data-kind'), el.getAttribute('data-key')); });
  });
  body.querySelectorAll('tr').forEach(tr => {
    const kind = tr.getAttribute('data-kind');
    if(kind === 'buffer') return;
    tr.addEventListener('click', () => {
      const key = tr.getAttribute('data-key'), iso = tr.getAttribute('data-date');
      goToMonthOf(iso); selectItem(kind, key);
      document.getElementById('detailCard').scrollIntoView({behavior:'smooth', block:'center'});
    });
  });
}

function goToMonthOf(iso){
  const mk = monthKey(parseISO(iso));
  const idx = MONTHS.indexOf(mk);
  if(idx >= 0){ monthIdx = idx; renderMonth(); }
}

document.getElementById('prevBtn').addEventListener('click', () => { if(monthIdx>0){ monthIdx--; renderMonth(); }});
document.getElementById('nextBtn').addEventListener('click', () => { if(monthIdx<MONTHS.length-1){ monthIdx++; renderMonth(); }});
document.getElementById('todayBtn').addEventListener('click', () => { goToMonthOf(LESSONS.some(l => l.date === TODAY_ISO) ? TODAY_ISO : LESSONS[0].date); });
document.getElementById('searchBox').addEventListener('input', e => renderAgenda(e.target.value));

/* ---------- Collapsible lower sections ---------- */
document.querySelectorAll('.section-toggle').forEach(t => {
  t.addEventListener('click', () => {
    const target = document.getElementById(t.getAttribute('data-target'));
    const open = target.classList.toggle('open');
    t.classList.toggle('open', open);
  });
});

function showToast(msg){
  const t = document.getElementById('toast');
  t.textContent = msg;
  t.classList.add('show');
  clearTimeout(t._h);
  t._h = setTimeout(() => t.classList.remove('show'), 2600);
}

/* ---------- Persistence ---------- */
function scheduleSave(){
  clearTimeout(saveTimer);
  saveTimer = setTimeout(saveState, 900);
}
async function saveState(){
  let artifact;
  try{ artifact = await claude.use('artifact'); }catch(e){ artifact = null; }
  if(!artifact) return;
  let src = '<!doctype html>\n' + document.documentElement.outerHTML;
  const replaced = src.replace(/let LESSONS = \[[\s\S]*?\];\nconst CATALOG/, 'let LESSONS = ' + JSON.stringify(LESSONS) + ';\nconst CATALOG');
  if(replaced === src){ return; }
  try{
    await artifact.publish(replaced);
  }catch(err){
    if(err && err.code === 'conflict'){
      showToast('This page changed elsewhere — reload to see the latest before editing again.');
    }
  }
}

/* ---------- Export ---------- */
function toCSV(){
  const header = ['Date','Day','Period','Time','Type','Codes','Focus','Notes','Completed','SlidesUrls','ExitTicketUrls'];
  const rows = [header.join(',')];
  computeDisplaySchedule().forEach(l => {
    let codes='', focus='', slides='', exit='';
    if(l.type === 'content'){
      codes = l.items.map(i=>i.code).join(' | ');
      focus = l.items.map(i=>i.code+' '+i.text).join(' | ');
      slides = l.items.map(i=>i.slidesUrl||'').join(' | ');
      exit = l.items.map(i=>i.exitTicketUrl||'').join(' | ');
    } else if(l.type === 'ia'){
      focus = 'Internal Assessment introduction & work session'; slides=l.slidesUrl||''; exit=l.exitTicketUrl||'';
    } else if(l.type === 'assessment'){
      codes = (l.assessedCodes||[]).join(' | ');
      focus = 'Assessment covering: ' + (l.assessedCodes||[]).join(', '); slides=l.slidesUrl||''; exit=l.exitTicketUrl||'';
    } else {
      focus = 'Review / catch-up';
    }
    const notes = l.type === 'ia' ? 'IA work session' : l.type === 'assessment' ? 'Assessment' : l.type === 'buffer' ? 'No new content scheduled' : '';
    const cells = [l.date, l.day, l.period, l.time, l.type, codes, focus, notes, l.completed?'TRUE':'FALSE', slides, exit].map(c => {
      c = String(c).replace(/"/g,'""');
      return /[",\n]/.test(c) ? `"${c}"` : c;
    });
    rows.push(cells.join(','));
  });
  return rows.join('\n');
}
async function exportCSV(){
  const csv = toCSV();
  const filename = 'dp1-hl-cs-calendar.csv';
  try{
    const downloads = await claude.use('downloads');
    if(downloads){
      await downloads.save({filename, data: new Blob([csv], {type:'text/csv'})});
      showToast('Calendar exported as ' + filename);
      return;
    }
  }catch(err){
    if(err && err.code === 'declined'){ return; }
  }
  try{
    const blob = new Blob([csv], {type:'text/csv'});
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url; a.download = filename;
    document.body.appendChild(a); a.click(); document.body.removeChild(a);
    URL.revokeObjectURL(url);
    showToast('Calendar exported as ' + filename);
  }catch(err){
    showToast('Could not export - try again');
  }
}
document.getElementById('exportBtn').addEventListener('click', exportCSV);

/* ---------- Import ---------- */
document.getElementById('unlockBtn').addEventListener('click', () => {
  document.getElementById('passwordRow').classList.add('show');
  document.getElementById('pwInput').focus();
});
document.getElementById('pwSubmit').addEventListener('click', checkPassword);
document.getElementById('pwInput').addEventListener('keydown', e => { if(e.key === 'Enter') checkPassword(); });
function checkPassword(){
  const val = document.getElementById('pwInput').value;
  if(val === IMPORT_PASSWORD){
    document.getElementById('passwordRow').classList.remove('show');
    document.getElementById('importArea').classList.add('show');
    document.getElementById('pwError').textContent = '';
    document.getElementById('lockedNote').textContent = 'Unlocked for this session.';
  } else {
    document.getElementById('pwError').textContent = 'Wrong password.';
  }
}

function truthy(v){ return /^(true|yes|1|y)$/i.test(String(v||'').trim()); }

function rowsToLessons(rows){
  const out = [];
  rows.forEach(row => {
    const rawDate = row.Date || row.date;
    if(!rawDate) return;
    let iso;
    const s = String(rawDate).trim();
    if(/^\d{4}-\d{2}-\d{2}/.test(s)) iso = s.slice(0,10);
    else if(/^\d{1,2}\/\d{1,2}\/\d{4}/.test(s)){
      const [d,m,y] = s.split('/').map(Number);
      iso = `${y}-${String(m).padStart(2,'0')}-${String(d).padStart(2,'0')}`;
    } else {
      const d = new Date(s);
      if(isNaN(d)) return;
      iso = d.toISOString().slice(0,10);
    }
    const d = parseISO(iso);
    const day = d.toLocaleDateString('en-GB', {weekday:'long'});
    const period = (row.Period || row.period || 'P1').toString().trim();
    const time = row.Time || row.time || PERIOD_TIMES[period] || '';
    let type = (row.Type || '').toLowerCase().trim();
    const codes = String(row.Codes || row.Code || '').split('|').map(c=>c.trim()).filter(Boolean);
    if(!type) type = codes.length ? 'content' : 'buffer';
    let items = [], slidesUrl = '', exitTicketUrl = '';
    if(type === 'content'){
      const slidesList = String(row.SlidesUrls||'').split('|').map(s=>s.trim());
      const exitList = String(row.ExitTicketUrls||'').split('|').map(s=>s.trim());
      items = codes.map((code,i) => {
        const cat = CATALOG_BY_CODE[code];
        return {code, text: cat?cat.text:'', level: cat?cat.level:'core', topic: code.split('.')[0],
          slidesUrl: slidesList[i]||'', exitTicketUrl: exitList[i]||''};
      });
    } else if(type === 'ia' || type === 'assessment'){
      slidesUrl = String(row.SlidesUrls||'').split('|')[0] || '';
      exitTicketUrl = String(row.ExitTicketUrls||'').split('|')[0] || '';
    }
    const lesson = { date: iso, day, period, time, type, items, completed: truthy(row.Completed), slidesUrl, exitTicketUrl };
    if(type === 'assessment') lesson.assessedCodes = codes;
    out.push(lesson);
  });
  out.sort((a,b) => a.date.localeCompare(b.date) || a.period.localeCompare(b.period));
  return out;
}

function applyImportedRows(rows, filename){
  const newLessons = rowsToLessons(rows);
  if(!newLessons.length){
    document.getElementById('importMsg').textContent = 'No valid rows found - check the Date column.';
    return;
  }
  LESSONS = newLessons;
  MONTHS = monthList(LESSONS);
  monthIdx = 0;
  selected = null;
  document.getElementById('detailEmpty').style.display = 'block';
  document.getElementById('detailBody').style.display = 'none';
  renderMonth(); renderAgenda('');
  document.getElementById('importMsg').textContent = `Loaded ${newLessons.length} lessons from ${filename}.`;
  showToast('Calendar updated from ' + filename);
  scheduleSave();
}

function parseCSVText(text){
  const lines = text.split(/\r?\n/).filter(l => l.length);
  if(!lines.length) return [];
  const splitLine = line => {
    const cells = []; let cur=''; let inQ=false;
    for(let i=0;i<line.length;i++){
      const ch = line[i];
      if(inQ){
        if(ch === '"' && line[i+1] === '"'){ cur+='"'; i++; }
        else if(ch === '"'){ inQ=false; }
        else cur += ch;
      } else {
        if(ch === '"') inQ = true;
        else if(ch === ','){ cells.push(cur); cur=''; }
        else cur += ch;
      }
    }
    cells.push(cur);
    return cells;
  };
  const header = splitLine(lines[0]).map(h => h.trim());
  return lines.slice(1).map(line => {
    const cells = splitLine(line);
    const row = {};
    header.forEach((h,i) => row[h] = cells[i] !== undefined ? cells[i] : '');
    return row;
  });
}

document.getElementById('fileInput').addEventListener('change', async e => {
  const file = e.target.files[0];
  if(!file) return;
  const msg = document.getElementById('importMsg');
  msg.textContent = 'Reading ' + file.name + '…';
  try{
    if(/\.xlsx$/i.test(file.name)){
      if(typeof XLSX === 'undefined'){
        msg.textContent = 'Excel import is unavailable right now - please save as CSV and import that instead.';
        return;
      }
      const buf = await file.arrayBuffer();
      const wb = XLSX.read(buf, {type:'array'});
      const sheet = wb.Sheets[wb.SheetNames[0]];
      const rows = XLSX.utils.sheet_to_json(sheet, {defval:''});
      applyImportedRows(rows, file.name);
    } else {
      const text = await file.text();
      const rows = parseCSVText(text);
      applyImportedRows(rows, file.name);
    }
  }catch(err){
    msg.textContent = 'Could not read that file: ' + err.message;
  }
});

/* ---------- Syllabus reference ---------- */
function renderSyllabus(){
  const byTopic = {};
  CATALOG.forEach(it => {
    byTopic[it.topic_code] = byTopic[it.topic_code] || {title: it.topic_title, subs: {}};
    byTopic[it.topic_code].subs[it.subtopic_code] = byTopic[it.topic_code].subs[it.subtopic_code] || {title: it.subtopic_title, items: []};
    byTopic[it.topic_code].subs[it.subtopic_code].items.push(it);
  });
  const order = ['A1','A2','A3','A4','B1','B2','B3','B4'];
  let html = '';
  order.forEach(code => {
    const t = byTopic[code];
    if(!t) return;
    const nItems = Object.values(t.subs).reduce((a,s)=>a+s.items.length,0);
    html += `<details class="syllabus-topic"><summary>${code} &ndash; ${t.title} <span class="hrs">(${nItems} items)</span></summary>`;
    Object.entries(t.subs).forEach(([sc, s]) => {
      html += `<div class="syllabus-sub"><div class="st-title">${sc} ${s.title}</div>`;
      s.items.forEach(it => {
        const covered = it.done_already ? ' covered' : '';
        const hl = it.level === 'hl' ? '<span style="font-size:9px;background:var(--accent);color:#fff;border-radius:3px;padding:0 4px;margin-left:3px;">HL</span>' : '';
        html += `<div class="syllabus-item${covered}"><span class="code">${it.code}</span><span>${it.text}${hl}${it.done_already ? ' &mdash; already covered' : ''}</span></div>`;
      });
      html += `</div>`;
    });
    html += `</details>`;
  });
  document.getElementById('syllabusRef').innerHTML = html;
}

/* ---------- Exam countdown ---------- */
const EXAM_DATE = new Date(2028, 3, 25, 0, 0, 0); // 25 April 2028, first assessment
function renderCountdown(){
  let diff = EXAM_DATE.getTime() - Date.now();
  if(diff < 0) diff = 0;
  const totalSec = Math.floor(diff / 1000);
  const days = Math.floor(totalSec / 86400);
  const hours = Math.floor((totalSec % 86400) / 3600);
  const mins = Math.floor((totalSec % 3600) / 60);
  const secs = totalSec % 60;
  const set = (id, val) => { const el = document.getElementById(id); if(el) el.textContent = val; };
  set('cdDays', days);
  set('cdHours', String(hours).padStart(2,'0'));
  set('cdMins', String(mins).padStart(2,'0'));
  set('cdSecs', String(secs).padStart(2,'0'));
}

/* ---------- init ---------- */
renderCalHead();
renderMonth();
renderAgenda('');
renderSyllabus();
goToMonthOf(LESSONS.some(l => l.date === TODAY_ISO) ? TODAY_ISO : LESSONS[0].date);
renderCountdown();
setInterval(renderCountdown, 1000);
</script>
</body>
</html>
"""

html = html.replace("{}", "&lt;/&gt;", 1)
html = html.replace("__LESSONS_JSON__", LESSONS_JSON).replace("__CATALOG_JSON__", CATALOG_JSON)

with open('/home/claude/g11_planner_v2/g11_calendar.html', 'w') as f:
    f.write(html)

print('written, bytes:', len(html))
