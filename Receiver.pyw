"""Console-free application entry point. Wi-Fi is not started by this application."""

from TrayApp import main


if __name__ == "__main__":
    raise SystemExit(main())
