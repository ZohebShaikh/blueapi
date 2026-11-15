"""Benchmarks for the BlueskyContext: plan registration and parameter handling."""

from dodal import plans as bp

from blueapi.core import BlueskyContext
from blueapi.service.model import DeviceModel, PlanModel
from blueapi.worker.task import Task


def test_register_dodal_plans_module(benchmark, context_with_devices):
    ctx: BlueskyContext = context_with_devices

    @benchmark
    def _():
        ctx.plans.clear()
        ctx.with_plan_module(bp)

    assert "count" in ctx.plans


def test_plan_models_json_schema(benchmark, context_with_devices):
    ctx: BlueskyContext = context_with_devices
    plans = list(ctx.plans.values())

    @benchmark
    def _():
        return [PlanModel.from_plan(plan) for plan in plans]


def test_device_models(benchmark, context_with_devices):
    ctx: BlueskyContext = context_with_devices
    devices = [entry.device for entry in ctx.devices.values()]

    @benchmark
    def _():
        return [DeviceModel.from_device(device) for device in devices]


def test_find_nested_device(benchmark, context_with_devices):
    ctx: BlueskyContext = context_with_devices

    @benchmark
    def _():
        for _ in range(100):
            ctx.find_device("x.user_readback")
            ctx.find_device("y.velocity")


def test_task_prepare_params_num_scan(benchmark, context_with_devices):
    ctx: BlueskyContext = context_with_devices
    task = Task(
        name="num_scan",
        params={"detectors": ["x"], "params": [["y", [0.0, 10.0]]], "num": 11},
    )
    _, kwargs = benchmark(task.prepare_params, ctx)
    assert kwargs["num"] == 11


def test_task_prepare_params_count(benchmark, context_with_devices):
    ctx: BlueskyContext = context_with_devices
    task = Task(name="count", params={"detectors": ["x", "y"], "num": 5})
    benchmark(task.prepare_params, ctx)
