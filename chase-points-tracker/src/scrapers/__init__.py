from src.scrapers.base import BaseScraper
from src.scrapers.google_flights import GoogleFlightsScraper
from src.scrapers.hotel_scraper import HotelScraper
from src.scrapers.points_guy import PointsGuyScraper

ALL_SCRAPERS: list[type[BaseScraper]] = [
    GoogleFlightsScraper,
    HotelScraper,
    PointsGuyScraper,
]
