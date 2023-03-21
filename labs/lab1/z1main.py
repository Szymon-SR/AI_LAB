import argparse
import logging

# Lepiej zrobic uproszczona wersje niz nie zrobic wcale - np mulitgraf do zwyklego grafu

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        'Shortest paths between bus stops'
    )

    parser.add_argument('source')
    parser.add_argument('destination')
    parser.add_argument('optimize_by')
    parser.add_argument('starting_time')

    args = parser.parse_args()
    logger.info(f'Input data: travel from {args.source} to {args.destination}, optimized by {args.optimize_by}. Starting time {args.starting_time}.')