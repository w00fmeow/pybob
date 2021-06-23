#!/usr/bin/env python3
import argparse
from src.pybob import PyBob

parser = argparse.ArgumentParser(description="Fill monthly attendance in one click. Thanks, Bob")

parser.add_argument("-e", "--email", help='Email address you use to login to Bob. Example: test@test.com', required=True)
parser.add_argument("-p","--password", help="Password you use to login to Bob. Example: qwerty", required=True)
parser.add_argument("--start_hour", help="Optional indicator when do you start to work. Defaults to 9. Example: 8",type=int, default=9)
parser.add_argument("--end_hour", help="Optional indicator when do you finish work every day. Defaults to 18. Example: 17",type=int, default=18)
parser.add_argument("--month_starts", help="Optional indicator what day to start filling the dates. Defaults to 25. Example: 5",type=int, default=25)


args = parser.parse_args()

bob = PyBob( args.email, args.password,
                start_hour=args.start_hour,
                end_hour=args.end_hour,
                month_starts=args.month_starts)

bob.fill_monthly_attendance()
