from pathlib import Path


def get_project_root():
	PROJECT_ROOT = Path(__file__)


	while not (PROJECT_ROOT / "pyproject.toml").exists():

		if PROJECT_ROOT == PROJECT_ROOT.parent:
			raise FileNotFoundError("Project root not found!")

		PROJECT_ROOT = PROJECT_ROOT.parent

	return PROJECT_ROOT