from mock import Mock
import unittest
from pcp_pidstat import CpuProcessPrioritiesReporter

class TestProcessPriorityReporter(unittest.TestCase):
    def setUp(self):
        process_1 = Mock(pid = Mock(return_value = 1),
                        process_name = Mock(return_value = "process_1"),
                        user_name = Mock(return_value='pcp'),
                        user_id = Mock(return_value=1000),
                        priority = Mock(return_value=99),
                        policy = Mock(return_value='FIFO'))

        self.processes = [process_1]

    def test_print_report_without_filtering(self):
        process_priority = Mock()
        process_filter = Mock()
        printer = Mock()
        process_filter.filter_processes = Mock(return_value=self.processes)
        reporter = CpuProcessPrioritiesReporter(process_priority, process_filter, printer)

        reporter.print_report(123)

        printer.assert_called_with("123\t1000\t1\t99\tFIFO\tprocess_1")

if __name__ == "__main__":
    unittest.main()
