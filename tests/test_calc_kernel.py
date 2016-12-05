import pytest


@pytest.fixture
def empty_kernel():
    from iap.forecasting.workbench.calculation_kernel import CalculationKernel
    kernel = CalculationKernel()
    return kernel


@pytest.fixture
def kernel(empty_kernel):
    from iap.common.dev_template import dev_template_JJOralCare
    empty_kernel.load_instructions(dev_template_JJOralCare['calc_instructions'])
    return empty_kernel

@pytest.mark.skip()
def test_serialization(kernel, empty_kernel):
    backup = kernel.get_backup()
    recovered_kernel = empty_kernel
    recovered_kernel.load_from_backup(backup)


