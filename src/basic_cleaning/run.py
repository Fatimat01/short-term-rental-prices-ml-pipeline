#!/usr/bin/env python
"""
Performs basic cleaning on the data and save the results in Weights & Biases
"""
import argparse
import logging
import wandb
import pandas as pd
import os


logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()


def go(args):

    run = wandb.init(job_type="basic_cleaning")
    run.config.update(args)

    # Download input artifact. This will also log that this script is using this
    # particular version of the artifact
    # artifact_local_path = run.use_artifact(args.input_artifact).file()

    # data cleaning code goes here
    logger.info("Basic cleaning step is done!")
    # Download the data from W&B.
    artifact = run.use_artifact(args.input_artifact)
    artifact_path = artifact.file()
    df = pd.read_csv(artifact_path)

    # Drop the duplicates
    logger.info("Dropping duplicates")
    df = df.drop_duplicates().reset_index(drop=True)

    # Remove outliers based on the price column.
    # Use args.min_price and args.max_price for filtering outliers.

    logger.info("Removing outliers")
    df = df[(df['price'] >= args.min_price) & (df['price'] <= args.max_price)].copy()
    
    # Save the cleaned data to a new CSV file
    filename = "clean_sample.csv"
    idx = df['longitude'].between(-74.25, -73.50) & df['latitude'].between(40.5, 41.2)
    df = df[idx].copy()
    df.to_csv(filename, index=False)

    # Create a new artifact for the cleaned data
    artifact = wandb.Artifact(
        name=args.output_artifact,
        type=args.output_type,
        description=args.output_description,
    )
    artifact.add_file(filename)
    run.log_artifact(artifact)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="his steps cleans the data")
    
    parser.add_argument(
        "--input_artifact",
        type=str,
        help="The input artifact to be cleaned",
        required=True
    )

    parser.add_argument(
        "--output_artifact", 
        type=str,
        help="The name for the output artifact",
        required=True
    )

    parser.add_argument(
        "--output_type",
        type=str,
        help="The type for the output artifact",
        required=True
    )
    parser.add_argument(
        "--output_description",
        type=str,
        help="The description for the output artifact",
        required=True
    )

    parser.add_argument(
        "--min_price",
        type=float,
        help="The minimum price of the rentals",
        required=True
    )

    parser.add_argument(
        "--max_price",
        type=float,
        help="The maximum price of the rentals",
        required=True
    )

    args = parser.parse_args()

    go(args)
