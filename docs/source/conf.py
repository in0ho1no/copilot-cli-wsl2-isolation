"""Markdown とキャラクターを使うスライドの Sphinx 設定。

sphinx-revealjs-mascot の雛形 (.agents/skills/markdown-to-slides/assets/starter) を基にしている。
"""

project = 'sphinx-revealjs-mascot サンプル'
extensions = ['myst_parser', 'sphinx_revealjs_mascot']
root_doc = 'index'
source_suffix = {'.md': 'markdown'}
language = 'ja'
exclude_patterns = ['_build']

revealjs_static_path = ['_static']
revealjs_css_files = ['slides.css']
revealjs_style_theme = 'white'
revealjs_script_conf = {
    'width': 1280,
    'height': 720,
    'margin': 0.06,
    'center': False,
    'transition': 'none',
    'hash': True,
}
revealjs_script_plugins = [
    {'name': 'RevealNotes', 'src': 'revealjs/plugin/notes/notes.js'},
]

# キャラクターの全体設定。既定値 (右下表示・M キーで表示切り替え) のままでよければ削除してよい
revealjs_mascot_position = 'bottom-right'
revealjs_mascot_toggle_key = 'm'
