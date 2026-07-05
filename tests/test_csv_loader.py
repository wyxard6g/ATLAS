from pathlib import Path

from atlas.data.csv_loader import CSVLoader


def test_csv_loader(tmp_path: Path):
    csv_file = tmp_path / "candles.csv"

    csv_file.write_text(
        "\n".join(
            [
                "timestamp,open,high,low,close,volume",
                "2026-01-01T00:00:00,100,105,99,104,1000",
                "2026-01-01T00:01:00,104,106,103,105,1200",
            ]
        )
    )

    loader = CSVLoader()

    candles = loader.load(str(csv_file))

    assert len(candles) == 2
    assert candles[0].close == 104
    assert candles[1].volume == 1200