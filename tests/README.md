# Tests

Automated tests for t23b.org.

Test cases and user stories are in `main-page/test-cases/` and `main-page/user-stories/`.

**Logs and screenshots:** Request the `step_logger` fixture. Call `step_logger.start_step("description")` per step and `step_logger.checkpoint("what passed")` after assertions. For each run there is a folder `results/YYYY-MM-DD_HH-MM-SS/`, inside it per test case folders like `TC_03/` and inside them files per pytest function: `<n>_<name>_log.txt` and, for browser tests, `<n>_<name>_end.png`. Browser runs headless.
