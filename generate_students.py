#!/usr/bin/env python3
"""
Generate students.html from assets/data/students.csv

Usage:
    python3 generate_students.py

Edit students.csv to add/remove/update students, then re-run this script.
The CSV columns are:
  id, name, degree, programme, status, role, research_title, research_focus,
  funding, cosupervisors, project_page, linkedin, scholar, email

- status: "current" or "alumni"
- role: "Main Supervisor" or "Co-Supervisor"
- project_page: filename like "project-deepspray.html" (leave empty if none)
- cosupervisors: semicolon-separated list
"""

import csv
import os
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
CSV_PATH = SCRIPT_DIR / "assets" / "data" / "students.csv"
OUTPUT_PATH = SCRIPT_DIR / "students.html"

# Project page -> short display name mapping
PROJECT_NAMES = {
    "project-deepspray.html": "Deep Spray+",
    "project-ted2.html": "Cloud-based Radiation Dosimetry",
    "project-bridging-cyber.html": "Bridging the Cyber Skills Gap",
    "project-best.html": "BEST",
    "project-impactxchange.html": "ImpactXChange",
    "project-susthack.html": "SustHack",
}


def read_students(csv_path):
    students = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # strip whitespace from all fields
            row = {k: (v.strip() if v else "") for k, v in row.items()}
            students.append(row)
    return students


def render_card(s):
    role_class = "role-main" if "Main" in s["role"] else "role-co"
    degree_label = f'{s["degree"]} in {s["programme"]}' if s["programme"] else s["degree"]

    lines = []
    lines.append(f'      <div class="student-card" id="{s["id"]}">')
    lines.append(f'        <div class="student-card-header">')
    if s.get("photo"):
        lines.append(
            f'          <img class="student-photo" src="{s["photo"]}" alt="{s["name"]}" loading="lazy" />'
        )
    else:
        lines.append(
            f'          <div class="student-photo-placeholder"><i class="fa-solid fa-user"></i></div>'
        )
    lines.append(f'          <div>')
    lines.append(f'            <div class="student-name">{s["name"]}</div>')
    lines.append(
        f'            <div class="student-role"><span class="{role_class}">{s["role"]}</span> &middot; {degree_label}</div>'
    )
    lines.append(f"          </div>")
    lines.append(f"        </div>")

    if s.get("position"):
        lines.append(
            f'        <div class="student-position"><i class="fa-solid fa-briefcase"></i> {s["position"]}</div>'
        )

    if s.get("research_title"):
        lines.append(
            f'        <div class="student-research">{s["research_title"]}</div>'
        )

    if s.get("research_focus"):
        lines.append(f'        <div class="student-focus">{s["research_focus"]}</div>')

    # Meta tags (funding + project)
    meta_parts = []
    if s.get("funding"):
        meta_parts.append(
            f'          <span class="student-meta-tag meta-funding"><i class="fa-solid fa-coins"></i> {s["funding"]}</span>'
        )
    if s.get("project_page"):
        proj_name = PROJECT_NAMES.get(s["project_page"], s["project_page"])
        meta_parts.append(
            f'          <a href="{s["project_page"]}" class="student-meta-tag meta-project"><i class="fa-solid fa-diagram-project"></i> {proj_name}</a>'
        )
    if meta_parts:
        lines.append(f'        <div class="student-meta">')
        lines.extend(meta_parts)
        lines.append(f"        </div>")

    # Co-supervisors
    if s.get("cosupervisors"):
        cosups = s["cosupervisors"].replace(";", ",")
        label = "Main supervisor" if "Co" in s["role"] else "Co-supervisors"
        if cosups.startswith("Main:"):
            label = "Main supervisor"
            cosups = cosups.replace("Main:", "").strip()
        lines.append(
            f'        <div class="student-cosupervisors"><strong>{label}:</strong> {cosups}</div>'
        )

    # External links
    link_parts = []
    if s.get("scholar"):
        link_parts.append(
            f'          <a href="{s["scholar"]}" target="_blank" rel="noopener"><i class="fa-solid fa-graduation-cap"></i> Google Scholar</a>'
        )
    if s.get("linkedin"):
        link_parts.append(
            f'          <a href="{s["linkedin"]}" target="_blank" rel="noopener"><i class="fa-brands fa-linkedin"></i> LinkedIn</a>'
        )
    if link_parts:
        lines.append(f'        <div class="student-links">')
        lines.extend(link_parts)
        lines.append(f"        </div>")

    lines.append(f"      </div>")
    return "\n".join(lines)


