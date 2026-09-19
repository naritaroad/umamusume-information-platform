"""
Django apps 實體目錄對照。

所有 `app_*` 套件集中於 `app/<module>/`，但 Python 匯入名稱維持 `app_*`
（由 register_app_paths() 把各模組資料夾加入 sys.path），因此：
- INSTALLED_APPS / migrations / app_label 不必改
- 檔案系統路徑請用 django_app_dir() 或 PROJECT_ROOT，勿假設套件在專案根目錄
"""
from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
APP_ROOT = PROJECT_ROOT / 'app'

# Django app label → app/<module>/ 子目錄
APP_GROUPS: dict[str, str] = {
    # 輿情分析
    'app_character_pk': 'analysis',
    'app_user_keyword': 'analysis',
    'app_user_keyword_association': 'analysis',
    'app_user_keyword_sentiment': 'analysis',
    'app_user_keyword_db': 'analysis',
    'app_user_keyword_llm_report': 'analysis',
    'app_uma_top_keyword': 'analysis',
    'app_uma_top_character': 'analysis',
    'app_correlation_analysis': 'analysis',
    'app_dashboard': 'analysis',
    # 資料採集與控制台
    'app_crawler_admin': 'ingest',
    'app_uma_news': 'ingest',
    'app_uma_comments': 'ingest',
    'app_comment_sentiment': 'ingest',
    'app_youtube_uma': 'ingest',
    # AI Agent / RAG
    'app_agent_uma': 'agent',
    'app_rag_uma': 'agent',
    'app_rag_agent': 'agent',
    'app_agent_langchain': 'agent',
    'app_agent_langgraph': 'agent',
    # 社群整合
    'app_discord_bot': 'community',
    'app_uma_info_portal': 'community',
    # 介紹頁
    'app_poa_introduction': 'pages',
    'app_course_intro': 'pages',
    # 課程遺留、未掛載
    'app_scchen': 'legacy',
    'app_taipei_mayor': 'legacy',
    'app_top_keyword': 'legacy',
    'app_top_ner': 'legacy',
    'app_top_person': 'legacy',
    'app_top_person_db': 'legacy',
    'app_top_person_sqlalchemy_db': 'legacy',
}


def django_app_dir(label: str) -> Path:
    """回傳指定 Django app 的實體目錄。"""
    group = APP_GROUPS.get(label)
    if group:
        return APP_ROOT / group / label
    # 後備：尚未列入對照表時，仍嘗試在 app/ 底下尋找
    for found in APP_ROOT.glob(f'*/{label}'):
        if found.is_dir():
            return found
    return PROJECT_ROOT / label


def rag_index_dir() -> Path:
    return django_app_dir('app_rag_uma') / 'index'


def rag_index_file() -> Path:
    return rag_index_dir() / 'uma_knowledge.faiss'


def rag_build_script() -> Path:
    return django_app_dir('app_rag_uma') / 'build_index.py'


def register_app_paths() -> None:
    """將 app/<module>/ 加入 sys.path，使 `import app_*` 仍可用。"""
    if not APP_ROOT.is_dir():
        return
    for group_dir in sorted(APP_ROOT.iterdir()):
        if not group_dir.is_dir():
            continue
        if group_dir.name.startswith(('.', '_')):
            continue
        path_str = str(group_dir)
        if path_str not in sys.path:
            sys.path.insert(0, path_str)
