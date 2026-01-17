import json

from app import fizz_buzz, load_max_from_json


def test_fizz_buzz_values() -> None:
    assert fizz_buzz(1) == "1"
    assert fizz_buzz(3) == "Fizz"
    assert fizz_buzz(5) == "Buzz"
    assert fizz_buzz(15) == "FizzBuzz"


def test_load_max_from_json(tmp_path) -> None:
    config_path = tmp_path / "config.json"
    config_path.write_text(json.dumps({"max": 7}), encoding="utf-8")
    assert load_max_from_json(config_path) == 7
