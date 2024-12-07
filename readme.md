# Fish cli wrapped

 This is a "wrapped" of your utilization of the fish shell. It will print out statistics of your usage of the fish shell in the last year.

## Installation

To use a virtual environment and install requirements with pip, follow these steps:

1. **Create a virtual environment**:
    ```bash
    python -m venv venv
    ```

2. **Activate the virtual environment**:
    - On macOS and Linux using fish:
        ```bash
        source venv/bin/activate.fish
        ```

3. **Install the requirements**:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

To use the script, run the following command:

```bash
python cli-wrapped.py
```

## Issues
> [!WARNING]
> fish deduplicates commands, so if you run the same command multiple times, it will only be counted once. This is a limitation of the fish shell, and not of this script.