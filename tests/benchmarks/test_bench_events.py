"""Benchmarks for worker event (de)serialization and CLI formatting."""

import io

from blueapi.cli.format import OutputFormat
from blueapi.core.bluesky_types import DataEvent
from blueapi.worker.event import (
    ProgressEvent,
    StatusView,
    TaskStatus,
    WorkerEvent,
    WorkerState,
)

WORKER_EVENT = WorkerEvent(
    state=WorkerState.RUNNING,
    task_status=TaskStatus(
        task_id="b3c0f2d9-6a54-4e1f-9a6f-3cbb7c2b8f11",
        result=None,
        task_complete=False,
        task_failed=False,
    ),
    errors=[],
    warnings=["something to be aware of"],
)

PROGRESS_EVENT = ProgressEvent(
    task_id="b3c0f2d9-6a54-4e1f-9a6f-3cbb7c2b8f11",
    statuses={
        f"status_{i}": StatusView(
            display_name=f"motor_{i}",
            current=float(i),
            initial=0.0,
            target=100.0,
            unit="mm",
            precision=3,
            done=False,
            percentage=i / 100,
            time_elapsed=1.5,
            time_remaining=3.0,
        )
        for i in range(20)
    },
)

DATA_EVENT = DataEvent(
    name="event",
    doc={
        "descriptor": "d6a3c9b2",
        "seq_num": 1,
        "time": 1700000000.0,
        "data": {f"det_{i}": float(i) for i in range(50)},
        "timestamps": {f"det_{i}": 1700000000.0 for i in range(50)},
        "filled": {},
        "uid": "e7a4b1c3",
    },
    task_id="b3c0f2d9-6a54-4e1f-9a6f-3cbb7c2b8f11",
)


def test_worker_event_roundtrip(benchmark):
    @benchmark
    def _():
        for _ in range(100):
            WorkerEvent.model_validate_json(WORKER_EVENT.model_dump_json())


def test_progress_event_roundtrip(benchmark):
    @benchmark
    def _():
        for _ in range(10):
            ProgressEvent.model_validate_json(PROGRESS_EVENT.model_dump_json())


def test_display_full_events(benchmark):
    @benchmark
    def _():
        out = io.StringIO()
        for event in (WORKER_EVENT, PROGRESS_EVENT, DATA_EVENT):
            OutputFormat.FULL.display(event, out)


def test_display_json_events(benchmark):
    @benchmark
    def _():
        out = io.StringIO()
        for event in (WORKER_EVENT, PROGRESS_EVENT, DATA_EVENT):
            OutputFormat.JSON.display(event, out)
