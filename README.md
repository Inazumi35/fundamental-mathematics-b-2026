# 基礎数学B（2026年度）

石川工業高等専門学校 ／ 担当：稲積泰宏

## 概要

- **対象**: 1年生
- **教科書**: 新 基礎数学 改訂版（大日本図書）
- **評価**: 前期中間35%、前期末35%、課題・レポート30%

## 公開サイト

学生向けページを GitHub Pages で公開しています。

<https://inazumi35.github.io/fundamental-mathematics-b-2026/>

`index.html` がそのまま公開ページになります（配信元は `master` ブランチのルート）。掲載しているのは問題集の解説PDF、グラフアプリへのリンク、試験の解答です。

## ファイル構成

```
.
├── index.html                 # 公開ページ（GitHub Pages）
├── topics_basic_math_b.yaml   # 授業トピック定義（前期15コマ・後期30コマ）
├── TODO.md                    # 作業メモ
├── solutions/                 # 問題集の解説（TeX + PDF）
│   ├── kaitoushu.sty          #   解説用スタイル
│   ├── solutions_template.tex #   新規作成時のひな形
│   ├── ch3_*.tex / *.pdf      #   3章 関数とグラフ
│   ├── ch4_*.tex / *.pdf      #   4章 指数関数と対数関数
│   └── ch5_*.tex / *.pdf      #   5章 三角関数
├── lecture/                   # 授業スライド（TeX、beamer）
│   ├── beamer_template.sty
│   ├── math_macros.sty
│   ├── lecture_NN.tex         #   前期
│   └── lecture_second_NN.tex  #   後期
└── past_exams/                # 実施後に公開する試験の解答
```

解説ファイルの命名規則は `ch<章>_<種別>_p<教科書ページ>` です。種別は `basic` / `check` / `renshu` の3つです。

## 運用方針（2026年度）

授業ではスライドを使用しません。学生に配布するのは `solutions/` の解説PDFです。`lecture/` の TeX は次年度以降のために残してあります。

`index.html` に掲載しているのは練習問題A（1・A、2・A）のみです。B は授業で扱わないためリンクしていません。ファイル自体は `solutions/` に残っているので、扱うことになればリンクを追加するだけで公開できます。

## ビルド方法

解説PDFは LuaLaTeX でコンパイルします。`solutions/` 内で実行してください。

```bash
cd solutions
lualatex ch5_basic_p56.tex
```

スライドは `lecture/` 内で同様にコンパイルします。既定は配布資料レイアウト（4スライド/ページ）です。フルスクリーン版が必要な場合は `\slidemode` に 1 を渡します。

```bash
cd lecture
lualatex lecture_second_01.tex                          # 配布資料
lualatex "\def\slidemode{1}\input{lecture_second_01}"   # フルスクリーン
```

生成した PDF は解説・スライドとも Git 管理下に置いています（学生が直接ダウンロードできるようにするため）。

## 試験ファイルについて

試験問題と解答は非公開リポジトリ [`fund-math-b-exams`](https://github.com/Inazumi35/fund-math-b-exams) で管理します。**このリポジトリは公開されているため、試験ファイルを置かないでください。**

`.gitignore` で `exam/` 以下とルート直下の `exam_*.tex` / `exam_*.pdf` などを除外していますが、`.gitignore` は既に追跡済みのファイルには効きません。コミット前に `git status` で追加対象を確認してください。

実施後に公開する解答は `past_exams/` に置きます。
