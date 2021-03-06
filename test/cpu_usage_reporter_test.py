from mock import Mock
import unittest
from pcp_pidstat import CpuUsageReporter

class TestCpuUsageReporter(unittest.TestCase):
    def setUp(self):
        self.options = Mock(
                        per_processor_usage = False,
                        show_process_user = None)

        process_1 = Mock(pid = Mock(return_value = 1),
                        process_name = Mock(return_value = "process_1"),
                        user_name = Mock(return_value='pcp'),
                        user_id = Mock(return_value=1000),
                        user_percent = Mock(return_value=2.43),
                        system_percent = Mock(return_value=1.24),
                        guest_percent = Mock(return_value=0.00),
                        total_percent = Mock(return_value=3.67),
                        cpu_number = Mock(return_value=1),)

        self.processes = [process_1]

    def test_print_report_without_filtering(self):
        cpu_usage = Mock()
        process_filter = Mock()
        printer = Mock()
        process_filter.filter_processes = Mock(return_value=self.processes)
        reporter = CpuUsageReporter(cpu_usage, process_filter, 1, printer, self.options)

        reporter.print_report(123, 4)

        printer.assert_called_with("123\t1000\t1\t2.43\t1.24\t0.0\t3.67\t1\tprocess_1")

    def test_print_report_with_user_name(self):
        self.options.show_process_user = 'pcp'
        cpu_usage = Mock()
        process_filter = Mock()
        printer = Mock()
        process_filter.filter_processes = Mock(return_value=self.processes)
        reporter = CpuUsageReporter(cpu_usage, process_filter, 1, printer, self.options)

        reporter.print_report(123, 4)

        printer.assert_called_with("123\tpcp\t1\t2.43\t1.24\t0.0\t3.67\t1\tprocess_1")

    def test_print_report_with_per_processor_usage(self):
        self.options.per_processor_usage = True
        cpu_usage = Mock()
        process_filter = Mock()
        printer = Mock()
        process_filter.filter_processes = Mock(return_value=self.processes)
        reporter = CpuUsageReporter(cpu_usage, process_filter, 1, printer, self.options)

        reporter.print_report(123, 4)

        printer.assert_called_with("123\t1000\t1\t2.43\t1.24\t0.0\t0.92\t1\tprocess_1")

    def test_print_report_with_user_percent_none(self):
        cpu_usage = Mock()
        process_filter = Mock()
        printer = Mock()
        self.processes[0].user_percent = Mock(return_value=None)
        process_filter.filter_processes = Mock(return_value=self.processes)
        reporter = CpuUsageReporter(cpu_usage, process_filter, 1, printer, self.options)

        reporter.print_report(123, 4)

        printer.assert_called_with("123\t1000\t1\t?\t1.24\t0.0\t3.67\t1\tprocess_1")

    def test_print_report_with_guest_percent_none(self):
        cpu_usage = Mock()
        process_filter = Mock()
        printer = Mock()
        self.processes[0].guest_percent = Mock(return_value=None)
        process_filter.filter_processes = Mock(return_value=self.processes)
        reporter = CpuUsageReporter(cpu_usage, process_filter, 1, printer, self.options)

        reporter.print_report(123, 4)

        printer.assert_called_with("123\t1000\t1\t2.43\t1.24\t?\t3.67\t1\tprocess_1")

    def test_print_report_with_system_percent_none(self):
        cpu_usage = Mock()
        process_filter = Mock()
        printer = Mock()
        self.processes[0].system_percent = Mock(return_value=None)
        process_filter.filter_processes = Mock(return_value=self.processes)
        reporter = CpuUsageReporter(cpu_usage, process_filter, 1, printer, self.options)

        reporter.print_report(123, 4)

        printer.assert_called_with("123\t1000\t1\t2.43\t?\t0.0\t3.67\t1\tprocess_1")

    def test_print_report_with_total_percent_none(self):
        cpu_usage = Mock()
        process_filter = Mock()
        printer = Mock()
        self.processes[0].total_percent = Mock(return_value=None)
        process_filter.filter_processes = Mock(return_value=self.processes)
        reporter = CpuUsageReporter(cpu_usage, process_filter, 1, printer, self.options)

        reporter.print_report(123, 4)

        printer.assert_called_with("123\t1000\t1\t2.43\t1.24\t0.0\t?\t1\tprocess_1")

if __name__ == "__main__":
    unittest.main()
