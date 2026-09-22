from pytest import CaptureFixture

from app import main


def test_main_prints_greeting(capsys: CaptureFixture[str]) -> None:
    main()

    assert capsys.readouterr().out == "Hello from app!\n"
