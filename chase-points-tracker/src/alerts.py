from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from src.models import DealAlert

console = Console()


def display_alerts(alerts: list[DealAlert]) -> None:
    """Display deal alerts in a formatted table."""
    if not alerts:
        console.print("[dim]No deals found above your threshold.[/dim]")
        return

    console.print()
    console.print(
        Panel.fit(
            f"[bold green]{len(alerts)} deal(s) flagged![/bold green]",
            title="Chase Points Deal Alerts",
            border_style="green",
        )
    )
    console.print()

    table = Table(show_header=True, header_style="bold cyan")
    table.add_column("Type", style="dim", width=8)
    table.add_column("Deal", min_width=30)
    table.add_column("Partner", width=18)
    table.add_column("Cash", justify="right", width=10)
    table.add_column("Points", justify="right", width=10)
    table.add_column("CPP", justify="right", width=6, style="bold green")
    table.add_column("Savings", justify="right", width=10)

    for alert in alerts:
        d = alert.deal
        savings = alert.savings_vs_portal
        savings_style = "green" if savings > 0 else "red"

        table.add_row(
            d.deal_type.value.upper(),
            d.title,
            d.transfer_partner or "Portal",
            f"${d.cash_price:,.0f}",
            f"{d.points_price:,}",
            f"{d.cents_per_point:.1f}",
            f"[{savings_style}]${savings:,.0f}[/{savings_style}]",
        )

    console.print(table)
    console.print()

    for alert in alerts:
        console.print(f"  [yellow]>[/yellow] {alert.reason}")
    console.print()


def display_deals_table(deals: list) -> None:
    """Display all tracked deals in a table."""
    if not deals:
        console.print("[dim]No deals tracked yet. Run 'chase-points scan' first.[/dim]")
        return

    table = Table(show_header=True, header_style="bold cyan")
    table.add_column("Type", style="dim", width=8)
    table.add_column("Deal", min_width=30)
    table.add_column("Source", width=16)
    table.add_column("Cash", justify="right", width=10)
    table.add_column("Points", justify="right", width=10)
    table.add_column("CPP", justify="right", width=6)
    table.add_column("Date", width=12)

    for d in deals:
        table.add_row(
            d.deal_type.value.upper(),
            d.title,
            d.source,
            f"${d.cash_price:,.0f}",
            f"{d.points_price:,}",
            f"{d.cents_per_point:.1f}",
            str(d.travel_date) if d.travel_date else "-",
        )

    console.print(table)
