#!/usr/bin/env python3
from __future__ import annotations

from app_pages_home import render_page
from app_shell import setup_page


def main() -> None:
    setup_page("Retirement Planning Suite")
    render_page()


if __name__ == "__main__":
    main()
