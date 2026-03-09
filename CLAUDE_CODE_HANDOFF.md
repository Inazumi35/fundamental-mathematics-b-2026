# Claude Code 引き継ぎ指示書
## 基礎数学B スライド自動生成パイプライン

---

## プロジェクト概要

石川高専 1年「基礎数学B」の授業スライドを
YAMLから自動生成するパイプラインを構築する。

- 前期：15週×1回 = 15ファイル
- 後期：15週×2回（lesson_a・lesson_b）= 30ファイル
- 合計：45ファイルのBeamer PDFを生成する

---

## ファイル構成

```
topics_basic_math_b.yaml   # 授業計画・スライド構成の全情報
beamer_template.sty        # Beamerのスタイルファイル
math_macros.sty            # 数式マクロ（必要に応じて拡張）
```

---

## YAMLの構造

### 前期（zenki）
```yaml
schedule:
  zenki:
    - week: 1
      topic: 関数とグラフ
      goal: ...
      summary: [...]        # まとめスライドの箇条書き
      slides:
        slide1:
          title: 表紙
          goal: ...         # 授業の目標文
          terms: [...]      # 用語・定義のリスト
        slide2:
          title: 公式・性質
          content: [...]
        slide3:
          title: 図・グラフ
          content: [...]
        slide4:
          title: 例1→問1
          example: '例1) p.73'
          exercise: '問1) p.73'
        slide5:
          title: 例2→問2
          example: ...
          exercise: ...
        slide6:
          title: まとめ
          summary: true     # week の summary フィールドを使う
          basic: [143, 144] # 問題集の番号（Basic）
```

### 前期 演習回（week 8・14）
```yaml
slides:
  slide1:
    title: 表紙（目標＋範囲）
    goal: ...
    note: Check（授業中演習）回
  slide2:
    title: Check（演習）
    workbook: [143, 144, ...]  # 問題集番号一覧
    note: 問題集から各自取り組む
  slide3:
    title: 解説
    note: 授業後半に重要問題を板書で解説
    key_problems: [151, 154, 163]
```

### 後期（kouki）
```yaml
schedule:
  kouki:
    - week: 1
      lesson_a:
        topic: 累乗根・指数の拡張（１）
        goal: ...
        basic: [201, 202, 203, 204]   # 問題集 Basic
        slides:
          slide1: ...
          ...
          slide6:
            title: まとめ
            summary: true
      lesson_b:
        topic: 累乗根・指数の拡張（２）
        ...
```

---

## スライドの基本構成（通常回）

| スライド | 内容 | 備考 |
|---------|------|------|
| slide1 | 表紙＋目標＋用語・定義 | `\begin{block}{用語・定義}` |
| slide2 | 公式・性質 | `\begin{block}{}` |
| slide3 | 図・グラフ | TikZコード（手動記述） |
| slide4 | 例1 → 問1 | `\begin{exampleblock}{}` + `\begin{block}{}` |
| slide5 | 例2 → 問2 | 同上 |
| slide6 | まとめ＋問題集番号 | `\begin{itemize}` + 問題番号表示 |
| （slide7） | 追加例3→問3 | 内容が多い週のみ |

枚数は5〜7枚で柔軟に対応。YAMLのスライド数に応じて自動調整。

---

## TeXテンプレートの共通部分

```latex
% !TEX program = lualatex
\documentclass[aspectratio=43,professionalfonts,handout]{beamer}
\usepackage{beamer_template}

\newcommand{\LectureNum}{1}
\newcommand{\LectureTitle}{関数とグラフ}
\newcommand{\TextPages}{p.72〜75}
\newcommand{\NextTopic}{２次関数のグラフ（１）}
\newcommand{\NextPages}{p.75〜77}
```

### beamer_template.sty で定義済みのマクロ
- `\CourseName`：基礎数学B（デフォルト値、上書き可）
- `\TermName`：前期 or 後期（上書き可）
- `\TeacherName`：稲積泰宏（上書き可）
- `\kw{用語}`：キーワードの強調
- TikZ・pgfplots・日本語（LuaLaTeX）対応済み

### 5学科対応について
学科名はスライドに表示しない。5学科で同じテンプレートを使い回す。
教員名・科目名は `.tex` ファイル冒頭で上書きする：

```latex
\renewcommand{\TeacherName}{担当教員名}
\renewcommand{\CourseName}{基礎数学B}
% \renewcommand{\TermName}{前期} % 必要に応じて
```

スクリプト生成時は `TeacherName` と `CourseName` を
引数またはconfigファイルで渡せるようにする。

---

## 自動生成スクリプトの仕様

### 生成対象
```
lecture_01.tex 〜 lecture_15.tex        # 前期
lecture_k01a.tex 〜 lecture_k15b.tex    # 後期
```

### 処理フロー
1. YAMLを読み込む
2. 各週・各スライドのデータを取得
3. TeXテンプレートに流し込む
4. `.tex` ファイルを出力
5. `lualatex` でコンパイル（2回）
6. PDF確認

### スライド3（図・グラフ）の扱い
TikZコードはYAMLに格納できないため、以下の方針で対応：

- **オプションA**：graph_type フラグ（例：`parabola`、`hyperbola`など）をYAMLに持ち、
  テンプレート側でコードを選択
- **オプションB**：スライド3は空のフレームを生成し、
  `.tex` 編集で手動追加
- **推奨**：まずオプションBで全ファイルを生成し、
  後からスライド3を個別に充実させる

### まとめスライドの問題番号表示例
```latex
\begin{frame}{まとめ}
  \begin{itemize}
    \item 関数とは x の値に y がただ1つ対応する関係
    ...
  \end{itemize}
  \vfill
  \begin{block}{問題集（Basic）}
    \textbf{No. 143, 144}
  \end{block}
\end{frame}
```

---

## コンパイル環境

- **エンジン**：LuaLaTeX（日本語対応）
- **必要パッケージ**：texlive-lang-japanese, texlive-luatex
- **コマンド**：`lualatex -interaction=nonstopmode lecture_01.tex`

---

## 優先順位

1. 前期15週の `.tex` 生成スクリプト作成・動作確認
2. 前期15週のPDF一括生成
3. 後期30回の生成（同じスクリプトで対応）
4. スライド3（グラフ）の充実化

