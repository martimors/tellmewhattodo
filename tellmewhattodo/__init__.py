import streamlit.logger
from logging import basicConfig, INFO, getLogger

streamlit.logger.get_logger = getLogger
streamlit.logger.setup_formatter = None
streamlit.logger.update_formatter = lambda *a, **k: None
streamlit.logger.set_log_level = lambda *a, **k: None


basicConfig(
    level=INFO, format="%(asctime)s %(levelname)7s %(name)s %(message)s", force=True
)
