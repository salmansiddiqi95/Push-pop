"""Module to setup fastapi API to expose API to the outside world."""
import logging
import random
from typing import Any, Dict

from fastapi import FastAPI
import uvicorn

ERROR_CODES = [error_code for error_code in range(50)]
LOGGER = logging.getLogger("API")
app = FastAPI()
req = 0
matchResUnres = 0
matchResBlog = 0
matchUnresBlog = 0

def _generate_lists() -> Dict[str, Any]:
    """Generate resolved, unresolved and backlog lists."""
    return {
        'resolved': [{
            'index': error_idx,
            'code': random.choice(ERROR_CODES),
            'text': 'Error ABC occured, that is `resolved`'
        } for error_idx in range(50)],
        'unresolved': [{
            'index': error_idx,
            'code': random.choice(ERROR_CODES),
            'text': 'Error DEF occured, that is `unresolved`'
        } for error_idx in range(50, 100)],
        'backlog': [{
            'index': error_idx,
            'code': random.choice(ERROR_CODES),
            'text': 'Error XYZ occured, that is in the `backlog`'
        } for error_idx in range(100, 150)]
    }


@app.get("/get_lists")
def get_lists() -> Dict[str, Any]:
    """Return resolved, unresolved and backlog lists."""
    LOGGER.info('Generating resolved, unresolved and backlog lists.')
    global req
    req = req + 1
    print(req)
    return _generate_lists()


@app.get("/get_list_intersection_counts")
def get_list_intersection_counts() -> Dict[str, int]:
    """Return the error intersection counts between a set of resolved, unresolved and backlog lists.

    Returns
    -------
    intersection_counts: Dict[str, int]
        The intersection counts between resolved, unresolved and backlog lists, e.g.:
        ```json
        {
            "resolved_unresolved": 12,
            "resolved_backlog": 6,
            "unresolved_backlog": 35
        }
        ```
        `"resolved_unresolved": 12` describes that there are `12` errors with the *same error code*  shared
        between a `resolved` and `unresolved` list, `"resolved_backlog": 6` describes that there are `6`
        errors with the *same error code*  shared between a `resolved` and `backlog` list.

        The three lists required for this calculation are generated by calling `_generate_lists`.

        Code that checks whether errors from the resolved and unresolved list `intersect`, could look like:
        ```python
        error_lists = _generate_lists()
        resolved, unresolved, backlog = error_lists['resolved'], error_lists['unresolved'], error_lists['backlog']

        error_from_resolved = resolved[0]
        error_from_unresolved  = unresolved[0]
        if error_from_resolved.code == error_from_unresolved.code:
            print('Errors intersect')
        else:
            print('Errors do not intersect')
        ```

    """
    LOGGER.info('Generating the intersection counts between a set of resolved, unresolved and backlog lists.')

    error_lists = _generate_lists()
    resolved, unresolved, backlog = error_lists['resolved'], error_lists['unresolved'], error_lists['backlog']

    # TODO: Implement the code that calculates how many errors with *the same error code* are shared between
    # the possible pairs of lists here. Then return a Dict like the one shown in the documentation string above,
    # e.g.:


    #error_from_resolved = resolved
    #error_from_unresolved  = unresolved
    #error_from_backlog  = backlog

    global matchResUnres
    matchResUnres = 0

    global matchResBlog
    matchResBlog = 0

    global matchUnresBlog
    matchUnresBlog = 0
    
    for key in resolved:
        for key2 in unresolved:
            if key['code'] == key2['code']:
                matchResUnres = matchResUnres + 1

    print("matchResUnres : " , matchResUnres )


    for key in resolved:
        for key2 in backlog:
            if key['code'] == key2['code']:
                matchResBlog = matchResBlog + 1

    print("matchResBlog : " , matchResBlog )

    for key in unresolved:
        for key2 in backlog:
            if key['code'] == key2['code']:
                matchUnresBlog = matchUnresBlog + 1

    print("matchUnresBlog : " , matchUnresBlog )

    #print(new_dict.get("code"))

    #for x, val in resolved:
    #    print(x,val)
    
    #if error_from_resolved["code"] == error_from_backlog["code"]:
    #    print('Resolved/Backlog Errors intersect')
    #else:
    #    print('Resolved/Backlog Errors do not intersect')

    #if error_from_unresolved["code"] == error_from_backlog["code"]:
    #    print('Unresolved/Backlog Errors intersect')
    #else:
    #    print('Unresolved/Backlog Errors do not intersect')

    return  {
        'resolved_unresolved': matchResUnres,
        'resolved_backlog': matchResBlog,
        'unresolved_backlog': matchUnresBlog
    }


    # NOTE: THIS IS JUST AN EXAMPLE, REPLACE WITH YOUR OWN CODE AND `return`!


def run(host: str, port: int) -> None:
    """Run the code challenge API."""
    uvicorn.run(app, host=host, port=port)
