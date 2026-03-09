# 基礎数学B（2026年度）

## 概要
- **対象**: 1年生
- **教科書**: 新 基礎数学 改訂版（大日本図書）
- **評価**: 前期中間35%、前期末35%、課題・レポート30%

## ファイル構成
```
基礎数学B/
├── topics_basic_math_b.yaml   # 授業トピック定義
├── generate_tex.py            # TeXファイル生成スクリプト
├── CLAUDE_CODE_HANDOFF.md     # Claude Code引き継ぎ情報
└── lecture/                   # 各回のTeXファイル
    ├── lecture_01.tex
    ├── lecture_02.tex
    └── ...
```

## 使い方
1. `topics_basic_math_b.yaml` を編集して授業内容を更新する
2. `generate_tex.py` を実行してTeXファイルを生成する
3. TeXファイルをコンパイルしてPDFを作成する
