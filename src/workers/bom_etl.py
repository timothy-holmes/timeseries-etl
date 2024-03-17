import datetime

import requests
from tinyflux import Point


class ExtractorBOM:
    PARAMS = {
        "cookies": {
            "_ga": "GA1.1.121450838.1706667718",
            "__utmz": "172860464.1709514035.12.6.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided)",
            "_easyab_seed": "860.8294039057097",
            "bm_mi": "D946BE6915517EF50035AA078C0F815C~YAAQJE3cF2FLYOmNAQAAyrv3KxeljR+Jol0B3+lJ1vGUq/5rULKSlZ4IYpK0sWBJetfuA9bd57SNf04NPR+fA3aZXnhIoqQzCHIDkTc0ZPzPqFWrIHvz4yhu6zRQJTrNEBndarvxrNS4MZ9b7Afo9evsstalleR/gdStep82xHDyIweU/ztBUOgmCEGQg2nz8tFkEqhRXnxhvOrxc3IGKarKYh3iXcspPQ79ViZ4X0mRM7bvaFGNP57tQ4SMKdcegdJrISkzj7II/tGi3oyWe759kRLg+nPlhSWVmFw0OrVNPcjl3CKPBRwQyoZpySPE4IfxRMrPcrga/jHkvnQCD55Fsw==~1",
            "__utma": "172860464.681292704.1706667718.1709584200.1710134640.14",
            "__utmc": "172860464",
            "__utmt": "1",
            "ak_bmsc": "D43F27806DC08BC8AF43C9D7CD80716A~000000000000000000000000000000~YAAQDV8wFyAO1RiOAQAAIr/3Kxfbhn1Qu8o0JGUXV/UA6Ue0eD41QicsYijYvRGQfsZs2K/3pcFrVh8cfVVtkm6k9Cpfh3cNuVMpuLF46NMOe1RgDszPG1Vk+2kC8CD/BZECQq8K2DUamjQzqN/IO8CEC7nhKJeLI9+PlqAEaCAA9YwEXzFObLCLEhNLlfvuB86sh3bwaLvAgT/nAvHN5vMJGtThascMUlUJftZq1ma2gUqKZXfM0KSwFQUU1/L8z6gO1IZg67j7U62MKUXPv/dtFvgzwHs4oP4PwfVaBxtZy4M8qUcVutKaCYjQGiTbNHkxWSYL0LekDLg0UoI4lszL2GHxexOavNqJP/rHQvJo2FMI0iRC4zfkAUTSX/fl0l7+eDp3/50AASNLNSl8WJSloUxLjLpPnBqqYgsRJvfeXdW75w==",
            "bm_sv": "532B55E99254B6337E28C2A14F8D8071~YAAQH18wF07PSOmNAQAAvNv5Kxc3Jv5VbahhD8/hnYRTZ1Umm4DLp96bVsy+J51gm+cLcXyqP1fjdRTLZNuAN1ViVPkQShXkPtje9xFT1MK9zvltLlWCTLhjINv46+yAbtrHfDihq68iUi/ZDg2mPamSebodKqPxCllxzrLjdt27TrMdH463Bp2jG4kzz8hh0jcFIzUm2JsRzsRPeH5zPl0UQSFjH8OSvBV6vKin6SB6EyETIjcKvlelLN01P7wnag==~1",
            "__utmb": "172860464.16.9.1710134673737",
            "_ga_Y4Z1NSQVJ5": "GS1.1.1710134640.15.1.1710134788.0.0.0",
        },
        "headers": {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Language": "en-AU,en;q=0.9,en-GB-oxendict;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            "Connection": "keep-alive",
            # 'Cookie': '_ga=GA1.1.121450838.1706667718; __utmz=172860464.1709514035.12.6.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); _easyab_seed=860.8294039057097; bm_mi=D946BE6915517EF50035AA078C0F815C~YAAQJE3cF2FLYOmNAQAAyrv3KxeljR+Jol0B3+lJ1vGUq/5rULKSlZ4IYpK0sWBJetfuA9bd57SNf04NPR+fA3aZXnhIoqQzCHIDkTc0ZPzPqFWrIHvz4yhu6zRQJTrNEBndarvxrNS4MZ9b7Afo9evsstalleR/gdStep82xHDyIweU/ztBUOgmCEGQg2nz8tFkEqhRXnxhvOrxc3IGKarKYh3iXcspPQ79ViZ4X0mRM7bvaFGNP57tQ4SMKdcegdJrISkzj7II/tGi3oyWe759kRLg+nPlhSWVmFw0OrVNPcjl3CKPBRwQyoZpySPE4IfxRMrPcrga/jHkvnQCD55Fsw==~1; __utma=172860464.681292704.1706667718.1709584200.1710134640.14; __utmc=172860464; __utmt=1; ak_bmsc=D43F27806DC08BC8AF43C9D7CD80716A~000000000000000000000000000000~YAAQDV8wFyAO1RiOAQAAIr/3Kxfbhn1Qu8o0JGUXV/UA6Ue0eD41QicsYijYvRGQfsZs2K/3pcFrVh8cfVVtkm6k9Cpfh3cNuVMpuLF46NMOe1RgDszPG1Vk+2kC8CD/BZECQq8K2DUamjQzqN/IO8CEC7nhKJeLI9+PlqAEaCAA9YwEXzFObLCLEhNLlfvuB86sh3bwaLvAgT/nAvHN5vMJGtThascMUlUJftZq1ma2gUqKZXfM0KSwFQUU1/L8z6gO1IZg67j7U62MKUXPv/dtFvgzwHs4oP4PwfVaBxtZy4M8qUcVutKaCYjQGiTbNHkxWSYL0LekDLg0UoI4lszL2GHxexOavNqJP/rHQvJo2FMI0iRC4zfkAUTSX/fl0l7+eDp3/50AASNLNSl8WJSloUxLjLpPnBqqYgsRJvfeXdW75w==; bm_sv=532B55E99254B6337E28C2A14F8D8071~YAAQH18wF07PSOmNAQAAvNv5Kxc3Jv5VbahhD8/hnYRTZ1Umm4DLp96bVsy+J51gm+cLcXyqP1fjdRTLZNuAN1ViVPkQShXkPtje9xFT1MK9zvltLlWCTLhjINv46+yAbtrHfDihq68iUi/ZDg2mPamSebodKqPxCllxzrLjdt27TrMdH463Bp2jG4kzz8hh0jcFIzUm2JsRzsRPeH5zPl0UQSFjH8OSvBV6vKin6SB6EyETIjcKvlelLN01P7wnag==~1; __utmb=172860464.16.9.1710134673737; _ga_Y4Z1NSQVJ5=GS1.1.1710134640.15.1.1710134788.0.0.0',
            "Referer": "http://www.bom.gov.au/products/IDV60801/IDV60801.99821.shtml",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        },
    }

    SITES = [
        {
            "name": "Trentham (CFA)",
            "url": "http://www.bom.gov.au/fwo/IDV60801/IDV60801.99821.json",
        },
        {
            "name": "Ballan (CFA)",
            "url": "http://www.bom.gov.au/fwo/IDV60801/IDV60801.99820.json",
        },
        {
            "name": "Essendon Airport",
            "url": "http://www.bom.gov.au/fwo/IDV60801/IDV60801.95866.json",
        },
        {
            "name": "Kilmore Gap",
            "url": "http://www.bom.gov.au/fwo/IDV60801/IDV60801.94860.json",
        },
    ]

    @classmethod
    def get_site_observations(cls, url) -> list[dict]:
        return (
            requests.get(
                url, headers=cls.PARAMS["headers"], params=cls.PARAMS["cookies"]
            )
            .json()
            .get("observations")
            .get("data")
        )

    @staticmethod
    def ob_to_point(ob) -> Point:
        # Datetime object that is "timezone-aware".
        ts = datetime.datetime.strptime(ob["local_date_time_full"], "%Y%m%d%H%M%S")

        # Tags as a dict of string/string key values.
        tags = {"source": "BOM", "loc_name": ob["name"]}

        # Fields as a dict of string/numeric key values.
        fields = {
            "air_temp": float(ob["air_temp"]),
            "rel_hum": float(ob["rel_hum"]),
        }

        # Initialize the Point with the above attributes.
        return Point(
            measurement="climate",
            time=ts,
            tags=tags,
            fields=fields,
        )

    @classmethod
    def get_points(cls) -> list[Point]:
        observations = [
            obs for site in cls.SITES for obs in cls.get_site_observations(site["url"])
        ]

        return [cls.ob_to_point(ob) for ob in observations]
