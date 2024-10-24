VERSION = 1.0.0


all: build install

ensure_env_exists:
	@if [ ! -d "env" ]; then \
		python3 -m venv env; \
	fi

ensure_testenv_exists:
	@if [ ! -d "testenv" ]; then \
		python3 -m venv testenv; \
	fi

install_build_deps: ensure_env_exists
	env/bin/pip install -r requirements.txt

build: ensure_env_exists install_build_deps
	env/bin/feanor pack.py --debug -pv $(VERSION)

install: ensure_testenv_exists
	testenv/bin/pip install dist/*.whl --force-reinstall

start:
	testenv/bin/melkor --debug config.json
