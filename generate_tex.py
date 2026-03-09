#!/usr/bin/env python3
"""基礎数学B: YAML → 初期 .tex スキャフォールド生成（1回限り）"""

import yaml
import os
import re

YAML_FILE = "topics_basic_math_b.yaml"
OUTPUT_DIR = "lecture"

def escape_tex(s):
    """LaTeX特殊文字の最低限エスケープ。Unicode数学記号はそのまま残す（LuaLaTeX対応）"""
    if not isinstance(s, str):
        s = str(s)
    s = s.replace('%', '\\%')
    s = s.replace('#', '\\#')
    s = s.replace('&', '\\&')
    # _ と ^ はテキストモードでエラーになるので安全な形に
    # ただし既に $...$ の中にある場合はそのままにしたいが、
    # スキャフォールドなので一律テキスト安全な形にする
    s = s.replace('_', '\\_')
    s = s.replace('^', '\\^{}')
    # → は矢印として残す（LuaLaTeXで表示可能）
    return s

def tex_clean(s):
    """数式変換せずそのまま返す（LuaLaTeXがUnicodeを処理）"""
    return escape_tex(s)

def get_next_info(lessons, idx):
    """次回のtopic/pagesを取得"""
    if idx + 1 < len(lessons):
        nxt = lessons[idx + 1]
        return nxt.get('topic', ''), nxt.get('textbook_pages', '')
    return '', ''

def render_slide_terms(terms, indent=2):
    """用語リストを \\description で出力"""
    sp = '  ' * indent
    lines = []
    if not terms:
        lines.append(f"{sp}% TODO: 用語を追加")
        return lines
    lines.append(f"{sp}\\begin{{description}}[labelwidth=5.5em]")
    for t in terms:
        lines.append(f"{sp}  \\item[\\kw{{{escape_tex(t)}}}] ~")
    lines.append(f"{sp}\\end{{description}}")
    return lines

def render_slide_items(items, indent=2):
    """箇条書き"""
    sp = '  ' * indent
    lines = []
    if not items:
        lines.append(f"{sp}\\begin{{itemize}}")
        lines.append(f"{sp}  \\item % TODO: 内容を追加")
        lines.append(f"{sp}\\end{{itemize}}")
        return lines
    lines.append(f"{sp}\\begin{{itemize}}")
    for item in items:
        lines.append(f"{sp}  \\item {tex_clean(item)}")
    lines.append(f"{sp}\\end{{itemize}}")
    return lines

def render_example_exercise(slide_data, indent=1):
    """例題→問 のスライド"""
    sp = '  ' * indent
    lines = []
    ex = slide_data.get('example', '')
    pr = slide_data.get('exercise', '')
    note = slide_data.get('note', '')
    if ex:
        lines.append(f"{sp}\\begin{{exampleblock}}{{{escape_tex(ex)}}}")
        lines.append(f"{sp}  （板書で解説）")
        lines.append(f"{sp}\\end{{exampleblock}}")
        lines.append("")
        lines.append(f"{sp}\\vfill")
        lines.append("")
    if pr:
        lines.append(f"{sp}\\begin{{block}}{{{escape_tex(pr)}\\quad 自分で解いてみよう}}")
        lines.append(f"{sp}  （ノートに解くこと）")
        lines.append(f"{sp}\\end{{block}}")
    if note:
        lines.append(f"{sp}% NOTE: {note}")
    return lines