def generate_html(students):
    current = [s for s in students if s["status"] == "current"]
    alumni = [s for s in students if s["status"] == "alumni"]

    phd_current = [s for s in current if s["degree"] == "PhD"]
    msc_current = [s for s in current if s["degree"] == "MSc"]
    phd_alumni = [s for s in alumni if s["degree"] == "PhD"]
    msc_alumni = [s for s in alumni if s["degree"] == "MSc"]

    total_current = len(current)
    total_alumni = len(alumni)

    phd_cards = "\n\n".join(render_card(s) for s in phd_current)
    msc_cards = "\n\n".join(render_card(s) for s in msc_current)

    alumni_section = ""
    if alumni:
        alumni_cards = "\n\n".join(render_card(s) for s in alumni)
        alumni_section = f"""
    <section class="students-section" id="alumni">
      <h2 class="students-section-title"><i class="fa-solid fa-award" style="color:var(--warm);"></i> Alumni</h2>

{alumni_cards}
    </section>"""

    # Stats
    stats_items = []
    if phd_current:
        stats_items.append(
            f'        <div class="students-stat"><div class="students-stat-number">{len(phd_current)}</div><div class="students-stat-label">PhD</div></div>'
        )
    if msc_current:
        stats_items.append(
            f'        <div class="students-stat"><div class="students-stat-number">{len(msc_current)}</div><div class="students-stat-label">Master</div></div>'
        )
    stats_items.append(
        f'        <div class="students-stat"><div class="students-stat-number">{total_current}</div><div class="students-stat-label">Total Current</div></div>'
    )
    if alumni:
        stats_items.append(
            f'        <div class="students-stat"><div class="students-stat-number">{total_alumni}</div><div class="students-stat-label">Alumni</div></div>'
        )
    stats_html = "\n".join(stats_items)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Students &amp; Alumni &mdash; Sian Lun Lau</title>
  <meta name="description" content="Current and former research students supervised by Prof. Ts. Dr.-Ing. Sian Lun Lau at Sunway University." />
  <meta name="author" content="Sian Lun Lau" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css" />
  <link rel="icon" type="image/png" sizes="32x32" href="assets/img/favicon-32.png" />
  <link rel="icon" type="image/png" sizes="16x16" href="assets/img/favicon-16.png" />
  <link rel="apple-touch-icon" sizes="180x180" href="assets/img/apple-touch-icon.png" />
  <link rel="stylesheet" href="assets/css/style.css" />
  <style>
    .students-header {{ padding: 7rem 0 2rem; text-align: center; }}
    .students-header .back-link {{
      display: inline-flex; align-items: center; gap: 0.4rem;
      color: var(--accent); font-size: 0.88rem; font-weight: 500;
      text-decoration: none; margin-bottom: 1.5rem;
    }}
    .students-header .back-link:hover {{ text-decoration: underline; }}
    .students-header h1 {{ font-size: 2.2rem; font-weight: 800; letter-spacing: -0.03em; margin-bottom: 0.5rem; }}
    .students-header p {{ color: var(--text-secondary); font-size: 1rem; max-width: 650px; margin: 0 auto; }}
    .students-stats {{ display: flex; gap: 1.5rem; justify-content: center; margin-top: 1.5rem; flex-wrap: wrap; }}
    .students-stat {{ background: var(--bg-card); border: 1px solid var(--border-color); border-radius: 10px; padding: 0.75rem 1.25rem; text-align: center; min-width: 100px; }}
    .students-stat-number {{ font-family: 'JetBrains Mono', monospace; font-size: 1.5rem; font-weight: 700; color: var(--accent); }}
    .students-stat-label {{ font-size: 0.75rem; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.05em; }}
    .students-section {{ padding: 2rem 0; }}
    .students-section-title {{ font-size: 1.4rem; font-weight: 700; margin-bottom: 1.5rem; padding-bottom: 0.5rem; border-bottom: 2px solid var(--accent-soft-border); display: flex; align-items: center; gap: 0.5rem; }}
    .students-section-title .degree-badge {{ font-size: 0.7rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.06em; padding: 0.25rem 0.6rem; border-radius: 6px; }}
    .degree-phd {{ background: var(--accent-soft); color: var(--accent); border: 1px solid var(--accent-soft-border); }}
    .degree-msc {{ background: var(--warm-soft); color: var(--warm); border: 1px solid var(--warm-border); }}
    .student-card {{ background: var(--bg-card); border: 1px solid var(--border-color); border-radius: 12px; padding: 1.5rem; margin-bottom: 1rem; transition: box-shadow 0.3s, border-color 0.3s; }}
    .student-card:hover {{ box-shadow: var(--card-shadow-hover); border-color: var(--accent-soft-border); }}
    .student-card-header {{ display: flex; align-items: flex-start; gap: 1rem; flex-wrap: wrap; }}
    .student-photo {{ width: 56px; height: 56px; border-radius: 50%; object-fit: cover; flex-shrink: 0; border: 2px solid var(--border-color); }}
    .student-photo-placeholder {{ width: 56px; height: 56px; border-radius: 50%; flex-shrink: 0; background: var(--bg-secondary); border: 2px solid var(--border-color); display: flex; align-items: center; justify-content: center; color: var(--text-muted); font-size: 1.2rem; }}
    .student-name {{ font-size: 1.1rem; font-weight: 700; margin-bottom: 0.15rem; }}
    .student-role {{ font-size: 0.78rem; color: var(--text-muted); font-weight: 500; }}
    .student-role .role-main {{ color: var(--accent); }}
    .student-role .role-co {{ color: var(--warm); }}
    .student-position {{ font-size: 0.82rem; color: var(--text-secondary); margin-top: 0.5rem; display: flex; align-items: center; gap: 0.4rem; }}
    .student-position i {{ color: var(--accent); font-size: 0.75rem; }}
    .student-research {{ font-size: 0.88rem; font-weight: 600; color: var(--text-primary); margin-top: 0.75rem; line-height: 1.5; }}
    .student-focus {{ font-size: 0.85rem; color: var(--text-secondary); line-height: 1.7; margin-top: 0.5rem; }}
    .student-meta {{ display: flex; flex-wrap: wrap; gap: 0.5rem; margin-top: 0.75rem; }}
    .student-meta-tag {{ font-size: 0.75rem; padding: 0.3rem 0.7rem; border-radius: 6px; display: inline-flex; align-items: center; gap: 0.3rem; }}
    .meta-funding {{ background: var(--bg-secondary); color: var(--text-secondary); border: 1px solid var(--border-subtle); }}
    .meta-project {{ background: var(--accent-soft); color: var(--accent); border: 1px solid var(--accent-soft-border); text-decoration: none; font-weight: 500; }}
    .meta-project:hover {{ text-decoration: underline; }}
    .student-cosupervisors {{ font-size: 0.8rem; color: var(--text-muted); margin-top: 0.5rem; }}
    .student-links {{ display: flex; gap: 0.75rem; margin-top: 0.75rem; }}
    .student-links a {{ font-size: 0.82rem; color: var(--accent); font-weight: 500; display: inline-flex; align-items: center; gap: 0.3rem; }}
    .student-links a:hover {{ text-decoration: underline; }}
    .students-note {{ text-align: center; padding: 2rem 0 1rem; color: var(--text-muted); font-size: 0.82rem; }}
    @media (max-width: 640px) {{ .student-card {{ padding: 1.15rem; }} .student-card-header {{ flex-direction: column; }} }}
  </style>
