import csv
from concurrent.futures import ThreadPoolExecutor

from benchmarking.base_benchmark import BaseBenchmark


def test_record_result_streams_rows(tmp_path):
    out_path = tmp_path / "stream.csv"
    bench = BaseBenchmark([], [], str(out_path), spotify_client=None)
    fieldnames = ["model", "prompt"]

    bench.initialize_csv(fieldnames)
    bench.record_result({"model": "m1", "prompt": "p1"})
    bench.record_result({"model": "m2", "prompt": "p2"})

    with out_path.open("r", encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))

    assert len(rows) == 2
    assert rows[0]["model"] == "m1"
    assert rows[1]["prompt"] == "p2"


def test_record_result_is_thread_safe(tmp_path):
    out_path = tmp_path / "parallel.csv"
    bench = BaseBenchmark([], [], str(out_path), spotify_client=None)
    fieldnames = ["idx", "value"]

    bench.initialize_csv(fieldnames)

    rows = [{"idx": str(i), "value": str(i * i)} for i in range(25)]

    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(bench.record_result, row) for row in rows]
        for fut in futures:
            fut.result()

    with out_path.open("r", encoding="utf-8", newline="") as f:
        written = list(csv.DictReader(f))

    assert len(written) == len(rows)
    assert {row["idx"] for row in written} == {row["idx"] for row in rows}