def generate_lecture(lesson, num, semester, next_topic, next_pages):
    """1回分の .tex を生成"""
    topic = lesson.get('topic', '')
    goal = lesson.get('goal', '')
    pages = lesson.get('textbook_pages', '')
    sc = lesson.get('slide_content', {})
    slides_data = lesson.get('slides', {})
    summary = lesson.get('summary', [])
    basic_nums = lesson.get('basic', [])

    # メタデータ
    text_pages = f"p.\\,{pages}" if pages else "対応なし"
    next_pages_str = f"p.\\,{next_pages}" if next_pages else "対応なし"

    if semester == 'first':
        filename = f"lecture_{num:02d}.tex"
        lecture_num = f"{num:02d}"
        term_name = "前期"
    else:
        filename = f"lecture_second_{num:02d}.tex"
        lecture_num = str(num)
        term_name = "後期"

    lines = []
    lines.append("% !TEX program = lualatex")
    lines.append(f"\\documentclass[aspectratio=43,professionalfonts,handout]{{beamer}}")
    lines.append(f"\\usepackage{{beamer_template}}")
    lines.append("")
    lines.append(f"\\newcommand{{\\LectureNum}}{{{lecture_num}}}")
    lines.append(f"\\newcommand{{\\LectureTitle}}{{{escape_tex(topic)}}}")
    lines.append(f"\\newcommand{{\\TextPages}}{{{escape_tex(text_pages)}}}")
    lines.append(f"\\newcommand{{\\NextTopic}}{{{escape_tex(next_topic)}}}")
    lines.append(f"\\newcommand{{\\NextPages}}{{{escape_tex(next_pages_str)}}}")
    lines.append(f"\\newcommand{{\\CourseName}}{{基礎数学B}}")
    lines.append(f"\\renewcommand{{\\TermName}}{{{term_name}}}")
    lines.append("")
    lines.append("\\begin{document}")
    lines.append("")

    # --- スライド1: 表紙＋目標＋用語 ---
    lines.append("% -----------------------------------------------")
    lines.append("% スライド1: 表紙＋目標＋用語・定義")
    lines.append("% -----------------------------------------------")
    lines.append("\\begin{frame}{\\CourseName\\quad 第\\LectureNum 回「\\LectureTitle 」}")
    lines.append("  {\\small \\TermName\\quad \\TeacherName\\quad ／\\quad 教科書 \\TextPages\\quad")
    lines.append(f"  \\textbf{{目標}}：{tex_clean(goal)}}}")
    lines.append("")

    # 用語
    s1 = slides_data.get('slide1', {})
    terms = s1.get('terms', [])
    defs = sc.get('definitions', [])
    if terms:
        lines.append("  \\begin{block}{用語・定義}")
        lines.extend(render_slide_terms(terms, indent=1))
        lines.append("  \\end{block}")
    elif defs:
        lines.append("  \\begin{block}{用語・定義}")
        lines.extend(render_slide_terms([d.split('：')[0] if '：' in d else d for d in defs[:6]], indent=1))
        lines.append("  \\end{block}")
    lines.append("\\end{frame}")
    lines.append("")

    # --- スライド2: 公式・性質 ---
    s2 = slides_data.get('slide2', {})
    s2_content = s2.get('content', [])
    if not s2_content:
        s2_content = sc.get('definitions', [])
    lines.append("% -----------------------------------------------")
    lines.append("% スライド2: 公式・性質")
    lines.append("% -----------------------------------------------")
    lines.append("\\begin{frame}{公式・性質}")
    lines.append("  \\begin{block}{}")
    lines.extend(render_slide_items(s2_content, indent=1))
    lines.append("  \\end{block}")
    lines.append("\\end{frame}")
    lines.append("")

    # --- スライド3: 図・グラフ ---
    s3 = slides_data.get('slide3', {})
    s3_content = s3.get('content', [])
    lines.append("% -----------------------------------------------")
    lines.append("% スライド3: 図・グラフ（TikZコードを手動追加）")
    lines.append("% -----------------------------------------------")
    lines.append("\\begin{frame}{図・グラフ}")
    lines.append("  \\centering")
    if s3_content:
        lines.append(f"  % TODO: {'; '.join(s3_content)}")
    lines.append("  \\begin{tikzpicture}[scale=0.65]")
    lines.append("    \\draw[->,thick] (-3.5,0) -- (4.5,0) node[right]{$x$};")
    lines.append("    \\draw[->,thick] (0,-2.5) -- (0,4.5) node[above]{$y$};")
    lines.append("    \\node[below left] at (0,0) {O};")
    lines.append("    \\draw[gray!40, very thin] (-3,-2) grid (4,4);")
    lines.append("    % ここにグラフを描画")
    lines.append("  \\end{tikzpicture}")
    lines.append("\\end{frame}")
    lines.append("")

    # --- スライド4,5: 例題→問 ---
    for sn, key in [('4', 'slide4'), ('5', 'slide5')]:
        sd = slides_data.get(key, {})
        if not sd:
            continue
        title = sd.get('title', f'例題→問')
        lines.append("% -----------------------------------------------")
        lines.append(f"% スライド{sn}: {title}")
        lines.append("% -----------------------------------------------")
        lines.append(f"\\begin{{frame}}{{{escape_tex(title)}}}")
        lines.extend(render_example_exercise(sd))
        lines.append("\\end{frame}")
        lines.append("")

    # --- スライド6: まとめ ---
    lines.append("% -----------------------------------------------")
    lines.append("% まとめ")
    lines.append("% -----------------------------------------------")
    lines.append("\\begin{frame}{まとめ}")
    if summary:
        lines.append("  \\begin{itemize}")
        for s in summary:
            lines.append(f"    \\item {tex_clean(s)}")
        lines.append("  \\end{itemize}")
    else:
        lines.append("  \\begin{itemize}")
        lines.append("    \\item % TODO: まとめを記入")
        lines.append("  \\end{itemize}")

    # 基本問題番号
    if basic_nums:
        nums_str = ', '.join(str(n) for n in basic_nums)
        lines.append("")
        lines.append("  \\vfill")
        lines.append(f"  {{\\small 基本問題：{nums_str}}}")

    lines.append("\\end{frame}")
    lines.append("")
    lines.append("\\end{document}")
    lines.append("")

    return filename, '\n'.join(lines)


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    yaml_path = os.path.join(script_dir, YAML_FILE)
    output_dir = os.path.join(script_dir, OUTPUT_DIR)
    os.makedirs(output_dir, exist_ok=True)

    with open(yaml_path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)

    schedule = data.get('schedule', {})

    # === 前期: 15回 ===
    zenki = schedule.get('zenki', [])
    zenki_lessons = []
    for w in zenki:
        lesson = {
            'topic': w.get('topic', ''),
            'goal': w.get('goal', ''),
            'textbook_pages': w.get('textbook_pages', ''),
            'slide_content': w.get('slide_content', {}),
            'slides': w.get('slides', {}),
            'summary': w.get('summary', []),
            'basic': w.get('slides', {}).get('slide6', {}).get('basic', []),
        }
        zenki_lessons.append(lesson)

    # === 後期: 30回 (各weekにlesson_a, lesson_b) ===
    kouki = schedule.get('kouki', [])
    kouki_lessons = []
    for w in kouki:
        for key in ['lesson_a', 'lesson_b']:
            les = w.get(key, {})
            if les:
                lesson = {
                    'topic': les.get('topic', ''),
                    'goal': les.get('goal', ''),
                    'textbook_pages': les.get('textbook_pages', ''),
                    'slide_content': les.get('slide_content', {}),
                    'slides': les.get('slides', {}),
                    'summary': les.get('summary', []),
                    'basic': les.get('basic', []),
                }
                kouki_lessons.append(lesson)

    # 生成
    count = 0

    for i, lesson in enumerate(zenki_lessons):
        nt, np_ = get_next_info(zenki_lessons, i)
        filename, content = generate_lecture(lesson, i + 1, 'first', nt, np_)
        filepath = os.path.join(output_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  {filename}")
        count += 1

    for i, lesson in enumerate(kouki_lessons):
        nt, np_ = get_next_info(kouki_lessons, i)
        filename, content = generate_lecture(lesson, i + 1, 'second', nt, np_)
        filepath = os.path.join(output_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  {filename}")
        count += 1

    print(f"\nTotal: {count} files generated.")


if __name__ == '__main__':
    main()
