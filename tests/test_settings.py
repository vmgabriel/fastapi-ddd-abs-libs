from src import settings


def test_settings_inject_attributes() -> None:
    expected_injected = {"data": "check_data"}

    configuration = settings.DevSettings()

    configuration.inject(expected_injected)

    for key, value in expected_injected.items():
        assert getattr(configuration, key) == value
