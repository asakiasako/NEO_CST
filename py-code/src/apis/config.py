from libs.config import get_config, set_config
from .ApiRouter import ApiRouter

# :config
ApiRouter().register_from_map({
    ':config:get': get_config,
    ':config:set': set_config,
})