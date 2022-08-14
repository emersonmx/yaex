from invoke import Context, task


@task
def run(c):
    # type: (Context) -> None
    c.run("python yaex.py")


@task(aliases=("fmt",))
def format(c, all_files=False):
    # type: (Context, bool) -> None
    precommit_options = []

    if all_files:
        precommit_options.append("--all-files")

    hooks = [
        "trailing-whitespace",
        "end-of-file-fixer",
        "pyupgrade",
        "add-trailing-comma",
        "yesqa",
        "isort",
        "black",
    ]
    for hook in hooks:
        cmd = " ".join(["pre-commit", "run", *precommit_options, hook])
        c.run(cmd)


@task
def lint(c, all_files=False):
    # type: (Context, bool) -> None
    precommit_options = []

    if all_files:
        precommit_options.append("--all-files")

    hooks = [
        "check-ast",
        "debug-statements",
        "name-tests-test",
        "check-merge-conflict",
        "check-added-large-files",
        "detect-private-key",
        "flake8",
        "mypy",
        "vulture",
        "bandit",
    ]
    for hook in hooks:
        cmd = " ".join(["pre-commit", "run", *precommit_options, hook])
        c.run(cmd)


@task
def tests(c, watch=False, quiet=False):
    # type: (Context, bool, bool) -> None
    pytest_options: list[str] = []
    if quiet:
        pytest_options.append("-q")

    if watch:
        _watch_tests(c, pytest_options)
    else:
        _run_pytest(c, pytest_options)


def _watch_tests(c: Context, pytest_options: list[str]) -> None:
    import time

    from watchdog.events import (  # type: ignore
        EVENT_TYPE_CREATED,
        EVENT_TYPE_DELETED,
        EVENT_TYPE_MODIFIED,
        EVENT_TYPE_MOVED,
        RegexMatchingEventHandler,
    )
    from watchdog.observers import Observer  # type: ignore

    class MyEventHandler(RegexMatchingEventHandler):  # type: ignore
        def __init__(self, *args, **kwargs) -> None:  # type: ignore
            super().__init__(*args, **kwargs)
            self.has_modified = True

        def on_any_event(self, event):  # type: ignore
            super().on_any_event(event)
            events_to_watch = [
                EVENT_TYPE_CREATED,
                EVENT_TYPE_DELETED,
                EVENT_TYPE_MODIFIED,
                EVENT_TYPE_MOVED,
            ]
            if event.event_type in events_to_watch:
                self.has_modified = True

        def tick(self):  # type: ignore
            if self.has_modified:
                _run_pytest(c, pytest_options)
                self.has_modified = False

    event_handler = MyEventHandler(
        regexes=[r".*\.py$"],
        ignore_directories=True,
    )
    observer = Observer()
    observer.schedule(event_handler, ".", recursive=True)
    observer.start()
    try:
        while True:
            event_handler.tick()  # type: ignore
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


def _run_pytest(c: Context, pytest_options: list[str]) -> None:
    cmd = " ".join(
        [
            "coverage",
            "run",
            "-m",
            "pytest",
            *pytest_options,
        ],
    )
    c.run(cmd, warn=True)


@task
def coverage(c):
    # type: (Context) -> None
    c.run("coverage report")