</head>
<body>
  <div id="progress-bar"></div>
  <nav class="navbar" id="navbar">
    <a href="index.html" class="navbar-brand">Sian Lun Lau</a>
    <ul class="navbar-nav">
      <li><a href="index.html#about">About</a></li>
      <li><a href="index.html#research">Research</a></li>
      <li><a href="index.html#publications">Publications</a></li>
      <li><a href="index.html#projects">Projects</a></li>
      <li><a href="index.html#teaching">Teaching</a></li>
      <li><a href="index.html#talks">Professional</a></li>
      <li><a href="index.html#blog">Blog</a></li>
      <li><a href="index.html#contact">Contact</a></li>
    </ul>
    <div class="navbar-controls">
      <button class="theme-toggle" id="theme-toggle" aria-label="Toggle theme">
        <i class="fa-solid fa-moon" id="theme-icon-moon"></i>
        <i class="fa-solid fa-sun" id="theme-icon-sun" style="display:none;"></i>
      </button>
      <button class="hamburger" id="hamburger" aria-label="Menu">
        <span></span><span></span><span></span>
      </button>
    </div>
  </nav>
  <div class="mobile-menu" id="mobile-menu">
    <a href="index.html#about">About</a>
    <a href="index.html#research">Research</a>
    <a href="index.html#publications">Publications</a>
    <a href="index.html#projects">Projects</a>
    <a href="index.html#teaching">Teaching</a>
    <a href="index.html#talks">Professional</a>
    <a href="index.html#blog">Blog</a>
    <a href="index.html#contact">Contact</a>
  </div>

  <main class="container">
    <div class="students-header">
      <a href="index.html#teaching" class="back-link"><i class="fa-solid fa-arrow-left"></i> Back to Teaching</a>
      <h1>Students &amp; Alumni</h1>
      <p>Throughout my academic career, I am blessed with bright students who trusted me by choosing me as their supervisor.</p>
      <div class="students-stats">
{stats_html}
      </div>
    </div>

    <section class="students-section" id="phd">
      <h2 class="students-section-title"><span class="degree-badge degree-phd">PhD</span> Doctoral Researchers</h2>

