import pytest
from dodal import plans as bp
from ophyd_async.core import init_devices
from ophyd_async.sim import SimMotor

from blueapi.core import BlueskyContext


@pytest.fixture
def context_with_devices():
    ctx = BlueskyContext()
    with init_devices(mock=True):
        x = SimMotor()
        y = SimMotor()
    ctx.register_device(x, "x")
    ctx.register_device(y, "y")
    ctx.with_plan_module(bp)
    yield ctx
    ctx.run_engine.loop.call_soon_threadsafe(ctx.run_engine.loop.stop)
    ctx.run_engine._th.join()
