import json

from typing import Any

def pretty_print_json(response: Any, title: str) -> None:
    print(f"--- {title} ---")

    try:
        if hasattr(response, 'root'):
            data = response.root.model_dump(mode='json', exclude_none=True)
        else:
            data = response.model_dump(mode='json', exclude_none=True)

        json_str = json.dumps(data, indent=2, ensure_ascii=False)
        print(json_str)
    except Exception as e:
        print(f"Error pretty printing JSON: {e}")
        print(response)
