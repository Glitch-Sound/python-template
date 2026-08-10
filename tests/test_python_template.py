from pytest import CaptureFixture

from python_template import main


def test_main_prints_greeting(capsys: CaptureFixture[str]) -> None:
    main()

    assert capsys.readouterr().out == "Hello from python-template!\n"
