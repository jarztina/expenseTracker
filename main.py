"""
Terminal UI demo — Receipt/Expense Tracker
--------------------------------------------

Step 1: (For you guys to test out the program):
In terminal:
'pip install rich'

This is basically used to beautify the table in the terminal

Step 2:
Run the project demo, test it out
"""

import time
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.prompt import Prompt
from rich import box

console = Console()


# ---------- io_manager-style display functions ----------

def show_banner():
    console.print(Panel.fit(
        "[bold cyan]RECEIPT EXPENSE TRACKER[/bold cyan]\n"
        "[dim]AI-powered receipt classification[/dim]",
        border_style="cyan",
        padding=(1, 4),
    ))


def show_menu():
    console.print("\n[bold]What would you like to do?[/bold]")
    console.print("  [cyan]1[/cyan] · Scan a new receipt")
    console.print("  [cyan]2[/cyan] · View expense summary")
    console.print("  [cyan]3[/cyan] · Filter by category")
    console.print("  [cyan]4[/cyan] · Exit\n")
    return Prompt.ask("Choose an option", choices=["1", "2", "3", "4"], default="1")


def show_ai_progress(label="Sending receipt to AI for classification"):
    """Simulates ai_manager doing work — spinner instead of a silent freeze."""
    with Progress(
        SpinnerColumn(style="cyan"),
        TextColumn("[progress.description]{task.description}"),
        console=console,
        transient=True,
    ) as progress:
        progress.add_task(description=label, total=None)
        time.sleep(1.8)  # placeholder for the real API call


def show_receipt_result(record):
    """record = dict returned by ai_manager after validation."""
    table = Table(box=box.ROUNDED, show_header=False, padding=(0, 1))
    table.add_row("[bold]Merchant[/bold]", record["merchant"])
    table.add_row("[bold]Date[/bold]", record["date"])
    table.add_row("[bold]Category[/bold]", f"[yellow]{record['category']}[/yellow]")
    table.add_row("[bold]Total[/bold]", f"[green]${record['total']:.2f}[/green]")
    console.print(Panel(table, title="Receipt Parsed", border_style="green"))


def show_flag(message):
    """logic_manager-style alert, e.g. overspend flag."""
    console.print(Panel(f"[bold red]⚠ {message}[/bold red]", border_style="red"))


def show_summary(records):
    table = Table(title="Expense Summary", box=box.SIMPLE_HEAVY)
    table.add_column("Date", style="dim")
    table.add_column("Merchant")
    table.add_column("Category", style="yellow")
    table.add_column("Total", justify="right", style="green")

    running_total = 0.0
    for r in records:
        table.add_row(r["date"], r["merchant"], r["category"], f"${r['total']:.2f}")
        running_total += r["total"]

    console.print(table)
    console.print(f"\n[bold]Total spent:[/bold] [green]${running_total:.2f}[/green]\n")


# ---------- fake data / demo driver ----------

def fake_ai_classify(image_path):
    """Stand-in for ai_manager.classify_receipt() — returns a fixed record."""
    return {
        "merchant": "NTUC FairPrice",
        "date": "2026-09-14",
        "category": "Groceries",
        "total": 47.85,
    }


def run_demo():
    show_banner()
    records = []

    while True:
        choice = show_menu()

        if choice == "1":
            path = Prompt.ask("Enter path to receipt image", default="receipts/receipt_01.jpg")
            show_ai_progress()
            record = fake_ai_classify(path)
            show_receipt_result(record)
            records.append(record)

            # logic_manager-style multi-condition rule example
            if record["category"] == "Groceries" and record["total"] > 40:
                show_flag("Groceries spend this trip exceeds your $40 alert threshold.")

        elif choice == "2":
            if records:
                show_summary(records)
            else:
                console.print("[dim]No receipts scanned yet.[/dim]\n")

        elif choice == "3":
            category = Prompt.ask("Filter by category", default="Groceries")
            filtered = [r for r in records if r["category"].lower() == category.lower()]
            show_summary(filtered) if filtered else console.print("[dim]No matches.[/dim]\n")

        elif choice == "4":
            console.print("[cyan]Goodbye![/cyan]")
            break


if __name__ == "__main__":
    run_demo()