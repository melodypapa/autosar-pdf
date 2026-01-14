"""
Progress tracking utilities for long-running operations
"""

import sys
from typing import Optional, Callable
from pathlib import Path


class ProgressReporter:
    """
    Progress reporter for displaying console progress information.

    This class provides methods to display progress for operations
    like PDF conversion, file processing, and data extraction.
    """

    def __init__(self, verbose: bool = True):
        """
        Initialize progress reporter.

        Args:
            verbose (bool): Whether to show progress messages (default: True)
        """
        self.verbose = verbose
        self._use_tqdm = self._check_tqdm_available()

    def _check_tqdm_available(self) -> bool:
        """Check if tqdm is available for progress bars."""
        try:
            import tqdm

            return True
        except ImportError:
            return False

    def print(self, message: str, end: str = "\n") -> None:
        """
        Print a message if verbose mode is enabled.

        Args:
            message (str): Message to print
            end (str): String to append after message (default: "\n")
        """
        if self.verbose:
            print(message, end=end, file=sys.stdout)
            sys.stdout.flush()

    def start(self, operation: str) -> None:
        """
        Start a new operation and print start message.

        Args:
            operation (str): Description of the operation
        """
        self.print(f"\n{'=' * 70}")
        self.print(f"[START] {operation}")
        self.print("=" * 70)

    def finish(self, operation: str, success: bool = True) -> None:
        """
        Finish an operation and print completion message.

        Args:
            operation (str): Description of the operation
            success (bool): Whether the operation succeeded (default: True)
        """
        status = "[OK]" if success else "[FAILED]"
        self.print(f"{status} {operation}")

    def progress(self, current: int, total: int, operation: str = "Processing") -> None:
        """
        Display progress for an operation.

        Args:
            current (int): Current progress value
            total (int): Total value to complete
            operation (str): Description of the operation (default: "Processing")
        """
        if not self.verbose:
            return

        if self._use_tqdm:
            return

        percentage = (current / total) * 100 if total > 0 else 0
        bar_length = 40
        filled_length = int(bar_length * current // total) if total > 0 else 0
        bar = "█" * filled_length + "-" * (bar_length - filled_length)

        print(
            f"\r[{operation}] {bar} {percentage:.1f}% ({current}/{total})",
            end="",
            file=sys.stdout,
        )
        sys.stdout.flush()

        if current == total:
            print()

    def page_progress(
        self, page_num: int, total_pages: int, action: str = "Extracting"
    ) -> None:
        """
        Display progress for PDF page processing.

        Args:
            page_num (int): Current page number (0-indexed)
            total_pages (int): Total number of pages
            action (str): Description of the action (default: "Extracting")
        """
        self.progress(page_num + 1, total_pages, f"{action} page")

    def file_progress(
        self,
        file_num: int,
        total_files: int,
        filename: Optional[str] = None,
        action: str = "Processing",
    ) -> None:
        """
        Display progress for file processing.

        Args:
            file_num (int): Current file number (1-indexed)
            total_files (int): Total number of files
            filename (Optional[str]): Name of current file (default: None)
            action (str): Description of the action (default: "Processing")
        """
        self.progress(file_num, total_files, f"{action} file")

        if self.verbose and filename:
            print(f"  -> {filename}")

    def step(self, step_name: str, step_num: int, total_steps: int) -> None:
        """
        Display a multi-step operation step.

        Args:
            step_name (str): Description of the step
            step_num (int): Current step number (1-indexed)
            total_steps (int): Total number of steps
        """
        self.print(f"\n[{step_num}/{total_steps}] {step_name}...")

    def info(self, message: str) -> None:
        """
        Display informational message.

        Args:
            message (str): Informational message
        """
        self.print(f"[INFO] {message}")

    def success(self, message: str) -> None:
        """
        Display success message.

        Args:
            message (str): Success message
        """
        self.print(f"[SUCCESS] {message}")

    def warning(self, message: str) -> None:
        """
        Display warning message.

        Args:
            message (str): Warning message
        """
        self.print(f"[WARNING] {message}", file=sys.stderr)

    def error(self, message: str) -> None:
        """
        Display error message.

        Args:
            message (str): Error message
        """
        self.print(f"[ERROR] {message}", file=sys.stderr)

    def stats(self, stats: dict) -> None:
        """
        Display statistics dictionary.

        Args:
            stats (dict): Statistics to display
        """
        if not self.verbose:
            return

        self.print("\n" + "-" * 70)
        self.print("Statistics:")
        self.print("-" * 70)

        for key, value in stats.items():
            self.print(f"  {key.replace('_', ' ').title()}: {value}")

    def context(self, context: str) -> Callable:
        """
        Create a context manager for progress tracking.

        Args:
            context (str): Description of the context

        Returns:
            Callable: Context manager for the operation
        """

        class ProgressContext:
            def __init__(self, reporter, context_name):
                self.reporter = reporter
                self.context_name = context_name

            def __enter__(self):
                self.reporter.start(self.context_name)
                return self.reporter

            def __exit__(self, exc_type, exc_val, exc_tb):
                self.reporter.finish(self.context_name, success=exc_type is None)

        return ProgressContext(self, context)

    def create_progress_bar(self, total: int, description: str = "Processing"):
        """
        Create a progress bar for an operation.

        Args:
            total (int): Total number of items to process
            description (str): Description of the operation (default: "Processing")

        Returns:
            Progress bar object or None if verbose is disabled
        """
        if not self.verbose:
            return None

        if self._use_tqdm:
            try:
                import tqdm

                return tqdm.tqdm(
                    total=total, desc=description, unit="", file=sys.stdout
                )
            except ImportError:
                return self._create_simple_progress(total, description)
        else:
            return self._create_simple_progress(total, description)

    def _create_simple_progress(self, total: int, description: str):
        """Create simple text-based progress bar."""
        return SimpleProgress(total, description, self)


class SimpleProgress:
    """
    Simple text-based progress bar.
    """

    def __init__(self, total: int, description: str, reporter: ProgressReporter):
        self.total = total
        self.description = description
        self.reporter = reporter
        self.current = 0

    def update(self, n: int = 1) -> None:
        """
        Update progress by n items.

        Args:
            n (int): Number of items processed (default: 1)
        """
        self.current += n
        self.reporter.progress(self.current, self.total, self.description)

    def close(self) -> None:
        """Close the progress bar."""
        if self.current < self.total:
            self.reporter.progress(self.total, self.total, self.description)
