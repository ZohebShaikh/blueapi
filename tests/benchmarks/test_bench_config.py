"""Benchmarks for loading and validating blueapi configuration."""

from pathlib import Path

import yaml

from blueapi.config import ApplicationConfig, ConfigLoader, generate_config_schema

VALID_EXAMPLE_CONFIG = (
    Path(__file__).parent.parent / "unit_tests" / "valid_example_config"
)

CONFIG_VALUES = {
    "stomp": {
        "enabled": True,
        "url": "tcp://localhost:61613",
        "auth": {"username": "guest", "password": "guest"},
    },
    "env": {
        "sources": [
            {"kind": "planFunctions", "module": "dodal.plans"},
            {"kind": "planFunctions", "module": "dodal.plan_stubs.wrapped"},
            {"kind": "deviceManager", "module": "dodal.beamlines.i04", "mock": True},
        ],
        "events": {"broadcast_status_events": True},
    },
    "api": {"url": "http://0.0.0.0:8000"},
    "logging": {"level": "INFO"},
}


def test_config_loader_from_dict(benchmark):
    @benchmark
    def _():
        loader = ConfigLoader(ApplicationConfig)
        loader.use_values(CONFIG_VALUES)
        loader.load()


def test_config_loader_from_yaml(benchmark):
    # Read the files up front so the benchmark measures YAML parsing, merging and
    # validation rather than file system access.
    documents = [
        (VALID_EXAMPLE_CONFIG / name).read_text()
        for name in ("plans_and_devices.yaml", "stomp.yaml", "graylog.yaml")
    ]

    @benchmark
    def _():
        loader = ConfigLoader(ApplicationConfig)
        for document in documents:
            loader.use_values(yaml.load(document, yaml.Loader))
        loader.load()


def test_generate_config_schema(benchmark):
    schema = benchmark(generate_config_schema)
    assert "$defs" in schema