{phd_cards}
    </section>

    <section class="students-section" id="master">
      <h2 class="students-section-title"><span class="degree-badge degree-msc">Master</span> Master's Researchers</h2>

{msc_cards}
    </section>
{alumni_section}
    <p class="students-note">This page is generated from <code>assets/data/students.csv</code>. Edit the CSV and run <code>python3 generate_students.py</code> to regenerate.</p>
  </main>

  <footer style="text-align:center;padding:2rem 0;color:var(--text-muted);font-size:0.8rem;border-top:1px solid var(--border-color);margin-top:2rem;">
    &copy; 2026 Sian Lun Lau. All rights reserved.
  </footer>

  <script>
    const themeToggle = document.getElementById('theme-toggle');
    const moonIcon = document.getElementById('theme-icon-moon');
    const sunIcon = document.getElementById('theme-icon-sun');
    function setTheme(t) {{
      document.documentElement.setAttribute('data-theme', t);
      localStorage.setItem('theme', t);
      if (t === 'dark') {{ moonIcon.style.display = 'none'; sunIcon.style.display = 'inline'; }}
      else {{ moonIcon.style.display = 'inline'; sunIcon.style.display = 'none'; }}
    }}
    setTheme(localStorage.getItem('theme') || 'light');
    themeToggle.addEventListener('click', () => {{
      setTheme(document.documentElement.getAttribute('data-theme') === 'dark' ? 'light' : 'dark');
    }});
    const hamburger = document.getElementById('hamburger');
    const mobileMenu = document.getElementById('mobile-menu');
    hamburger.addEventListener('click', () => {{ mobileMenu.classList.toggle('open'); }});
    window.addEventListener('scroll', () => {{
      const h = document.documentElement.scrollHeight - window.innerHeight;
      document.getElementById('progress-bar').style.width = (h > 0 ? (window.scrollY / h) * 100 : 0) + '%';
    }});
  </script>
  <script data-goatcounter="https://sianlun.goatcounter.com/count" async src="//gc.zgo.at/count.js"></script>
</body>
</html>"""
    return html


def main():
    students = read_students(CSV_PATH)
    html = generate_html(students)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Generated {OUTPUT_PATH} with {len(students)} students")


if __name__ == "__main__":
    main()
