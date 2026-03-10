import click
from rich.console import Console

from src.alerts import display_alerts, display_deals_table
from src.config import get_config
from src.deal_tracker import scan_for_deals
from src.models import PointsConfig
from src.store import load_alerts, load_deals, save_alerts, save_deals

console = Console()


@click.group()
def cli() -> None:
    """Chase Reserve Points Deal Tracker — find the best use of your UR points."""
    pass


@cli.command()
def scan() -> None:
    """Scan all sources for deals and flag high-value opportunities."""
    config = get_config()
    console.print(f"[dim]Scanning with threshold: {config.cpp_threshold} cpp | Balance: {config.points_balance:,} points[/dim]")

    all_deals, alerts = scan_for_deals(config)

    # Persist
    save_deals(all_deals)
    if alerts:
        save_alerts(alerts)

    console.print(f"[dim]Found {len(all_deals)} deals across all sources.[/dim]")
    display_alerts(alerts)


@cli.command()
@click.option("--balance", type=int, help="Set your UR points balance")
@click.option("--threshold", type=float, help="Set minimum cpp to trigger alerts")
def config(balance: int | None, threshold: float | None) -> None:
    """View or update configuration."""
    current = get_config()

    if balance is None and threshold is None:
        console.print(f"  Points balance: [bold]{current.points_balance:,}[/bold]")
        console.print(f"  CPP threshold:  [bold]{current.cpp_threshold}[/bold]")
        console.print()
        console.print("[dim]Update with: chase-points config --balance 150000 --threshold 2.0[/dim]")
        console.print("[dim]Or set POINTS_BALANCE and CPP_THRESHOLD in your .env file.[/dim]")
        return

    if balance is not None:
        console.print(f"  Points balance: [bold]{balance:,}[/bold]")
        console.print("[dim]Set POINTS_BALANCE={balance} in your .env to persist.[/dim]")
    if threshold is not None:
        console.print(f"  CPP threshold:  [bold]{threshold}[/bold]")
        console.print("[dim]Set CPP_THRESHOLD={threshold} in your .env to persist.[/dim]")


@cli.command()
def history() -> None:
    """View past deal alerts."""
    alerts = load_alerts()
    if not alerts:
        console.print("[dim]No alert history yet. Run 'chase-points scan' first.[/dim]")
        return

    console.print(f"[bold]{len(alerts)} past alert(s):[/bold]")
    display_alerts(alerts)


@cli.command()
def deals() -> None:
    """List all tracked deals."""
    all_deals = load_deals()
    display_deals_table(all_deals)


if __name__ == "__main__":
    cli()
