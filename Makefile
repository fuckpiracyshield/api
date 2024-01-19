# Initializer

setup:
	@echo "Installing required packages"
	pip install -r requirements.txt

# Executables

run_server:
	@echo " -- Running API server (Piracy Shield ${PIRACYSHIELD_VERSION}) --"
	@python boot.py

run_worker:
	@echo " -- Running queue worker (Piracy Shield ${PIRACYSHIELD_VERSION}) --"
	@python bin/worker.py

run_mock_storage:
	@export AZURITE_ACCOUNTS="account1:key1:key2"; azurite -s -l /tmp/azurite_emulated_store

create_mock_container:
	@echo "Creating mock container on /tmp/azurite_emulated_store"
	@python tests/mock_storage.py

# Testing operations

test:
	@echo "Running tests"
	pytest

sast:
	@echo "Running SAST check"
	semgrep scan --config auto

bench:
	@echo "Running benchmark"
	ab -v 2 -n 20 -c 10 -k -T application/json -p tests/bench_params.txt 127.0.0.1:58008/api/v1/authentication/login
	#ab -v 2 -n 200 -c 10 -k 127.0.0.1:58008/api/v1/ping
