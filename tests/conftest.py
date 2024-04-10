import pytest
from pathlib import Path
from tests.helpers import make_algo_id


REPO_ROOT = Path(__file__).parent.parent


@pytest.fixture(params=REPO_ROOT.joinpath("algorithms").glob("*.py"), ids=make_algo_id)
def algorithm(request):
    print(request.param)
    if (request.param.name) == "__init__.py":
        return None
    return request.param.stem
